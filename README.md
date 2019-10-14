# printer-crawler

## 개요

파이썬을 배우다가 전 부서에 프린터(복합기) 소모품을 효율적으로 보급하고자 어떤 소모품이 필요하게 될지 체크하기 위해 만들어 본 프로그램입니다.


## 필요한 것들

### Python 3

파이썬으로 돌아가니 당연히 파이썬을 설치해야 합니다. https://www.python.org/downloads 에서 Python 3를 설치합니다.

### Selenium

Selenium은 동적 웹페이지 소스를 얻어올 때 사용하는 라이브러리입니다. Python Requests 모듈로 프린터의 웹페이지 소스를 받아보면 HTML이 아닌 자바 스크립트나 XML이 리턴되는 경우가 있어 Selenium을 사용합니다. 

`pip install selenium` 명령어로 설치합니다.

### ChromeDriver 

ChromeDriver는 Selenium이 크롬 브라우저를 제어하기 위해 사용합니다. 따라서 사전에 반드시 크롬 브라우저를 설치해야 합니다.

https://chromedriver.chromium.org/downloads 에서 사용 중인 크롬 브라우저에 맞는 ChromeDriver를 다운받습니다.

### BeautifulSoup

BeautifulSoup는 HTML에서 원하는 정보를 추출하기 위해 사용합니다.

`pip install beautifulsoup4` 명령어로 설치합니다.


## 사용 방법

1. crawling_target.py에 크롤링할 프린터 정보를 입력합니다.
2. pntcrawler/config.py에 ChromeDriver 실행파일의 위치를 **절대경로**로 지정합니다.
3. `python main.py` 명령어를 실행하거나 `main.bat` 파일을 실행합니다.
4. 크롤링이 완료되면 기본적으로 crawldata 폴더에 엑셀파일이 생성됩니다.



## 프로그램 구조

### 최상위 폴더

#### main.py

프로그램 실행부

#### crawling_target.py

크롤링 할 프린터 정보(부서명, 모델명, ip주소)


### pntcrawler 폴더

프린터 크롤러 패키지입니다.

#### common.py

여러 모듈에서 공통적으로 사용하는 함수 정의

* get_page_source(): html을 얻어옴
* get_empty_data(): 크롤링 에러 발생 시 빈 데이터 반환
* create_xlsx(): 크롤링 최종 결과를 엑셀파일로 수합

#### config.py

프린터 크롤러 패키지에서 사용하는 설정 값

* chromedriver_path: 크롬 드라이버 절대경로
* save_folder: 크롤링 결과를 저장할 폴더 명(기본: crawldata)
* save_file_prefix: 엑셀 파일명에 붙일 접두어
* strftime_param: 엑셀 파일명에 시간을 명시할 때 strftime() 함수에 적용할 매개변수

#### oki.py

OKI 프린터 크롤링 함수 정의

* get_oki_c843(): C843 모델 크롤링
* get_oki_es5112(): ES5112 모델 크롤링

#### sindoh.py

신도리코 프린터 크롤링 함수 정의

* get_sindoh_cm3091(): CM3091 모델 크롤링
* get_sindoh_d417(): D417, D716, CM3091 일부 모델 크롤링

#### xerox.py

제록스 프린터 크롤링 함수 정의

* get_xerox_c2265(): DCIVC2265, APVC2275, APVC3373, DCVC3374, DCVC3376, DCVIC3371, DPC5005D 모델 크롤링
* get_xerox_c5580(): APVC5580, DCVC5585 모델 크롤링
* get_xerox_dp3055(): DP3055 모델 크롤링


## 변경내역

* 2019-10-04: 최초 작성
* 2019-10-14: 제록스 APVC5580, DCVC5585 모델 
