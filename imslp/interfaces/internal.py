
import glob
import json
import os
import typing
import zipfile

import requests

import imslp


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "HashablePageRecord",

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


class HashablePageRecord(dict):
    """
    Subclass of a dictionary that can contain an IMSLP API record that
    can be hashed, using a string hash of the `permlink` of the record.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __hash__(self):
        hash_id = hash(self["permlink"])
        return hash_id


def _raw_call(imslp_url_pattern: str, start: int = 0, count: int = None):
    """
    Returns the result of a request made to the internal IMSLP API
    to retrieve a list of works or of people. This method is a helper
    method called by `list_people()` and `list_works()`.
    """

    results = []
    more_results = True

    while more_results:
        try:
            req = requests.get(imslp_url_pattern.format(start=start))
            if not req.ok:
                continue
            obj = req.json()
        except:
            break

        more_results = False

        if "metadata" in obj:
            metadata = obj.get("metadata", dict())
            more_results = metadata.get("moreresultsavailable", False)
            del obj["metadata"]

        new_results = list(obj.values())
        start += len(new_results)
        results += new_results

        if count is not None and 0 <= count <= len(results):
            return results[:count]

    return results[:count]


def list_people(
        start: int = 0,
        count: typing.Optional[int] = None,
        cache: bool = True
) -> typing.List[HashablePageRecord]:
    if cache:
        if _cache_people is None:
            load_cache()
        return _cache_people[start:start+count if count is not None else None]

    return list(map(HashablePageRecord, _raw_call(
        imslp_url_pattern=IMSLP_API_PEOPLE,
        start=start,
        count=count,
    )))


def list_works(start: int = 0, count: int = None, cache: bool = True):
    if cache:
        if _cache_works is None:
            load_cache()
        return _cache_works[start:start+count if count is not None else None]

    return list(map(HashablePageRecord, _raw_call(
        imslp_url_pattern=IMSLP_API_WORKS,
        start=start,
        count=count,
    )))


def reset_cache(from_file: bool = True) -> typing.NoReturn:
    """

    :param from_file:
    :return:
    """

    global _cache_people, _cache_works

    _cache_people = None
    _cache_works = None

    return load_cache(from_file=from_file)


# noinspection PyBroadException
def load_cache(from_file: bool = True) -> typing.NoReturn:
    """
    Loads a copy of the IMSLP people and works to memory cache, so that
    subsequent queries will be faster; if `from_file` is `True`, this
    method will attempt to load a partial cache from the package's
    internal files and only request newer entries from IMSLP. This
    considerably speeds up operations by about 4 minutes on a typical
    high-speed bandwidth.

    :param from_file: Determines whether to use package's internal cache
    :return:
    """

    global _cache_people, _cache_works

    # this is slow when not using the disk cache (which makes the
    # package quite large unfortunately! but at least not routinely
    # downloading 60 MB)
    #
    # on my computer + with my bandwidth (just as order of magnitude):
    # - list_people: 164880 items, 200 seconds to load
    # - list_works: 30559 items, 35 seconds to load

    if _cache_people is None:

        if from_file:
            # Try to load from file
            possible_files = sorted(
                list(map(os.path.abspath,
                         map(os.path.expanduser,
                             glob.glob(os.path.join(
                                 imslp.__path__[0],
                                 "../cache/imslp-people-cache-*.zip"))))),
                reverse=True)

            if len(possible_files) > 0:
                zf = zipfile.ZipFile(possible_files[0], mode="r")
                partial_contents = json.loads(zf.read(zf.namelist()[0]))
                try:
                    remainder_contents = list_people(start=len(partial_contents), cache=False)
                    _cache_people = partial_contents + remainder_contents
                except:
                    _cache_people = None

                _cache_people = list(map(HashablePageRecord, _cache_people))

        if _cache_people is None:
            _cache_people = list_people(cache=False)

    if _cache_works is None:

        if from_file:
            # Try to load from file
            possible_files = sorted(
                list(map(os.path.abspath,
                         map(os.path.expanduser,
                             glob.glob(os.path.join(
                                 imslp.__path__[0],
                                 "../cache/imslp-works-cache-*.zip"))))),
                reverse=True)

            if len(possible_files) > 0:
                zf = zipfile.ZipFile(possible_files[0], mode="r")
                partial_contents = json.loads(zf.read(zf.namelist()[0]))
                try:
                    remainder_contents = list_works(start=len(partial_contents), cache=False)
                    _cache_works = partial_contents + remainder_contents
                except:
                    _cache_works = None

                _cache_works = list(map(HashablePageRecord, _cache_works))

        if _cache_works is None:
            _cache_works = list_works(cache=False)

