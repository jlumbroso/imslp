
import mwclient


__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "ImslpMwClient",
]


#
IMSLP_HOST = "imslp.org"
IMSLP_API_PATH = "/"
IMSLP_SCHEME = "https"


class ImslpMwClient(mwclient.Site):

    _site = None

    def __init__(self, username=None, password=None):
        super().__init__(
            host=IMSLP_HOST,
            path=IMSLP_API_PATH,
            scheme=IMSLP_SCHEME,
        )

        if username is not None and password is not None:
            self.login(username=username, password=password)

    def login(
        self,
        username: str = None,
        password: str = None,
        cookies: dict = None,
        domain: str = None,
    ):
        # these cookies are necessary to allow for proper download of images/PDFs
        combined_cookies = {
            "imslp_wikiLanguageSelectorLanguage": "en",
            "imslpdisclaimeraccepted": "yes",
        }

        # include user provided cookies
        if cookies is not None:
            combined_cookies.update(cookies)

        super().login(
            username=username,
            password=password,
            cookies=combined_cookies,
            domain=domain,
        )
