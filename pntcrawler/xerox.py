from bs4 import BeautifulSoup
from pntcrawler.common import get_empty_data, get_page_source


# 작동 모델(컬러복합기): Xerox DCIVC2265, APVC2275, APVC3373, DCVC3374, DCVC3376, DCVIC3371
# 작동 모델(컬러프린터): Xerox DPC5005D
def get_xerox_c2265(dept, model, ip):
    try: 
        print(dept + " 부서의 " + model + " 소모품 정보 크롤링 중...")

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
            'toner_k': int(data[5].contents[0].replace('%', '')),
            'toner_c': int(data[8].contents[0].replace('%', '')),
            'toner_m': int(data[11].contents[0].replace('%', '')),
            'toner_y': int(data[14].contents[0].replace('%', '')),
            'drum_k' : str(data[22].contents[0]).replace('%', ''), # 제록스 드럼은 잔량이 아닌 '양호', '교체'로 표기되므로 str로 변환
            'drum_c' : str(data[24].contents[0]).replace('%', ''),
            'drum_m' : str(data[26].contents[0]).replace('%', ''),
            'drum_y' : str(data[28].contents[0]).replace('%', ''),
            'note': ""
        }

        print("성공!")
        return info

    except Exception as ex:
        data = get_empty_data(ex, dept, model, ip)
        return data


# 작동 모델(컬러복합기): APVC5580, DCVC5585
def get_xerox_c5580(dept, model, ip):
    try: 
        print(dept + " 부서의 " + model + " 소모품 정보 크롤링 중...")

        # 크롤링
        url = "http://" + ip + "/stsply.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('small')
        
        # 이 컬러복합기는 검정 토너를 2개 장착함
        toner_k1 = int(data[5].contents[0].replace('%', ''))
        toner_k2 = int(data[8].contents[0].replace('%', ''))

        # Dictionary 생성
        info = {
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_k': toner_k1 if toner_k1 < toner_k2 else toner_k2,  # 두 블랙 토너 중 작은 값
            'toner_c': int(data[11].contents[0].replace('%', '')), 
            'toner_m': int(data[14].contents[0].replace('%', '')), 
            'toner_y': int(data[17].contents[0].replace('%', '')), 
            'drum_k' : str(data[25].contents[0]), 
            'drum_c' : str(data[27].contents[0]), 
            'drum_m' : str(data[29].contents[0]), 
            'drum_y' : str(data[31].contents[0]), 
            # 'staple_crtridge': str(data[35].contents[0]),  # 스테이플 카트리지
            # 'staple_crtridge_front': str(data[39].contents[0]),  # 제본용 스테이플 카트리지(앞쪽)
            # 'staple_crtridge_inside': str(data[41].contents[0]),  # 제본용 스테이플 카트리지(안쪽)
            'note': f"Black 토너(K1): {toner_k1}, Black 토너(K2): {toner_k2}"  # 두 블랙 토너 정보
        }

        print("성공!")
        return info
    
    except Exception as ex:
        data = get_empty_data(ex, dept, model, ip)
        return data


# 제록스 DP3055 모델에서 작동
def get_xerox_dp3055(dept, model, ip):
    try: 
        print(dept + " 부서의 " + model + " 소모품 정보 크롤링 중...")
        
        # 크롤링
        url = "http://" + ip + "/ews/status/statsupl.htm"
        source = get_page_source(url)
        soup = BeautifulSoup(source, 'html.parser')
        data = soup.findAll('font', {'size': '-1'})
        toner_k = str(data[5].contents[1]).replace(" %", "")

        # Dictionary 생성
        info = {
            'dept': dept,
            'model': model,
            'ip': ip,
            'toner_k': toner_k if toner_k == '교환시기' else int(toner_k), # 토너잔량이 '교환시기' 또는 숫자로 뜸
            'toner_c': "",
            'toner_m': "",
            'toner_y': "",
            'drum_k' : "", # 드럼토너 일체형 모델
            'drum_c' : "",
            'drum_m' : "",
            'drum_y' : "",
            'note': ""
        }

        print("성공!")
        return info

    except Exception as ex:
        data = get_empty_data(ex, dept, model, ip)
        return data
