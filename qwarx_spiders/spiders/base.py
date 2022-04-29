class BaseSpider(object):
    custom_settings = {
    }

    @property
    def is_test_mode(self):
        return self.settings.getbool('TEST_MODE', False)
