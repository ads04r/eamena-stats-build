from staticmap import StaticMap, Polygon, CircleMarker
import os, json

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
dist_path = os.path.join(base_path, 'dist')
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
static_path = os.path.join(data_path, 'static')
summary_file = os.path.join(data_path, 'marea_grid_summaries.json')
map_file = os.path.join(docs_path, 'map.png')

with open(summary_file, 'r') as fp:
	data = json.load(fp)

m = StaticMap(2000, 1000, url_template="https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png")

complete_status = ['archescomplete', 'complete', 'completed', 'uploaded']
incomplete_status = ['inprogress', 'pinningcomplete', 'pinningcomplete/partlyuploadedtoarches', 'pinneduptothelineofthegebel', 'inprogress2020/21', 'incompletegesurvey;existingpinsuploadedtodb', 'pinninginprogress', 'pinninginprogress2019/20', 'pinningcomplete-bulkuploadsheetcomplete', 'readytoupload', 'gecomplete']

for grid_key in data.keys():
	item = data[grid_key]
	if not 'progress' in item:
		continue
	if not 'uploadstatus' in item:
		continue
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

	status = item['progress'].lower().strip().replace(' ', '')
	upload_status = item['uploadstatus'].lower().strip().replace(' ', '')
	try:
		pinned = int(item["numberofgepins"])
	except:
		pinned = 0
	try:
		uploaded = int(item["pinsinarches"])
	except:
		uploaded = 0

	if status in complete_status:
		polygon = Polygon(coords=coordinates, fill_color='#007F00', outline_color='#000000', simplify=False)
		m.add_polygon(polygon)
		continue

	if status in incomplete_status:
		polygon = Polygon(coords=coordinates, fill_color='#FFFF00', outline_color='#000000', simplify=False)
		m.add_polygon(polygon)
		continue

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
