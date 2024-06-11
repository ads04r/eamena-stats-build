import json, csv, os, sys

base_path = os.path.abspath(os.path.dirname(__file__))

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
	grid = {}
	for item in grid_data[grid_id]:
		site_id = item['ID']
		tiles = []
		if site_id in data:
			tiles = data[site_id]
		grid[site_id] = {'id': site_id, 'label': item['Label'], 'tiles': tiles}
	ret[grid_id] = grid

print(json.dumps(ret, indent=4))
