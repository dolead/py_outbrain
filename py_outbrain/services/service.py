import logging

from datetime import date, timedelta
from dateutil.parser import parse as parsedate
from .base import BaseService, CrudService

logger = logging.getLogger(__name__)
MAX_CAMPAIGNS_PER_REQUEST = 50
MAX_PROMOTED_LINKS_PER_REQUEST = 100


class BudgetService(BaseService):

    def __init__(self, client):
        super().__init__(client)
        self.endpoint = 'budgets'

    def delete_budget(self, budget_id):
        return self.execute('DELETE', self.build_uri(budget_id))


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

    def get_budgets(self, element_id, detached_only):
        params = {}
        if detached_only:
            params['detachedOnly'] = True
        url = '{}/{}'.format(element_id, 'budgets')
        return self.execute('GET', self.build_uri(url), query_params=params)

    def create_budget(self, element_id, amount: float = 0,
                      name: str = 'defaultName',
                      start_date: str = None,
                      end_date: str = None,
                      pacing: str = 'AUTOMATIC',
                      budget_type: str = 'CAMPAIGN',
                      daily_target: float = None):
        params = {}
        if start_date is None:
            start_date = date.today().isoformat()
        params['startDate'] = start_date
        if end_date is None:
            # params['runForever'] = True  # doesn't work
            # must still provide an endDate, although runForver is true
            params['endDate'] = '2099-12-31'
        else:
            params['endDate'] = end_date
        params['name'] = name
        params['amount'] = amount
        params['type'] = budget_type
        params['pacing'] = pacing
        if daily_target is not None:
            params['dailyTarget'] = daily_target

        url = '{}/{}'.format(element_id, 'budgets')
        return self.execute('POST', self.build_uri(url), **params)


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
