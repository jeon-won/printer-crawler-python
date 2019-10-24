from bs4 import BeautifulSoup
from pntcrawler.common import get_error_data, get_page_source
import re


def get_oki_c843(dept, model, ip):
    """
    OKI C843 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """

    try:
        # 크롤링
        url = f"http://{ip}/printer/suppliessum.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('td', {'width': '70%'})

        # Dictionary 생성
        info = {
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_k': int(re.findall(r"\d+", data[0].contents[1])[0]),
            'toner_c': int(re.findall(r"\d+", data[1].contents[1])[0]),
            'toner_m': int(re.findall(r"\d+", data[2].contents[1])[0]),
            'toner_y': int(re.findall(r"\d+", data[3].contents[1])[0]),
            'drum_k': int(re.findall(r"\d+", data[4].contents[2])[0]),
            'drum_c': int(re.findall(r"\d+", data[5].contents[2])[0]),
            'drum_m': int(re.findall(r"\d+", data[6].contents[2])[0]),
            'drum_y': int(re.findall(r"\d+", data[7].contents[2])[0]),
            # 'belt': int(re.findall("\d+", data[7].contents[2])[0]),
            # 'fuser': int(re.findall("\d+", data[8].contents[2])[0]),
            'note': ""
        }

        print(f"{dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(info)
        return info

    except Exception as ex:
        info = get_error_data(ex, dept, model, ip)
        return info


def get_oki_es5112(dept, model, ip):
    """
    OKI ES5112 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """

    try:
        # 크롤링
        url = f"http://{ip}/printer/suppliessum.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('img', {'src': '../img/blackbar.gif'})

        # Dictionary 생성
        info = {
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_k': int(re.findall(r"\d+", data[0]['width'])[0]),
            'toner_c': "",
            'toner_m': "",
            'toner_y': "",
            'drum_k': int(re.findall(r"\d+", data[1]['width'])[0]),
            'drum_c': "",
            'drum_m': "",
            'drum_y': "",
            'note': ""
        }

        print(f"{dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(info)
        return info

    except Exception as ex:
        info = get_error_data(ex, dept, model, ip)
        return info
