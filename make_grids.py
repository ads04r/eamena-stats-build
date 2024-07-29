import json, csv, os, sys

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
disturbances_file = os.path.join(data_path, 'disturbances.json')
template_file = os.path.join(base_path, 'grid_template.md')

with open(template_file, 'r') as fp:
	template = fp.read()
with open(disturbances_file, 'r') as fp:
	disturbances = json.load(fp)

h = []
data = {}
ret = {}
with open(os.path.join(data_path, 'tiles.csv'), 'r') as fp:
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
			item[h[i]] = row[i]

		id = item['resourceinstanceid']
		if not id in data:
			data[id] = []
		k = item['name'].split(' / ')[0].replace('"', '')
		v = int(item['tiles'])
		data[id].append([k, v])

with open(os.path.join(data_path, 'grid_data.json'), 'r') as fp:
	grid_data = json.load(fp)

for gridk in grid_data.keys():
	grid_id = str(gridk)
	ret = {"sites": []}
	for item in grid_data[grid_id]:
		uuid = item['ID']
		tiles = []
		item['Disturbances'] = []
		if uuid in data:
			tiles = data[uuid]
		if uuid in disturbances:
			if 'disturbances' in disturbances[uuid]:
				item['Disturbances'] = disturbances[uuid]['disturbances']
		item['Tiles'] = tiles
		ret['sites'].append(item)
	with open(os.path.join(docs_path, grid_id + '.md'), 'w') as fp:
		fp.write(template.replace("%%%", grid_id))
	with open(os.path.join(data_path, 'grids', grid_id + '.json'), 'w') as fp:
		fp.write(json.dumps(ret))

#    "38e6731d-7e36-41e4-8155-3e453cc5d79a": {
#        "resourceinstanceid": "38e6731d-7e36-41e4-8155-3e453cc5d79a",
#        "data": {
#            "Disturbance Cause Certainty": [
#                "High"
#            ],
#            "Disturbance Date From": [],
#            "Disturbance Cause Type": [
#                "Wind Action"
#            ],
#            "Disturbance Date To": []
#        },
#        "disturbances": [
#            "Wind Action"
#        ]
#    }
