#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Python Beispiele zu
# http://www.thomas-guettler.de/vortraege/python/einfuehrung.html
#
# (c) 2003-2012 Thomas Güttler
# http://www.thomas-guettler.de/
#


# Beispiel ZINSEN:
# Ein Versicherungsvertreter verspricht dir, dass du einen großen
# Betrag bekommst, wenn du 35 Jahre jährlich 900 Euro einzahlst. Du
# willst nun wissen, wieviel Geld du hättest, wenn du keine
# Rentenversicherung abschließt, sondern das Geld mit 5 Prozent
# Zinsen anlegst. Vielleicht gibt es dafür eine Formel, aber iterativ
# (in einer Schleife) lässt sich das auch leicht berechnen.

sum=0
for i in range(35):
    sum*=1.05 # 5 Prozent Zinsen
    sum+=900
    print 'Jahr %s Betrag: %s' % (i+1, sum)


#---------------------------------------------------------------------
#Beispiel FIFO:
#FIFO (first in first out) (Queue)
#Vergleich: Autobahntunnel
#
l=[] # Nehme eine leere Liste
for i in range(10):
    l.append(i)    # An Liste anhängen
print l
while l: # Solange 'l' nicht leer ist ...
    print l.pop(0) # Entferne erstes Element der Liste

#Ergebnis: 0, 1, 2, ...


#---------------------------------------------------------------------
#Beispiel FILO:
#FILO (first in last out) (Stack)
#Vergleich: Stapel von Münzen
#
l=[]
for i in range(10):
    l.append(i)
while l:
    print l.pop() # Entferne letztes Element der Liste

#Ergebnis: 9, 8, 7, ...

#---------------------------------------------------------------------
#Beispiel ZÄHLEN
for i, wort in enumerate(['null', 'eins', 'zwei']):
    print i, wort # 0 null, 1 eins, ....

#---------------------------------------------------------------------
#Beispiel ENDE:
#Das dicke Ende
#
file='foo.jpg'
if file[-4:]=='.jpg':     #unschön
    print 'Foto'
if file.endswith('.jpg'): #besser, analog 'startswith()'
    print 'Foto'


#---------------------------------------------------------------------
#Beispiel DIE WAHRHEIT:
#Was ist wahr und was ist falsch?
#Folgende Bedingungen sind wahr:
#
if True:
    print 'wahr'
if 1:
    print 'wahr'
if -1:      # Alle Zahlen außer 0 sind wahr
    print 'wahr'
if '0':     # Nichtleere Zeichenkette
    print 'wahr'
if 'False': # Nichtleere Zeichenkette
    print 'wahr'
if [[]]:    # Nichtleere Liste
    print 'wahr'

if not False:
    print 'wahr'
if not 0:
    print 'wahr'
if not []: # Leere Liste
    print 'wahr'
if not {}: # Leeres Dictionary
    print 'wahr'
if not '': # Leere Zeichenkette
    print 'wahr'
if not None:
    print 'wahr'
if not bool('0'):
    print 'wahr'
if True and True:
    print 'wahr'
if False or True:
    print 'wahr'

#---------------------------------------------------------------------
#Beispiel REFERENZ:
#Referenz vs. Kopie
#
list1=[1, 2, 3, 4]
list2=list1 # Zwei Referenzen zeigen auf eine Liste
list2[0]=5
print list1==list2 # --> 1

list1=[1, 2, 3, 4]
list2=list1[:] # Erstelle eine Kopie der ersten Liste
list2[0]=5
print list1==list2 # --> 0


#---------------------------------------------------------------------
#Beispiel UNIQUE a:
#Doppelte Einträge aus einer Liste entfernen:
mylist=[1, 1, 7, 7, 7, 6, 2, 3, 4, 4, 4, 5]
unique={} # dictionary
for item in mylist: 
    unique[item]=1
mylist=unique.keys()
mylist.sort()
print mylist # --> [1, 2, 3, 4, 5, 6, 7]

#Beispiel UNIQUE b:
#Besser mit set (Menge)
mylist=[1, 1, 7, 7, 7, 6, 2, 3, 4, 4, 4, 5]
myset=set(mylist)
mylist=list(myset)
mylist.sort()
print mylist # --> [1, 2, 3, 4, 5, 6, 7]


#---------------------------------------------------------------------
#Beispiel SORTDICT:
#Ein Dictionary sortieren.
#Da Dictionaries nicht sortiert gespeichert werden,
#will man sie für die Ausgabe ggf. sortieren:
mydict={'a': ['Auto', 'Ampel'],
        'b': ['Bus', 'Banane'],
        'c': ['Chemnitz', 'Chaos'],
        'd': ['Dame', 'Diesel'],
        'e': ['Esel']}
