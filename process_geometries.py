import json, csv, os, sys, geojson

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
summary_file = os.path.join(data_path, 'summary.json')
grid_geom_file = os.path.join(data_path, 'grid_geometries.json')
input_file = os.path.join(data_path, 'geometries.csv')
output_file = os.path.join(data_path, 'grid_matches.csv')

geom_id = '5348cf67-c2c5-11ea-9026-02e7594ce0a0'
site_geometries = {}
grid_geometries = {}

with open(summary_file, 'r') as fp:
	summary = json.load(fp)
with open(grid_geom_file, 'r') as fp:
	grid_geometries = json.load(fp)

h = []
with open(input_file, 'r') as fp:
	r = csv.reader(fp, delimiter=',', quotechar='"')
	for row in r:
		if len(h) == 0:
			h = row
			continue
		item = {}
		if len(row) > len(h):
			continue
		if len(row) == 0:
			continue
		item = {}
		for i in range(0, len(row)):
			k = h[i]
			if k == 'position':
				data = json.loads(row[i])
				if geom_id in data:
					item[k] = data[geom_id]
				continue
			item[k] = row[i]

		id = item['resourceinstanceid']
		if not 'position' in item:
			continue
		site_geometries[id] = item['position']

# [{'AddedToDatabase': '2023-05-01', 'Country': {'id': '049dda8d-9fd3-49a9-b31d-de825de40951', 'label': 'Libya'}, 'Date': '2023-05-01', 'Grid': {'id': 'cbf4d911-e681-4c18-85c1-a4eddd1552f3', 'label': 'E13N26-13'}, 'ID': '00000fe9-df52-4815-9d94-a158deef35df', 'Label': 'EAMENA-0000580'}, {'AddedToDatabase': '2023-05-01', 'Country': {'id': '049dda8d-9fd3-49a9-b31d-de825de40951', 'label': 'Libya'}, 'Date': '2023-05-01', 'Grid': {'id': 'cbf4d911-e681-4c18-85c1-a4eddd1552f3', 'label': 'E13N26-13'}, 'ID': '25810a88-af27-4634-8c3b-63e21faa8028', 'Label': 'EAMENA-0000579'}, {'AddedToDatabase': '2023-05-01', 'Country': {'id': '049dda8d-9fd3-49a9-b31d-de825de40951', 'label': 'Libya'}, 'Date': '2023-05-01', 'Grid': {'id': 'cbf4d911-e681-4c18-85c1-a4eddd1552f3', 'label': 'E13N26-13'}, 'ID': '30aa9189-90cd-4c82-9c4d-6727e1504c71', 'Label': 'EAMENA-0000578'}, {'AddedToDatabase': '2023-05-01', 'Country': {'id': '049dda8d-9fd3-49a9-b31d-de825de40951', 'label': 'Libya'}, 'Date': '2023-05-01', 'Grid': {'id': 'cbf4d911-e681-4c18-85c1-a4eddd1552f3', 'label': 'E13N26-13'}, 'ID': '9489169f-e113-4884-af22-448da4155228', 'Label': 'EAMENA-0000575'}, {'AddedToDatabase': '2023-05-01', 'Country': {'id': '049dda8d-9fd3-49a9-b31d-de825de40951', 'label': 'Libya'}, 'Date': '2023-05-01', 'Grid': {'id': 'cbf4d911-e681-4c18-85c1-a4eddd1552f3', 'label': 'E13N26-13'}, 'ID': '9792216f-6130-4703-ae9e-8fbc1947477a', 'Label': 'EAMENA-0000576'}, {'AddedToDatabase': '2023-05-01', 'Country': {'id': '049dda8d-9fd3-49a9-b31d-de825de40951', 'label': 'Libya'}, 'Date': '2023-05-01', 'Grid': {'id': 'cbf4d911-e681-4c18-85c1-a4eddd1552f3', 'label': 'E13N26-13'}, 'ID': '9d6e04e7-7586-4a55-9b80-7e6d849a10fd', 'Label': 'EAMENA-0000577'}]
# {'features': [{'geometry': {'coordinates': [[[51.25, 26.0], [51.25, 26.25], [51.5, 26.25], [51.5, 26.0], [51.25, 26.0]]], 'type': 'Polygon'}, 'id': '4b0cfc8d-3b58-4808-a954-0b150bdd1db7', 'properties': {}, 'type': 'Feature'}], 'type': 'FeatureCollection'}

with open(output_file, 'w') as fp:
	w = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	for site_id_k in summary.keys():

		site_id = str(site_id_k)
		site = summary[site_id]

		if not 'ID' in site:
			continue
		if not 'Grid' in site:
			continue

		label = site['ID']

		if isinstance(site['Grid'], list):
			grids = site['Grid']
		else:
			grids = [site['Grid']]
		for grid in grids:
			grid_id = grid['label']

			grid_geom = {}
			site_geom = {}
			if grid_id in grid_geometries:
				grid_geom = grid_geometries[grid_id]
			if site_id in site_geometries:
				site_geom = site_geometries[site_id]

			min_lat = 999.0
			max_lat = -999.0
			min_lon = 999.0
			max_lon = -999.0

			try:
				cs = list(geojson.utils.coords(geojson.loads(json.dumps(site_geom)))) # If no geometry then the grid doesn't matter.
			except:
				cs = None
			if cs is None:
				continue
			total_points = 0
			grid_points = 0
			for c in list(geojson.utils.coords(geojson.loads(json.dumps(grid_geom)))):
				if c[0] < min_lon:
					min_lon = c[0]
				if c[0] > max_lon:
					max_lon = c[0]
				if c[1] < min_lat:
					min_lat = c[1]
				if c[1] > max_lat:
					max_lat = c[1]
			for c in cs:
				total_points = total_points + 1
				if c[0] < min_lon:
					continue
				if c[0] > max_lon:
					continue
				if c[1] < min_lat:
					continue
				if c[1] > max_lat:
					continue
				grid_points = grid_points + 1

			w.writerow([site_id, min_lat, min_lon, max_lat, max_lon, total_points, grid_points])

#   "00000fe9-df52-4815-9d94-a158deef35df" : {
#      "AddedToDatabase" : "2023-05-01",
#      "Country" : {
#         "id" : "049dda8d-9fd3-49a9-b31d-de825de40951",
#         "label" : "Libya"
#      },
#      "Date" : "2023-05-01",
#      "Grid" : {
#         "id" : "cbf4d911-e681-4c18-85c1-a4eddd1552f3",
#         "label" : "E13N26-13"
#      },
#      "ID" : "EAMENA-0000580"
#   },
