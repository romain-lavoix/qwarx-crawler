from algoliasearch import algoliasearch


class AlgoliaSearchBase(object):
    def get_algolia_index(self, index=None):
        index = index or self.settings.get('ALGOLIA_SEARCH_INDEX')
        algolia_client = algoliasearch.Client(
            self.settings.get('ALGOLIA_SEARCH_APP_ID'),
            self.settings.get('ALGOLIA_SEARCH_APP_KEY'),
        )

        return algolia_client.init_index(index)