print 'Unsortiert:', mydict
for buchstabe, woerter in sorted(mydict.items()):
    print '%s: %s' % (buchstabe, woerter)


#---------------------------------------------------------------------
#Beispiel SORTITEMS a:
#Sortieren einer Liste von Paaren.
#Die Einträge bestehen aus einer ID und einem Namen.
#Die Liste soll anhand der Namen sortiert werden.
#
mylist=[
    (1, 'Dresden'),
    (2, 'Chemnitz'),
    (3, 'Bayreuth'),
    (4, 'Freiburg'),
    (5, 'Berlin')]

def mycmp(a, b):
	# Bsp: a==(1, 'Dresden')  und  b==(2, 'Chemnitz')
	# Diese Compare (Vergleichs) Funktion, vergleicht
	# jeweils die zweiten Einträge in der Liste.
    return cmp(a[1], b[1])

# Es wird eine Referenz auf unsere Sortierfunktion übergeben.
# Analog einem Funktionspointer in C.
mylist.sort(mycmp) 
print mylist

# Erläuterung: Die built-in Funktion 'cmp' vergleicht zwei
# Elemente. Sie gibt 0 zurück falls beide identisch sind, -1 falls das
# erste kleiner ist, und 1 falls das erste Element größer ist.
# Beispiele:
#   cmp( (1, 2, 3), (1, 2, 3) ) --->  0
#   cmp( (1, 2, 3), (1, 2) )    --->  1
#   cmp( (1, 100),  (2, 1) )    ---> -1
#   cmp( (1, 2),    (1, 3) )    ---> -1

#Beispiel SORTITEMS b:
#Wenn 'mycmp' auf Daten zugreifen muss, die nicht
#in den Argumenten a oder b stehen, kann man mit
#'Decorate Sort Undecorate' (DSU) arbeiten, das bei großen Listen
#auch schneller ist als 'mycmp'
#Siehe auch http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52234
names={ 1: 'Dresden', 2: 'Chemnitz', 3: 'Bayreuth', 4: 'Freiburg'}
decorated=[]
for key, stadt in names.items():
    decorated.append((stadt, key))
decorated.sort() # Es wird nach Städten sortiert
ids=[]
for stadt, key in decorated:
    ids.append(key)
print ids
# ids ist nun entsprechend den zugehörigen Werten in 'names' sortiert


#---------------------------------------------------------------------
##Beispiel DOWNLOAD:
##Herunterladen eine Webseite:
#
#import urllib2
#fd=urllib2.urlopen('http://www.python.org/')
#content=fd.read()
#fd.close()
#print content
#


#---------------------------------------------------------------------
##Beispiel WEBBROWSER:
##Anzeigen der heruntergeladene Seite in einem Browser:
##Es wird der Standard-Browser des System genommen (Netscape, Mozilla, IE, ...)
#
#import tempfile
#import webbrowser
#htmlfile=tempfile.mktemp('foo.html')
#fd=open(htmlfile, 'w')
#fd.write(content)
#fd.close()
#webbrowser.open('file://%s' % htmlfile)


#---------------------------------------------------------------------
#Beispiel ISOTIME:
#Datum im ISO-Format (2003-12-31 23:59:59)
#
import time
print 'Es ist jetzt: %s' % time.strftime('%Y-%m-%d %H:%M:%S')


#---------------------------------------------------------------------
# Beispiel CHARCOUNT:
# Zähle wie oft die Zeichen einer Datei vorkommen
datei='beispiele.py'
fd=open(datei)
inhalt=fd.read() # Lese die gesamte Datei
countdict={}     # Erstelle leeres Dictionary
for char in inhalt:  # char (character) == Zeichen
    old=countdict.get(char, 0) # Falls Zeichen noch nicht gezählt, nehme die Null
    old+=1              # Zähle um eins hoch
    countdict[char]=old # Speichere Zähler im Dictionary (char == key (Schlüssel)
    
items=countdict.items() # Liste [(key1, value1), (key2, value2), ...]
items.sort() # Sortiere die Liste nach den Zeichen
for char, count in items:
    if char=='\n':
        char='\\n' # Newline als \n ausgeben.
    print 'Zeichen %s: %4d' % (  # %4d --> rechtsbündig (vier Zeichen)
        char, count)


#---------------------------------------------------------------------
#Beispiel ISSTRING
#Ist ein Objekt eine Zeichenkette?
#
myobj='abc'
if isinstance(myobj, basestring):
    print 'Ja, das ist eine Zeichenkette: %s' % myobj

#---------------------------------------------------------------------
#Beispiel UNICODE:
#Zeichensatz-Konvertierung:
#
text=u'Der in deutschland übliche Zeichensatz: iso-8851-1 (latin1)' # wg u'... Unicode
print len(text)
print len(text.encode('latin1')) # von Unicode zu Bytefolge 
print len(text.encode('utf8')) # von Unicode zu Bytefolge 
# 59, 59, 60

