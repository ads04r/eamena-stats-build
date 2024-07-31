import json, csv, os, sys

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
geo_matches_file = os.path.join(data_path, 'grid_matches.csv')
grid_file = os.path.join(data_path, 'grid_data.json')
output_file = os.path.join(docs_path, 'errors.md')

def flatten(item, key='label'):
	ret = []
	if isinstance(item, list):
		for subitem in item:
			ret.append(subitem[key])
	elif isinstance(item, dict):
		ret.append(item[key])
	elif isinstance(item, str):
		ret.append(item)
	try:
		return ', '.join(ret)
	except:
		return ''

geo_stats = {}
ret = []
with open(geo_matches_file, 'r') as fp:
	r = csv.reader(fp, delimiter=',', quotechar='"')
	for row in r:
		site_id = row.pop(0)
		geo_stats[site_id] = row

with open(grid_file, 'r') as fp:
	for sites in json.load(fp).values():
		for site in sites:
			site_id = site['ID']
			if not(site_id in geo_stats):
				continue
			info = geo_stats[site_id]
			site['problems'] = []
			all_points = int(info[4])
			grid_points = int(info[5])
			if info[0] == '999.0':
				site['problems'].append("No grid square referenced.")
			if all_points == 0:
				site['problems'].append("No geometry for site.")
			if len(site['problems']) == 0:
				if grid_points == 0:
					site['problems'].append("Geometry falls entirely outside the assigned grid square.")
				elif grid_points < all_points:
					site['problems'].append("Geometry falls partially outside the assigned grid square.")
			if len(site['problems']) == 0:
				continue
			ret.append(site)

with open(output_file, 'w') as fp:

	fp.write("| EAMENA ID | Grid Square | Country | Name | Role | URL | Information |\n");
	fp.write("|-----------|-------------|---------|------|------|-----|-------------|\n");

	for item in ret:

		row = ['', '', '', '', '', '', '']
		row[0] = item['Label']
		if 'Grid' in item:
			row[1] = flatten(item['Grid'], 'label')
		if 'Country' in item:
			row[2] = flatten(item['Country'], 'label')
		if 'Actor' in item:
			row[3] = flatten(item['Actor'], 'label')
		if 'Role' in item:
			row[4] = flatten(item['Role'], 'label')
		if 'ID' in item:
			row[5] = "https://database.eamena.org/report/" + item['ID']
		if 'problems' in item:
			row[6] = item['problems'][0]
		fp.write("| " + (" | ".join(row)) + " |\n")
