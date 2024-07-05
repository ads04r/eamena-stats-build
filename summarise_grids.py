import pyexcel, os, json, datetime

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
static_path = os.path.join(data_path, 'static')
geometry_file = os.path.join(data_path, 'grid_geometries.json')
input_file = os.path.join(static_path, 'MarEA_Grid_SquaresProgress_v2.xlsx')
output_file = os.path.join(data_path, 'marea_grid_summaries.json')

def encoder(item):
	if isinstance(item, datetime.datetime):
		return item.strftime("%Y-%m-%d %H:%M:%S")
	if isinstance(item, datetime.date):
		return item.strftime("%Y-%m-%d")
	return str(item)

with open(geometry_file, 'r') as fp:
	geometries = json.load(fp)

book = pyexcel.get_book(file_name=input_file)
sheets = book.to_dict()
ret = {}
for sheet_key in sheets.keys():
	sheet = sheets[sheet_key]
	if len(sheet) == 0:
		continue
	if len(sheet[0]) == 0:
		continue
	if sheet[0][0].lower() != 'grid square':
		continue
	headers = sheet[0]
	for i in range(1, len(sheet)):
		row = sheet[i]
		if len(row) > len(headers):
			continue
		item = {}
		for j in range(0, len(row)):
			item[headers[j].lower().replace(' ', '')] = row[j]
		if not 'gridsquare' in item:
			continue
		id = item['gridsquare'].upper().strip()
		if id == '':
			continue
		item['geometry'] = None
		if id in geometries:
			item['geometry'] = geometries[id]
		ret[id] = item

with open(output_file, 'w') as fp:
	fp.write(json.dumps(ret, indent=4, default=encoder))
