import open_maps_scrape as oms
import pandas as pd
import numpy as np
from tqdm import tqdm
import time
import sqlite_db as sdb
import sqlite3

def bbox_segmented_query(macro_bbox_bottom_left, macro_bbox_top_right):

    grid_lat = np.linspace(macro_bbox_bottom_left[0], macro_bbox_top_right[0], 10)
    grid_lon = np.linspace(macro_bbox_bottom_left[1], macro_bbox_top_right[1], 10)
    conn = sqlite3.connection('housing_pipeline_ml.db')

    # iterate on the grid to scrape a smaller area
    df = pd.DataFrame()
    for i in tqdm(range(len(grid_lat) - 1)):
        for j in range(len(grid_lon) - 1):
            micro_bb_bl = [grid_lat[i], grid_lon[j]]
            micro_bb_tr = [grid_lat[i + 1], grid_lon[j + 1]]

            maps_data = oms.get_residential_addresses(micro_bb_bl, micro_bb_tr)
            # check there was a return from the api query
            if maps_data is not None:
                sdb.insert_without_duplicates(maps_data, conn, 'open_street_maps_residential')
            else:
                pass

            # openmaps has a limit to how much data can be downloaded
            time.sleep(7)

    conn.close()
    return df

if __name__ == "__main__":

    #initial goal is to scrape everything in N of 101 and W of I17
    macro_bbox_bottom_left = [33.66772764797897, -112.30735141606544]
    macro_bbox_top_right = [33.757544665988554, -112.10848170826618]

    df = bbox_segmented_query(macro_bbox_bottom_left, macro_bbox_top_right)

    pass