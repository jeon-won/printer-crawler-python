# 크롤링 함수 등 import
from pntcrawler.oki import get_oki_c843, get_oki_es5112
from pntcrawler.sindoh import get_sindoh_d417, get_sindoh_cm3091
from pntcrawler.xerox import get_xerox_c2265, get_xerox_dp3055
from pntcrawler.common import create_xlsx

# 크롤링 할 프린터(복합기) 정보 import
from crawling_target import *

consumable_list = []

# 신도 컬러복합기(D417, D716, 일부 CM3091) 크롤링
for d417 in dept_sindoh_d417:
    item = get_sindoh_d417(d417['dept'], d417['model'], d417['ip'])
    consumable_list.append(item)

# 신도 컬러복합기(CM3091) 복합기 크롤링
for cm3091 in dept_sindoh_cm3091:
    item = get_sindoh_cm3091(cm3091['dept'], cm3091['model'], cm3091['ip'])
    consumable_list.append(item)

# 제록스 컬러복합기(DCIVC2265, APVC2275, APVC3373, DCVC3374, DCVC3376, DCVIC3371) 및 컬러프린터(DPC5005D) 크롤링
for xerox in dept_xerox_c2265:
    item = get_xerox_c2265(xerox['dept'], xerox['model'], xerox['ip'])
    consumable_list.append(item)
    
# 제록스 컬러복합기(APVC5580, DCVC5585) 크롤링
for c5580 in dept_xerox_c5580:
    item = get_xerox_c5580(c5580['dept'], c5580['model'], c5580['ip'])
    consumable_list.append(item)

# 제록스 흑백프린터(DP3055) 크롤링
for xerox in dept_xerox_dp3055:
    item = get_xerox_dp3055(xerox['dept'], xerox['model'], xerox['ip'])
    consumable_list.append(item)

# OKI 컬러프린터(C843) 크롤링
for oki in dept_oki_c843:
    item = get_oki_c843(oki['dept'], oki['model'], oki['ip'])
    consumable_list.append(item)

# OKI 흑백프린터(ES5112) 크롤링
for oki in dept_oki_es5112:
    item = get_oki_es5112(oki['dept'], oki['model'], oki['ip'])
    consumable_list.append(item)

# 크롤링 결과 엑셀 파일로 저장
create_xlsx(consumable_list)
