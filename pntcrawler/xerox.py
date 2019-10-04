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
