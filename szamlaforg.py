#!/usr/bin/python
# -*- coding: utf-8 -*-
#-----------------------------
# szamlaforg.py v0.1
# OTP számlaforgalom előzmények sqlite3 adatbázisba emelése
# Szoke, Sandor (mail@szokesandor.hu), 2019.01.01
# importer module
#
# Történet:
#  2019.01.01: létrehozás
#-----------------------------
from bs4 import BeautifulSoup
import unicodedata
import sqlite3 as sql3
import glob
#-----------------------------
SQL_FILE=u"szamla.db"
#-----------------------------
class szamla:
  def __init__(self,  name = None):
    if name is None:
      self.sqlite3_db_file = SQL_FILE
    else:
      self.sqlite3_db_file = name
  #----------
  def dict_factory(self, cursor, row):
      d = {}
      for idx, col in enumerate(cursor.description):
          d[col[0]] = row[idx]
      return d
  #---------- https://docs.python.org/dev/library/sqlite3.html#sqlite3.Connection.row_factory
  def SQL_connect(self):
    try:
      self.db = sql3.connect(self.sqlite3_db_file, detect_types=sql3.PARSE_DECLTYPES)
      #db.row_factory = sql3.Row     # Row factory
      self.db.row_factory = self.dict_factory
      self.cursor = self.db.cursor()
    except Exception as e:
      print e
  #----------
  def load_file(self,fajlnev):
    with open(fajlnev) as file:  
      page = file.read() 

    soup = BeautifulSoup(page, 'html.parser')

    # szűrés eredménytáblára
    table = soup.find('table', attrs={'class':'eredmenytabla'})

    #-----------------------------
    # letrehozza a fejlécet
    head = []
    table_head = table.find('thead')
    rows_head = table_head.find_all('th')
    for row in rows_head:
      col = unicodedata.normalize("NFKD", row.get_text()).strip()
      head.append(col)

    #-----------------------------
    # léterhozza az egyes rekordokat, listában
    data = []
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        # kiveszi a \xa0 karaktereket
        cols = [unicodedata.normalize("NFKD", ele.text.strip()) for ele in cols]
        data.append(cols)
    return head,data
#-----------------------------
# SQL tábla:
#
# forgalom típusa
# könyvelési dátum
# értéknap
# összeg
# új könyvelt egyenleg
# ellenoldali számlaszám
# ellenoldali név
# közlemény
# (banki tranzakció azonosító) -- nincs használva mert 2012-ben még nem létezett
  def SQL_create_table(self,):
    sql = """DROP TABLE IF EXISTS `szamlaforgalom`;"""
    try:
      self.cursor.execute(sql)
      #print "SQL:" + sql
    except Exception as e:
      print "failed drop of szamlaforgalom table: " + str(e)

    sql = """CREATE TABLE `szamlaforgalom` (
      `forgalom_tipusa`	TEXT NOT NULL,
      `konyvelesi_datum`	DATE NOT NULL,
      `erteknap`	DATE NOT NULL,
      `osszeg`	REAL NOT NULL,
      `konyvelt_egyenleg`	REAL,
      `ellenoldali_szamlaszam`	TEXT,
      `ellenoldali_nev`	TEXT,
      `kozlemeny`	TEXT,
      `banki_tranzakcio_azonosito`	TEXT
    );"""
    try:
      self.cursor.execute(sql)
      #print "SQL:" + sql
    except Exception as e:
      print "failed create of szamlaforgalom table: " + str(e)
  #-----------------------------
  # FIXME: van pár olyan forgalom típusa, ahol van előtte pár azonosító amit tisztítani kell
  def SQL_insert(self,rekordok):
    for i in rekordok:
      try:
        #variables = (i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]) # (banki tranzakció azonosító)-val
        variables = (i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8])
      except Exception as e:
          print len(i), i
      try:
        #sql = u'''INSERT INTO szamlaforgalom (forgalom_tipusa, konyvelesi_datum, erteknap,osszeg, konyvelt_egyenleg, ellenoldali_szamlaszam, ellenoldali_nev, kozlemeny, banki_tranzakcio_azonosito) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");''' % (i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9]) # (banki tranzakció azonosító)-val
        sql = u'''INSERT INTO szamlaforgalom (forgalom_tipusa, konyvelesi_datum, erteknap,osszeg, konyvelt_egyenleg, ellenoldali_szamlaszam, ellenoldali_nev, kozlemeny) VALUES (?, ?, ?, ?, ?, ?, ?, ?);'''
        #print sql
        self.cursor.execute(sql, variables)
      except Exception as e:
        print "SQL insert Error: " + str(e) + sql + str(variables)
        print i
    try:
      self.db.commit() # minden egyes fájl után kiírjuk az adatbázist
    except Exception as e:
      self.db.rollback()
      print "SQL insert Error: " + str(e)
  #-----------------------------
  # Hasznos SQL lekérdezések
  #
  # : forgalom típusainak lekérdezése
  #  select distinct(forgalom_tipusa) from szamlaforgalom
  #
#----------
if __name__ == '__main__':
  print "OTP számlaforgalom előzmények (xls) beemelése sqlite3 adatbázisba v0.1 - (C) 2019 Szőke, Sándor mail@szokesandor.hu"
  OTP = szamla()
  OTP.SQL_connect()
  OTP.SQL_create_table()

  fajlok = glob.glob("xls/*.xls")
  for fajl in fajlok:
    header,rekordok = OTP.load_file(fajl)
    OTP.SQL_insert(rekordok)
    print "* " + fajl + " feldolgozva"
    

  
