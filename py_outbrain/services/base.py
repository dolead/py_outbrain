import logging


logger = logging.getLogger(__name__)


class BaseService:
    """
    Service class, expose calls

    """
    def __init__(self, client):
        self.client = client
        self.endpoint = client.base_url

    def build_uri(self, endpoint=None):
        if not endpoint:
            return self.endpoint
        while endpoint.startswith('/'):
            endpoint = endpoint[1:]
        return '{}/{}'.format(self.endpoint, endpoint)

    def execute(self, method, uri, query_params=None, **payload):
        return self.client.execute(method, uri,
                                   query_params=query_params,
                                   **payload)

    def get_child_elements(self, element_id, child_endpoint, params):
        if 'offset' not in params:
            params['offset'] = 0
        url = '{}/{}'.format(element_id, child_endpoint)
        while True:
            result = self.execute('GET', self.build_uri(url),
                                  query_params=params)
            yield from result[child_endpoint]
            params['offset'] += len(result[child_endpoint])
            if params['offset'] >= result['totalCount']:
                break


class CrudService(BaseService):

    def list(self):
        return self.execute('GET', self.build_uri())

    def get(self, element_id, extra_fields=None):
        params = None
        if extra_fields:
            params = {'extraFields': extra_fields}
        return self.execute('GET', self.build_uri(element_id),
                            query_params=params)

    def create(self, **attrs):
        return self.execute('POST', self.build_uri(), **attrs)

    def update(self, element_id, **attrs):
        return self.execute('PUT', self.build_uri(element_id), **attrs)
