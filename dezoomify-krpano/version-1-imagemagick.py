import os
import urllib.request

#-----------------------------------------------------------------------

#url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/sztabowa_Kreis_Oels/index.html'
tiles_url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/sztabowa_Kreis_Oels/sztabowa_Kreis_Oels.tiles/'

# stworzenie podkatalogu jeśli jeszcze nie istnieje

os.makedirs('tiles', exist_ok=True)

#-----------------------------------------------------------------------
# ściąganie kafelek
#-----------------------------------------------------------------------

for row in range(1, 8):
    for col in range(1, 10):
        url_name = f'l4/{row:02}/l4_{row:02}_{col:02}.jpg'
        filename = f'tiles/l4_{row:02}_{col:02}.jpg'

        print('ściąganie:', url_name, '->', filename)
        urllib.request.urlretrieve(tiles_url + url_name, filename)

#-----------------------------------------------------------------------
# sklejanie za pomocą zewnętrznego pogramu `ImageMagick`
#-----------------------------------------------------------------------

# sklejanie kafalek w wiersze (plus w +append)
for row in range(1, 8):
    print(f'sklejanie: tiles/l4_{row:02}_*.jpg -> tiles/row_{row:02}.jpg')
    os.system(f'convert +append tiles/l4_{row:02}_*.jpg tiles/row_{row:02}.jpg')

# sklejanie wierszy w kolumnę (minus w -append)
print('sklejanie: tiles/row_*.jpg -> mapa.jpg')
os.system(f'convert -append tiles/row_*.jpg mapa.jpg')
