from bs4 import BeautifulSoup
from pntcrawler.common import get_empty_data, get_page_source

# 작동 모델: OKI C843
def get_oki_c843(dept, model, ip):
    try: 
        print(dept + " 부서의 " + model + " 소모품 정보 크롤링 중...")

        # 크롤링
        url = "http://" + ip + "/printer/suppliessum.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('td', {'width': '70%'})

        # Dictionary 생성
        info = { 
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_k': int(data[0].contents[1].replace('\n', '').replace('\t', '').replace('%', '')),
            'toner_c': int(data[1].contents[1].replace('\n', '').replace('\t', '').replace('%', '')),
            'toner_m': int(data[2].contents[1].replace('\n', '').replace('\t', '').replace('%', '')),
            'toner_y': int(data[3].contents[1].replace('\n', '').replace('\t', '').replace('%', '')),
            'drum_k' : int(data[4].contents[2].replace('\n', '').replace('\t', '').replace('%', '')),
            'drum_c' : int(data[5].contents[2].replace('\n', '').replace('\t', '').replace('%', '')),
            'drum_m' : int(data[6].contents[2].replace('\n', '').replace('\t', '').replace('%', '')),
            'drum_y' : int(data[7].contents[2].replace('\n', '').replace('\t', '').replace('%', '')),
            # 'belt': int(data[7].contents[2].replace('\n', '').replace('\t', '').replace('%', '')),
            # 'fuser': int(data[8].contents[2].replace('\n', '').replace('\t', '').replace('%', '')),
            'note': ""
        }

        print("성공!")
        return info

    except Exception as ex:
        data = get_empty_data(ex, dept, model, ip)
        return data


# 작동 모델: OKI ES5112
def get_oki_es5112(dept, model, ip):
    try: 
        print(dept + " 부서의 " + model + " 소모품 정보 크롤링 중...")

        # 크롤링
        url = "http://" + ip + "/printer/suppliessum.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('img', {'src': '../img/blackbar.gif'})

        # Dictionary 생성
        info = { 
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_k': int(data[0]['width'].replace('%', '')),
            'toner_c': "",
            'toner_m': "",
            'toner_y': "",
            'drum_k' : int(data[1]['width'].replace('%', '')),
            'drum_c': "",
            'drum_m': "",
            'drum_y': "",
            'note': ""
        }

        print("성공!")
        return info

    except Exception as ex:
        data = get_empty_data(ex, dept, model, ip)
        return data
