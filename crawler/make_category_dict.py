from bs4 import BeautifulSoup
import urllib3
import re
import os
import json

        
def main():
    url = 'https://townwork.net/shizuoka/'
    req = urllib3.PoolManager()
    res = req.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')
    cate_list = soup.find(id="jsi-job-category-accordion-wrapper").find_all(id=re.compile(r"checkboxfield\d+"))

    jc_cate, jc_value = None, None
    jc_dicts, jmc_dicts = [], []
    for c in cate_list:
        if c.get('name') == 'jc':
            jc_cate = c.get('data-selection-category')
            jc_value = c.get('value')
            jc_dicts.append(
                dict(
                    category=jc_cate,
                    name=c.get('data-selection-name'),
                    value=jc_value
                )
            )
        elif c.get('name') == 'jmc' and c.get('data-selection-category') == jc_cate:
            jmc_dicts.append(
                dict(
                    category=c.get('data-selection-category'),
                    name=c.get('data-selection-name'),
                    jc_value=jc_value,
                    jmc_value=c.get('value')
                )
            )
        else:
            raise ValueError()
            
    category_dict = dict(
        jc=jc_dicts,
        jmc=jmc_dicts
    )
    
    jcs = list(map(lambda x : x.get('category'), category_dict['jc']))
    jmcs = {category: [name] for category, name in list(map(lambda x : (x.get('category'), x.get('name')) , category_dict['jc']))}
    for category, name in list(map(lambda x : (x.get('category'), x.get('name')) , category_dict['jmc'])):
        jmcs.get(category).append(name)
    
    os.makedirs('./townwork/json', exist_ok=True)
    with open('./townwork/json/category_dict.json', 'w', encoding='utf-8') as f:
        json.dump(category_dict, f, indent=6, ensure_ascii=False)
    with open('./townwork/json/jc.json', 'w', encoding='utf-8') as f:
        json.dump(jcs, f, indent=6, ensure_ascii=False)
    with open('./townwork/json/jmc.json', 'w', encoding='utf-8') as f:
        json.dump(jmcs, f, indent=6, ensure_ascii=False)
    with open('./townwork/json/all.json', 'w', encoding='utf-8') as f:
        json.dump(sum(jmcs.values(), []), f, ensure_ascii=False)
    

if __name__ == "__main__":
    main()