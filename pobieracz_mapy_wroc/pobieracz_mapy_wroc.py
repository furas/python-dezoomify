#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
import sys
import urllib
import Image
import cStringIO

if ( len(sys.argv) < 3):
  print("""Użycie:
  pobieraczmap nazwa_pliku "adres jednego kafelka"

  formt pliku w jakim zostanie zapisana mapa zależy od końcówki nazwy (rozszerzenia) zalecane .png albo .jpeg
  aby ustalić jakie są X i Y oraz adres w firefoksie naciśnij ctrl+shift+k w operze/chrome ctrl+shift+i
  """)
  exit(0)

nazwa_pliku=sys.argv[1]

start_title=sys.argv[2].split("-")

url_s=start_title[0]+"-"

#print((start_title)
param=start_title[2].split(".")


xs=int(start_title[1])
ys=int(param[0])

zoom=url_s[-2:-1]
print("Zoom: "+zoom

szer=0
x=xs
while (szer==0):
  url=url_s+str(x)+"-"+str(ys)+".jpg"
  print("test_x "+url
  try:
      file = urllib.urlopen(url)
      im = cStringIO.StringIO(file.read())
      img = Image.open(im)
      del img
      del im
  except IOError:
      szer=x
      print("Szerokość "+str(szer)
  x+=1

y=ys
t=0
wys=0

while (wys==0):
  url_t=url_s[0:-4]+str(t)+"/"+zoom+"-"
  url=url_t+str(xs)+"-"+str(y)+".jpg"
  print("test_y "+url
  try:
      file = urllib.urlopen(url)
      im = cStringIO.StringIO(file.read())
      img = Image.open(im)
      del img
      del im
  except IOError:
      y-=1
      t+=1
      if (t>30):
    wys=y
    print("Wysokość "+str(wys)
  y+=1


if (wys*szer>2500):
  print("Uwaga: mapa bardzo duża! Jak nie starczy pamięci spróbuj niższego powiększenia."

mapa = Image.new("RGB", (szer*256,wys*256))


y=0
t=0

while (y<wys-1):
  x=0
  while (x<szer-1):
    try:
      url_t=url_s[0:-4]+str(t)+"/"+zoom+"-"
      url=url_t+str(x)+"-"+str(y)+".jpg"
      print((url)
      file = urllib.urlopen(url)
      im = cStringIO.StringIO(file.read())
      img = Image.open(im)
      mapa.paste(img, (x*256,y*256,(x+1)*256 ,(y+1)*256))
      del img
      del im
    except IOError:
      x-=1
      t+=1
    x+=1
  y+=1

mapa.save(nazwa_pliku)
