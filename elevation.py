import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
from folium import Marker
import math
from st_pages import Page, show_pages
import dataset

def main():
    sea_level = st.slider(
        '해수면 선택 (단위 \: m)',
        0, 40, 1
    )

    df = dataset.load_data()

    dot = df[['POI_NM','CL_NM','LC_LA','LC_LO','ELEVATION']]

    dot.reset_index(drop=True, inplace=True)
    dot.columns = ['info', 'category', 'lat', 'lon','elev']

    danger_dot = dot.loc[dot['elev']<sea_level]

    st.info('해수면 ' + str(sea_level) + 'm 상승 시, ' + str(len(danger_dot)) + '개의 유적지가 잠깁니다.')

    centerX, centerY = danger_dot['lat'].mean(), danger_dot['lon'].mean()

    if math.isnan(centerX): centerX = 36.02
    if math.isnan(centerY): centerY = 128.02

    # Draw a basemap
    m = folium.Map(location=[centerX, centerY], tiles='openstreetmap', zoom_start=6.3)

    # Add points with marker-cluster
    mc = MarkerCluster()
    for _, row in danger_dot.iterrows():
        color = dataset.ca_col[row['category']]
        mc.add_child(
            Marker(location=[row['lat'], row['lon']],
                   tooltip=row['info'],
                   icon=folium.Icon(color=color))
        )

    m.add_child(mc)

    with st.spinner('loading...'):
        col1, col2 = st.columns([1.5, 2.5])
        with col1:
            count_df = danger_dot['category'].value_counts().reset_index()
            count_df.columns = ['category', 'count']

            color_lst = []
            for _, row in count_df.iterrows():
                color_lst.append(dataset.ca_col[row['category']])
            count_df['color'] = color_lst
            #
            st.write('▶️ 유적지 분류')
            st.dataframe(count_df.style.apply(dataset.color_style, subset='color', axis=1))

        with col2:
            folium_static(m, width=730, height=700)

if __name__ == '__main__':
    title = "해수면 정보"
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