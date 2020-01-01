from bs4 import BeautifulSoup
from pntcrawler.common import get_crawl_data, get_error_data, get_page_source
import re

"""
컬러 복합기(프린터)
"""

def get_xerox_c2265(dept, model, ip, chrome_driver_path):
    """
    Xerox DCIVC2265, APVC2275, APVC3373, DCVC3374, DCVC3376, DCVIC3371, DPC5005D 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소
        chrome_driver_path (str): 크롬 드라이버 실행파일 절대경로

    Return:
        <class 'dict'>
    """

    try: 
        # 크롤링
        url = f"http://{ip}/stsply.htm"
        source = get_page_source(url, chrome_driver_path)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('small')

        # Dictionary 생성
        data = get_crawl_data(dept = dept, model = model, ip = ip,
            toner_k = int(re.findall(r"\d+", data[5].getText())[0]), # 문자열에서 숫자만 추출
            toner_c = int(re.findall(r"\d+", data[8].getText())[0]),
            toner_m = int(re.findall(r"\d+", data[11].getText())[0]), 
            toner_y = int(re.findall(r"\d+", data[14].getText())[0]),
            drum_k = data[22].getText(), # 제록스 드럼은 잔량이 아닌 '양호', '교체'로 표기되므로 str로 변환, 
            drum_c = data[24].getText(), 
            drum_m = data[26].getText(), 
            drum_y = data[28].getText())

        print(f"# {dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(data)

        return data
        
    except Exception as ex:
        data = get_error_data(ex, dept, model, ip)
        return data


def get_xerox_c5580(dept, model, ip, chrome_driver_path):
    """
    Xerox APVC5580, DCVC5585 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소
        chrome_driver_path (str): 크롬 드라이버 실행파일 절대경로

    Return:
        <class 'dict'>
    """

    try: 
        # 크롤링
        url = f"http://{ip}/stsply.htm"
        source = get_page_source(url, chrome_driver_path)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('small')
        
        # 이 컬러복합기는 검정 토너를 2개 장착함
        toner_k1 = int(re.findall(r"\d+", data[5].getText())[0])
        toner_k2 = int(re.findall(r"\d+", data[8].getText())[0])

        # Dictionary 생성
        data = get_crawl_data(dept = dept, model = model, ip = ip,
            toner_k = toner_k1 if toner_k1 < toner_k2 else toner_k2,  # 두 블랙 토너 중 작은 값
            toner_c = int(re.findall(r"\d+", data[11].getText())[0]), 
            toner_m = int(re.findall(r"\d+", data[14].getText())[0]), 
            toner_y = int(re.findall(r"\d+", data[17].getText())[0]), 
            drum_k = data[25].getText(), 
            drum_c = data[27].getText(), 
            drum_m = data[29].getText(), 
            drum_y = data[31].getText(),
            note = f"Black 토너(K1): {toner_k1}, Black 토너(K2): {toner_k2}") # 두 블랙 토너 정보
        # 'staple_crtridge': str(data[35].getText()),  # 스테이플 카트리지
        # 'staple_crtridge_front': str(data[39].getText()),  # 제본용 스테이플 카트리지(앞쪽)
        # 'staple_crtridge_inside': str(data[41].getText()),  # 제본용 스테이플 카트리지(안쪽)

        print(f"# {dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(data)
        return data
    
    except Exception as ex:
        data = get_error_data(ex, dept, model, ip)
        return data


def get_xerox_c1110(dept, model, ip, chrome_driver_path):
    """
    Xerox DPC1110 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소
        chrome_driver_path (str): 크롬 드라이버 실행파일 절대경로

    Return:
        <class 'dict'>
    """

    try: 
        # 크롤링
        url = f"http://{ip}/ews/status/statsupl.htm"
        source = get_page_source(url, chrome_driver_path)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('font', {'size': '-1'})

        toner_c = str(data[5].getText())
        toner_m = str(data[8].contents[1])
        toner_y = str(data[11].contents[1])
        toner_k = str(data[14].contents[1])
        drum = str(data[17].getText())  # 드럼 4종류 일체형? 모델
        # _fuser = str(data[20].getText())

        # Dictionary 생성
        data = get_crawl_data(dept = dept, model = model, ip = ip,
            toner_c = toner_c if toner_c == '교환시기' else int(re.findall(r"\d+", toner_c)[0]),
            toner_m = toner_m if toner_m == '교환시기' else int(re.findall(r"\d+", toner_m)[0]),
            toner_y = toner_y if toner_y == '교환시기' else int(re.findall(r"\d+", toner_y)[0]),
            toner_k = toner_k if toner_k == '교환시기' else int(re.findall(r"\d+", toner_k)[0]),
            drum_c = drum if drum == '교환시기' else int(re.findall(r"\d+", drum)[0]),  # 드럼 4종류 일체형? 모델
            drum_m = drum if drum == '교환시기' else int(re.findall(r"\d+", drum)[0]),
            drum_y = drum if drum == '교환시기' else int(re.findall(r"\d+", drum)[0]),
            drum_k = drum if drum == '교환시기' else int(re.findall(r"\d+", drum)[0]),)
        # fuser = _fuser if _fuser == '교환시기' else int(re.findall(r"\d+", _fuser)[0]),

        print(f"# {dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(data)
        return data
    
    except Exception as ex:
        data = get_error_data(ex, dept, model, ip)
        return data


def get_xerox_c2200(dept, model, ip, chrome_driver_path):
    """
    Xerox DPC2200 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소
        chrome_driver_path (str): 크롬 드라이버 실행파일 절대경로

    Return:
        <class 'dict'>
    """

    try: 
        # 크롤링
        url = f"http://{ip}/status/statsupl.htm"
        source = get_page_source(url, chrome_driver_path)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('font', {'size': '-1'})

        toner_c = str(data[5].contents[1])
        toner_m = str(data[8].contents[1])
        toner_y = str(data[11].contents[1])
        toner_k = str(data[14].contents[1])
        # _fuser = str(data[17].getText())
        # _belt_unit = str(data[20].getText())

        # Dictionary 생성
        data = get_crawl_data(dept = dept, model = model, ip = ip,
            toner_c = toner_c if toner_c == '교환시기' else int(re.findall(r"\d+", toner_c)[0]),
            toner_m = toner_m if toner_m == '교환시기' else int(re.findall(r"\d+", toner_m)[0]),
            toner_y = toner_y if toner_y == '교환시기' else int(re.findall(r"\d+", toner_y)[0]), 
            toner_k = toner_k if toner_k == '교환시기' else int(re.findall(r"\d+", toner_k)[0]),
            drum_c = toner_c if toner_c == '교환시기' else int(re.findall(r"\d+", toner_c)[0]), # 드럼 토너 일체형 모델
            drum_m = toner_m if toner_m == '교환시기' else int(re.findall(r"\d+", toner_m)[0]),
            drum_y = toner_y if toner_y == '교환시기' else int(re.findall(r"\d+", toner_y)[0]),
            drum_k = toner_k if toner_k == '교환시기' else int(re.findall(r"\d+", toner_k)[0]),)
        # fuser = _fuser if _fuser == '교환시기' else int(re.findall(r"\d+", _fuser)[0]),  # 정착부
        # belt_unit = _belt_unit if _belt_unit == '교환시기' else int(re.findall(r"\d+", _belt_unit)[0]),  # 벨트 유닛

        print(f"# {dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(data)
        return data

    except Exception as ex:
        data = get_error_data(ex, dept, model, ip)
        return data


"""
흑백 프린터
"""

def get_xerox_iv2060(dept, model, ip, chrome_driver_path):
    """
    Xerox DCIV2060, DCIII3007, DCIV3060, DCIV3065 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소
        chrome_driver_path (str): 크롬 드라이버 실행파일 절대경로

    Return:
        <class 'dict'>
    """

    try: 
        # 크롤링
        url = f"http://{ip}/stsply.htm"
        source = get_page_source(url, chrome_driver_path)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('small')

        # Dictionary 생성
        data = get_crawl_data(dept = dept, model = model, ip = ip,
            toner_k = int(re.findall(r"\d+", data[5].getText())[0]),
            drum_k = data[9].getText())
        # fuser = data[13].getText()  # 정착부

        print(f"# {dept} 부서의 {model} 소모품 정보 크롤링 성공!")        
        print(data)
        return data

    except Exception as ex:
        data = get_error_data(ex, dept, model, ip)
        return data


def get_xerox_ii3005(dept, model, ip, chrome_driver_path):
    """
    Xerox DCII3005 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소
        chrome_driver_path (str): 크롬 드라이버 실행파일 절대경로

    Return:
        <class 'dict'>
    """

    try: 
        # 크롤링
        url = f"http://{ip}/stsply.htm"
        source = get_page_source(url, chrome_driver_path)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('small')

        # Dictionary 생성
        data = get_crawl_data(dept = dept, model = model, ip = ip,
            toner_k = int(re.findall(r"\d+", data[3].getText())[0]),
            drum_k = data[7].getText())

        print(f"# {dept} 부서의 {model} 소모품 정보 크롤링 성공!")
        print(data)
        return data

    except Exception as ex:
        data = get_error_data(ex, dept, model, ip)
        return data


def get_xerox_dp3055(dept, model, ip, chrome_driver_path):
    """
    Xerox DP3055 모델의 소모품 정보를 Dictionary로 반환합니다.

    Args:
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소
        chrome_driver_path (str): 크롬 드라이버 실행파일 절대경로

    Return:
        <class 'dict'>
    """

    try: 
        # 크롤링
        url = f"http://{ip}/ews/status/statsupl.htm"
        source = get_page_source(url, chrome_driver_path)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('font', {'size': '-1'})
        
        toner_k = str(data[5].getText())

        # Dictionary 생성
        data = get_crawl_data(dept = dept, model = model, ip = ip,
            toner_k = toner_k if toner_k == '교환시기' else int(re.findall(r"\d+", toner_k)[0]), # 토너잔량이 '교환시기' 또는 숫자로 뜸
            drum_k = toner_k if toner_k == '교환시기' else int(re.findall(r"\d+", toner_k)[0])) # 드럼토너 일체형 모델)

        print(f"# {dept} 부서의 {model} 소모품 정보 크롤링 성공!")  
        print(data)

        return data

    except Exception as ex:
        data = get_error_data(ex, dept, model, ip)
        return data
