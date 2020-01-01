import pntcrawler.oki as o  # 크롤링 함수 import
import pntcrawler.sindoh as s
import pntcrawler.xerox as x
import json
from pntcrawler.common import create_xlsx  # 엑셀 저장 함수 import
from pathlib import Path

logo = r"""
  _____      _       _                          
 |  __ \    (_)     | |                         
 | |__) | __ _ _ __ | |_ ___ _ __               
 |  ___/ '__| | '_ \| __/ _ \ '__|              
 | |   | |  | | | | | ||  __/ |                 
 |_|   |_| _|_|_| |_|\__\___|_|     _           
          / ____|                  | |          
         | |     _ __ __ ___      _| | ___ _ __ 
         | |    | '__/ _` \ \ /\ / / |/ _ \ '__|
         | |____| | | (_| |\ V  V /| |  __/ |   
          \_____|_|  \__,_| \_/\_/ |_|\___|_|   
                                                
"""

# 설정 파일 불러오기
with open('config.json', 'rt', encoding='UTF8') as json_file:
    config = json.load(json_file)

# 뽀대용 로고 출력
print(logo)
print(f"v{config['version']}\n\n")

# 크롤링 결과를 담을 list 생성
consumable_list = []


# =============== 컬러복합기 크롤링 ===============

# 신도 D417, D716, 일부 CM3091
with open(f"{config['crawling_target_folder']}/dept_sindoh_d417.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = s.get_sindoh_d417(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)

# 신도 CM3091, CM6011
with open(f"{config['crawling_target_folder']}/dept_sindoh_cm3091.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = s.get_sindoh_cm3091(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)

# 제록스 DCIVC2265, APVC2275, APVC3373, DCVC3374, DCVC3376, DCVIC3371 및 DPC5005D
with open(f"{config['crawling_target_folder']}/dept_xerox_c2265.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = x.get_xerox_c2265(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)

# 제록스 APVC5580, DCVC5585
with open(f"{config['crawling_target_folder']}/dept_xerox_c5580.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = x.get_xerox_c5580(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)


# =============== 컬러프린터 크롤링 ===============

# 제록스 DPC1110: 이제 안 쓰는 프린터라 주석 처리
with open(f"{config['crawling_target_folder']}/dept_xerox_c1110.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = x.get_xerox_c1110(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)

# 제록스 DPC2200
with open(f"{config['crawling_target_folder']}/dept_xerox_c2200.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = x.get_xerox_c2200(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)

# OKI C843
with open(f"{config['crawling_target_folder']}/dept_oki_c843.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = o.get_oki_c843(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)


# =============== 흑백프린터 크롤링 ===============

# 신도 B605n
with open(f"{config['crawling_target_folder']}/dept_sindoh_b605n.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = s.get_sindoh_b605n(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)

# 제록스 DCII3005
with open(f"{config['crawling_target_folder']}/dept_xerox_ii3005.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = x.get_xerox_ii3005(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)

# 제록스 DCIV2060, DCIII3007, DCIV3060, DCIV3065
with open(f"{config['crawling_target_folder']}/dept_xerox_iv2060.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = x.get_xerox_iv2060(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)

# 제록스 DP3055
with open(f"{config['crawling_target_folder']}/dept_xerox_dp3055.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = x.get_xerox_dp3055(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)

# OKI ES5112
with open(f"{config['crawling_target_folder']}/dept_xerox_es5112.json", 'rt', encoding='UTF8') as json_file:
    json_obj = json.load(json_file)
    for item in json_obj:
        result = o.get_oki_es5112(
            item['dept'], item['model'], item['ip'], config['chromedriver_path'])
        consumable_list.append(result)


# 크롤링 결과를 엑셀 파일로 저장
create_xlsx(consumable_list, config['save_folder'],
            config['strftime_param'], config['save_file_prefix'],
            config['toner_warning'], config['toner_alert'],
            config['drum_warning'], config['drum_alert'],
            config['warning_color'], config['alert_color'])
