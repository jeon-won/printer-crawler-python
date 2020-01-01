# printer-crawler

## 개요

각종 네트워크 프린터의 소모품 정보(토너, 드럼 잔량)를 수합하여 엑셀 파일로 저장하는 프로그램입니다.


## 필요한 것들

### Python 3
파이썬으로 돌아가니 당연히 파이썬을 설치해야 합니다. https://www.python.org/downloads 에서 Python 3.6 이상 버전을 설치합니다.

### Selenium
Selenium은 동적 웹페이지 소스를 얻어올 때 사용하는 라이브러리입니다. Python Requests 모듈로 프린터의 웹페이지 소스를 받아보면 HTML이 아닌 자바 스크립트나 XML이 리턴되는 경우가 있어 Selenium을 사용합니다. 

`pip install selenium` 명령어로 설치합니다.

### 크롬 드라이버
크롬 드라이버는 Selenium이 크롬 브라우저를 제어하기 위해 사용합니다. 따라서 사전에 반드시 크롬 브라우저를 설치해야 합니다.

https://chromedriver.chromium.org/downloads 에서 사용 중인 크롬 브라우저에 맞는 ChromeDriver를 다운받습니다.

### BeautifulSoup
BeautifulSoup는 HTML에서 원하는 정보를 추출하기 위해 사용합니다.

`pip install beautifulsoup4` 명령어로 설치합니다.

### openpyxl
openpyxl을 사용하여 크롤링 결과를 엑셀 파일로 저장합니다.

`pip install openpyxl` 명령어로 설치합니다.


## 사용 방법
1. crawling_target 폴더에 크롤링할 네트워크 프린터 정보를 입력합니다.
2. config.json에 크롬 드라이버 실행파일의 위치를 **절대경로**로 지정합니다.
3. `python main.py` 명령어를 실행하거나 `main.bat` 파일을 실행합니다.
4. 크롤링이 완료되면 기본적으로 crawldata 폴더에 엑셀파일이 생성됩니다.


## 문제점
크롬 78 버전에서 Selenium이 html 소스를 얻어오지 못하는 문제가 있습니다. [stackoverflow](https://stackoverflow.com/questions/58589425/possible-issue-with-chromedriver-78-selenium-can-not-find-web-element-of-pdf-op)에 올라온 글을 보면 아마 크롬 드라이버 문제인 것 같습니다. 크롬 76 버전에서 정상 작동되며 최신 버전의 크롬을 이미 설치한 경우 [chrome offline installer](https://www.neowin.net/news/google-chrome-76-offline-installer)를 사용하여 크롬 76 버전을 사용할 수 있습니다.

MacOS 크롬 79 버전에서 Selenium이 html 소스를 제대로 얻어오는 걸 확인했습니다. 윈도 크롬 79버전은 귀찮아서 아직 테스트를 안 해봤습니다...


## 프로그램 구조

### 최상위 폴더

#### main.py
프로그램 실행부

#### config.json
크롤링 설정 모음
* 메인 프로그램 관련
  - version: 프로그램 버전
  - crawling_target_folder: 크롤링할 부서 정보(부서명, 모델명, IP주소)가 담긴 JSON 파일이 위치한 폴더 이름 (기본: crawling_target)
  - chromedriver_path: 크롬 드라이버 실행파일 **절대경로**
* 엑셀 파일 저장 관련
  - save_folder: 크롤링 결과를 저장할 폴더 이름 (기본: crawldata)
  - save_file_prefix: 엑셀 파일명에 붙일 접두어
  - strftime_param: 엑셀 파일명에 시간을 명시할 때 strftime() 함수에 적용할 매개변수
* 토너 주의 및 경고 잔량: 잔량이 아래 값 이하인 경우 엑셀파일에 색상이 표시됩니다.
  - warning_color: 주의 색상
  - alert_color: 경고 색상
  - toner_warning: 토너 주의 잔량
  - toner_alert: 토너 경고 잔량
  - drum_warning: 드럼 주의 잔량
  - drum_alert: 드럼 경고 잔량


### pntcrawler 폴더
프린터 크롤링 함수들을 모아놓은 패키지입니다.

#### common.py
여러 모듈에서 공통적으로 사용하는 함수 정의
* get_page_source(): html을 얻어옴
* get_crawl_data(): 크롤링 결과를 입력받아 프린터 소모품 정보가 담긴 데이터 반환
* get_error_data(): 크롤링 에러 발생 시 에러 데이터 반환
* create_xlsx(): 크롤링 최종 결과를 엑셀파일로 수합

#### oki.py
OKI 프린터 크롤링 함수 정의
* get_oki_c843(): C843 모델 크롤링
* get_oki_es5112(): ES5112 모델 크롤링

#### sindoh.py
신도리코 프린터 크롤링 함수 정의
* get_sindoh_cm3091(): CM3091, CM6011 모델 크롤링
* get_sindoh_d417(): D417, D716, CM3091 일부 모델 크롤링
* get_sindoh_b605n(): B605n 모델 크롤링

#### xerox.py
제록스 프린터 크롤링 함수 정의
* get_xerox_c2265(): DCIVC2265, APVC2275, APVC3373, DCVC3374, DCVC3376, DCVIC3371, DPC5005D 모델 크롤링
* get_xerox_c5580(): APVC5580, DCVC5585 모델 크롤링
* get_xerox_c1110(): DPC1110 모델 크롤링
* get_xerox_c2200(): DPC2200 모델 크롤링
* get_xerox_iv2060(): DCIV2060, DCIII3007, DCIV3060, DCIV3065 모델 크롤링
* get_xerox_ii3005(): DCII3005 모델 크롤링
* get_xerox_dp3055(): DP3055 모델 크롤링


## 버전 이력
* v1.0.0(?): 최초 작성
* v2.0.0
  - 설정 정보를 파이썬 딕셔너리에서 JSON 파일에서 불러오도록 변경
  - 프로그램 구조 다수 변경
