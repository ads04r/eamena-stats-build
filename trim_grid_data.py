import json, csv, os, sys

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')

with open(os.path.join(data_path, 'grid_data.json'), 'r') as fp:
	grid_data = json.load(fp)

for grid_id in grid_data.keys():
	c = len(grid_data[grid_id])
	for i in range(0, c):
		keys = list(grid_data[grid_id][i].keys())
		for k in ['ID', 'Label', 'Role', 'Date', 'MissingFields']:
			if k in keys:
				keys.remove(k)
		for k in keys:
			del grid_data[grid_id][i][k]

with open(os.path.join(data_path, 'grid_data_trimmed.json'), 'w') as fp:
	fp.write(json.dumps(grid_data))
