
def test_import_all():

    # ignore the deprecation warnings of yaql and aoihttp
    import warnings
    warnings.filterwarnings("ignore", category=DeprecationWarning)

    import imslp
    import imslp.helpers.string_search
    import imslp.helpers
    import imslp.interfaces.constants
    import imslp.interfaces.internal
    import imslp.interfaces.mw_api
    import imslp.interfaces.scraping
    import imslp.interfaces
    import imslp.client

    assert True

