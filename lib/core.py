import json
import pprint
from urllib2 import urlopen
from urllib import urlencode
from urllib import quote_plus
from urllib import quote
class CoreApiRequestor:

    def __init__(self, repository_id, api_key):
        self.repository_id = repository_id
        self.endpoint = 'http://core.ac.uk/api-v2'
        self.method = '/articles/search'
        self.query = 'repositories.id:' + str(self.repository_id)
        self.api_key = api_key
        self.pagesize = 10

    def get_request_url(self, page):
        params = {'apiKey': self.api_key,
                  'page': page,
                  'pageSize': self.pagesize}

        encoded_params = urlencode(params)
        return self.endpoint + self.method + '/' + self.query + '?' \
                             + encoded_params

    def parse_response(self, decoded):
        res = []
        for item in decoded['data']:
            doi = None
            if 'identifiers' in item:
                for identifier in item['identifiers']:
                    if identifier and identifier.startswith('doi:'):
                        doi = identifier
                        break
            res.append([item['title'], doi])
        return res

    def get_docs_from_core(self, page):
        res = urlopen(self.get_request_url(page))
        #res = urllib.request.urlopen(req)
        return res.read()


if __name__ == '__main__':
    page = 1
    oxford_repository_id = 88
    r = CoreApiRequestor(oxford_repository_id, 'nTo627BU8jPNth4EbsrDue9IXWzAfZiY')
    print(r.get_request_url(page))

