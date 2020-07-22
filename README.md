# imslp

🎼 The clean and modern way of accessing IMSLP data and scores programmatically. 🎶

## Installation

The package is available on PyPi and can be installed using your favorite package
manager:

```shell
pip install imslp
```

## Data Sources

This project attempts to use robust sources of data, that do not require web scraping of some sort:

- **MediaWiki API.** IMSLP is [one of tens of thousands of websites](https://wikiapiary.com/wiki/IMSLP)
built on top of [MediaWiki](https://www.mediawiki.org/wiki/MediaWiki), the framework created for
[Wikipedia.org](https://en.wikipedia.org/wiki/MediaWiki). As such, it can be accessed through
the [MediaWiki API](https://www.mediawiki.org/wiki/API:Main_page) for which, fortunately,
there exists a fantastic Python wrapper library called [`mwclient`](https://github.com/mwclient/mwclient).

- **IMSLP API.** For convenience, the IMSLP built some *ad-hoc* scripts that can be used to get a
list of people and a list of works, in a variety of different formats, including JSON.

## Related Projects

Here are a handful of other related projects available on GitHub to access the IMSLP data programmatically:

- [jjjake/imslp-scrape](https://github.com/): Last commit in May 2012 (32 commits), mix of Python and shell, scraping
the website for data (people, score links) with HTML parsing.

- [FrankTheCodeMonkey/IMSLP-Scraper](https://github.com/FrankTheCodeMonkey/IMSLP-Scraper): Last commit in June 2020 
(6 commits), Python, scraping the website for data and scores, with HTML parsing and Selenium.

- [josefleventon/imslp-api](https://github.com/josefleventon/imslp-api): Last commit in May 2020 (17 commits),
JavaScript, uses [IMSLP's custom API](https://imslp.org/wiki/IMSLP:API) to get the list of people and list of works
programmatically through a web API query. 

## Acknowledgements

Let's be clear that all the heavy lifting is done by [`mwclient`](https://github.com/mwclient/mwclient)—and
the volunteers who uploaded and/or scanned and/or typeset the scores on IMSLP. 

## License

This project is licensed under the LGPLv3 license, with the understanding
that importing a Python modular is similar in spirit to dynamically linking
against a library.

- You can use the library `imslp` in any project, for any purpose, as long
  as you provide some acknowledgement to this original project for use of
  the library.

- If you make improvements to `imslp`, you are required to make those
  changes publicly available.
  