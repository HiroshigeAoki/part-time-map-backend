from scrapy.spiders import SitemapSpider
import re
from townwork.items import Area

# 範囲を広げる時に使いたいURLを取得するために使う。
class URLSpider(SitemapSpider):
    name = 'url'
    allowed_domains = ['townwork.net']

    sitemap_urls = [
        'https://townwork.net/robots.txt'
    ]

    # 地域、駅、地下鉄のリストのみ辿る。
    sitemap_follow = [
        r'sitemap_marea', # 政令指定都市・県庁
        r'sitemap_sarea', # その他の市・区
        r'sitemap_ssarea', # 町・村
        #r'sitemap_station',
        #r'sitemap_railway.xml'
    ]

    # とりあえず浜松市中区静大周辺・冨塚・佐鳴台だけを扱う。
    sitemap_rules = [
        (r'shizuoka/ct_ma60001/tw_sa99129/sc_ss9912904/', 'parse_area')
    ]


    def parse_area(self, response):
        item = Area()
        if 'short' not in response.url and 'emc_02' not in response.url: #短期と派遣を削除
            item['url'] = response.url
            item['prefecture'] = re.match(r'https://townwork.net/(\w+)/.+$', item['url'])[0]
            
            
            