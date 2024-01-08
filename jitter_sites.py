import geopandas as gpd
import numpy as np
import shapely.geometry as sg


def jitter_point(epsg3857_point, distance_m=600):
    # Get random jitter in x and y
    dx, dy = np.random.uniform(-distance_m, distance_m, 2)
    # Add to point
    return sg.Point(epsg3857_point.x + dx, epsg3857_point.y + dy)


if __name__ == '__main__':
    # Import true sites
    true_sites_df = gpd.read_file("data/sites_true.geojson", crs=4326).to_crs(epsg=3857)
    # For each of the true sites, create jitter its location within the distance
    jitter_sites_df = gpd.GeoDataFrame(geometry=true_sites_df.geometry.apply(jitter_point, 1000), crs=3857).to_crs(
        epsg=4326)
    jitter_sites_df.to_file("data/sites_jittered.geojson", driver="GeoJSON")
