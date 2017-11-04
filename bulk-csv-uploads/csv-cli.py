"""CLI Python Script to rip through a folder and upload CSVs"""
import os
import pandas as pd
from arcgis import GIS
from arcgis.features import SpatialDataFrame
from arcgis.geometry import Point
from utils.systemutils import get_subdirectories, get_csvs
from utils.inpututils import get_list_input_index, get_list_input_smart, get_bool_input
from utils.searchutils import get_closest_match_list

# auto options for columsn to coordinate fields
XOPTIONS = ['x', 'lon', 'longitude']
YOPTIONS = ['y', 'lat', 'latitude']
ZOPTIONS = ['z', 'height', 'altitude']
OPTIONS = {
    'x': XOPTIONS,
    'y': YOPTIONS,
    'z': ZOPTIONS
}

def _get_dir_path():
    """get the path for directory containing the CSVs"""
    path = input("Folder Path (or `-L` for subdirs): ")
    while not os.path.isdir(path):
        if path == '-L':
            subdirs = get_subdirectories()
            path = get_list_input_index(subdirs)
        else:
            path = input("Folder Path (or `-L` for subdirs): ")
    return path

def _get_point_for_row(row, coord_fields):
    """construct point from a dataframe row"""
    p_dict = {}
    p_dict['x'] = row[coord_fields['x']]
    p_dict['y'] = row[coord_fields['y']]
    if 'z' in coord_fields and coord_fields['z']:
        p_dict['z'] = row[coord_fields['z']]
    return Point(p_dict)

def _get_coord_field(field, colnames, prev_fields):
    """get the correct coordinate field from available columns"""
    f_in = get_list_input_smart
    prompt = "{0} (`-L` or name): ".format(field)
    has_prev = field in prev_fields and prev_fields[field] in colnames
    return prev_fields[field] if has_prev else f_in(field, prompt, OPTIONS[field], colnames)

def _get_coord_fields(colnames, prev_fields, has_z=False):
    """get the correct coordinate fields from the column names"""
    fields = {}
    fields['x'] = _get_coord_field('x', colnames, prev_fields)
    fields['y'] = _get_coord_field('y', colnames, prev_fields)
    if not has_z:
        return fields
    fields['z'] = _get_coord_field('z', colnames, prev_fields)
    return fields

def main():
    """run the show!"""
    print("\n\nHELLO! This is a quick tool to upload CSVs\n")

    # connect to GIS
    gis = GIS("https://www.arcgis.com", "mpayson_startups", "AcheTeVitu0811")

    # get the directory containing the csvs
    dir_path = _get_dir_path()

    # create a new folder in the GIS to store the layers
    folder = os.path.basename(dir_path)
    gis_folder = gis.content.create_folder(folder)

    # get an array of all the csvs in the directory
    csvs = get_csvs(dir_path)
    csv_paths = [os.path.join(dir_path, csv) for csv in csvs]
    n_paths = len(csv_paths)
    print("Pushing {0} csvs".format(n_paths))

    coord_fields = {}
    has_z = False

    # loop through csvs, build spatial dataframe, upload layers to GIS, move to new folder
    for i, csv_path in enumerate(csv_paths):
        
        # read csv
        df = pd.read_csv(csv_path)
        cols = df.columns

        # check if there are Z coords on first csv, if not ask if there are Zs
        if i == 0:
            has_z = get_closest_match_list(ZOPTIONS, cols, 0.95)[0] is not None
            has_z = get_bool_input("Z coordinates? (Y/N) ") if not has_z else has_z

        # get the coordinate fields for the current CSV
        coord_fields = _get_coord_fields(cols, coord_fields, has_z)

        # construct geometries and build a spatial dataframe
        df_geom = df.apply(lambda row: _get_point_for_row(row, coord_fields), axis=1)
        sdf = SpatialDataFrame(data=df, geometry=df_geom)

        # get title from csv
        title = os.path.splitext(os.path.basename(csv_path))[0]

        # import the csv and move it to the folder
        csv_lyr = gis.content.import_data(sdf, title=title)
        csv_lyr.move(gis_folder)

        print("{0}/{1}".format(i + 1, n_paths))


if __name__ == "__main__":
    # fail gracefully
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nSee ya later!")
