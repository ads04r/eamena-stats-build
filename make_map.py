from staticmap import StaticMap, Polygon, CircleMarker
import os, json, sys

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
dist_path = os.path.join(base_path, 'dist')
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
static_path = os.path.join(data_path, 'static')
grids_file = os.path.join(data_path, 'grid_data.json')
geometry_file = os.path.join(data_path, 'grid_geometries.json')
map_file = os.path.join(docs_path, 'map.png')

with open(grids_file, 'r') as fp:
	data = json.load(fp)
with open(geometry_file, 'r') as fp:
	geometries = json.load(fp)

m = StaticMap(2000, 1000, url_template="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

for grid_key in data.keys():

	grid_id = str(grid_key)
	item = data[grid_id]
	if not 'MarEA' in json.dumps(item):
		continue
	if not grid_id in geometries:
		continue
	geom = geometries[grid_id]

	try:
		coordinates = geom['features'][0]['geometry']['coordinates'][0]
	except:
		coordinates = []

	polygon = Polygon(coords=coordinates, fill_color='#007F00', outline_color='#000000', simplify=False)
	m.add_polygon(polygon)

image = m.render(zoom=5)
image.save(map_file)
