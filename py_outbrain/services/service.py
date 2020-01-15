import logging

from .base import BaseService, CrudService

logger = logging.getLogger(__name__)
MAX_CAMPAIGNS_PER_REQUEST = 50


class AccountService(BaseService):

    def __init__(self, client):
        super().__init__(client)
        self.endpoint = 'marketers'

    def list(self):
        return self.execute('GET', self.build_uri())

    def get(self, element_id):
        return self.execute('GET', self.build_uri(element_id))

    def update(self, element_id, **attrs):
        return self.execute('POST', self.build_uri(element_id), **attrs)

    def _get_campaigns(self, element_id):
        params = {'limit': MAX_CAMPAIGNS_PER_REQUEST, 'offset': 0}
        url = '{}/campaigns'.format(element_id)
        do_continue = True
        while do_continue:
            result = self.execute('GET', self.build_uri(url),
                                  query_params=params)
            yield from result['campaigns']
            params['offset'] += len(result['campaigns'])
            if params['offset'] >= result['totalCount']:
                break

    def get_campaigns(self, element_id):
        return list(self._get_campaigns(element_id))


class CampaignService(CrudService):

    def __init__(self, client, account_id):
        super().__init__(client, account_id)
        self.endpoint = 'campaigns'
