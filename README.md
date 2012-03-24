kaantaja
=========

kaantaja is a Python3 library for interfacing with Microsoft Translate API.

licensed under the [Apache Licence, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html)

Features
--------

kaantaja can:

- detect a language based on text
- translate a text or html file in a language into another language


Example
-------


~~~~.python
#Detects Frenchness and then translates it to English by default.
trans = Translator()
text = "poivre gonfleur"
print(trans.translate(text, trans.detect(text)))
~~~~

Command Line:

~~~~.bash
#translate to english by default
python translate.py -tfr poivre gonfleur

#load file and translate to arabic (you can omit the -f(from[espanol]) and it will be detected
python translate.py -ses -tar -fespanoldict.txt

#detects language of file
python translate.py -d -fespanoldict.txt
~~~~
