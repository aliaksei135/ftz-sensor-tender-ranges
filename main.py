import folium
import geopandas as gpd
import streamlit as st
from streamlit_folium import st_folium

SOLENT_CENTRE = (50.76, -1.193)
BOUNDS_DF = gpd.read_file("data/bounds.geojson")
SITES_DF = gpd.read_file("data/sites_jittered.geojson")


def create_folium_map(geojson, bounds=True):
    m = folium.Map(location=SOLENT_CENTRE,
                   zoom_start=10)
    folium.GeoJson(geojson).add_to(m)
    if bounds:
        folium.GeoJson(BOUNDS_DF.to_json(), style_function=lambda _: {
            "fillColor": "#ffff00",
            "dashArray": "5, 5",
        }
                       ).add_to(m)
    return m


def main():
    st.title("FTZ Sensor Tender Range Analyser")

    st.subheader("Bounds and Sensor Sites:")
    info_map = folium.Map(location=SOLENT_CENTRE,
                          zoom_start=10)
    folium.GeoJson(BOUNDS_DF.to_json()).add_to(info_map)
    folium.GeoJson(SITES_DF.to_json()).add_to(info_map)
    st_folium(info_map)
    # Create buttons for downloads of bounds and sites
    st.download_button("Download Bounds GeoJSON", data=BOUNDS_DF.to_json(), file_name="bounds.geojson")
    st.download_button("Download Sites GeoJSON", data=SITES_DF.to_json(), file_name="sites.geojson")

    st.divider()
    # Upload coverage file
    st.subheader("Analyse Coverage:")
    user_coverage_file = st.file_uploader("Upload a GeoJSON file of coverage polygons", type=["geojson"])

    if user_coverage_file is not None:
        # Read GeoJSON file
        coverage_df = gpd.read_file(user_coverage_file)
        # Create latitudes and longitudes from geometry column

        # Display Folium map
        st.subheader("Your Coverage Map:")
        st_folium(create_folium_map(coverage_df.to_json(), bounds=False))

        st.divider()

        # Work out actual coverage of bounds
        intersected_coverage = gpd.overlay(coverage_df, BOUNDS_DF, how='intersection')
        coverage_area = intersected_coverage.to_crs(epsg=27700).area.sum()
        st.subheader("Coverage of Interest:")
        st.text(f"Intersection area: {coverage_area:.0f} m^2")
        st_folium(create_folium_map(intersected_coverage.to_json(), bounds=True))


if __name__ == "__main__":
    main()
