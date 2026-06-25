from staticmap import StaticMap, Polygon, CircleMarker
import os, json, sys, csv, datetime

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
dist_path = os.path.join(base_path, 'dist')
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
static_path = os.path.join(data_path, 'static')
grids_file = os.path.join(data_path, 'grid_data.json')
geometry_file = os.path.join(data_path, 'grid_geometries.json')
summary_file = os.path.join(data_path, 'summary.json')
map_file = os.path.join(docs_path, 'map_{}.png'.format(datetime.datetime.now().strftime("%Y%m%d")))
empty_file = os.path.join(data_path, 'eamena_empty_records.csv')
empty_map_file = os.path.join(docs_path, 'empty_map.png')
mds = []
empty = []

with open(grids_file, 'r') as fp:
	data = json.load(fp)
with open(geometry_file, 'r') as fp:
	geometries = json.load(fp)
with open(summary_file, 'r') as fp:
	for item in json.load(fp).values():
		if not 'Grid' in item:
			continue
		if not 'label' in item['Grid']:
			continue
		if item['Grid']['label'] in mds:
			continue
		if not 'MissingFields' in item:
			continue
		if len(item['MissingFields']) == 0:
			continue
		mds.append(item['Grid']['label'])
with open(empty_file, newline='') as fp:
	reader = csv.DictReader(fp)
	for row in reader:
		if not 'Grid Square' in row:
			continue
		grid_id = row['Grid Square']
		if grid_id in empty:
			continue
		empty.append(grid_id)

m = StaticMap(2000, 1000, url_template="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

for grid_key in data.keys():

	grid_id = str(grid_key)
	item = data[grid_id]
	fill_colour = '#CFCF7F'
	if 'MarEA' in json.dumps(item):
		fill_colour = '#007F00'
	if not grid_id in geometries:
		continue
	geom = geometries[grid_id]

	try:
		coordinates = geom['features'][0]['geometry']['coordinates'][0]
	except:
		coordinates = []

	polygon = Polygon(coords=coordinates, fill_color=fill_colour, outline_color='#000000', simplify=False)
	m.add_polygon(polygon)

image = m.render(zoom=5)
image.save(map_file)

m = StaticMap(2000, 1000, url_template="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

for grid_key in data.keys():

	grid_id = str(grid_key)
	item = data[grid_id]
	if not grid_id in mds:
		continue
	if not grid_id in geometries:
		continue
	fill_colour = '#FFCFCF'
	if grid_id in empty:
		fill_colour = '#FF2020'
	geom = geometries[grid_id]

	try:
		coordinates = geom['features'][0]['geometry']['coordinates'][0]
	except:
		coordinates = []

	polygon = Polygon(coords=coordinates, fill_color=fill_colour, outline_color='#000000', simplify=False)
	m.add_polygon(polygon)

image = m.render(zoom=5)
image.save(empty_map_file)
