import geopandas as gpd
import numpy as np

if __name__ == '__main__':
    # Import the jittered sites
    jitter_sites_df = gpd.read_file("data/sites_jittered.geojson", crs=4326)
    # Pick a random number of the sites
    n_sites = np.random.randint(1, len(jitter_sites_df))
    # Pick some random sites and convert to epsg3857
    random_sites_df = jitter_sites_df.sample(n_sites).to_crs(epsg=3857)
    # Put some 5km circles around the sites
    coverage_df = gpd.GeoDataFrame(geometry=random_sites_df.geometry.buffer(5000), crs=3857).to_crs(epsg=4326)
    # Save the coverage
    coverage_df.to_file("data/demo_coverage.geojson", driver="GeoJSON")
