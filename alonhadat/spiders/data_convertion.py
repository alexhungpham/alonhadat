import glob
import pandas as pd
import json
import datetime
from datetime import date
import re

recorddate = str(date.today())
files = "./../alonhadat-tradings_"+recorddate+".json"
with open("./../alonhadat-tradings_"+recorddate+".json", encoding='utf-8') as data :
    table = pd.read_json(data)
    
#mylink = table['link']
#postid = (re.split('[/,.-]', mylink))
#table['id'] = postid[len(postid)-2]

for x in table['postdate']:
    result = x.replace("Hôm nay", str(date.today()))
table['postdate'] = result
for x in table['postdate']:
    result2 = x.replace("Hôm qua",str(date.today()-datetime.timedelta(days=1)))
table['postdate'] = result2
table['postdate']

table.to_json(files)