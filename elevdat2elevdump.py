#ChrisMiuchiz
#Written for Python 3.6.0
#For use in conjunction with Xaoc elevdump editor to produce elevdumps from elev.dat.
#Xaoc elevdump editor: http://xaoc.50webs.com/terrain/ - will require msstdfmt.dll
#The results of this program will need to be trimmed by 1 block on the west and north, which Xaoc elevdump can do.
#Different trimmed results can be easily combined with a text editor.

def readbytes(contents, address, bytenum):
    result = 0
    i = bytenum-1
    while i >= 0:
        result = result + int(contents[address+i])*256**i
        i -= 1
    return result

def AOBScan(AOB, contents, desiredresult): #Returns address at which the AOB is located.
    resultnumber = 0
    address = 0
    while address <= len(contents)-len(AOB):
        j=0
        while j<len(AOB) and contents[address+j]==AOB[j]:
            j+=1
            if j == len(AOB):
                resultnumber += 1
                if resultnumber == desiredresult:
                    return address
#                print(address)
        address += 1
#    print("AOB scan result",desiredresult,"not found.")
    return -1

def ReadElevDat(contents, page, returntype):
    if returntype == "heights":
        heights = 1
    elif returntype == "textures":
        heights = 0
    else:
        "ReadElevDat was not provided a valid returntype."
        return -1
    #Copied from a really old LUA script for Cheat Engine
    scanAddress = AOBScan([0xFA, 0xFA, 0x0E, 0x80], contents, page)
    if scanAddress==-1:
        return [-1]
    addressStart = scanAddress+0x0000000E
    result = []
    if heights==1:
        addressEnd = addressStart+0x0000FFFF
        addressDiff = addressEnd - addressStart
        i=0
        while i<=addressDiff:
            longInt=readbytes(contents, addressStart+i, 4)
            if longInt>=4294867295 and longInt<=4294967295:
                longInt=longInt-4294967296
            result.append(longInt)
            i += 4
    else:
        addressStartTextures=addressStart+0x00010000
        addressEnd = addressStartTextures+0x00007FFF
        addressDiff = addressEnd - addressStartTextures
        i=0
        while i<=addressDiff:
            result.append(readbytes(contents, addressStartTextures+i, 2))
            i += 2
    return result

#start
try:
    file = open(input("Enter elevdat to convert: "),"rb")
except:
    print("File could not be opened.")
else:
    print("File opened successfully. Reading...")
    try:
        filecontents = file.read()
    except:
        print("Error reading file.")
    else:
        print("File successfully read.")
        file.close()
        page = 1
        EOF = False
        print("Starting to convert file...")
        while not EOF:
            textures = ReadElevDat(filecontents, page, "textures")
            if textures[0]==-1:
                print("End of file reached.")
                EOF = True
            else:
                heights = ReadElevDat(filecontents, page, "heights")
                try:
                    outputfile = open ("convert_elevdump_page"+str(page)+".txt","w")
                except:
                    print("Error opening file convert_elevdump_page"+str(page)+".txt")
                else:
                    outputfile.write("elevdump version 2\n")#Python will interpret \n (0x0A) as \r\n (0x0D, 0x0A), and if that changes, xaoc elevdump editor won't be able to read this.
                    h=0
                    i=0
                    while h<=127:
                        t=0
                        while t<=127:
                           outputfile.write("0 0 " + str(h) + " " + str(t) + " 1 1 1 " + str(textures[i]) + " "+ str(heights[i]) + "\n")
                           t += 1
                           i += 1
                        h += 1
                    outputfile.close()
                    print("Generated file convert_elevdump_page"+str(page)+".txt.")
                page += 1



