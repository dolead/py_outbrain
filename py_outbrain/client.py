import json
import logging
import requests

from py_outbrain.errors import Unauthorized
from py_outbrain.utils import parse_response

logger = logging.getLogger(__name__)


class OutbrainClient:
    def __init__(self, access_token, username, password, base_url):
        self.base_url = base_url or 'https://api.outbrain.com/amplify/v0.1'

        if not access_token:
            access_token = self.generate_new_token(username, password)
        self.access_token = access_token

    def generate_new_token(self, username, password):
        login_url = '{}/login'.format(self.base_url)

        basic_auth = requests.auth.HTTPBasicAuth(username, password)
        r = requests.get(login_url, auth=basic_auth)
        results = json.loads(r.text)
        return results['OB-TOKEN-V1']

    @property
    def authorization_header(self):
        if not self.access_token:
            raise Exception
        return {
            'OB-TOKEN-V1': self.access_token
        }

    def execute(self, method, uri, query_params=None,
                allow_refresh=True, raw=False, authenticated=True,
                **payload):
        url = '{}/{}'.format(self.base_url, uri)
        headers = self.authorization_header if authenticated else {}
        if method.upper() in ('POST', 'PUT') and not raw:
            headers['Content-Type'] = 'application/json'

        try:
            data = None
            if payload:
                data = payload if raw else json.dumps(payload)
            result = requests.request(method, url, data=data,
                                      params=query_params,
                                      headers=headers)
            return parse_response(result)
        except Unauthorized:
            if not allow_refresh:
                raise
            self.generate_new_token()
            return self.execute(method, uri, query_params=query_params,
                                raw=raw, allow_refresh=False, **payload)
