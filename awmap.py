PAGE_SIZE = 128
CHUNK_SIZE = 8
class Page():
    def __init__(self, height=0, texture=0):
        self.pixels = [[{'height': height, 'texture': texture} for _ in range(PAGE_SIZE)] for _ in range(PAGE_SIZE)] 

class Map():
    def __init__(self):
        self.pages = {}

    def Chunk(self, x,y):
        #print('X:', x, 'Y:', y)
        chunk_size = 8
        chunk = []
        for column in range(x, x+chunk_size):
            chunk.append([])
            for row in range(y, y+chunk_size):
                #print(column, row)
                chunk[-1].append(self.pixels[column][row])
                #print(self.pixels[column][row].height)
        return chunk

    def SetPixel(self, pageCoord, subCoord, height, texture):
        if pageCoord not in self.pages:
            self.pages[pageCoord] = Page()
            
        pixel = self.pages[pageCoord].pixels[subCoord[0]][subCoord[1]]
        pixel['height'] = height
        pixel['texture'] = texture
                
    def GenerateElevdump(self, fileName):
        lines = []

        for pageCoord in sorted(list(self.pages)):
            page = self.pages[pageCoord]
            for x in range(0, PAGE_SIZE, CHUNK_SIZE):
                for y in range(0, PAGE_SIZE, CHUNK_SIZE):
                    heights = []
                    textures = []
                    for chunky in range(8):
                        for chunkx in range(8):
                            heights.append(page.pixels[x + chunkx][y + chunky]['height'])
                            textures.append(page.pixels[x + chunkx][y + chunky]['texture'])

                    if heights == [heights[0]] * len(heights): heights = heights[0:1]
                    if textures == [textures[0]] * len(textures): textures = textures[0:1]
                    lines.append(f"{pageCoord[0]} {pageCoord[1]} {x} {y} 4 {len(textures)} {len(heights)} {' '.join([str(x) for x in textures])} {' '.join([str(x) for x in heights])}")

        data = 'elevdump version 2\n' + '\n'.join(lines) + '\n\n'
        with open(fileName, 'w') as f:
            f.write(data)