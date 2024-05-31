import json, datetime, sys

this_year = datetime.datetime.now().year
ret = list(range(2019, this_year))
ret.reverse()

sys.stdout.write(json.dumps(ret))
