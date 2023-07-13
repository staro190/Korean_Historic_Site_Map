import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from folium import Marker
from st_pages import Page, show_pages
import dataset

def main():
    df = dataset.load_data()

    with st.form('main'):
        option = st.selectbox('지역을 선택하세요.', dataset.location)

        selected_category = st.multiselect(
            '유적지 분류를 선택하세요',
            dataset.main_category,
            ['유명사적/유적지','자연경관','문화유산'])

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

        step = ['0','[1-2]','[2-7]','[7-24]','[24-99]','[99-664]','4,127K']
        hash = {'0': 0, '[1-2]': 2, '[2-7]': 7, '[7-24]': 24,'[24-99]': 99, '[99-664]': 664, '4,127K': 4127001}

        hash_min, hash_max = st.select_slider(
            '인스타그램 태그 수 범위 지정',
            options=step,
            value=('0', '4,127K')
        )

        submitted = st.form_submit_button('Submit')

        if submitted:
            st.markdown('---')
            if option =='전국':
                dot = df[(df['TAGS'] <= hash[hash_max])&(df['TAGS'] >= hash[hash_min])][['POI_NM','CL_NM','LC_LA','LC_LO']]
            else:
                dot = df[(df['CTPRVN_NM'] == option)&(df['CL_NM'].isin(selected_category_seperate))&
                         (df['TAGS'] <= hash[hash_max])&(df['TAGS'] >= hash[hash_min])][['POI_NM','CL_NM','LC_LA','LC_LO']]

            dot.reset_index(drop=True, inplace=True)
            dot.columns = ['info', 'category', 'lat', 'lon']

            centerX, centerY = dot['lat'].mean(), dot['lon'].mean()

            # Draw a basemap
            m = folium.Map(location=[centerX, centerY], tiles='openstreetmap', zoom_start=7)

            # Add points with marker-cluster
            mc = MarkerCluster()
            for _, row in dot.iterrows():
                color = dataset.ca_col[row['category']]
                mc.add_child(
                    Marker(location=[row['lat'], row['lon']],
                           tooltip=row['info'],
                           icon=folium.Icon(color=color))
                )

            m.add_child(mc)

            with st.spinner('loading...'):
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.write('▶️ 선택지역 : ' + option)
                    st.write('▶️ 유적지 수 : ' + str(len(dot)) + '개')

                    count_df = dot['category'].value_counts().reset_index()
                    count_df.columns = ['category', 'count']

                    color_lst = []
                    for _, row in count_df.iterrows():
                        color_lst.append(dataset.ca_col[row['category']])
                    count_df['color'] = color_lst

                    st.dataframe(count_df.style.apply(dataset.color_style, subset='color', axis=1))

                with col2:
                    folium_static(m, width=850, height=700)

if __name__ == '__main__':
    title = "지역별 문화 유적지"
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
