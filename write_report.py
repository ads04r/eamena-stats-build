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

output_file = os.path.join(docs_path, 'marea.md')

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

		# Everything from here gets added

		item['Disturbances'] = []
		item['UUID'] = uid
		if uid in disturbances:
			if 'disturbances' in disturbances[uid]:
				item['Disturbances'] = disturbances[uid]['disturbances']
		if not item['ID'] in marea_sites:
			marea_sites[item['ID']] = item

for item in marea_sites.values():

#   "EAMENA-0000505" : {
#      "Actor" : [
#         {
#            "id" : "351b56f1-628c-429c-bbcd-3deec068423c",
#            "label" : "Julia Nikolaus"
#         },
#         {
#            "id" : "780a6fe2-4ab2-4fa5-98d9-8f52d51d9335",
#            "label" : "Nichole Sheldrick"
#         }
#      ],
#      "AddedToDatabase" : "2023-05-01",
#      "Country" : {
#         "id" : "049dda8d-9fd3-49a9-b31d-de825de40951",
#         "label" : "Libya"
#      },
#      "Date" : [
#         "2016-12-02",
#         "2024-08-22"
#      ],
#      "Disturbances" : [],
#      "Grid" : {
#         "id" : "dc39428a-6c93-4ebf-bb41-b3cf92de1f16",
#         "label" : "E13N25-44"
#      },
#      "ID" : "EAMENA-0000505",
#      "Role" : [
#         {
#            "id" : "270e5b36-4d18-4b6e-a7ee-c49e3d301620",
#            "label" : "MarEA Project Staff"
#         },
#         {
#            "id" : "20b1a4e0-97e1-41f7-b519-124a7317266b",
#            "label" : "EAMENA Project Staff"
#         }
#      ],
#      "UUID" : "736f93ae-0a90-4e26-b7c1-b224a0f8a615"
#   }

	disturbances = []
	actors = []
	site_id = item['UUID']
	site_label = item['ID']
	if 'Disturbances' in item:
		disturbances = item['Disturbances']
	if 'Actor' in item:
		if isinstance(item['Actor'], list):
			actors = item['Actor']
		else:
			actors.append(item['Actor'])

	if 'Country' in item:
		country_id = item['Country']['id']
		country_label = item['Country']['label']
		if not country_id in marea_countries:
			marea_countries[country_id] = {'id': country_id, 'label': country_label, 'disturbances': {}, 'people': {}, 'sites': {}}
		if not site_id in marea_countries[country_id]['sites']:
			marea_countries[country_id]['sites'][site_id] = site_label
		for actor in actors:
			actor_id = actor['id']
			if not actor_id in marea_countries[country_id]['people']:
				marea_countries[country_id]['people'][actor_id] = actor
		for d in disturbances:
			if not d in marea_countries[country_id]['disturbances']:
				marea_countries[country_id]['disturbances'][d] = 0
			marea_countries[country_id]['disturbances'][d] = marea_countries[country_id]['disturbances'][d] + 1


	if 'Grid' in item:
		grid_id = item['Grid']['id']
		grid_label = item['Grid']['label']
		if not grid_id in marea_grids:
			marea_grids[grid_id] = {'id': grid_id, 'label': grid_label, 'disturbances': {}, 'people': {}, 'sites': {}}
		if not site_id in marea_grids[grid_id]['sites']:
			marea_grids[grid_id]['sites'][site_id] = site_label
		for actor in actors:
			actor_id = actor['id']
			if not actor_id in marea_grids[grid_id]['people']:
				marea_grids[grid_id]['people'][actor_id] = actor
		for d in disturbances:
			if not d in marea_grids[grid_id]['disturbances']:
				marea_grids[grid_id]['disturbances'][d] = 0
			marea_grids[grid_id]['disturbances'][d] = marea_grids[grid_id]['disturbances'][d] + 1

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

	page_data = sorted(marea_grids.values(), reverse=True, key=lambda x: len(x['sites']))
	page_data = [{'label': x['label'], 'sites': len(x['sites']), 'people': (', '.join([str(y['label']) for y in x['people'].values()]))}for x in page_data]

	fp.write("```js\n")
	fp.write("\n")
	fp.write("const site_doc_data = " + json.dumps(page_data) + ";\n")
	fp.write("\n")

	fp.write("const grid_sel = view(Inputs.table(site_doc_data, {\n")
	fp.write("        columns: ['label', 'sites', 'people'],\n")
	fp.write("        header: {'label': 'Grid square', 'sites': 'Sites', 'people': 'Researchers'},\n")
	fp.write("        format: {\n")
	fp.write("                'label': (x) => htl.html`<strong>${ x }</strong> <a href=\"${ x }.html\">Detail</a>`,\n")
	fp.write("        },\n")
	fp.write("  }));\n")

	fp.write("\n")
	fp.write("```\n")

	total = 0
	for grid in sorted(marea_grids.values(), reverse=True, key=lambda x: len(x['sites'])):
		total = total + len(grid['sites'])

