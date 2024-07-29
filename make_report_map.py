from staticmap import StaticMap, Polygon, CircleMarker
import os, json, sys

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
dist_path = os.path.join(base_path, 'dist')
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
static_path = os.path.join(data_path, 'static')
summary_file = os.path.join(data_path, 'marea_grid_summaries.json')
map_file = os.path.join(docs_path, 'map_report.png')
grids_file = os.path.join(data_path, 'marea_grids_phase1_report.csv')

completed = []
with open(summary_file, 'r') as fp:
	data = json.load(fp)
with open(grids_file, 'r') as fp:
	for l in fp.readlines():
		grid_id = l.strip()
		if len(grid_id) == 0:
			continue
		completed.append(grid_id)

m = StaticMap(2000, 1000, url_template="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")
complete_status = ['archescomplete', 'complete', 'completed', 'uploaded', 'pinningcomplete', 'pinningcomplete/partlyuploadedtoarches', 'readytoupload', 'gecomplete']
incomplete_status = ['inprogress', 'pinneduptothelineofthegebel', 'inprogress2020/21', 'incompletegesurvey;existingpinsuploadedtodb', 'pinninginprogress', 'pinninginprogress2019/20', 'pinningcomplete-bulkuploadsheetcomplete']

for grid_key in data.keys():
	item = data[grid_key]
	if not 'geometry' in item:
		continue
	if item['geometry'] is None:
		continue
	if not 'features' in item['geometry']:
		continue
	try:
		coordinates = item['geometry']['features'][0]['geometry']['coordinates'][0]
	except:
		coordinates = []

	if not(item['gridsquare'] in completed):
		if 'progress' in item:
			status = item['progress'].lower().strip().replace(' ', '')
			if status in complete_status:
				polygon = Polygon(coords=coordinates, fill_color='#007F00', outline_color='#000000', simplify=False)
				m.add_polygon(polygon)
		continue

	polygon = Polygon(coords=coordinates, fill_color='#007F00', outline_color='#000000', simplify=False)
	m.add_polygon(polygon)

image = m.render(zoom=5)
image.save(map_file)

# ['archescomplete', 'inprogress', '', 'pinningcomplete', 'pinningcomplete/partlyuploadedtoarches', 'complete', 'completed', 'progress', 'pinneduptothelineofthegebel', 'uploaded', 'inprogress2020/21', 'incompletegesurvey;existingpinsuploadedtodb', 'pinninginprogress', 'pinninginprogress2019/20', 'pinningcomplete-bulkuploadsheetcomplete', 'readytoupload', 'gecomplete', 'n/a']
# ['uploaded', 'notreadyforbulkupload', '', 'n/a', 'inprogress', 'readyforbulkupload']

#    "E34N29-24": {
#        "gridsquare": "E34N29-24",
#        "person": "ST; HH",
#        "progress": "Arches Complete",
#        "numberofgepins": 13,
#        "pinsinarches": "",
#        "datepinningcompleted": 2021,
#        "inbulkuploadform": "",
#        "fullrecordsinarches": 13,
#        "datearchesrecordscompleted": 2021,
#        "personcompletingrecords": "ST (Jordan); HH (KSA)",
#        "notes": "completed; Jordan part was documented by ST in 2019, Saudi part by HH in 2021",
#        "country": "Jordan/Saudi Arabia",
#        "progresssummarycategory": "Complete/fully assessed",
#        "progressyearassessment/pinningcompleted": 2021,
#        "progresssummarynotes": "Added to sheet in 2021",
#        "uploadstatus": "Uploaded",
#        "geometry": {
#            "features": [
#                {
#                    "geometry": {
#                        "coordinates": [
#                            [
