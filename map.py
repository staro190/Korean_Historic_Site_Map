import streamlit as st
import folium
from streamlit_folium import folium_static
from folium import plugins
import json
from st_pages import Page, show_pages
import dataset

def main():
    df = dataset.load_data()

    with st.form('map'):
        selected_category = st.multiselect(
            '유적지 분류를 선택하세요',
            dataset.main_category,
            ['자연경관'])

        st.info('''
            ▶️ 유적지 분류
            1) 고택/생가/민속마을
            2) 유명사적/유적지
            3) 자연경관 : 군락/서식지/생태보호구역,  동굴,  바위,  봉우리/고지,  암자,  천연기념물
            4) 문화유산 : 보물,  국보
            5) 전통문화유산 : 비/탑/문/각,  성/성터,  왕릉/고분,  궁궐/종묘
            6) 온천지역
            ''')

        selected_category_seperate = []
        for i in selected_category:
            selected_category_seperate.extend(dataset.ma_ca[i])

        heatmap_option_lst = ['히트맵', '단계구분도']
        heatmap_option =st.radio('맵 선택',
                        heatmap_option_lst, horizontal=True)

        submitted = st.form_submit_button('Submit')

        if submitted:
            st.markdown('---')
            dot = df[df['CL_NM'].isin(selected_category_seperate)][['POI_NM','CL_NM','LC_LA','LC_LO']]
            dot.reset_index(drop=True, inplace=True)
            dot.columns = ['info', 'category', 'lat', 'lon']

            centerX, centerY = dot['lat'].mean(), dot['lon'].mean()

            col1, col2 = st.columns(2)
            historic = dataset.load_historic()

            if heatmap_option == heatmap_option_lst[0]:
                with col1:
                    historic['cnt_sum'] = 0
                    m1 = folium.Map(location=[centerX, centerY], tiles='openstreetmap', zoom_start=7)
                    st.write('▶️ 해시태그 수 분포')
                    for i in selected_category:
                        historic['cnt_sum'] = historic['cnt_sum'] + historic[dataset.ma_ca_code[i][1]]
                    m1.add_child(plugins.HeatMap(zip(historic['Latitude'],
                                                     historic['Longitude'],
                                                     historic['cnt_sum']), radius=18))
                    folium_static(m1, width=550, height=600)

                with col2:
                    historic['cnt_sum'] = 0
                    m2 = folium.Map(location=[centerX, centerY], tiles='openstreetmap', zoom_start=7)
                    st.write('▶️ 유적지 분류별 분포')
                    for i in selected_category:
                        historic['cnt_sum'] = historic['cnt_sum'] + historic[dataset.ma_ca_code[i][0]]

                    m2.add_child(plugins.HeatMap(zip(historic['Latitude'],
                                                     historic['Longitude'],
                                                     historic['cnt_sum']), radius=18))
                    folium_static(m2, width=550, height=600)

            else:
                with open('korea.geojson', encoding='UTF-8') as f:
                    korea_geo = json.load(f)

                for x in korea_geo['features']:
                    if dataset.do_to_code[x['properties']['SIG_CD'][:2]] == '세종특별자치시':
                        x['gov_id'] = dataset.do_to_code[x['properties']['SIG_CD'][:2]]
                    else:
                        x['gov_id'] = dataset.do_to_code[x['properties']['SIG_CD'][:2]] + " " + x['properties']['SIG_KOR_NM']

                with col1:
                    historic['cnt_sum'] = 0
                    m3 = folium.Map(location=[centerX, centerY], tiles='cartodbpositron', zoom_start=6.5)
                    st.write('▶️ 해시태그 수 분포')
                    for i in selected_category:
                        historic['cnt_sum'] = historic['cnt_sum'] + historic[dataset.ma_ca_code[i][1]]

                    folium.Choropleth(
                        geo_data=korea_geo,
                        data=historic,
                        columns=['gov_ID', 'cnt_sum'],
                        fill_color='YlOrRd',
                        fill_opacity=0.7,
                        line_opacity=0.2,
                        key_on='gov_id',
                        legend_name="유적지수"
                    ).add_to(m3)
                    folium_static(m3, width=550, height=600)

                with col2:
                    historic['cnt_sum'] = 0
                    m4 = folium.Map(location=[centerX, centerY], tiles='cartodbpositron', zoom_start=6.5)
                    st.write('▶️ 유적지 분류별 분포')
                    for i in selected_category:
                        historic['cnt_sum'] = historic['cnt_sum'] + historic[dataset.ma_ca_code[i][0]]
                    folium.Choropleth(
                        geo_data=korea_geo,
                        data=historic,
                        columns=['gov_ID', 'cnt_sum'],
                        fill_color='YlOrRd',
                        fill_opacity=0.7,
                        line_opacity=0.2,
                        key_on='gov_id',
                        legend_name="유적지수"
                    ).add_to(m4)
                    folium_static(m4, width=550, height=600)

if __name__ == '__main__':
    title = "전국 유적지 분포"
    st.set_page_config(
        page_title=title,
        page_icon="🏛️",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    show_pages(
        [
            Page('search.py', '유적지명 검색'),
            Page('local.py', '지역별 유적지'),
            Page('map.py', '전국 유적지 분포'),
            Page('elevation.py', '해수면 정보')
        ]
    )
    st.title(title)
    st.markdown('---')
    main()
