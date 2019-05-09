import os
import requests
import certifi
from scrapers.spiders.broward import Broward

CERTIFIED_JUDGEMENTS = ['233', '238', '239', '240', '242', '243', '250', '251', '252', '852', '852']
CERTIFIED_JUDGEMENTS_DESC = ['CERTIFIED COPY OF A COURT JUDGEMENT/CERTIFIED COPY OF A COURT ORDER',
                             'CERTIFIED COPY OF A COURT JUDGMENT OR ORDER']
DEEDS = ['103', '295', '297', '302', '306', '314', '315', '595', '596', '796', '815', '859']
DEED_DESC = ['Deed', 'QUIT CLAIM DEED', 'TAX DEED', 'DEED']
SATISFACTIONS = ['856', '889']
SAT_DESC = ['CORPORATE SATISFACTION', 'SATISFACTION']

maps = {}
for k in CERTIFIED_JUDGEMENTS_DESC:
    maps[k] = 'JUD C'

for k in DEED_DESC:
    maps[k] = 'D'

for k in SAT_DESC:
    maps[k] = 'SAT'


# hack to trust ca
try:
    print('Checking connection .')
    test = requests.get('https://officialrecords.mypinellasclerk.org/search/Disclaimer?st=/search/SearchTypeDocType')
    print('Connection OK.')
except requests.exceptions.SSLError as err:
    print('SSL Error. Adding custom certs to Certifi store...')
    cafile = certifi.where()
    here = os.path.dirname(os.path.realpath(__file__))
    myca = os.path.join(here, 'digi.crt')
    with open(myca, 'rb') as infile:
        customca = infile.read()

    with open(cafile, 'ab') as outfile:
        outfile.write(customca)
    print('That might have worked.')


class Pinellas(Broward):
    name = 'pinellas'
    start_urls = ['https://officialrecords.mypinellasclerk.org/search/SearchTypeDocType']
    disclaimer = 'https://officialrecords.mypinellasclerk.org/search/Disclaimer'
    grid_results = 'https://officialrecords.mypinellasclerk.org/Search/GridResults'
    has_results = None
    id = 'https://officialrecords.mypinellasclerk.org'
    image_url = 'https://officialrecords.mypinellasclerk.org/Image/DocumentPdf/'

    init_days_increment = 14
    page_size = 10000

    _doctypes = ', '.join(CERTIFIED_JUDGEMENTS + DEEDS + SATISFACTIONS)
    _doctype_maps = maps
    overflow_err_msg = 'but is not allowed to exceed more than'
