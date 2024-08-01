import json, csv, os, sys
from pykml import parser

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
static_path = os.path.join(data_path, 'static')
input_file = os.path.join(static_path, 'grids.kml')
output_file = os.path.join(data_path, 'grid_geometries.json')

def process_polygon(id, coords):

	min_lon = 999.0
	min_lat = 999.0
	max_lon = -999.0
	max_lat = -999.0
	for item in coords:
		if item[0] < min_lon:
			min_lon = item[0]
		if item[0] > max_lon:
			max_lon = item[0]
		if item[1] < min_lat:
			min_lat = item[1]
		if item[1] > max_lat:
			max_lat = item[1]
	return {"type":"FeatureCollection", "features":[{"type":"Feature", "properties":{}, "id":id, "geometry":{"type":"Polygon", "coordinates":[[[min_lon, min_lat], [max_lon, min_lat], [max_lon, max_lat], [min_lon, max_lat], [min_lon, min_lat]]]}}]}

root = parser.parse(open(input_file, 'rb')).getroot()
grids = root.Document.Folder
ret = {}
for country in grids.Folder:
	for grid in country.Placemark:
		grid_id = str(grid.name).strip().upper()
		coord_strings = str(grid.MultiGeometry.Polygon.outerBoundaryIs.LinearRing.coordinates).strip().split(' ')
		coords = []
		for cs in coord_strings:
			c = cs.split(',')
			coords.append([float(c[0]), float(c[1])])
		if not grid_id in ret:
			ret[grid_id] = []
		for coord in coords:
			ret[grid_id].append(coord)

for grid_id in ret.keys():
	ret[grid_id] = process_polygon(grid_id, ret[grid_id])

with open(output_file, 'w') as fp:
	fp.write(json.dumps(ret))
