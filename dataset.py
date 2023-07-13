import pandas as pd
import streamlit as st

location = ['강원도','경기도', '경상남도', '경상북도',  '광주광역시', '대구광역시', '대전광역시', '부산광역시', '서울특별시', '세종특별자치시',
         '울산광역시', '인천광역시', '전라남도', '전라북도' ,'제주특별자치도', '충청남도', '충청북도', '전국']

color = ['red', 'blue', '#98fb98', 'purple', 'orange', 'darkred', '#e05e43', 'beige', 'darkblue', 'darkgreen',
        'cadetblue', '#450459', 'lightgray', 'pink', 'lightblue', 'lightgreen', 'gray']

main_category = ['고택/생가/민속마을','유명사적/유적지','자연경관','문화유산','전통문화유산','온천지역']

categories = ['고택/생가/민속마을', '국보','군락/서식지/생태보호구역','궁궐/종묘','동굴', '바위','보물','봉우리/고지','비/탑/문/각',
        '성/성터','암자','온천지역','왕릉/고분','유명사적/유적지','천연기념물']

ma_ca = {'고택/생가/민속마을':['고택/생가/민속마을'],
        '유명사적/유적지':['유명사적/유적지'],
        '자연경관':['군락/서식지/생태보호구역','동굴', '바위','봉우리/고지','암자'],
        '문화유산':['보물','국보'],
        '전통문화유산':['비/탑/문/각', '성/성터', '왕릉/고분', '궁궐/종묘'],
        '온천지역':['온천지역']
}

ma_ca_code = {'고택/생가/민속마을':['Cnt_Cat1', 'Tag_Cat1'],
        '유명사적/유적지':['Cnt_Cat2', 'Tag_Cat2'],
        '자연경관':['Cnt_Cat3', 'Tag_Cat3'],
        '문화유산':['Cnt_Cat4', 'Tag_Cat4'],
        '전통문화유산':['Cnt_Cat5', 'Tag_Cat5'],
        '온천지역':['Cnt_Cat6', 'Tag_Cat6']
}

do_to_code = {'11' :'서울특별시','26':'부산광역시','27':'대구광역시','28':'인천광역시','29':'광주광역시','30':'대전광역시','31':'울산광역시',
              '36':'세종특별자치시', '41':'경기도','42':'강원도','43':'충청북도','44' :'충청남도','45':'전라북도',
              '46':'전라남도','47':'경상북도','48':'경상남도','50':'제주특별자치도'}

ca_col={}
for i in range(15):
    ca_col[categories[i]] = color[i]

def color_style(row):
    return ['background-color: {}; color: {};'.format(row['color'], row['color'])]

@st.cache_data
def load_data():
    data = pd.read_csv('Historic.csv')
    return data

@st.cache_data
def load_historic():
    df = pd.read_csv('Historic_Statistics_by_City.csv', encoding='cp949')
    df['cnt_sum'] = 0
    return df