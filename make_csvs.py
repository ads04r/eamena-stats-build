import json, csv, os, sys

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
geometries_file = os.path.join(data_path, 'geometries.csv')
summary_file = os.path.join(data_path, 'summary.json')

ret = {}
with open(summary_file, 'r') as fp:
	data = json.load(fp)

with open(geometries_file, 'r') as fp:
	r = csv.reader(fp, delimiter=',', quotechar='"')
	for row in r:
		if row[0] in data:
			data[row[0]]['Geometry'] = json.loads(row[1])

for id, item in data.items():
	if not 'Actor' in item:
		continue
	if not 'Geometry' in item:
		continue
	if not 'Role' in item:
		continue
	if not '270e5b36-4d18-4b6e-a7ee-c49e3d301620' in json.dumps(item['Role']): # ugh
		continue
	if isinstance(item['Actor'], list):
		actor_ids = [x['id'] for x in item['Actor']]
	elif isinstance(item['Actor'], dict):
		actor_ids = [item['Actor']['id']]

	item['URL'] = 'https://database.eamena.org/report/' + id
	for actor_id in actor_ids:
		if not actor_id in ret:
			ret[actor_id] = []
		ret[actor_id].append(item)

for person_id, items in ret.items():

	person_file = os.path.join(data_path, 'people', person_id + '.csv')
	with open(person_file, 'w') as fp:
		w = csv.writer(fp, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for item in items:
			w.writerow([item['ID'], item['URL'], json.dumps(item['Geometry'])])

