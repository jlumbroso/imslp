
import typing

import mwclient

import imslp
import imslp.helpers
import imslp.helpers.string_search
import imslp.interfaces
import imslp.interfaces.constants
import imslp.interfaces.internal
import imslp.interfaces.mw_api
import imslp.interfaces.scraping


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "ImslpClient",
]


class ImslpClient:

    # the mwclient object
    _site = None               # type: mwclient.Site

    # the download wait time (in seconds)
    _wait_time = 15            # type: int

    def __init__(self, username=None, password=None):

        self._site = imslp.interfaces.mw_api.ImslpMwClient(
            username=username,
            password=password,
        )

    def login(
            self,
            username: str = None,
            password: str = None,
            cookies: dict = None,
            domain: str = None,
    ):
        self._site.login(
            username=username,
            password=username,
            cookies=cookies,
            domain=domain,
        )

    @property
    def logged_in(self) -> bool:
        """
        Returns whether the client is currently logged in.
        """
        return (
                self._site is not None and
                self._site.connection is not None and
                self._site.connection.cookies is not None and
                len(self._site.connection.cookies) > 1 and
                imslp.interfaces.constants.IMSLP_COOKIE_NAME_USERNAME in self._site.connection.cookies and
                self._site.connection.cookies[imslp.interfaces.constants.IMSLP_COOKIE_NAME_USERNAME] != ""
        )

    @property
    def username(self) -> typing.Optional[str]:
        """
        Returns the username of the logged in account if the client is
        logged in, and `None` otherwise.
        """
        if not self.logged_in:
            return

        return self._site.connection.cookies[imslp.interfaces.constants.IMSLP_COOKIE_NAME_USERNAME]

    @staticmethod
    def search_works(
        title: imslp.helpers.string_search.ImslpSearchExpression = None,
        composer: imslp.helpers.string_search.ImslpSearchExpression = None,
        intersect: bool = True,
        case_insensitive: bool = True
    ) -> typing.Set[imslp.interfaces.internal.HashablePageRecord]:
        """

        :param title:
        :param composer:
        :param intersect:
        :param case_insensitive:
        :return:
        """

        results = set(imslp.interfaces.internal.list_works())

        results_by_title = results
        if title is not None:
            results_by_title = set(filter(
                lambda record:
                imslp.helpers.string_search.check_search_expr_to_query(
                    query=record["intvals"]["worktitle"],
                    search_expr=title,
                    intersect=intersect,
                    case_insensitive=case_insensitive),
                results_by_title
            ))

        results_by_composer = results
        if composer is not None:
            results_by_composer = set(filter(
                lambda record:
                imslp.helpers.string_search.check_search_expr_to_query(
                    query=record["intvals"]["composer"],
                    search_expr=composer,
                    intersect=intersect,
                    case_insensitive=case_insensitive),
                results_by_composer
            ))

        if intersect:
            results = results_by_title.intersection(results_by_composer)
        else:
            results = results_by_title.union(results_by_composer)

        return results

    @staticmethod
    def search_people(
            name: imslp.helpers.string_search.ImslpSearchExpression,
            intersect: bool = True,
            case_insensitive: bool = True
    ) -> typing.Set[imslp.interfaces.internal.HashablePageRecord]:
        """

        :param name:
        :param intersect:
        :param case_insensitive:
        :return:
        """

        results = set(imslp.interfaces.internal.list_people())

        if name is not None:
            results = set(filter(
                lambda record:
                imslp.helpers.string_search.check_search_expr_to_query(
                    query=record["id"],
                    search_expr=name,
                    intersect=intersect,
                    case_insensitive=case_insensitive),
                results
            ))

        return results

