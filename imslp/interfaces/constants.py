
__author__ = "Jérémie Lumbroso <lumbroso@cs.princeton.edu>"

__all__ = [
    "IMSLP_SUBCATEGORIES",
    "IMSLP_COOKIE_NAME_USERNAME",
]


# These are the subcategories available for some categories
# NOTE: should this be an enum?
IMSLP_SUBCATEGORIES = [
    "Compositions",
    "Collaborations",
    "Collections",

    "As Arranger",
    "As Copyist",
    "As Dedicatee",
    "As Editor",

    "Books",
    "Pasticcios",
]

# IMSLP cookie name where user is stored
IMSLP_COOKIE_NAME_USERNAME = "imslp_wikiUserName"
