import json
import logging
import requests
import requests.auth

from py_outbrain.errors import Unauthorized
from py_outbrain.utils import parse_response

logger = logging.getLogger(__name__)

MOCK_URL = 'https://private-anon-832f2f406c-amplifyv01.apiary-mock.com'
PROD_URL = 'https://api.outbrain.com/amplify/v0.1'


class OutbrainClient:

    default_access_token = None

    def __init__(self, username, password, dry_run=False,
                 token_getter=None, token_setter=None):
        if dry_run:
            self.base_url = MOCK_URL
        else:
            self.base_url = PROD_URL
        self.username = username
        self.password = password

        def _default_token_setter(token):
            self.default_access_token = token

        def _default_token_getter():
            return self.default_access_token

        self._token_getter = token_getter or _default_token_getter
        self._token_setter = token_setter or _default_token_setter

    def generate_new_token(self):
        login_url = '{}/login'.format(self.base_url)

        basic_auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        r = requests.get(login_url, auth=basic_auth)
        results = json.loads(r.text)
        token = results['OB-TOKEN-V1']
        self.access_token = token
        return token

    @property
    def authorization_header(self):
        if not self.access_token:
            raise Exception
        return {
            'OB-TOKEN-V1': self.access_token
        }

    @property
    def access_token(self):
        token = self._token_getter()
        if not token:
            token = self.generate_new_token()
        return token

    @access_token.setter
    def access_token(self, access_token):
        self._token_setter(access_token)

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
