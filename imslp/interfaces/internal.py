
import requests


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "list_people",
    "list_works",
    "load_cache",
]


# URL patterns for the IMSLP API
# For more information, see: https://imslp.org/wiki/IMSLP:API

# Generic URL pattern
IMSLP_API_GENERIC = (
    "http://imslp.org/imslpscripts/API.ISCR.php?"
    "account=worklist/disclaimer=accepted/sort=id/type={typ}/start={{start}}/retformat=json")

# URL for list of people (composers, performers, editors, etc.)
IMSLP_API_PEOPLE = IMSLP_API_GENERIC.format(typ=1)

# URL for list of works
IMSLP_API_WORKS = IMSLP_API_GENERIC.format(typ=2)


# Internal variables to cache calls
_cache_people = None
_cache_works = None


def _raw_call(imslp_url_pattern: str, start: int = 0, count: int = None):
    """
    Returns the result of a request made to the internal IMSLP API
    to retrieve a list of works or of people. This method is a helper
    method called by `list_people()` and `list_works()`.
    """

    results = []
    more_results = True
    start = 0
    while more_results:
        try:
            req = requests.get(imslp_url_pattern.format(start=start))
            if not req.ok:
                continue
            obj = req.json()
        except:
            continue

        metadata = obj.get("metadata", dict())
        more_results = metadata.get("moreresultsavailable", False)

        if "metadata" in obj:
            del obj["metadata"]

        new_results = list(obj.values())
        start += len(new_results)
        results += new_results

        if count is not None and count >= 0 and len(results) >= count:
            return results[:count]

    return results[:count]


def list_people(start=0, count=None, cache=True):
    if cache:
        if _cache_people is None:
            load_cache()
        return _cache_people[start:start+count if count is not None else None]

    return _raw_call(
        imslp_url_pattern=IMSLP_API_PEOPLE,
        start=start,
        count=count,
    )


def list_works(start: int = 0, count: int = None, cache: bool = True):
    if cache:
        if _cache_works is None:
            load_cache()
        return _cache_works[start:start+count if count is not None else None]

    return _raw_call(
        imslp_url_pattern=IMSLP_API_WORKS,
        start=start,
        count=count,
    )


def load_cache(start: int = 0, count: int = None, cache: bool = True):
    global _cache_people, _cache_works
    # on my computer + with my bandwidth (just as order of magnitude):
    # - list_people: 164880 items, 200 seconds to load
    # - list_works: 30559 items, 35 seconds to load

    if _cache_people is None:
        _cache_people = list_people(cache=False)

    if _cache_works is None:
        _cache_works = list_works(cache=False)
