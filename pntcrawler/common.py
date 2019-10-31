import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from datetime import datetime
from pntcrawler.config import *


def get_page_source(url):
    """
    Selenium을 사용하여 url에 대응하는 html을 반환합니다.

    Args:
        url (str): html을 얻어올 url

    Return:
        <class 'str'>
    """

    # Selenium Headless(창 숨김 모드) 설정
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('lang=ko_KR')

    # Selenium을 이용하여 소모품 정보 페이지 HTML 얻어오기
    path = chromedriver_path
    driver = webdriver.Chrome(path, options=chrome_options)
    # driver.implicitly_wait(10)
    driver.get(url)
    pagesource = driver.page_source
    driver.close()

    return pagesource


def get_error_data(error, dept, model, ip):
    """
    크롤링 에러 정보를 반환합니다.

    Args:
        error (Exception): Exception 객체
        dept (str): 부서 명
        model (str): 프린터 모델 명
        ip (str): 프린터 IP 주소

    Return:
        <class 'dict'>
    """

    info = { 
      'dept': dept, 'model': model, 'ip': ip,
      'toner_k': "", 'toner_c': "", 'toner_m': "", 'toner_y': "",
      'drum_k' : "", 'drum_c' : "", 'drum_m' : "", 'drum_y' : "",
      'note': str(error)
    }
    
    print(f"{dept} 부서의 {model} 크롤링 실패... 원인은 다음과 같습니다.")
    print(error)
    
    return info


def create_xlsx(data):
    """
    크롤링 최종 결과를 엑셀파일로 수합하여 저장합니다. 엑셀 파일명은 config.py 에서 설정할 수 있습니다.

    Args:
        data (list): 크롤링 수합 정보가 담긴 list
    """

    wb = Workbook()  # 워크북
    ws = wb.active  # 워크시트
    
    # 틀 고정 및 컬럼 명 찍기
    ws.freeze_panes = "A2"
    ws.append([
        '부서명', '모델', 'IP', 
        '토너(K)', '토너(C)', '토너(M)', '토너(Y)', 
        '드럼(K)', '드럼(C)', '드럼(M)', '드럼(Y)',
        '비고'
    ])

    try:
        # 폴더 생성
        if not(os.path.isdir(save_folder)):
            os.makedirs(os.path.join(save_folder))
        
        # 각 부서별 토너 및 드럼 잔량 찍기
        for item in data:
            print(item["dept"] + " 부서의 " + item["model"] + " 소모품 정보 저장 중...")
            ws.append([
                item["dept"], item["model"], f'=HYPERLINK("http://{item["ip"]}")',  # IP 열에 하이퍼링크 지정
                item["toner_k"], item["toner_c"], item["toner_m"], item["toner_y"], 
                item["drum_k"], item["drum_c"], item["drum_m"], item["drum_y"],
                item["note"]
            ])

        # 토너 잔량이 주의 및 경고인 경우 색칠하기
        cells = ws[f"d2:g{ws.max_row}"]  # D~G열: 토너 잔량 표시 범위
        for cell in cells:
            for item in cell:
                if isinstance(item.value, int) and item.value <= toner_alert:
                    item.fill = PatternFill(start_color=alert_color, end_color=alert_color, fill_type='solid')
                elif isinstance(item.value, int) and toner_alert < item.value <= toner_warning:
                    item.fill = PatternFill(start_color=warning_color, end_color=warning_color, fill_type='solid')

        # 드럼 잔량이 주의 및 경고인 경우 색칠하기
        cells = ws[f"h2:k{ws.max_row}"]  # H~K열: 드럼 잔량 표시 범위
        for cell in cells:
            for item in cell:
                if isinstance(item.value, int) and item.value <= drum_alert:
                    item.fill = PatternFill(start_color=alert_color, end_color=alert_color, fill_type='solid')  
                elif item.value is None:
                    continue
                elif isinstance(item.value, str) and '양호' not in item.value:  ## 빈 셀은 색칠하지 않으려 하는데... 작동하지 않음;;;
                    item.fill = PatternFill(start_color=alert_color, end_color=alert_color, fill_type='solid')
        
        # 파일명 지정
        date = datetime.today().strftime(strftime_param)
        fileName = f"{save_folder}/{save_file_prefix}_{date}.xlsx"
        
        # 파일 저장
        wb.save(fileName)
        wb.close()
        print("저장 완료!")
    
    except OSError as e:
        print("폴더 생성 실패... 원인은 다음과 같습니다.")
        print(e)

    except Exception as e:
        print("엑셀 파일 생성 실패... 원인은 다음과 같습니다.")
        print(e)
