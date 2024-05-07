import json, os, sys

base_path = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(base_path, 'roles.json'), 'r') as fp:
	data = json.load(fp)

ret = []
for id in data:

	item = data[id]
	reports = []
	for report in item['reports']:
		filename = os.path.join(base_path, report['filename'])
		with open(filename, 'r') as fp:
			reports.append(json.load(fp))
	item['reports'] = reports
	ret.append(item)

print(json.dumps(ret, indent=4))
