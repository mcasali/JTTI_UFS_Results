#!/usr/bin/env python3


import streamlit as st
import geopandas as gpd
import leafmap.foliumap as leafmap
from PIL import Image

# Set wide mode
st.set_page_config(layout='wide')

# Set session state variables
if 'zoom_center_x' not in st.session_state:
    st.session_state.zoom_center_x = 33
if 'zoom_center_y' not in st.session_state:
    st.session_state.zoom_center_y = -96
if 'zoom_level' not in st.session_state:
    st.session_state.zoom_level = 4


# Main page text
st.title("JTTI/UFS Lake Ensemble Plots")

lake_dic = {'Pontchartrain': 68, 'Mille Lacs': 746, 'Salton': 829, 'Saint Clair': 66, 'Head Gates Reservoir': 766,
            'Lake Moultrie': 830, 'Red Lake Reservoir': 61, 'Okeechobee': 69, 'Lake Marion': 828, 'Champlain': 64,
            'Flathead Lake': 730, 'Manitoba': 53, 'Mono Lake': 798, 'Winnebago': 762, 'Tahoe': 792, 'Great Salt': 67,
            'Goose Lake': 780, 'Lake Winnipesaukee': 768, 'Oneida Lake': 770}

plot_dic = {'Pontchartrain': 'pontchartrain', 'Mille Lacs': 'mille_lacs_lake', 'Salton': 'salton_sea',
            'Saint Clair': 'st_clair', 'Head Gates Reservoir': 'sebago', 'Lake Moultrie': 'moultrie',
            'Red Lake Reservoir': 'lower_red', 'Okeechobee': 'okeechobee', 'Lake Marion': 'marion',
            'Champlain': 'champlain', 'Flathead Lake': 'flathead', 'Manitoba': 'manitoba', 'Mono Lake': 'mono',
            'Winnebago': 'winnebago', 'Tahoe': 'tahoe', 'Great Salt': 'great_salt_lake', 'Goose Lake': 'goose',
            'Lake Winnipesaukee': 'winnipesaukee', 'Oneida Lake': 'oneida'}


def get_centroid(lake_id1):
    gdf = gpd.read_file("./Data/Geojsons/{}.geojson".format(lake_id1))
    st.session_state.zoom_center_y = float(gdf["geometry"].centroid.x)
    st.session_state.zoom_center_x = float(gdf["geometry"].centroid.y)
    st.session_state.zoom_level = 9
    return gdf


def show_map(lake_id2, lake_name):
    gdf2 = get_centroid(lake_id2)
    m = leafmap.Map(
        center=(st.session_state.zoom_center_x, st.session_state.zoom_center_y),
        zoom=st.session_state.zoom_level,
        google_map="SATELLITE",
        plugin_Draw=True,
        Draw_export=True,
        locate_control=True,
        plugin_LatLngPopup=False,
    )
    bounds = gdf2.total_bounds
    m.add_gdf(gdf2, layer_name=lake_name, zoom_to_layer=True, fill_colors=['blue'], info_mode='on_hover',)
    m.zoom_to_bounds(bounds)
    m.to_streamlit(responsive=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("T_GRND2D Plot")
        image = Image.open(".Data/Plots/T_GRND2D/{}_T_GRND2D.png".format(plot_dic[lake_name]))
        st.image(image)

    with col2:
        st.write("T2 Plot")
        image = Image.open(".Data/Plots/T2/{}_T2.png".format(plot_dic[lake_name]))
        st.image(image)

    with col3:
        st.write("TSK Plot")
        image = Image.open(".Data/Plots/TSK/{}_TSK.png".format(plot_dic[lake_name]))
        st.image(image)


with st.container():
    st.sidebar.title("Select a lake:")
    lake = st.sidebar.selectbox("Lakes:", ('Champlain', 'Flathead Lake', 'Goose Lake', 'Great Salt',
                                                   'Head Gates Reservoir', 'Lake Marion', 'Lake Moultrie',
                                                   'Lake Winnipesaukee', 'Manitoba', 'Mille Lacs', 'Mono Lake',
                                                   'Okeechobee', 'Oneida Lake', 'Pontchartrain', 'Red Lake Reservoir',
                                                   'Saint Clair', 'Salton', 'Tahoe', 'Winnebago'))


with st.container():
    if lake:
        show_map(lake_dic[lake], lake)
