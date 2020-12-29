import csv

import shapefile
import pycrs
from pyproj import Proj, transform


def parse_shp(path):
    sf = shapefile.Reader(path)
    crs = pycrs.load.from_file(path.replace('.shp', '.prj'))
    input_projection = Proj(crs.to_proj4())  # or init="ESRI:102718"
    output_projection = Proj(init="epsg:4326")

    return sf, {
        "input": input_projection,
        "output": output_projection,
    }


def read_data(sf, projections):
    shapes = sf.shapes()
    records = sf.records()

    data = []
    for idx, shape in enumerate(shapes):
        record = records[idx]
        x, y = shape.points[0]
        lat, lng = transform(projections["input"], projections["output"], x, y)
        data.append({
            "lat": lat,
            "lng": lng,
            "service_point_id": int(record[0]),
            "address": record[1],
            "meter_id": record[2],
            "service_connection_id": int(record[3])
        })

    return data


def save_data(data, output):
    with open(output, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(data[0].keys()))
        writer.writeheader()
        writer.writerows(data)


def run(input_path, output_path):
    # get shapefile data and input/output projections
    sf, projections = parse_shp(input_path)

    # load data to list of dictionaries
    data = read_data(sf, projections)

    # save to csv
    save_data(data, output_path)


run(input_path=r'C:\Users\user\Desktop\Projects\locations-202012\\Export_Output.shp', output_path='test.csv')
