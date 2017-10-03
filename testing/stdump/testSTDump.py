
from sttools import STDump

stData = STDump("scatter_log.txt")
stData.readAll()
stData.filterPart("TURN",11)

#print("".join("%s: %s\n" % item for item in vars(stData).items()))
