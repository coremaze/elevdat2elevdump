from struct import *
from IDX import *
from Page import *

nDat = input("Enter elev.dat: ")
nIdx = nDat[:-3]+'idx'
print(nIdx)

entries = GetEntries(nIdx, nDat)

hDat = open(nDat, 'rb')
cDat = hDat.read()
hDat.close()

HEIGHTS_LEN = 0x10000
HEIGHTS_WIDTH = 4
TEXTURES_LEN = 0x8000
TEXTURES_WIDTH = 2

pages = []
for entry in entries:
    
    if entry.length != 0x1800E:
        continue
    
    p = Page(entry.x, entry.z, [], [])
    pages.append(p)
    
    TerrainStart = entry.address+0x0E
    TexturesStart = TerrainStart + HEIGHTS_LEN

    for i in range(0, HEIGHTS_LEN//HEIGHTS_WIDTH):
        p.heights.append( unpack('i', cDat[ TerrainStart+i*HEIGHTS_WIDTH : TerrainStart+(i+1)*HEIGHTS_WIDTH ])[0] )

    for i in range(0, TEXTURES_LEN//TEXTURES_WIDTH):
        p.textures.append( unpack('H', cDat[ TexturesStart+i*TEXTURES_WIDTH : TexturesStart+(i+1)*TEXTURES_WIDTH ])[0] )

print("%d page(s) found." % len(pages))
hOut = open('convert_elevdump.txt', 'w')
hOut.write("elevdump version 2\n")
pages = sorted(pages, key=lambda x: (x.x, x.z), reverse=False)
for pagenum, p in enumerate(pages):
    for x in range(0, 129):
        for z in range(0, 129):
            i = (x*128 + z)

            #Put empty border on north and east side and let xaoc take it out
            if z == 128 or x == 128:
                hOut.write("%d %d %d %d 1 1 1 0 0\n" % (p.x, p.z, x, z))
                continue

            line = "%d %d %d %d 1 1 1 %d %d\n" % (p.x, p.z, x, z, p.textures[i], p.heights[i])
            hOut.write(line)
    print("%d page(s) complete." % pagenum)

hOut.close()
            