# {"id": "c4e8738c-c3a5-4aba-a3f5-31f3890150e0",
#  "label": "E34N31-32",
#  "disturbances": {"Clearance (Bulldozing/Levelling)": 1},
#  "people": {
#      "77fef06f-3a14-4bdb-8a0a-59cddb4ff35b": {"id": "77fef06f-3a14-4bdb-8a0a-59cddb4ff35b", "label": "Mohammad Jaradat"},
#      "60097680-0c07-4f91-a076-7a30b390e60f": {"id": "60097680-0c07-4f91-a076-7a30b390e60f", "label": "Georgia Andreou"},
#      "90ae76cf-865d-4e68-971c-c2b2af9be18c": {"id": "90ae76cf-865d-4e68-971c-c2b2af9be18c", "label": "Michael Fradley"}
#  }
# }

	fp.write("## Disturbance Cause Analysis\n\n")

	for countryid, country in marea_countries.items():

		if len(country['disturbances']) == 0:
			continue

# {"id": "4be2c4ce-df4a-4f9d-92e4-7f88c6fa6753", "label": "Egypt", "disturbances": {"Occupation/Continued Use": 1, "Construction": 1, "Clearance (Bulldozing/Levelling)": 1, "Water and/or Wind Action": 1}, "people": {"351b56f1-628c-429c-bbcd-3deec068423c": {"id": "351b56f1-628c-429c-bbcd-3deec068423c", "label": "Julia Nikolaus"}, "c278483d-0c2f-435d-b0b8-bfd1ced3c76c": {"id": "c278483d-0c2f-435d-b0b8-bfd1ced3c76c", "label": "Mohamed Osman"}, "4764f6bd-bc2b-4a60-b095-114fed6158e2": {"id": "4764f6bd-bc2b-4a60-b095-114fed6158e2", "label": "Mohamed Kenawi"}, "89e3c852-f4a4-4372-b5fc-1f13e6667fe8": {"id": "89e3c852-f4a4-4372-b5fc-1f13e6667fe8", "label": "Mohamed Ashmawy"}}, "sites": ["

		fp.write("### " + country['label'] + "\n\n")
		fp.write('Based on reports of ' + str(len(country['sites'])) + ' sites by ' + (', '.join([x['label'] for x in country['people'].values()])) + '\n\n')

		fp.write("#### Threats \n\n")
		fp.write("```mermaid\n")

		x = []
		y = []
		config = {'config': {'theme': 'dark', 'xyChart': {'showDataLabel': True, 'plotReservedSpacePercent': 90}}}
		for d, f in country['disturbances'].items():
			y.append(d)
			x.append(f)
		fp.write('---\n' + yaml.dump(config) + '---\n')
		fp.write("xychart-beta\n")
		fp.write("  x-axis " + json.dumps(y) + "\n")
		fp.write("  y-axis \"Number identified\"\n")
		fp.write("  bar " + json.dumps(x) + "\n")
		fp.write("\n")
		fp.write("```\n\n")

#		fp.write("gantt")
#		fp.write("  todayMarker off\n")
#		fp.write("  dateFormat X\n")
#		fp.write("  axisFormat %\n")
#		fp.write("\n")
#		for d, f in country['disturbances'].items():
#			fp.write("  " + str(d) + " (" + str(f) + ") : 0, " + str(f) + "\n")
#		fp.write("```\n\n")