#---------------------------------------------------------------------
#Beispiel UNICODE II:
#Bytefolge vs Unicode
print len('üöäß')
print len(u'üöäß')

#---------------------------------------------------------------------
#Beispiel UNICODE III:
#Einzelnes de- und encode() vermeiden.
import codecs
content=codecs.open('beispiele.py', 'rt', 'utf8').read()

#---------------------------------------------------------------------
#Beispiel EINMALEINS:
#Das Einmaleins als HTML-Tabelle
#
import tempfile
import webbrowser

rows=[]
heading=[]
for i in range(1, 11):
    heading.append('<th bgcolor="gray">%s</th>' % i)
    cols=[]
    for j in range(1, 11):
        cols.append('<td align="right">%s</td>' % (i*j))
    row='<tr><th bgcolor="gray">%s</th>%s</tr>' % (i, ''.join(cols))
    rows.append(row)
html=u'''
 <html>
  <head><title>Einmaleins</title></head>
  <body>
   <table border="1">
    <tr>
     <th>&nbsp;</th> %s
    </tr>
    %s
   </table> 
  </body>
 </html>''' % (''.join(heading), ''.join(rows))

temp='%s.html' % tempfile.mktemp()
fd=open(temp, 'w')
fd.write(html)
fd.close()
webbrowser.open(temp)
# Bei Mozilla oder Firefox muss ggf. noch 'strg-r' (Reload) gedrückt werden.


#---------------------------------------------------------------------
#Beispiel SCRIPTDIR:
#Script-Verzeichnis finden: 
#Oft stehen im Verzeichnis des Scripts zusätzliche Dateien (z.B. Bilder)
#Das Verzeichnis in dem das Script steht
#erhält man wie folgt:
import os
import sys
scriptdir=os.path.abspath(os.path.dirname(sys.argv[0]))
print 'Scriptdir:', scriptdir


#---------------------------------------------------------------------
#Beispiel STACKTRACE:
#Stacktrace einer Exception als String
#Anwendung: Fehler bei einer Web-Anwendung als Email
#verschicken:
def foo():
    raise Exception('Das ist eine Exception')
try:
    foo()
except Exception:
    import traceback
    exc_string=''.join(traceback.format_exc())
    print exc_string
    # raise ohne Argumente führt ein 're-raise' aus:
    #Die aufgefangene Exception wird wieder ausgelöst
    raise 

# Hinweis: Eine 'catch-all' Regel, die alle Exceptions auffängt
# sollte vermieden werden. Normalerweise sollte man
# nur bestimmte Exceptions auffangen. Beispiel:
i='abc'
try:
    i=int(i)
except ValueError:
    print '%r ist keine Ganzzahl' % i
    

#---------------------------------------------------------------------
#Beispiel KONFIG:
#Parsen einfacher Konfig-Dateien
#Variable=Wert
import re
fd=open('myapp.config')
for line in fd:
    line=line.strip() # Leerzeichen am Anfang und Ende entfernen
    if not line:
        continue # Überspringe leere Zeilen
    if line.startswith('#'):
        continue # Überspringe Kommentarzeilen
    match=re.match(r'(.*?)\s*=\s*(.*)$', line) # Regulärer Ausdruck
    assert match, 'Syntax Fehler in folgender Zeile: %s' % line
    variable=match.group(1)
    wert=match.group(2)
    print '%s --> %s' % (variable, wert)


#---------------------------------------------------------------------
#Beispiel DICTTEMPLATE:
#HTML im Quelltext ist nicht schön. Noch schlimmer finde ich jedoch,
#Programmierung in HTML wie bei PHP.
#Dem 'magischen' Prozentzeichen kann man auch ein Dictionary übergeben.
#Zum Beispiel locals() (Dictionary der lokalen Variablen)
import time
heute=time.strftime('%d.%m.%Y')
title='Das ist der Titel' # Wird zweimal verwendet (Im Kopf, und als <h1>)
html=u'''
 <html>
  <head>
   <title>%(title)s</title>
  </head>
  <body>
   <h1>%(title)s</title>
    ...
   Heute ist der %(heute)s

   ....
  </body>
 </html>''' % locals()
print html


#---------------------------------------------------------------------
#Beispiel LISTCOMPREHENSION:
#Listcomprehension verwende ich selten, da man genauso mit einer
#Schleife arbeiten kann:

#Mit Listcomprehension
staedte=['Augsburg', 'Bremen', 'Hamburg', 'Berlin']
staedte_mit_b=[s for s in staedte if s.startswith('B')]
print staedte_mit_b

#Mit Schleife
staedte_mit_b=[]
for s in staedte:
    if s.startswith('B'):
        staedte_mit_b.append(s)
