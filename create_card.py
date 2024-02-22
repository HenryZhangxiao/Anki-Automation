import json
import pprint

f = open("test-1.json", encoding='utf8')
f_loaded = json.load(f)

pprint.pprint(f_loaded['card-info'][0])
pprint.pprint(f_loaded['card-info'][1])

