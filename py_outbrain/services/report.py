import logging
from datetime import datetime, date

from py_outbrain.services.base import AccountScopedService


logger = logging.getLogger(__name__)


class ReportService(AccountScopedService):
    allowed_filters = ()

    def __prepare_filters(self, start, end, **filters):
        assert isinstance(start, (datetime, date)), \
            "Start date filter must be a date/datetime instance"
        assert isinstance(end, (datetime, date)), \
            "End date filter must be a date/datetime instance"

        if isinstance(start, datetime):
            start = start.date()
        if isinstance(end, datetime):
            end = end.date()

        f = {'start_date': start.isoformat(),
             'end_date': end.isoformat()}

        for key, value in filters.items():
            if key in self.allowed_filters:
                f[key] = value
            else:
                logger.debug('%s is not allowed as a filter for %s',
                             key, self.__class__.__name__)
        return f

    def fetch(self, url, start_date, end_date, **filters):
        real_filters = self.__prepare_filters(start_date, end_date, **filters)
        res =  self.execute('GET', self.build_uri(url),
                            query_params=real_filters)
        return res


class CampaignSummaryReport(ReportService):

    def fetch(self, element_id, start_date, end_date, periodic='monthly', campaignId=None):
        self.endpoint = 'reports/marketers'
        url = '{}/campaigns/periodic'.format(element_id)
        query_params = {
            'includeConversionDetails': True,
            'conversionsByClickDate': True,
            'from': start_date,
            'to': end_date,
            'breakdown': periodic
        }
        if campaignId:
            query_params['campaignId'] = campaignId

        return self.execute('GET', self.build_uri(url),
                            query_params=query_params)

    allowed_filters = ('campaign', 'platform', 'country', 'site')
