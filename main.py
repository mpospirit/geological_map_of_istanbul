import folium
from folium.plugins import Geocoder
import streamlit as st
from PIL import Image
import numpy as np
from streamlit_folium import st_folium

page_config = {
    "page_title": "Geological Map of Istanbul",
    "layout": "wide",
    "initial_sidebar_state": "expanded",
    "page_icon": "🪨",
}

st.set_page_config(**page_config)

with st.sidebar:
    st.header("Geological Map of Istanbul")
    st.markdown(
        "Made by [Çağrı Gökpunar](https://www.cagrigokpunar.com/)",
        unsafe_allow_html=True,
    )

    st.subheader("sahibinden.com Coordinates Fetcher")
    st.markdown(
        "Go to the [sahibinden.com](https://www.sahibinden.com/) and open the ad you want to get the coordinates of. Then, open the developer console and paste the following code and press enter. The coordinates will be copied to your clipboard."
    )

    st.code(
        "copy(parseFloat(document.getElementById('gmap').getAttribute('data-lat')) + ', ' + parseFloat(document.getElementById('gmap').getAttribute('data-lon')))",
        language="javascript",
    )
    st.markdown("I have tried to automate this process but it is not possible due to the security measures of the website.")
    st.markdown(
        """
                ##### Example URL:
                https://www.sahibinden.com/ilan/emlak-konut-kiralik-bu-sitede-bu-fiyata-kaciran-gercekten-uzulur-siddetle-tafsiye-1159589399/detay
                """
    )

    st.subheader("Geological Map Quality")
    st.markdown("Significantly affects the performance.")
    map_quality = st.selectbox("Quality", ["Medium", "Low"])

    if map_quality == "Medium":
        map_quality_str = "mq"
    else:
        map_quality_str = "lq"

    st.subheader("Geological Map Opacity")

    opacity = st.slider("Opacity", 0, 100, 100, 1)
    opacity = opacity / 100

    st.subheader("Source")
    st.markdown(
        "[İstanbul İli Jeoloji Haritası, İstanbul Büyükşehir Belediyesi](https://drive.google.com/file/d/1NO_ZwvPrsm9RcXLGyWgt5meGt8mWnDrY/view)"
    )

st.title("Geological Map of Istanbul")
st.markdown(
        "Made by [Çağrı Gökpunar](https://www.cagrigokpunar.com/)",
        unsafe_allow_html=True,
    )
st.markdown(
    """This application is provided for informational purposes only. The information contained herein is not intended to substitute professional advice or services. Users should consult appropriate professionals for specific advice tailored to their situation. I do not guarantee the accuracy, completeness, or reliability of any information provided in this application. Use of this application is at the user's own risk."""
)

consent = st.checkbox("I understand and agree to the disclaimer above.")

if consent:
    legend = Image.open("img/legend.jpg")

    with st.expander("Show Legend"):
        st.image(legend, use_column_width=True)

    m = folium.Map(location=[41.133449, 29.003216], zoom_start=10)

    # Opening the image file
    img = Image.open(f"img/{map_quality_str}.png")

    # Converting the image to a NumPy array
    img_array = np.array(img)

    # Using the array in ImageOverlay
    folium.raster_layers.ImageOverlay(
        image=img_array,
        bounds=[[40.8018, 27.955], [41.6, 29.97]],
        opacity=opacity,
    ).add_to(m)

    Geocoder().add_to(m)

    # call to render Folium map in Streamlit
    the_map = st_folium(m, use_container_width=True, returned_objects=[])