import pntcrawler.oki as o  # 크롤링 함수 import
import pntcrawler.sindoh as s
import pntcrawler.xerox as x
from pntcrawler.common import create_xlsx  # 엑셀 저장 함수 import
from crawling_target import *  # 크롤링 할 프린터 정보 import


consumable_list = []

## 컬러복합기(프린터) 크롤링

# 신도 D417, D716, 일부 CM3091
for sindoh in dept_sindoh_d417:
    item = s.get_sindoh_d417(sindoh['dept'], sindoh['model'], sindoh['ip'])
    consumable_list.append(item)

# 신도 CM3091
for sindoh in dept_sindoh_cm3091:
    item = s.get_sindoh_cm3091(sindoh['dept'], sindoh['model'], sindoh['ip'])
    consumable_list.append(item)

# 제록스 DCIVC2265, APVC2275, APVC3373, DCVC3374, DCVC3376, DCVIC3371 및 DPC5005D
for xerox in dept_xerox_c2265:
    item = x.get_xerox_c2265(xerox['dept'], xerox['model'], xerox['ip'])
    consumable_list.append(item)

# 제록스 APVC5580, DCVC5585
for xerox in dept_xerox_c5580:
    item = x.get_xerox_c5580(xerox['dept'], xerox['model'], xerox['ip'])
    consumable_list.append(item)

# 제록스 DPC1110
for xerox in dept_xerox_c1110:
    item = x.get_xerox_c1110(xerox['dept'], xerox['model'], xerox['ip'])
    consumable_list.append(item)

# 제록스 DPC2200
for xerox in dept_xerox_c2200:
    item = x.get_xerox_c2200(xerox['dept'], xerox['model'], xerox['ip'])
    consumable_list.append(item)

# OKI C843
for oki in dept_oki_c843:
    item = o.get_oki_c843(oki['dept'], oki['model'], oki['ip'])
    consumable_list.append(item)


## 흑백프린터 크롤링

# 신도 B605n
for sindoh in dept_sindoh_b605n:
    item = s.get_sindoh_b605n(sindoh['dept'], sindoh['model'], sindoh['ip'])
    consumable_list.append(item)

# 제록스 DCII3005
for xerox in dept_xerox_ii3005:
    item = x.get_xerox_ii3005(xerox['dept'], xerox['model'], xerox['ip'])
    consumable_list.append(item)

# 제록스 DCIV2060
for xerox in dept_xerox_iv2060:
    item = x.get_xerox_iv2060(xerox['dept'], xerox['model'], xerox['ip'])
    consumable_list.append(item)

# 제록스 DP3055
for xerox in dept_xerox_dp3055:
    item = x.get_xerox_dp3055(xerox['dept'], xerox['model'], xerox['ip'])
    consumable_list.append(item)

# OKI ES5112
for oki in dept_oki_es5112:
    item = o.get_oki_es5112(oki['dept'], oki['model'], oki['ip'])
    consumable_list.append(item)


# 크롤링 결과 엑셀 파일로 저장
create_xlsx(consumable_list)
