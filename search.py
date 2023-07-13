import streamlit as st
import folium
from streamlit_folium import folium_static
from st_pages import Page, show_pages
import dataset

def main():
    with st.form('my_form'):
        st.markdown('### 유적지명 검색')
        search = st.text_input('찾고자 하는 유적지명을 입력하세요.')
        submitted = st.form_submit_button('Submit')

        if submitted:
            if search == '':
                st.info('유적지를 입력해주세요!')

            else:
                df = dataset.load_data()
                dot = df[df['POI_NM'] == search][['POI_NM','CL_NM','LC_LA','LC_LO','address']]

                if dot.empty:
                    st.info('등록되지 않은 유적지입니다!')
                else:
                    st.markdown('---')
                    dot.reset_index(drop=True, inplace=True)
                    dot.columns = ['info', 'category','lat', 'lon', 'address']

                    centerX, centerY = dot['lat'].mean(), dot['lon'].mean()

                    # Draw a basemap
                    m = folium.Map(location=[centerX, centerY], tiles='openstreetmap', zoom_start=7)

                    # Add points
                    for name, category, lat, lon in zip(dot['info'], dot['category'], dot['lat'], dot['lon']):
                        color=dataset.ca_col[category]
                        folium.Marker(
                            [lat, lon], tooltip=name, icon=folium.Icon(color=color)
                        ).add_to(m)

                    with st.spinner('loading...'):
                        col1, col2 = st.columns([1.5, 2.5])
                        with col1:
                            st.write('▶️ 검색 유적지: ' + search)

                            count_df = dot['category'].value_counts().reset_index()
                            count_df.columns = ['category', 'count']

                            color_lst = []
                            for _, row in count_df.iterrows():
                                color_lst.append(dataset.ca_col[row['category']])
                            count_df['color'] = color_lst

                            st.write('▶️ 유적지 분류')
                            st.dataframe(count_df.style.apply(dataset.color_style, subset='color', axis=1))

                            st.write('▶️ 유적지 수 : ' + str(len(dot)) + '개')
                            st.dataframe(dot[['info', 'category', 'address']], width=450)


                        with col2:
                            folium_static(m, width=750, height=700)

if __name__ == '__main__':
    title = "유적지명 검색"
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
