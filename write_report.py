import yaml, datetime, os, json, sys

date_start = datetime.date(2024, 7, 1)
date_end = datetime.date(2025, 9, 1)
front_matter = {'toc': False}

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
summary_file = os.path.join(data_path, 'summary.json')
disturbances_file = os.path.join(data_path, 'disturbances.json')
marea_uuid = '270e5b36-4d18-4b6e-a7ee-c49e3d301620'

#output_file = os.path.join(docs_path, 'marea.md')
output_file = os.path.join(base_path, 'marea-dev.md')

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
		if not 'Date' in item:
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
		dsa = item['Date']
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
			break
		if not item['ID'] in marea_sites_total:
			marea_sites_total[item['ID']] = item
		for grid in grids:
			if not grid['id'] in marea_grids_total:
				marea_grids_total[grid['id']] = grid
		if in_range is False:
			continue
		item['Disturbances'] = {}
		item['UUID'] = uid
		if uid in disturbances:
			item['Disturbances'] = disturbances[uid]
		if not item['ID'] in marea_sites:
			marea_sites[item['ID']] = item
		for grid in grids:
			grid['disturbances'] = {}
			grid['people'] = {}
			grid['sites'] = []
			if not grid['id'] in marea_grids:
				marea_grids[grid['id']] = grid
			if not uid in marea_grids[grid['id']]['sites']:
				marea_grids[grid['id']]['sites'].append(uid)
		for country in countries:
			country['disturbances'] = {}
			country['people'] = {}
			country['sites'] = []
			if not country['id'] in marea_countries:
				marea_countries[country['id']] = country
			if not uid in marea_countries[country['id']]['sites']:
				marea_countries[country['id']]['sites'].append(uid)
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
		if 'Actor' in item:
			actors = item['Actor']
			if not isinstance(actors, list):
				actors = [item['Actor']]
			for actor in actors:
				for grid in grids:
					if grid['id'] in marea_grids:
						marea_grids[grid['id']]['people'][actor['id']] = actor
				for country in countries:
					if country['id'] in marea_countries:
						marea_countries[country['id']]['people'][actor['id']] = actor

front_stats.append("<p>MarEA Sites</p><h2>" + str(len(marea_sites)) + "</h2>")
front_stats.append("<p>MarEA Grids</p><h2>" + str(len(marea_grids)) + "</h2>")
front_stats.append("<p>Total MarEA Sites</p><h2>" + str(len(marea_sites_total)) + "</h2>")
front_stats.append("<p>Total MarEA Grids</p><h2>" + str(len(marea_grids_total)) + "</h2>")

with open(output_file, 'w') as fp:

	fp.write('---\n' + yaml.dump(front_matter) + '---\n')
	fp.write(headers)
	fp.write("# MarEA Stats Page\n\n")

	fp.write(map_html + '\n\n')

	fp.write("## Site Documentation\n\n")

	if len(front_stats) > 0:
		fp.write("<div class=\"grid grid-cols-4\">\n")
		for card in front_stats:
			fp.write("<div class=\"card\">" + card + "</div>\n")
		fp.write("</div>\n\n")

	fp.write("| Grid Square | Sites       | Researchers  |\n")
	fp.write("|-------------|-------------|--------------|\n")
	total = 0
	for grid in sorted(marea_grids.values(), reverse=True, key=lambda x: len(x['sites'])):
		fp.write('| ' + (' | '.join([grid['label'], str(len(grid['sites'])), (', '.join([str(x['label']) for x in grid['people'].values()]))])) + ' |\n')
		total = total + len(grid['sites'])
	fp.write('| ' + (' | '.join(['TOTAL', str(total), ''])) + ' |\n')
	fp.write("\n")

# {"id": "c4e8738c-c3a5-4aba-a3f5-31f3890150e0", "label": "E34N31-32", "disturbances": {"Clearance (Bulldozing/Levelling)": 1}, "people": {"77fef06f-3a14-4bdb-8a0a-59cddb4ff35b": {"id": "77fef06f-3a14-4bdb-8a0a-59cddb4ff35b", "label": "Mohammad Jaradat"}, "60097680-0c07-4f91-a076-7a30b390e60f": {"id": "60097680-0c07-4f91-a076-7a30b390e60f", "label": "Georgia Andreou"}, "90ae76cf-865d-4e68-971c-c2b2af9be18c": {"id": "90ae76cf-865d-4e68-971c-c2b2af9be18c", "label": "Michael Fradley"}}}

	fp.write("## Threat Analysis\n\n")

	for countryid, country in marea_countries.items():

		if len(country['disturbances']) == 0:
			continue

		fp.write("### " + country['label'] + "\n\n")
		fp.write((', '.join([x['label'] for x in country['people'].values()])) + '\n\n')

		fp.write("#### Threats \n\n")
		fp.write("```mermaid\n")
		fp.write("gantt")
		fp.write("  todayMarker off\n")
		fp.write("  dateFormat X\n")
		fp.write("  axisFormat %\n")
		fp.write("\n")
		for d, f in country['disturbances'].items():
			fp.write("  " + str(d) + " (" + str(f) + ") : 0, " + str(f) + "\n")
		fp.write("```\n\n")


# {"Actor": {"id": "780a6fe2-4ab2-4fa5-98d9-8f52d51d9335", "label": "Nichole Sheldrick"},
#  "AddedToDatabase": "2023-05-02",
#  "Country": {"id": "049dda8d-9fd3-49a9-b31d-de825de40951", "label": "Libya"},
#  "Date": "2019-07-17",
#  "Grid": {"id": "1776f647-4f45-4b29-a319-a89ab17e7b09", "label": "E13N31-13"},
#  "ID": "EAMENA-0188602",
#  "Role": {"id": "20b1a4e0-97e1-41f7-b519-124a7317266b", "label": "EAMENA Project Staff"} }
