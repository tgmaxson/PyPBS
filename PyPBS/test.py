from qstat import *
from util import *

results = qstat_process(qstat(user="tmaxson")+qstat(user="zeng46"))
zeng = subset(results, lambda x: "zeng46" in x["Owner"]) 
for id in zeng:
    if zeng[id]["State"] == "R":
        continue
    print id, zeng[id]["Name"]
