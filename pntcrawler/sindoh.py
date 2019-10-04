from bs4 import BeautifulSoup
from pntcrawler.common import get_empty_data, get_page_source

# 작동 모델: 신도 CM3091
def get_sindoh_cm3091(dept, model, ip):
    try:
        print(dept + " 부서의 " + model + " 소모품 정보 크롤링 중...")

        # 크롤링
        url = 'http://' + ip + '/wcd/system_consumable.xml'
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        levelPer1 = soup.findAll('input', {'class': 'LevelPer LevelPer1'}) # class="LevelPer LevelPer1"인 input 태그를 전부 가져옴
        levelPer2 = soup.findAll('input', {'class': 'LevelPer LevelPer2'})
        levelPer3 = soup.findAll('input', {'class': 'LevelPer LevelPer3'})
        levelPer4 = soup.findAll('input', {'class': 'LevelPer LevelPer4'})

        # Dictionary 생성
        data = { 
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_y': int(levelPer1[0]['value']), # input 태그의 value 속성 값을 가져옴
            'toner_m': int(levelPer2[0]['value']),
            'toner_c': int(levelPer3[0]['value']),
            'toner_k': int(levelPer4[0]['value']), 
            'drum_y' : int(levelPer1[1]['value']), # 이상하게 드럼 값은 class="levelPer LevelPer1"인 태그 쪽에 몰려있음... 
            'drum_m' : int(levelPer1[2]['value']),
            'drum_c' : int(levelPer1[3]['value']),
            'drum_k' : int(levelPer1[4]['value']),
            'note': ""
        }

        print("성공!")
        return data

    except Exception as ex:
        data = get_empty_data(ex, dept, model, ip)
        return data


# 작동 모델: 신도 D417, D716, CM3091 일부 모델
def get_sindoh_d417(dept, model, ip):
    try: 
        print(dept + " 부서의 " + model + " 소모품 정보 크롤링 중...")
        
        # 크롤링
        url = 'http://' + ip + '/wcd/system_consumable.xml'
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('td', {'width': '45px'})

        # Dictionary 생성
        data = { 
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_y': int(data[0].contents[0].replace('\n', '').replace('\t', '').replace('%', '')),
            'toner_m': int(data[1].contents[0].replace('\n', '').replace('\t', '').replace('%', '')),
            'toner_c': int(data[2].contents[0].replace('\n', '').replace('\t', '').replace('%', '')),
            'toner_k': int(data[3].contents[0].replace('\n', '').replace('\t', '').replace('%', '')),
            'drum_c' : int(data[4].contents[0].replace('\n', '').replace('\t', '').replace('%', '')),
            'drum_m' : int(data[5].contents[0].replace('\n', '').replace('\t', '').replace('%', '')),
            'drum_y' : int(data[6].contents[0].replace('\n', '').replace('\t', '').replace('%', '')),
            'drum_k' : int(data[7].contents[0].replace('\n', '').replace('\t', '').replace('%', '')),
            'note': ""
        }

        print("성공!")
        return data

    except Exception as ex:
        data = get_empty_data(ex, dept, model, ip)
        return data
