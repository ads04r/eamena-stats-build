import yaml, datetime, os, json, sys

date_start = datetime.date(2024, 7, 1)
date_end = datetime.date(2025, 9, 1)
front_matter = {'toc': False}

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
output_file = os.path.join(docs_path, 'marea.md')
summary_file = os.path.join(data_path, 'summary.json')
disturbances_file = os.path.join(data_path, 'disturbances.json')
marea_uuid = '270e5b36-4d18-4b6e-a7ee-c49e3d301620'

headers = """
<style>
.nocheckbox td:nth-child(1), .nocheckbox th:nth-child(1) {
  display: none;
}
.nocheckbox td:nth-child(2), .nocheckbox th:nth-child(2) {
  padding-left: 0px;
}
.card img {
  max-width: 100% !important;
}
</style>
"""
map_html = "<div class=\"card\">\n\n![Progress map](map.png)\n\n</div>"
marea_sites_total = {}
marea_grids_total = {}
marea_sites = {}
marea_grids = {}
marea_countries = {}
front_stats = []

with open(disturbances_file, 'r') as fp:
	disturbances = json.load(fp)

with open(summary_file, 'r') as fp:
	for uid, item in json.load(fp).items():
		if not 'Role' in item:
			continue
		if not 'AddedToDatabase' in item:
			continue
		if not marea_uuid in json.dumps(item['Role']):
			continue
		grids = []
		countries = []
		if 'Grid' in item:
			if isinstance(item['Grid'], list):
				grids = item['Grid']
			else:
				grids.append(item['Grid'])
		if 'Country' in item:
			if isinstance(item['Country'], list):
				countries = item['Country']
			else:
				countries.append(item['Country'])
		in_range = False
		dsa = item['AddedToDatabase']
		if not isinstance(dsa, list):
			dsa = [dsa]
		for ds in dsa:
			dss = ds.split('-')
			dt = datetime.date(int(dss[0]), int(dss[1]), int(dss[2]))
			if dt < date_start:
				continue
			if dt > date_end:
				continue
			in_range = True
		if not item['ID'] in marea_sites_total:
			marea_sites_total[item['ID']] = item
		for grid in grids:
			if not grid['id'] in marea_grids_total:
				marea_grids_total[grid['id']] = grid
		if not in_range:
			continue
		item['Disturbances'] = {}
		item['UUID'] = uid
		if uid in disturbances:
			item['Disturbances'] = disturbances[uid]
		if not item['ID'] in marea_sites:
			marea_sites[item['ID']] = item
		for grid in grids:
			grid['disturbances'] = {}
			if not grid['id'] in marea_grids:
				marea_grids[grid['id']] = grid
		for country in countries:
			country['disturbances'] = {}
			if not country['id'] in marea_countries:
				marea_countries[country['id']] = country
		if 'disturbances' in item['Disturbances']:
			for d in item['Disturbances']['disturbances']:
				for grid in grids:
					if grid['id'] in marea_grids:
						if not d in marea_grids[grid['id']]:
							marea_grids[grid['id']]['disturbances'][d] = 0
						marea_grids[grid['id']]['disturbances'][d] = marea_grids[grid['id']]['disturbances'][d] + 1
				for country in countries:
					if country['id'] in marea_countries:
						if not d in marea_countries[country['id']]:
							marea_countries[country['id']]['disturbances'][d] = 0
						marea_countries[country['id']]['disturbances'][d] = marea_countries[country['id']]['disturbances'][d] + 1

print(json.dumps(marea_grids, indent=4))
sys.exit(0)

front_stats.append("<p>MarEA Sites</p><h2>" + str(len(marea_sites)) + "</h2>")
front_stats.append("<p>MarEA Grids</p><h2>" + str(len(marea_grids)) + "</h2>")
front_stats.append("<p>Total MarEA Sites</p><h2>" + str(len(marea_sites_total)) + "</h2>")
front_stats.append("<p>Total MarEA Grids</p><h2>" + str(len(marea_grids_total)) + "</h2>")

with open(output_file, 'w') as fp:

	fp.write('---\n' + yaml.dump(front_matter) + '---\n')
	fp.write(headers)
	fp.write("# MarEA Stats Page\n\n")

	fp.write(map_html + '\n\n')

	if len(front_stats) > 0:
		fp.write("## Site Documentation\n\n")
		fp.write("<div class=\"grid grid-cols-4\">\n")
		for card in front_stats:
			fp.write("<div class=\"card\">" + card + "</div>\n")
		fp.write("</div>\n\n")

	fp.write("## Threat Analysis\n\n")

# {"Actor": {"id": "780a6fe2-4ab2-4fa5-98d9-8f52d51d9335", "label": "Nichole Sheldrick"},
#  "AddedToDatabase": "2023-05-02",
#  "Country": {"id": "049dda8d-9fd3-49a9-b31d-de825de40951", "label": "Libya"},
#  "Date": "2019-07-17",
#  "Grid": {"id": "1776f647-4f45-4b29-a319-a89ab17e7b09", "label": "E13N31-13"},
#  "ID": "EAMENA-0188602",
#  "Role": {"id": "20b1a4e0-97e1-41f7-b519-124a7317266b", "label": "EAMENA Project Staff"} }
