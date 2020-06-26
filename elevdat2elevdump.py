from struct import *
from IDX import *
from Page import *
from awmap import Map
import argparse

def ApplyDatabaseToMap(elevdump, databasePath, awtype):
    nIdx = databasePath + '.idx'
    nDat = databasePath + '.dat'
    print(f'Opening {nDat} and {nIdx}')
    entries = GetEntries(nIdx, nDat, awtype)

    with open(nDat, 'rb') as f:
        cDat = f.read()

    pages = []
    #Create a page for every valid entry
    for entry in entries:

        if entry.length < HEIGHTS_LEN+TEXTURES_LEN:
            print("Ignoring entry pointing to %s because its length is %s" % (hex(entry.address), hex(entry.length)))
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

    for p in pages:
        for x in range(128):
            for z in range(128):
                texture = p.textures[x*128 + z]
                height = p.heights[x*128 + z]
                elevdump.SetPixel((p.x, p.z), (x, z), height, texture)


HEIGHTS_LEN = 0x10000
HEIGHTS_WIDTH = 4
TEXTURES_LEN = 0x8000
TEXTURES_WIDTH = 2

parser = argparse.ArgumentParser(description='Converts elev databases to elevdumps.')
parser.add_argument('databases', type=str, help='Paths to databases, separated by the | symbol')
parser.add_argument('output', type=str, help='File to write resulting elevdump to')
parser.add_argument('version', type=int, help='AW version of the databases')
args = parser.parse_args()

databases = args.databases.split('|')
output = args.output
awtype = args.version

if awtype not in range(4, 7):
    print("Unfamiliar AW version.")
    quit()

elevdump = Map()

for database in databases:
    ApplyDatabaseToMap(elevdump, database, awtype)

elevdump.GenerateElevdump(output)
