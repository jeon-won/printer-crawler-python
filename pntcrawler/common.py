import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from openpyxl import Workbook
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
        'drum_k': "", 'drum_c': "", 'drum_m': "", 'drum_y': "",
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

    wb = Workbook()
    ws = wb.active

    # 컬럼 명 찍기
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
                # IP 열에 하이퍼링크 지정
                item["dept"], item["model"], f'=HYPERLINK("http://{item["ip"]}")',
                item["toner_k"], item["toner_c"], item["toner_m"], item["toner_y"],
                item["drum_k"], item["drum_c"], item["drum_m"], item["drum_y"],
                item["note"]
            ])

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
