import logging

from .base import BaseService, CrudService

logger = logging.getLogger(__name__)


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

    def get_campaigns(self, element_id):
        url = '{}/campaigns'.format(element_id)
        return self.execute('GET', self.build_uri(url))['campaigns']


class CampaignService(CrudService):

    def __init__(self, client, account_id):
        super().__init__(client, account_id)
        self.endpoint = 'campaigns'
