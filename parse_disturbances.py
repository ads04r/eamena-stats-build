import json, csv, os, sys

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
output_file = os.path.join(data_path, 'disturbances.json')

ret = []
map = {}

with open(os.path.join(data_path, 'values.csv'), 'r') as fp:
	h = []
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
		map[item['valueid']] = item['value']
with open(os.path.join(data_path, 'nodes.csv'), 'r') as fp:
	h = []
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
		map[item['nodeid']] = item['name']

with open(os.path.join(data_path, 'disturbances.csv'), 'r') as fp:
	h = []
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

		if 'tiledata' in item:
			item['data'] = {}
			data = json.loads(item['tiledata'])
			for kk in data.keys():
				k = str(kk)
				km = k
				if km in map:
					km = map[k].strip()
				if data[k]:
					if not isinstance(data[k], str):
						item['data'][km] = data[k]
						continue
					if not k in item['data']:
						item['data'][km] = []
					if data[k] in map:
						item['data'][km].append(map[data[k]].strip())
			if 'Disturbance Cause Type' in item['data']:
				item['disturbances'] = item['data']['Disturbance Cause Type']
			del(item['tiledata'])
			ret.append(item)

with open(output_file, 'w') as fp:
	fp.write(json.dumps(ret))
