import logging

from .base import BaseService, CrudService

logger = logging.getLogger(__name__)
MAX_CAMPAIGNS_PER_REQUEST = 50
MAX_PROMOTED_LINKS_PER_REQUEST = 100


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
        child_endpoint = 'campaigns'
        params = {'limit': MAX_CAMPAIGNS_PER_REQUEST}
        yield from self.get_child_elements(element_id, child_endpoint, params)

    def get_campaigns(self, element_id):
        return list(self._get_campaigns(element_id))


class CampaignService(CrudService):

    def __init__(self, client):
        super().__init__(client)
        self.endpoint = 'campaigns'

    def get_promoted_links(self, element_id, extra_fields=None):
        child_endpoint = 'promotedLinks'
        params = {'limit': MAX_PROMOTED_LINKS_PER_REQUEST}
        if extra_fields:
            params['extraFields'] = extra_fields
        return list(self.get_child_elements(element_id, child_endpoint,
                                            params))


class PromotedLinkService(CrudService):

    def __init__(self, client):
        super().__init__(client)
        self.endpoint = 'promotedLinks'
