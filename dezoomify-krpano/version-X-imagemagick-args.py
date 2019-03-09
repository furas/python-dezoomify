import argparse
import os
import sys
import urllib.request

def download(url_base, level, rows, cols, folder=''):
    """Ściąganie kafelek"""

    for row in range(1, rows+1):
        for col in range(1, cols+1):
            url_name = f'l{level}/{row:02}/l{level}_{row:02}_{col:02}.jpg'
            filename = f'{row:02}_{col:02}.jpg'
            filename = os.path.join(folder, filename)

            print(url_name, '->', filename)
            urllib.request.urlretrieve(url_base + url_name, filename)


def merge(rows, folder=''):
    """Sklejanie za pomocą ImageMagic"""

    file_input  = os.path.join(folder, '{row:02}_*.jpg')
    file_output = os.path.join(folder, 'row_{row:02}.jpg')
    template_row = f'convert +append {file_input} {file_output}'

    for row in range(1, rows+1):
        filename = file_output.format(row=row)

        print(filename)
        os.system(template_row.format(row=row))

    file_input  = os.path.join(folder, 'row_*.jpg')
    #file_output = os.path.join(folder, 'mapa.jpg')
    file_output = 'mapa.jpg'
    template_col = f'convert -append {file_input} {file_output}'

    print(file_output)
    os.system(template_col)
    os.system(f'rm {file_input}')

def get_tiles_base_url(url):
    if url.endswith('/'):
        url = url[:-1]
    parts = url.rsplit('/', 1)
    url += '/{}.tiles/'.format(parts[-1])

    return url

def find_xml(url):
    r = urllib.request.urlopen(url).read().decode()

    start = r.find('xml:"') + 5
    end = r.find('.xml"', start) + 4

    return r[start:end]


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='Url to page with krpano Panorama Viewer')
    parser.add_argument('-f', '--folder', help='folder for tiles')
    parser.add_argument('-m', '--merge', action='store_true', default=False, help='folder for tiles')
    parser.add_argument('-D', '--debug', action='store_true', default=False, help='Url to page with krpano Panorama Viewer')

    args = parser.parse_args()

    url = args.url
    #url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/sztabowa_Kreis_Oels/index.html'
    if args.debug:
        print('url      :', url)

    base_url = url
    if base_url.endswith('index.html'):
        base_url = base_url[:-len('index.html')]
    if args.debug:
        print('base_url :', base_url)

    xml_url = base_url + find_xml(url)
    if args.debug:
        print('xml_url  :', xml_url)

    # adres kafelkow powinien być raczej pobrany z pliku .xml
    tiles_url = get_tiles_base_url(base_url)
    if args.debug:
        print('tiles_url:', tiles_url)

    #tiles_url = 'http://olesnica.nienaltowski.net/Mapy_powiatu/sztabowa_Kreis_Oels/sztabowa_Kreis_Oels.tiles/'

    if args.folder:
        os.makedirs(args.folder, exist_ok=True)

    level = 4
    rows = 7
    cols = 9

    if not args.merge:
        download(tiles_url, level, rows, cols, args.folder)

    merge(rows, args.folder)
