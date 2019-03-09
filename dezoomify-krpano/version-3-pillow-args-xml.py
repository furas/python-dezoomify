import os
import glob
import urllib.request
from PIL import Image
import math
import argparse
#-----------------------------------------------------------------------

class MyArgumentParser(argparse.ArgumentParser):
    def error(self, error):
        print('error:', error)
        print('')
        self.print_help()
        exit(2)

parser = MyArgumentParser('script.py')
parser.add_argument('url',
    help='url to map zoommed with krpano')
parser.add_argument('file', default='map.jpg',
    help='filename for map (default: map.jpg)')
parser.add_argument('-f', '--folder', default='tiles',
    help='local folder for tiles')
parser.add_argument('-m', '--merge', action='store_true',
    help='merge tiles without downloading [not ready]')
parser.add_argument('-D', '--debug', action='store_true',
    help='display more messages')

args = parser.parse_args()

#-----------------------------------------------------------------------

# usunięcie starych plików

import shutil

shutil.rmtree(f'{args.folder}', ignore_errors=True)

# stworzenie podkatalogu jeśli jeszcze nie istnieje

os.makedirs(f'{args.folder}', exist_ok=True)

#-----------------------------------------------------------------------

#TODO: pobrać nazwę pliku .xml z index.html

# usunięcie 'index.html' lub dodanie końcowego '/'

base_url = args.url
if base_url.endswith('/index.html'):
    base_url = base_url[:-10]
elif base_url[-1] != '/':
    base_url += '/'
print(' base_url:', base_url)

# url do kafelek

parts = base_url.rsplit('/', 2)
tiles_url = base_url + parts[-2] + '.tiles/'
print('tiles_url:', tiles_url)
#tiles_url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/KreisOels/KreisOels.tiles/'

# url do .xml i jego pobranie

xml_name = parts[-2] + '.xml'
xml_url =  base_url + xml_name
print('  xml_url:', xml_url)
urllib.request.urlretrieve(base_url + xml_name, f'{args.folder}/{xml_name}')

# wczytanie .xml i wydobycie wielkosci obrazki, level, rows, colsimport lxml.etree

#import lxml.etree
#data = open('tiles/' + xml_name).read()
#tree = lxml.etree.fromstring(data)
#root = tree.getroottree()

import xml.etree.ElementTree as ET
tree = ET.parse(f'{args.folder}/{xml_name}')

tile_size = int(tree.find('.//image').attrib['tilesize'])
print('tile_size:', tile_size)

levels = tree.findall('.//level')
level = len(levels)
print('    level:', level)

image_width = int(levels[0].attrib['tiledimagewidth'])
image_height = int(levels[0].attrib['tiledimageheight'])
print('    width:', image_width)
print('   height:', image_height)

rows = math.ceil(image_height/tile_size)
cols = math.ceil(image_width/tile_size)
print('rows cols:', rows, cols)

#TODO: pobrać z .xml szablon nazwy plików - url="KreisOels.tiles/l5/%0v/l5_%0v_%0h.jpg"

#-----------------------------------------------------------------------
# ściąganie kafelek
#-----------------------------------------------------------------------

for row in range(1, rows+1):
    for col in range(1, cols+1):
        url_name = f'l{level}/{row:02}/l{level}_{row:02}_{col:02}.jpg'
        filename = f'{args.folder}/l{level}_{row:02}_{col:02}.jpg'

        print('ściąganie:', url_name, '->', filename)
        urllib.request.urlretrieve(tiles_url + url_name, filename)

#-----------------------------------------------------------------------
# sklejanie za pomocą `PIL/Pillow` (i z wykorzystaniem `glob`)
#-----------------------------------------------------------------------

def merge(filenames, output='output.jpg', in_row=True):
    """Łączenie plików w wiersz (in_row=True) lub kolumnę (in_row=False)"""

    # wczytanie wszystkich plików
    images = [Image.open(name) for name in filenames]

    # pobranie rozmiarów wszystkich obrazków
    sizes_x, sizes_y = zip(*[img.size for img in images])

    # wyliczenie docelowych wymiarów wiersza lub kolumny
    if in_row:
        full_size_x = sum(sizes_x)
        full_size_y = max(sizes_y)
    else:
        full_size_y = sum(sizes_y)
        full_size_x = max(sizes_x)

    #print('rozmiar:', full_size_x, full_size_y)

    # stworzenie pustego obrazka o docelowym wymiarze
    full_img = Image.new('RGB', (full_size_x, full_size_y))

    # wklejanie obrazków z odpowiednim przesunięciem

    offset_x = 0
    offset_y = 0

    for img in images:

        full_img.paste(img, (offset_x, offset_y))

        if in_row:
            # przesunięcie o szerokość wklejonego obrazka
            offset_x += img.size[0]
        else:
            # przesunięcie o wysokość wklejonego obrazka
            offset_y += img.size[1]

    # zapisanie docelowego obrazka
    if output:
        full_img.save(output)

    #return full_img

#-----

# sklejanie kafelek w wiersze

for row in range(1, rows+1):
    print(f'sklejanie: {args.folder}/l{level}_{row:02}_*.jpg -> {args.folder}/row_{row:02}.jpg')
    #filenames = [f'{args.folder}/l{level}_{row:02}_{col:02}.jpg' for col in range(1, cols+1)]
    filenames = sorted(glob.glob(f'{args.folder}/l{level}_{row:02}_*.jpg'))
    merge(filenames, f'{args.folder}/row_{row:02}.jpg')

# sklejanie wierszy w całość

print(f'sklejanie: {args.folder}/row_*.jpg -> map.jpg')
#filenames = [f'{args.folder}/pillow_row_{row:02}.jpg' for row in range(1, rows+1)]
filenames = sorted(glob.glob(f'{args.folder}/row_*.jpg'))
merge(filenames, f'{args.file}', in_row=False)