print staedte_mit_b


#---------------------------------------------------------------------
#Beispiel OWNEXCEPTIONS:
#Eigene Exceptions
#
#Hinweis: Das Auffangen aller Exceptions sollte vermieden werden,
#da Fehler wie MemoryError, KeyboardInterrupt oder ZeroDivisionError
#nicht stillschweigend übergangen werden sollten.

class MyException(Exception):
    pass

def test_func():
    raise MyException('Test')

try:
    test_func()
except MyException, exc:
    print 'Fehler: %s' % str(exc) # --> 'Fehler: Test'
    

#---------------------------------------------------------------------
#Beispiel DATETIME:
#Rechnen mit Tagen
import datetime
heute=datetime.date.today()
gestern=heute - datetime.timedelta(days=1)
morgen=heute + datetime.timedelta(days=1)
print gestern, heute, morgen


#---------------------------------------------------------------------
#Beispiel MTIME ZU DATETIME:
#mtime zu datetime
import os
import datetime
mtime=os.path.getmtime('/etc/fstab')   # Wert: Sekunden seit 1970
datetime.datetime.fromtimestamp(mtime) # High-Level Datumsangabe

#---------------------------------------------------------------------
#Beispiel SETS:
#Mengenlehre
bis_fuenf = set([1, 2, 3, 4, 5])
gerade = set([2, 4, 6, 8, 10])
vereinigung = bis_fuenf | gerade   # Union
schnittmenge = bis_fuenf & gerade  # Intersection
differenz = bis_fuenf - gerade
print 'Mengenlehre', vereinigung, schnittmenge, differenz

#---------------------------------------------------------------------
# Beispiel WRAPPER:
# Einen Funktionsaufruf mit allen Argumenten weiterleiten.
# Sie wollen einen Wrapper (Hülle/Mantel) um eine Funktion programmieren,
# um vor und nach dem Funktionsaufruf bestimmte Dinge zu tun. Zum Beispiel:
# Mittels Locking den eine Datei sperren. Mit '*args' und '**kwargs'
# (Keywordarguments) geht das ganz einfach:

def myfunc(a, b, c, name='...'):
    print a, b, c, name
    
def wrapper(*args, **kwargs):
    # Vorbereitungen ...
    myfunc(*args, **kwargs)
    # Aufräumarbeiten

wrapper(1, 2, 3, name='Till')

#---------------------------------------------------------------------
# Beispiel HOME:
# Unter Unix hat jeder Nutzer ein Home-Verzeichnis. Meist steht der Pfadname in
# der Umgebungsvariable HOME (os.environ['HOME']). Manchmal steht diese
# Variable jedoch nicht zu Verfügung. So kann man das HOME-Verzeichnis bekommen:

import os
import pwd
home=pwd.getpwuid(os.getuid())[5]

#---------------------------------------------------------------------
# Beispiel os.walk():
# Das Unix-Tool 'find' durchsucht Verzeichnisse rekursiv.
# In Python kann man dafür die Funktion os.walk() verwenden.
# Damit die Ergebnisse reproduzierbar sind, empfiehlt es sich
# die Verzeichnisse und Dateien vor dem durchforsten zu sortieren.
# In diesem Beispiel werden alle Verzeichnisse übersprungen die 'temp'
# oder 'tmp' heißen und Dateien die mit '.pyc' enden.

import os
start='.'
for root, dirs, files in os.walk(start):
   dirs[:]=[dir for dir in sorted(dirs) if not dir in ['temp', 'tmp']] # inplace Modifikation.
   for file in sorted(files):
       if file.endswith('.pyc'):
           continue
       file=os.path.join(root, file)
       print file


#---------------------------------------------------------------------
# Beispiel ETREE:
# Die Bibliothek ElementTree bietet eine einfache API um mit XML-Daten
# zu arbeiten. Einfache XPath Suchen sind möglich:

from xml.etree import ElementTree
etree=ElementTree.fromstring('<?xml version="1.0"?><root><test attr="value" /></root>')
print etree.findall('.//test')

#---------------------------------------------------------------------
# Beispiel Descriptoren
# An einer unbekannten Stelle wird das Attribut 'x' einer Klasse gesetzt. Wie
# kann man diese Stelle finden? Siehe auch http://docs.python.org/howto/descriptor.html
# Mit einem entsprechenden Descriptor kann man zB beim Setzen der Variable
# eine Exception werfen:

class ExceptionRaiser(object):
    def __set__(self, instance, value):
        raise AttributeError('instance=%r value=%r' % (instance, value))


class ClassToDebug(object):
    # Bestehende Klasse, deren Attribut Zugriff untersucht werden soll
    pass

r=ClassToDebug()
r.__class__.x=ExceptionRaiser()


# Diese Stelle soll gefunden werden:
r.x=1

