import os
import urllib.request

#-----------------------------------------------------------------------

#url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/sztabowa_Kreis_Oels/index.html'

#tiles_url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/sztabowa_Kreis_Oels/sztabowa_Kreis_Oels.tiles/'
#level = 4
#rows = 7
#cols = 9

tiles_url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/KreisOels/KreisOels.tiles/'
level = 5
rows = 8
cols = 9

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
# sklejanie za pomocą zewnętrznego pogramu `ImageMagick`
#-----------------------------------------------------------------------

# sklejanie kafalek w wiersze (plus w +append)
for row in range(1, rows+1):
    print(f'sklejanie: tiles/l{level}_{row:02}_*.jpg -> tiles/row_{row:02}.jpg')
    os.system(f'convert +append tiles/l{level}_{row:02}_*.jpg tiles/row_{row:02}.jpg')

# sklejanie wierszy w kolumnę (minus w -append)
print('sklejanie: tiles/row_*.jpg -> mapa.jpg')
os.system(f'convert -append tiles/row_*.jpg mapa.jpg')
