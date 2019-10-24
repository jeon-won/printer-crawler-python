from bs4 import BeautifulSoup
from pntcrawler.common import get_error_data, get_page_source
import re


def get_xerox_c2265(dept, model, ip):
    """
    Xerox DCIVC2265, APVC2275, APVC3373, DCVC3374, DCVC3376, DCVIC3371, DPC5005D 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """

    try:
        # 크롤링
        url = f"http://{ip}/stsply.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('small')

        # Dictionary 생성
        info = {
            'dept': dept,
            'model': model,
            'ip': ip,
            # 문자열에서 숫자만 추출
            'toner_k': int(re.findall(r"\d+", data[5].getText())[0]),
            'toner_c': int(re.findall(r"\d+", data[8].getText())[0]),
            'toner_m': int(re.findall(r"\d+", data[11].getText())[0]),
            'toner_y': int(re.findall(r"\d+", data[14].getText())[0]),
            # 제록스 드럼은 잔량이 아닌 '양호', '교체'로 표기되므로 str
            'drum_k': data[22].getText(),
            'drum_c': data[24].getText(),
            'drum_m': data[26].getText(),
            'drum_y': data[28].getText(),
            'note': ""
        }

        print(f"{dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(info)
        return info

    except Exception as ex:
        info = get_error_data(ex, dept, model, ip)
        return info


def get_xerox_c5580(dept, model, ip):
    """
    Xerox APVC5580, DCVC5585 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """

    try:
        # 크롤링
        url = f"http://{ip}/stsply.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('small')

        # 이 컬러복합기는 검정 토너를 2개 장착함
        toner_k1 = int(re.findall(r"\d+", data[5].getText())[0])
        toner_k2 = int(re.findall(r"\d+", data[8].getText())[0])

        # Dictionary 생성
        info = {
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_k': toner_k1 if toner_k1 < toner_k2 else toner_k2,  # 두 블랙 토너 중 작은 값
            'toner_c': int(re.findall(r"\d+", data[11].getText())[0]),
            'toner_m': int(re.findall(r"\d+", data[14].getText())[0]),
            'toner_y': int(re.findall(r"\d+", data[17].getText())[0]),
            'drum_k': data[25].getText(),
            'drum_c': data[27].getText(),
            'drum_m': data[29].getText(),
            'drum_y': data[31].getText(),
            # 'staple_crtridge': str(data[35].getText()),  # 스테이플 카트리지
            # 'staple_crtridge_front': str(data[39].getText()),  # 제본용 스테이플 카트리지(앞쪽)
            # 'staple_crtridge_inside': str(data[41].getText()),  # 제본용 스테이플 카트리지(안쪽)
            # 두 블랙 토너 정보
            'note': f"Black 토너(K1): {toner_k1}, Black 토너(K2): {toner_k2}"
        }

        print(f"{dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(info)
        return info

    except Exception as ex:
        info = get_error_data(ex, dept, model, ip)
        return info


def get_xerox_iv2060(dept, model, ip):
    """
    Xerox DCIV2060, DCIII3007, DCIV3060, DCIV3065 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """

    try:
        # 크롤링
        url = f"http://{ip}/stsply.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('small')

        # Dictionary 생성
        info = {
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_k': int(re.findall(r"\d+", data[5].getText())[0]),
            'toner_c': "",
            'toner_m': "",
            'toner_y': "",
            'drum_k': data[9].getText(),
            'drum_c': "",
            'drum_m': "",
            'drum_y': "",
            'note': "",
            # 'fuser': data[13].getText()  # 정착부
        }

        print(f"{dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(info)
        return info

    except Exception as ex:
        info = get_error_data(ex, dept, model, ip)
        return info


def get_xerox_dp3055(dept, model, ip):
    """
    Xerox DP3055 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """

    try:
        # 크롤링
        url = f"http://{ip}/ews/status/statsupl.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('font', {'size': '-1'})

        toner_k = str(data[5].getText())

        # Dictionary 생성
        info = {
            'dept': dept,
            'model': model,
            'ip': ip,
            # 토너잔량이 '교환시기' 또는 숫자로 뜸
            'toner_k': toner_k if toner_k == '교환시기' else int(re.findall(r"\d+", toner_k)[0]),
            'toner_c': "",
            'toner_m': "",
            'toner_y': "",
            'drum_k': "",  # 드럼토너 일체형 모델
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


def get_xerox_ii3005(dept, model, ip):
    """
    Xerox DCII3005 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """

    try:
        # 크롤링
        url = "http://" + ip + "/stsply.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('small')

        # Dictionary 생성
        info = {
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_k': int(re.findall(r"\d+", data[3].getText())[0]),
            'toner_c': "",
            'toner_m': "",
            'toner_y': "",
            'drum_k': data[7].getText(),
            'drum_c': "",
            'drum_m': "",
            'drum_y': "",
            'note': ""
        }

        print(f"{dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        return info

    except Exception as ex:
        info = get_error_data(ex, dept, model, ip)
        return info
