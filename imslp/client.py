
import typing

import mwclient

import imslp
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

