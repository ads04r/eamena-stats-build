import json, csv, os, sys

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docs', 'data')

h = []
data = {}
ret = {}
with open(os.path.join(base_path, 'tiles.csv'), 'r') as fp:
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
		k = item['name']
		v = int(item['tiles'])
		data[id].append([k, v])

with open(os.path.join(base_path, 'grid_data.json'), 'r') as fp:
	grid_data = json.load(fp)

for gridk in grid_data.keys():
	grid_id = str(gridk)
	ret = []
	for item in grid_data[grid_id]:
		uuid = item['ID']
		tiles = []
		if uuid in data:
			tiles = data[uuid]
		item['Tiles'] = tiles
		ret.append(item)
	with open(os.path.join(base_path, 'grids', grid_id + '.json'), 'w') as fp:
		fp.write(json.dumps(ret))
