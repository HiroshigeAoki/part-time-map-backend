from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import HtmlResponse
from geojson import Point
import json
import re
from datetime import datetime
from dateutil import tz
from scrapy.shell import inspect_response
from bs4 import BeautifulSoup
from normalize_japanese_addresses import normalize


from townwork.items import Job
from crawler.organize_db import OrganizeDB

class DetailSpider(CrawlSpider):
    name = 'detail'
    allowed_domains = ['townwork.net']
    custom_settings = {
        'ITEM_PIPELINES': {
            'townwork.pipelines.ValidationPipline': 200,
            'townwork.pipelines.MongoPipeline': 800,
        }
    }
    
    def __init__(self, *args, **kwargs):
        super(DetailSpider, self).__init__(*args, **kwargs)
        
        with open('json/urls.json') as f:
            urls =  list(json.load(f)[0].values())
            
        with open('json/category_dict.json') as f:
            category_dict = json.load(f)
        
        self.id2cat = {c['jmc_value']: c for c in category_dict.get('jmc')}
        
        self.jmc_list = category_dict.get('jmc')
        self.start_urls = []
        for url in urls:
            for jmc in self.jmc_list:
                self.start_urls.append(f"{url}jc_{jmc.get('jc_value')}/jmc_{jmc.get('jmc_value')}")

    # ignore existing urls in db.
    organizer = OrganizeDB()
    organizer.drop_expired()
    deny = organizer.existing_urls()

    rules = [
        Rule(LinkExtractor(allow=r'(/\w+)+/\?page=\d+')), # ページ遷移1~
        Rule(LinkExtractor(allow=[r'/detail/clc_\d+/joid_\w+/', r'/detail/clc_\d+/\?opf=\w+'], deny=deny, restrict_xpaths='//*[@class="job-lst-main-cassette-wrap"]'), callback='parse_detail') # 詳細ページをparse
    ]

    def _requests_to_follow(self, response):
        if not isinstance(response, HtmlResponse):
            return
        seen = set()
        jmc_id = re.findall(r'jmc_(\d+)', response.url)[0]
        jc_jmc = (
            dict(
                jc = self.id2cat.get(jmc_id).get('category'),
                jmc = self.id2cat.get(jmc_id).get('name')
            )
        )
        for rule_index, rule in enumerate(self._rules):
            links = [lnk for lnk in rule.link_extractor.extract_links(response)
                    if lnk not in seen]
            for link in rule.process_links(links):
                seen.add(link)
                request = self._build_request(rule_index, link)
                request.meta.update(jc_jmc)
                yield rule.process_request(request, response)

    def parse_detail(self, response):
        item = Job()
        #inspect_response(response, self)
        item["url"] = response.url
        item["jc"] = response.meta['jc']
        item["jmc"] = response.meta['jmc']
        item['name'] = BeautifulSoup(response.css('.jsc-company-txt').get(), features='lxml').getText().strip().replace('\u3000', ' ')
        preferences = BeautifulSoup(response.css('.job-detail-merit-inner').get(), features='lxml').getText().strip().split('\n')
        item['preferences'] = [p.replace('\n', '') for p in preferences if '\n' != p or '……' != p or p != '……\n']
        
        JST = tz.gettz('Asia/Tokyo')
        item['fetched_date'] = datetime.now(JST)#js-detailArea > div:nth-child(3) > div > div.job-age-txt.job-detail-remaining-date-age > p 

        dt_list = response.css('dt')
        for dt in dt_list:
            dt_value = dt.css('::text').get()
            if dt_value == '職種' and not 'type_of_job' in item.keys():
                item['type_of_job'] = BeautifulSoup(dt.xpath('./following-sibling::dd').get(), features='lxml').getText().strip().replace('\u3000', ' ')
            elif dt_value == '掲載期間' and not 'deadline' in item.keys():
                period = BeautifulSoup(dt.xpath('./following-sibling::dd').get(), features='lxml').getText().strip()
                item['deadline'] = datetime(*map(int, re.findall(r'～(\d+)年(\d+)月(\d+)日(\d+):(\d+)', period)[0]), tzinfo=JST)
                item['is_definite'] = True
            elif dt_value == '会社住所' and not 'address' in item.keys():
                item['address'] = BeautifulSoup(dt.xpath('./following-sibling::dd').get(), features='lxml').getText().strip().replace('\u3000', ' ')
            elif dt_value == '給与' and not 'wages' in item.keys():
                item['wages'] = BeautifulSoup(dt.xpath('./following-sibling::dd').get(), features='lxml').getText().strip().replace('\u3000', ' ')
            elif dt_value == '対象となる方・資格' and not 'target' in item.keys():
                item['target'] = BeautifulSoup(dt.xpath('./following-sibling::dd').get(), features='lxml').getText().strip().replace('\u3000', ' ')
            elif dt_value == '勤務時間' and not 'working_hours' in item.keys():
                item['working_hours'] = BeautifulSoup(dt.xpath('./following-sibling::dd').get(), features='lxml').getText().strip().replace('……', ':').replace('\n\n\n', ', ').replace('\n', '').replace('\u3000', ' ')
            elif dt_value == '勤務期間' and not 'work_period' in item.keys():
                item['work_period'] = BeautifulSoup(dt.xpath('./following-sibling::dd').get(), features='lxml').getText().strip().replace('……', ':').replace('\n\n\n', ', ').replace('\n', '').replace('\u3000', ' ')
            elif dt_value == '勤務地' and not 'loc' in item.keys():
                a_tag = BeautifulSoup(dt.xpath('./following-sibling::dd').get(), features='lxml').find('a')
                if a_tag is None:
                    continue
                item['loc'] = Point((float(a_tag['data-lon']), float(a_tag['data-lat'])))
                item['is_loc_accurate'] = True

        if not 'deadline' in item.keys(): # 応募が決まり次第募集終了。
            item['deadline'] = item['fetched_date']
            item['is_definite'] = False
                
        if not 'loc' in item.keys():
            nom = normalize(re.sub(r'^\d+-\d+', '', item['address'])) # delete zip code.
            if nom.get('level') <= 2: # 緯度経度情報がなく、住所が不正確な場合はdrop
                item['loc'] = None
            elif nom.get('level') == 3: # 町丁目まで判別できたが、緯度経度情報がのもので不正確。
                item['loc'] = Point((float(nom.get('lng')), float(nom.get('lat'))))
                item['is_loc_accurate'] = False

        esDic = {"[Ａ]": "アルバイト", "[Ｐ]": "パート", "[契]": "契約社員", "[社]": "正社員", "[派]": "派遣", "[委]": "業務委託", "[紹]": "職業紹介/紹介予定派遣"}
        item['es'] =  [esDic.get(es) for es in re.findall(r'\[.+?\]', item['type_of_job'])] # 雇用形態 employment status
        
        yield item