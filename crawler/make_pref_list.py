from bs4 import BeautifulSoup
import urllib3
import os
import json

        
def main():
    url = 'https://townwork.net/merit/'
    req = urllib3.PoolManager()
    res = req.request('GET', url)
    soup = BeautifulSoup(res.data, 'html.parser')
    pref_list = [a.getText() for a in soup.find_all(['a']) if "merit" in a.get('href') or "short" in a.get('href') or "kousyuunyuu" in a.get('href')]

    os.makedirs('./townwork/json', exist_ok=True)
    with open('./townwork/json/pref_list.json', 'w', encoding='utf-8') as f:
        json.dump(pref_list, f, indent=6, ensure_ascii=False)    

if __name__ == "__main__":
    main()