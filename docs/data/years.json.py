import json, datetime, sys

#this_year = datetime.datetime.now().year
ret = list(range(2019, 2025))
ret.reverse()

sys.stdout.write(json.dumps(ret))
