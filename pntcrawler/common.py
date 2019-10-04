import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from openpyxl import Workbook
from datetime import datetime
from pntcrawler.config import *

# Selenium을 사용하여 html을 얻어오는 함수
def get_page_source(url):
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
    pageSource = driver.page_source
    driver.close()

    return pageSource


# 크롤링 에러 발생 시 빈 데이터와 에러 정보를 반환하는 함수
def get_empty_data(error, dept, model, ip):
    info = { 
      'dept': dept, 'model': model, 'ip': ip,
      'toner_k': "", 'toner_c': "", 'toner_m': "", 'toner_y': "",
      'drum_k' : "", 'drum_c' : "", 'drum_m' : "", 'drum_y' : "",
      'note': str(error)
    }
    
    print("크롤링 실패... 원인은 다음과 같습니다.")
    print(error)

    return info


# 크롤링 최종 결과를 엑셀파일로 수합하는 함수
def create_xlsx(data):
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
            print(item['dept'] + " 부서의 " + item['model'] + " 소모품 정보 저장 중...")
            ws.append([
                item['dept'], item['model'], item['ip'], 
                item['toner_k'], item['toner_c'], item['toner_m'], item['toner_y'], 
                item['drum_k'], item['drum_c'], item['drum_m'], item['drum_y'],
                item['note']
            ])
        
        # 파일명 지정
        date = datetime.today().strftime(strftime_param)
        fileName = save_folder + "/" + save_file_prefix + "_" + date + '.xlsx'
        
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
