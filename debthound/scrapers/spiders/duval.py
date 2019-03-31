
from scrapers.spiders.broward import Broward


class Duval(Broward):
    name = 'duval'
    start_urls = ['https://or.duvalclerk.com/search/SearchTypeDocType?Length=6']
    disclaimer = 'https://or.duvalclerk.com/search/Disclaimer'
    grid_results = 'https://or.duvalclerk.com/Search/GridResults'
    has_results = 'https://or.duvalclerk.com/Search/HasResults'
    id = 'https://or.duvalclerk.com'
    image_url = 'https://or.duvalclerk.com/Image/DocumentPdfAllPages/'

    init_days_increment = 14
    page_size = 10000

    _doctypes = '79, 87, 129'
    # 79 = CC COURT JUDGMENT (CCCJUDG),
    # 87 = DEED (DEED)
    # 129 = SATISFACTION (SAT)
    # 130 = SATISFACTION NO FEE (SATNF)

    _doctype_maps = {
        'CC COURT JUDGMENT': 'JUD C',
        'DEED': 'D',
        'SATISFACTION': 'SAT'
    }

