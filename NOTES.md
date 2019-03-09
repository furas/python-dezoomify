# dezoomify.py


## Polish Python Coder Group (in Polish language)

[Old thread (2014/2015) about downloading maps](https://pl.python.org/forum/index.php?topic=5073.msg21512)

Script [pobieracz_mapy_wroc.py](https://sites.google.com/site/marekdrwota/pobieracz_mapy_wroc.py)

Links to maps:

- [http://www.bu.uni.wroc.pl/ozk/?lang=pl](http://www.bu.uni.wroc.pl/ozk/?lang=pl)

- [http://dk.bu.uni.wroc.pl/cymelia/showPicture.htm?docId=8200036650&shortTilesPath=/0/03/036/0369/03690/03690015.jpg](http://dk.bu.uni.wroc.pl/cymelia/showPicture.htm?docId=8200036650&shortTilesPath=/0/03/036/0369/03690/03690015.jpg)

- [http://dk.bu.uni.wroc.pl/midas/manu/tiles//0/03/036/0369/03690/03690015/TileGroup8/6-40-22.jpg](http://dk.bu.uni.wroc.pl/midas/manu/tiles//0/03/036/0369/03690/03690015/TileGroup8/6-40-22.jpg)


Using dezoomify:

- [https://sourceforge.net/projects/dezoomify/](https://sourceforge.net/projects/dezoomify/) (dezoomify-1.4.tar.gz) (2016)
- [https://github.com/valgur/dezoomify](https://github.com/valgur/dezoomify) (dezoomify-master.zip) (2016)

```
dezoomify.py -b 'http://dk.bu.uni.wroc.pl/midas/manu/tiles//0/03/036/0369/03690/03690015/ImageProperties.xml' output.jpg
```



## New maps (2019):

Zoomify:

- [http://fbc.pionier.net.pl/id/oai:kpbc.umk.pl:21499](http://fbc.pionier.net.pl/id/oai:kpbc.umk.pl:21499)
- [http://bc.biblio.olesnica.pl/dlibra/docmetadata?id=70](http://bc.biblio.olesnica.pl/dlibra/docmetadata?id=70)

krpano:


### [http://fbc.pionier.net.pl/id/oai:kpbc.umk.pl:21499](http://fbc.pionier.net.pl/id/oai:kpbc.umk.pl:21499)

After digging in HTML/HTTP (using DevTools in Firefox) I found url to `ImageProperties.xml`

```
http://kpbc.umk.pl/norestr/mapy/M_4772/files/ImageProperties.xml
```

which works with old dezoomify (using `-b`).

```bash
dezoomify.py -b 'http://kpbc.umk.pl/norestr/mapy/M_4772/files/ImageProperties.xml' output.jpg
```

Sometimes it have problem with timeout

```
urllib.error.URLError: <urlopen error [Errno 110] Connection timed out>
```

but it works with less threads ie. one thread `-t 1`

```bash
dezoomify.py -t 1 -b 'http://kpbc.umk.pl/norestr/mapy/M_4772/files/ImageProperties.xml' mapa-1.jpg
```


### [http://bc.biblio.olesnica.pl/dlibra/docmetadata?id=70](http://bc.biblio.olesnica.pl/dlibra/docmetadata?id=70)

After digging in HTML/HTTP (using DevTools in Firefox) I found url to `ImageProperties.xml`

```
http://bc.biblio.olesnica.pl/Content/70/scan425_kreis_oels/ImageProperties.xml?noCacheSfx=1551659522092
```

and after skiping `?noCacheSfx=1551659522092` it works with old dezoomify (using `-b`).

```
dezoomify.py -t 1 -s -b 'http://bc.biblio.olesnica.pl/Content/70/scan425_kreis_oels/ImageProperties.xml' output.jpg
```

### Info for old dezoomify

[https://sourceforge.net/p/dezoomify/wiki/Troubleshooting/](https://sourceforge.net/p/dezoomify/wiki/Troubleshooting/)


# On-line dezoomify (JavaScript):

It can download `zoomify`, `krpano` and many other

- [http://ophir.alwaysdata.net/dezoomify/dezoomify.html](http://ophir.alwaysdata.net/dezoomify/dezoomify.html)
- mirror: [http://jk.g6.cz/dezoomify.html](http://jk.g6.cz/dezoomify.html)
- older: [http://jk.g6.cz/archiv/dezoomify.html](http://jk.g6.cz/archiv/dezoomify.html)
- GitHub: [https://github.com/lovasoa/dezoomify](https://github.com/lovasoa/dezoomify)
