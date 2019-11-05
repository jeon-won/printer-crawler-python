from bs4 import BeautifulSoup
from pntcrawler.common import get_crawl_data, get_error_data, get_page_source
import re

"""
컬러 복합기
"""

def get_sindoh_cm3091(dept, model, ip):
    """
    Sindoh CM3091 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """

    try:
        # 크롤링
        url = f"http://{ip}/wcd/system_consumable.xml"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        levelPer1 = soup.findAll('input', {'class': 'LevelPer LevelPer1'}) # class="LevelPer LevelPer1"인 input 태그를 전부 가져옴
        levelPer2 = soup.findAll('input', {'class': 'LevelPer LevelPer2'})
        levelPer3 = soup.findAll('input', {'class': 'LevelPer LevelPer3'})
        levelPer4 = soup.findAll('input', {'class': 'LevelPer LevelPer4'})

        # Dictionary 생성
        data = get_crawl_data(dept = dept, model = model, ip = ip,
            toner_y = int(levelPer1[0]['value']), # input 태그의 value 속성 값을 가져옴
            toner_m = int(levelPer2[0]['value']),
            toner_c = int(levelPer3[0]['value']),
            toner_k = int(levelPer4[0]['value']), 
            drum_y = int(levelPer1[1]['value']), # 이상하게 드럼 값은 class="levelPer LevelPer1"인 태그 쪽에 몰려있음... 
            drum_m = int(levelPer1[2]['value']),
            drum_c = int(levelPer1[3]['value']),
            drum_k = int(levelPer1[4]['value']))

        print(f"{dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(data)
        return data

    except Exception as ex:
        data = get_error_data(ex, dept, model, ip)
        return data


def get_sindoh_d417(dept, model, ip):
    """
    Sindoh D417, D716 및 CM3091 일부 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """

    try: 
        # 크롤링
        url = f"http://{ip}/wcd/system_consumable.xml"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('td', {'width': '45px'})

        # Dictionary 생성
        data = get_crawl_data(dept = dept, model = model, ip = ip,
            toner_y = int(re.findall(r"\d+", data[0].getText())[0]),
            toner_m = int(re.findall(r"\d+", data[1].getText())[0]),
            toner_c = int(re.findall(r"\d+", data[2].getText())[0]),
            toner_k = int(re.findall(r"\d+", data[3].getText())[0]),
            drum_c = int(re.findall(r"\d+", data[4].getText())[0]),
            drum_m = int(re.findall(r"\d+", data[5].getText())[0]),
            drum_y = int(re.findall(r"\d+", data[6].getText())[0]),
            drum_k = int(re.findall(r"\d+", data[7].getText())[0]))

        print(f"{dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(data)
        return data

    except Exception as ex:
        data = get_error_data(ex, dept, model, ip)
        return data


"""
흑백 프린터
"""

def get_sindoh_b605n(dept, model, ip):
    """
    Sindoh B605n 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """
    try: 
        # 크롤링
        url = f"http://{ip}/status.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('font', {'id': 'smsz'})

        # Dictionary 생성
        data = get_crawl_data(dept = dept, model = model, ip = ip,
            toner_k = int(re.findall(r"\d+", data[2].getText())[0]),
            drum_k = "")  # 이상하게 드럼 정보는 찾을 수 없음...

        print(f"{dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(data)     
        return data

    except Exception as ex:
        data = get_error_data(ex, dept, model, ip)
        return data