import json, csv, os, sys

geometry_id = '7248e0d0-ca96-11ea-a292-02e7594ce0a0'

base_path = os.path.join(os.path.abspath(os.path.dirname(__file__)))
docs_path = os.path.join(base_path, 'docs')
data_path = os.path.join(docs_path, 'data')
static_path = os.path.join(data_path, 'static')
input_file = os.path.join(static_path, 'Grid_Square_2024-07-04_05-28-58.json')
output_file = os.path.join(data_path, 'grid_geometries.json')

with open(input_file, 'r') as fp:
	data = json.load(fp)
if not isinstance(data, dict):
	sys.exit(1)
if not 'business_data' in data:
	sys.exit(1)
if not 'resources' in data['business_data']:
	sys.exit(1)

ret = {}
for item in data['business_data']['resources']:
	id = item['resourceinstance']['resourceinstanceid']
	name = item['resourceinstance']['name'].upper()
	if name in ret:
		continue
	if not '-' in name:
		continue
	geo = None
	for tile in item['tiles']:
		if not 'data' in tile:
			continue
		if not geometry_id in tile['data']:
			continue
		geo = tile['data'][geometry_id]
		break
	if geo is None:
		continue
	ret[name] = geo

with open(output_file, 'w') as fp:
	fp.write(json.dumps(ret))


#{
#   "resourceinstance" : {
#      "descriptors" : {
#         "ar" : {
#            "description" : "Undefined",
#            "map_popup" : "Undefined",
#            "name" : "Undefined"
#         },
#         "en" : {
#            "description" : "E64N37-14",
#            "map_popup" : "E64N37-14",
#            "name" : "E64N37-14"
#         }
#      },
#      "graph_id" : "77d18973-7428-11ea-b4d0-02e7594ce0a0",
#      "graph_publication_id" : "9b8a53dc-6497-11ed-9618-08002727641f",
#      "legacyid" : "cbfe9125-7a8e-4b67-ac5a-ce0c4ad01ca6",
#      "name" : "E64N37-14",
#      "publication_id" : "9b8a53dc-6497-11ed-9618-08002727641f",
#      "resourceinstanceid" : "cbfe9125-7a8e-4b67-ac5a-ce0c4ad01ca6"
#   },
#   "tiles" : [
#      {
#         "data" : {
#            "b3628db0-742d-11ea-b4d0-02e7594ce0a0" : {
#               "en" : {
#                  "direction" : "ltr",
#                  "value" : "E64N37-14"
#               }
#            }
#         },
#         "nodegroup_id" : "b3628db0-742d-11ea-b4d0-02e7594ce0a0",
#         "parenttile_id" : null,
#         "provisionaledits" : null,
#         "resourceinstance_id" : "cbfe9125-7a8e-4b67-ac5a-ce0c4ad01ca6",
#         "sortorder" : 0,
#         "tileid" : "55e0b4f8-3b18-45d2-a692-30376cc4213b"
#      },
#      {
#         "data" : {
#            "7248e0d0-ca96-11ea-a292-02e7594ce0a0" : {
#               "features" : [
#                  {
#                     "geometry" : {
#                        "coordinates" : [
#                           [
#                              [
#                                 64.25,
#                                 37.25
#                              ],
#                              [
#                                 64.25,
#                                 37.5
#                              ],
#                              [
#                                 64.5,
#                                 37.5
#                              ],
#                              [
#                                 64.5,
#                                 37.25
#                              ],
#                              [
#                                 64.25,
#                                 37.25
#                              ]
#                           ]
#                        ],
#                        "type" : "Polygon"
#                     },
#                     "properties" : {
#                        "nodeId" : null
#                     },
#                     "type" : "Feature"
#                  }
#               ],
#               "type" : "FeatureCollection"
#            }
#         },
#         "nodegroup_id" : "7248e0d0-ca96-11ea-a292-02e7594ce0a0",
#         "parenttile_id" : null,
#         "provisionaledits" : null,
#         "resourceinstance_id" : "cbfe9125-7a8e-4b67-ac5a-ce0c4ad01ca6",
#         "sortorder" : 0,
#         "tileid" : "7e1457ee-a182-4b87-8741-e0508a716f36"
#      }
#   ]
#}



