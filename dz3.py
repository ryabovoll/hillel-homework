class Url:

    def __init__(self, scheme=None, authority=None, path=None, query=None, fragment=None):
        self.scheme = scheme
        self.authority = authority
        self.path = path
        self.query = query
        self.fragment = fragment

    def __eq__(self, other):
        return str(self) == other

    def __str__(self):
        string = f'{self.scheme}://{self.authority}'
        if self.path:
            for p in self.path:
                string += f'/{p}'
        if self.query:
            string += f"?{'&'.join(f'{k}={v}' for k,v in self.query.items())}"
        if self.fragment:
            string += f'#{self.fragment}'
        return string


class HttpsUrl(Url):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.scheme = 'https'


class HttpUrl(Url):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.scheme = 'http'


class GoogleUrl(HttpsUrl):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.authority = 'google.com'


class WikiUrl(HttpsUrl):

    def __init__(self, *args, **kwargs):
        super().__init__(self, *args, **kwargs)
        self.authority = 'wikipedia.org'


class UrlCreator:

    def __init__(self, scheme, authority, path=None, query=None, fragment=None):
        self.scheme = scheme
        self.authority = authority
        self.path = path
        self.query = query
        self.fragment = fragment

    def _create(self):
        return UrlCreator(self.scheme, self.authority, self.path, self.query, self.fragment)

    __eq__ = Url.__eq__

    __str__ = Url.__str__

    def __getattr__(self, name):
        if self.path:
            self.path += [name]
        else:
            self.path = [name]
        return self

    def __call__(self, *args, **kwargs):
        if args:
            self.path = list(args)
        if kwargs:
            self.query = kwargs
        return self


assert GoogleUrl() == HttpsUrl(authority='google.com')
assert GoogleUrl() == Url(scheme='https', authority='google.com')
assert GoogleUrl() == 'https://google.com'
assert WikiUrl() == str(Url(scheme='https', authority='wikipedia.org'))
assert WikiUrl(path=['wiki', 'python']) == 'https://wikipedia.org/wiki/python'
assert GoogleUrl(query={'q': 'python', 'result': 'json'}) == 'https://google.com?q=python&result=json'

url_creator = UrlCreator(scheme='https', authority='docs.python.org')
assert url_creator.docs.v1.api.list == 'https://docs.python.org/docs/v1/api/list'
assert url_creator('api', 'v1', 'list') == 'https://docs.python.org/api/v1/list'
assert url_creator('api', 'v1', 'list', q='my_list') == 'https://docs.python.org/api/v1/list?q=my_list'
assert url_creator('3').search(q='getattr', check_keywords='yes', area='default')._create() == \
       'https://docs.python.org/3/search?q=getattr&check_keywords=yes&area=default'
