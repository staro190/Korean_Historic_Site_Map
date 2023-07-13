# Korean_Historic_Site_Map  ![문화재](https://github.com/staro190/Korean_Historic_Site_Map/assets/16371108/09cb1eac-53ab-458c-b7c9-c7a81ac1ba39)

### 한국 유적지 지도 프로젝트

▶️ 분석 주제
KCISA(한국문화정보원)의 '국내 지역별 유적지 데이터'를 기반으로 해당 유적지의 SNS 태그 수와 공간정보를 함께 분석하였습니다.

▶️ 분석 결과
유적지 검색, 태그 수 또는 카테고리별 유적지 분류, 국내 유적지 분포, 해수면 상승에 따른 침수 위험 유적지 등의 정보를 도출하였고, streamlit 프레임워크를 사용하여 데이터 분석 결과 및 활용 예시를 볼 수 있는 대시보드를 제작하였습니다.

▶️ 활용 방안
1. 국내 유적지 홍보 정책 및 유적지 관광상품 개발 시 활용
- 국내의 다양한 유적지, 생태공원, 명소를 한 번에 보고 SNS(인스타그램)를 통해서 인기 명소를 확인할 수 있습니다.
- 도출된 비인기 명소의 경우, 지역 특색 또는 역사적 의미 등을 고려하여 신규 관광상품으로 탈바꿈하는 정책을 도입할 수 있습니다.

2. 공간정보를 통해 관리 취약 유적지 확인 및 선제적 대응
- 최근 이상기후 현상으로 인해 국지성 호우, 초대형 태풍 등이 증가하는 추세입니다. 또한 지구온난화의 영향으로 해수면이 급속도로 상승하고 있습니다. 해안 유적지, 생태 습지 등은 침수될 위기가 있으며, 반대로 절벽 근처, 비탈면에 위치한 유적지는 붕괴의 위험이 존재합니다. 해발고도 데이터를 이용하여 침수 취약 유적지를 탐색하고, 해수면 상승 혹은 이상기후에 사전에 대응할 수 있는 방안을 도입할 수 있습니다.

3. 플랫폼화 전략
- 유적지 검색 및 분류 기능을 활용하여 다양한 문화 유적지 정보를 사용자에게 제공할 수 있습니다.
- 과거 관광객 통계 정보를 추가하고 지속적으로 안정적인 해시태그 데이터를 수집하여 시계열 분석을 지원할 수 있습니다.
- 단순히 행정기관의 유적지 관리 기능뿐만 아니라 유적지 주변 소상공인, 관광사, 공원 운영사 등의 마케팅 정보로 활용될 수 있습니다.

▶️ 파일 구성
1. Code
   - Instagram Crawling : 인스타그램 검색 결과 가져오기
   - GIS Transform : EPSG 4326 <-> EPSG 5186
   - dataset : Data Loader
   - elevation : 해수면 page
   - local : 지역별 유적지 page
   - search : 유적지 검색 page
   - map : 유적지 분포 page
   
2. Data
   - Historic : 유적지 ID, 이름, 위치 등
   - Historic_Statistics_by_City : 도시별 유적지 개수

 <img src="https://img.shields.io/badge/파이썬-3776AB?style=flat&logo=python&logoColor=white"/> <img src="https://img.shields.io/badge/스트림릿-FF4B4B?style=flat&logo=streamlit&logoColor=white"/> <img src="https://img.shields.io/badge/엑셀-217346?style=flat&logo=microsoftexcel&logoColor=white"/> <img src="https://img.shields.io/badge/주피터-F37626?style=flat&logo=jupyter&logoColor=white"/> <img src="https://img.shields.io/badge/파이참-000000?style=flat&logo=pycharm&logoColor=white"/> <img src="https://img.shields.io/badge/인스타그램-E4405F?style=flat&logo=instagram&logoColor=white"/>
