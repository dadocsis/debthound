import abc
from lxml import html
from urllib.parse import urlencode

import requests
from werkzeug.contrib.cache import SimpleCache

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


def handler_factory(site: Site) -> ImageHandlerBase:
    handler = next(iter([cls() for cls in ImageHandlerBase.__subclasses__() if cls.handles == site.spider_name]), None)
    if not handler:
        handler = Default()
    return handler
