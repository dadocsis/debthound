import abc
from lxml import html
from urllib.parse import urlencode, parse_qs

import requests
from werkzeug.contrib.cache import SimpleCache
from urllib3.response import HTTPResponse
from urllib3.packages.six.moves import http_client as httplib

from data_api.models import Document, Site


cache = SimpleCache()


class ImageHandlerBase():
    handles = object()

    @abc.abstractmethod
    def handle(self, record: Document) -> requests.Response:
        ...


class Default(ImageHandlerBase):
    def handle(self, record: Document):
        rsp = requests.get(record.image_uri)
        return rsp


class PBC(ImageHandlerBase):
    handles = 'pbc'

    def handle(self, record: Document):
        rsp = requests.get(record.image_uri)
        _html = html.fromstring(rsp.text)
        xparms = _html.xpath('//form[@name="courtform"]/input[@type="hidden"]')
        _parms = ((p.name, (None, p.value)) for p in xparms)
        rsp = requests.post('http://oris.co.palm-beach.fl.us:8080/PdfServlet/PdfServlet27',
                            files=_parms,
                            cookies=rsp.cookies)
        return rsp


class Pinellas(ImageHandlerBase):
    handles = 'pinellas'

    def handle(self, record: Document):
        s = requests.session()

        def get():
            url = 'https://officialrecords.mypinellasclerk.org/search/Disclaimer'
            if cache.get('pinellas_image_cookies'):
                cookies = cache.get('pinellas_image_cookies')
                s.get(record.image_uri, cookies=cookies) # this will generate the full pdf for the subsequent request
            else:
                s.post(url, data=urlencode({'disclaimer': 'true'}), headers={'Content-Type': 'application/x-www-form-urlencoded'})
                cookies = s.cookies
                cache.set('pinellas_image_cookies', cookies)

            session_id = cookies.get('ASP.NET_SessionId')
            _, __, img_id = record.image_uri.rpartition('/')
            referer = 'https://officialrecords.mypinellasclerk.org/Image/DocumentImage1/{0}'.format(img_id)
            s.get('https://officialrecords.mypinellasclerk.org/Image/DocumentImage1/{1}?atalaremote=true' \
                '&atala_id=_docImageVwr' \
                '&atala_wiv=true' \
                '&atala_ipx=0&' \
                'atala_ipy=0&' \
                'atala_iw=1700&' \
                'atala_ih=2321&' \
                'atala_w=900px&' \
                'atala_h=900px&' \
                'atala_z=0.38776389487289964&' \
                'atala_az=1&' \
                '&atala_fi=0&' \
                'atala_and=1&' \
                'atala_bf=3&' \
                'atala_cin=1&' \
                'atala_rsh=0&' \
                'atala_rsx=0' \
                '&atala_rsy=0&' \
                'atala_rsw=0&' \
                'atala_rsv=false&' \
                'atala_rnd=78153063&' \
                'atala_rm=SaveAsPdf&' \
                'atala_ran0={1}'.format(session_id, img_id))
            return s.get('https://officialrecords.mypinellasclerk.org/WebAtalaCache/{0}_{1}_docPdf.pdf'.format(
                session_id, img_id), headers={'Referer': referer})

        rsp = get()
        # try one more time if failed
        if rsp.status_code != 200:
            return get()

        return rsp


class Polk(ImageHandlerBase):
    handles = 'polk'

    def handle(self, record: Document):
        s = requests.session()
        rsp = s.post('https://apps.polkcountyclerk.net/browserviewor/api/document', json={"ID": record.image_uri}, verify=False)
        data = rsp.json()
        pages = data['doc_pages']
        parms = {
            'ID': record.image_uri,
            'Pages': pages,
            'StartPage': 1
        }
        return s.post('https://apps.polkcountyclerk.net/browserviewor/api/pdf', json=parms, verify=False)


class Hills(ImageHandlerBase):
    handles = 'hillsborough'

    doc_type_map = {
        'JUD C': 'CCJ',
        'D': 'D',
        'SAT': 'SAT'
    }

    def handle(self, record: Document):
        base = 'http://pubrec3.hillsclerk.com/oncore/'
        qs = record.image_uri.split('?')[1]
        url1 = base + record.image_uri
        url2 = base + 'DetailTop.aspx?ref=search'
        url3 = f'{base}?{qs}'
        qs = parse_qs(qs)
        url4 = base + f'ImageBrowser/default.aspx?id={qs["id"][0]}&dtk={self.doc_type_map[record.doc_type.name]}'
        url5 = base + 'ImageBrowser/ShowPDF.aspx'
        s = requests.session()
        s.get(url1)
        s.get(url2)
        s.get(url3)
        s.get(url4)
        rsp = s.get(url5, headers={'Referer': url4, 'Accept-Encoding': 'gzip, deflate', 'Connection': 'keep-alive'}, stream=False)
        return rsp


def handler_factory(site: Site) -> ImageHandlerBase:
    handler = next(iter([cls() for cls in ImageHandlerBase.__subclasses__() if cls.handles == site.spider_name]), None)
    if not handler:
        handler = Default()
    return handler


# have to monkey patch as urlib would error doing a chumked stream with hillsborough pdfs
def _update_chunk_length(self):
    # First, we'll figure out length of a chunk and then
    # we'll try to read it from socket.
    if self.chunk_left is not None:
        return
    line = self._fp.fp.readline()
    line = line.split(b';', 1)[0]
    line = (len(line) > 0 and line or "0")
    try:
        self.chunk_left = int(line, 16)
    except ValueError:
        # Invalid chunked protocol response, abort.
        self.close()
        raise httplib.IncompleteRead(line)


HTTPResponse._update_chunk_length = _update_chunk_length
