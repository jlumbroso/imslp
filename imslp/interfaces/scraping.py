
import json
import re
import typing
import urllib.parse

import bs4
import mwclient.page
import requests


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "fetch_category_table",
    "fetch_images_metadata",
]


# Pattern of the URL base
IMSLP_BASE_URL = "https://imslp.org{}"

# Regular expression to extract the ratings
IMSLP_REGEXP_RATINGS = re.compile(r"IMSLPRatings=({[^}]+})")

# Regular expression to extract the page count
IMSLP_REGEXP_PAGE_COUNT = re.compile(r"(\d+)\s*pp*\.*")

# Pattern of URL to fetch category charts
IMSLP_SCRAPE_CATCHART_URL = IMSLP_BASE_URL.format("/index.php?title={}&customcat=ccperson1")

# class name and content string used to locate chart of works
IMSLP_SCRAPE_CATCHART_TABLE_CLASS = "wikitable"
IMSLP_SCRAPE_CATCHART_NEXT_CLASS = "categorypaginglink"
IMSLP_SCRAPE_CATCHART_NEXT_TEXT = "next 200"


def _extract_tag_text(tag: bs4.element.Tag) -> str:
    """
    Extracts the text content from a BeautifulSoup `Tag` object.

    :param tag: A BeautifulSoup tag.
    :return: The text contents of the tag.
    """
    if tag is None or tag.text is None:
        return ""

    # Convert non-breakable spaces to breakable spaces and strip ends
    return tag.text.replace("\xa0", " ").strip()


def fetch_category_table(category_name: str, subcategory: typing.Optional[str] = None):
    """
    Fetches the chart containing an index to a category's works.

    :param category_name:
    :param subcategory:
    :return:
    """

    # Compute the category name
    catname_full = "Category:{}".format(category_name)
    if subcategory is not None:
        catname_full += "/"
        catname_full += subcategory
    catname_urlenc = urllib.parse.quote(catname_full, safe='/:')

    # Accumulator variables
    header = None
    rows_parsed = []

    next_page_link = IMSLP_SCRAPE_CATCHART_URL.format(catname_urlenc)

    while next_page_link is not None:

        # Fetch the data chunk
        r = requests.get(next_page_link)
        s = bs4.BeautifulSoup(r.content)
        ts = s.find_all(name="table", attrs={"class": IMSLP_SCRAPE_CATCHART_TABLE_CLASS})
        t = ts[0]

        # Check whether there is more to collect
        next_page_link = None
        next_page_link_candidates = s.find_all(
            "a",
            attrs={
                "title": catname_full,
                "class": IMSLP_SCRAPE_CATCHART_NEXT_CLASS},
            text=IMSLP_SCRAPE_CATCHART_NEXT_TEXT,
        )
        if next_page_link_candidates is not None and len(next_page_link_candidates) > 0:
            next_page_link = IMSLP_BASE_URL.format(next_page_link_candidates[0]["href"])

        # Parse the data
        if header is None:
            # parse new header
            header = list(map(lambda tag: tag.text.strip(), t.find_all("th")))
        else:
            # confirm header is the same
            assert header == list(map(lambda tag: tag.text.strip(), t.find_all("th")))

        rows = t.find_all("tr")[1:]

        # Add to already parsed rows
        rows_parsed += [list(map(_extract_tag_text, row.find_all("td"))) for row in rows]

    # Turn into dicts
    rows_as_dicts = list(map(lambda parsed_row: dict(zip(header, parsed_row)), rows_parsed))

    return rows_as_dicts

def fetch_images_metadata(page: mwclient.page.Page) -> list:
    """
    Fetches the metadata associated with the images of an IMSLP page, as
    specified by a `mwclient.page.Page` object. This contains the download
    counter which is not available through the MediaWiki API and requires
    scraping to obtain.

    :param page:
    :return:
    """

    if page is None:
        return list()

    esc_title = urllib.parse.quote(page.base_title.replace(" ", "_"))

    u = "https://imslp.org/wiki/{}".format(esc_title)

    r = requests.get(u)
    if not r.ok:
        return list()

    s = bs4.BeautifulSoup(r.content, features="html.parser")

    images = []

    # obtain ratings dictionary from embedded JavaScript
    # (the ratings are then loaded into the DOM onLoad)
    ratings_dict = dict()
    m = IMSLP_REGEXP_RATINGS.search(s.__str__())
    if m is not None:
        ratings_dict_str = m.group(1)
        ratings_dict_old = json.loads(ratings_dict_str)

        for key, value in ratings_dict_old.items():
            try:
                ratings_dict[int(key)] = {
                    "rating": value[0],
                    "count": int(value[1]),
                }
            except ValueError:
                continue

    for f in page.images():

        f_title = f.base_title
        f_esc_title = urllib.parse.quote(f_title.replace(" ", "_"))

        # Hacky way of finding the relevant metadata
        t1 = s.find(attrs={"href": "/wiki/File:{}".format(f_esc_title)})
        t2 = s.find(attrs={"title": "File:{}".format(f_title)})

        if t1 is None and t2 is None:
            continue

        t = t1 or t2
        if t.text.strip() == "":
            continue

        page_count = None
        m = IMSLP_REGEXP_PAGE_COUNT.search(t.parent.text)
        if m is not None:
            try:
                page_count = int(m.group(1))
            except ValueError:
                pass

        file_id = int(t.text.replace("#", ""))

        t = s.find(attrs={"href": "/wiki/Special:GetFCtrStats/@{}".format(file_id)})
        if t is None:
            continue

        file_counter = int(t.text)

        # Fix image URL
        if f.imageinfo["url"][0] == "/":
            # URL is //imslp.org/stuff...
            f.imageinfo["url"] = "http:" + f.imageinfo["url"]

        images.append({
            "id": file_id,
            "rating": ratings_dict.get(file_id, dict()).get("rating", -1),
            "rating_count": ratings_dict.get(file_id, dict()).get("count", 0),
            "download_count": file_counter,
            "title": f_title,
            "url": f.imageinfo["url"],
            "page_count": page_count,
            "size": f.imageinfo.get("size"),
            "sha1": f.imageinfo.get("sha1"),
            "obj": f,
        })

    return images
