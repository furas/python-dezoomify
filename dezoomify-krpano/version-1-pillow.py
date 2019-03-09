import os
import glob
import urllib.request
from PIL import Image

#-----------------------------------------------------------------------

#url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/sztabowa_Kreis_Oels/index.html'

#tiles_url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/sztabowa_Kreis_Oels/sztabowa_Kreis_Oels.tiles/'
#level = 4
#rows  = 7
#cols  = 9

tiles_url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/KreisOels/KreisOels.tiles/'
level = 5
rows  = 8
cols  = 9

# stworzenie podkatalogu jeśli jeszcze nie istnieje

os.makedirs('tiles', exist_ok=True)

#-----------------------------------------------------------------------
# ściąganie kafelek
#-----------------------------------------------------------------------

for row in range(1, rows+1):
    for col in range(1, cols+1):
        url_name = f'l{level}/{row:02}/l{level}_{row:02}_{col:02}.jpg'
        filename = f'tiles/l{level}_{row:02}_{col:02}.jpg'

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
    print(f'sklejanie: tiles/l{level}_{row:02}_*.jpg -> tiles/row_{row:02}.jpg')
    #filenames = [f'tiles/l4_{row:02}_{col:02}.jpg' for col in range(1, cols+1)]
    filenames = sorted(glob.glob(f'tiles/l{level}_{row:02}_*.jpg'))
    merge(filenames, f'tiles/row_{row:02}.jpg')

# sklejanie wierszy w całość

print('sklejanie: tiles/row_*.jpg -> map.jpg')
#filenames = [f'tiles/pillow_row_{row:02}.jpg' for row in range(1, rows+1)]
filenames = sorted(glob.glob('tiles/row_*.jpg'))
merge(filenames, 'mapa.jpg', in_row=False)
