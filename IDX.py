from struct import *
class Entry():
    def __init__(s, data1, x, z, address, loc, length):
        s.data1 = data1 # 2 bytes
        s.x = x # 2 bytes int
        s.z = z # 2 bytes int
        s.address = address # 4 bytes int
        s.location = loc
        s.length = length
    def Details(s):
        print("Address: %s\nX, Z: %s, %s\ndata1: %s\nLocation: %s\n" % (hex(s.address),s.x,s.z,s.data1,hex(s.location)))

def GetEntries(nIdx, nDat):
    #read idx file
    hIdx = open(nIdx, 'rb')
    cIdx = hIdx.read()
    hIdx.close()

    hDat = open(nDat, 'rb')
    cDat = hDat.read()
    hDat.close()

    #Parse IDX header
    (IDXLength, #0
     IDXunk1, #4
     IDXEnd, #8
     IDXunk2, #C
     IDXunk3, #10
     IDXunk4, #14
     IDXunk5, #18
     IDXunk6, #1C
     IDXunk7, #20
     IDXunk8, #24
     IDXunk9, #28
     IDXunk10, #2C
     IDXunk11, #30
     IDXunk12, #34
     IDXunk13, #38
     IDXunk14, #3C  
     IDXunk15, #40
     IDXunk16, #44
     IDXStart, #48
     IDXunk18, #4C
     IDXunk19, #50
     IDXunk20, #54
     IDXunk21, #58
     IDXunk22, #5C
     IDXunk23, #60
     IDXunk24, #64
     IDXunk25, #68
     IDXunk26, #6C
     IDXunk27, #70
     IDXunk28, #74
     IDXunk29, #78
     IDXunk30 #7C
    ) = unpack('IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII', cIdx[0:0x80])

    lstentries = []

    IDX_OFFSET = 0x12

    ENTRY_LENTGTH = 0x0C

    BlockStart = IDXStart


    #Loop at least once, and stop when next block is at 0 (end of index)
    while True:
        forward, backward, entries, entrieslength = unpack('<IIHH', cIdx[BlockStart:BlockStart+12])
        loc = BlockStart + IDX_OFFSET
        print("Reading %s index entries from index block %s" % (entries, hex(BlockStart)))

        #Get entries until entry limit
        for entrycount in range(0, entries):
            address, data1, data2, data3, data4, data5, data6, data7, data8 = unpack("Ibbbbbbbb", cIdx[loc:loc+ENTRY_LENTGTH])
##            for x in [address, data1, data2, data3, data4, data5, data6, data7, data8]:
##                print(hex(x), end=' ')
##            print()
            length = unpack('I', cDat[address+2:address+6])[0]
            x, z = data1, data5

            #Entries whose data length are 0x0E contain no data
            if length != 0x0E:
                lstentries.append( Entry(data1, x, z, address, loc, length) )

            #Each index entry is 10 bytes long
            loc += ENTRY_LENTGTH

        if forward == 0x00000000:
            break
        
        BlockStart = forward

    return lstentries
