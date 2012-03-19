kaantaja
=========

kaantaja is a Python class for interfacing with Microsoft Translate API.

kaantaja is for Python 3

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