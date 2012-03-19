#!/usr/bin/env python3

import translate
import urllib.request

tarkus = translate.Translator()

print("Input Language is "+tarkus.detect("hello world"))
print("Input Language is "+tarkus.detect("bonjour"))
print("Translate 'bonjour' of language of 'bonjour' to language of 'hello world' "+tarkus.translate("bonjour", tarkus.detect("bonjour"), tarkus.detect("hello world")))
print("Translate english webpage to french \n"+tarkus.translate("http://docs.python.org/library/codecs.html", "fr"))

#note that detecting webpages language with the detect function has yet to return any result other than english for me.
#your best bet with this is extract data from title tag or something and try that
#also, don't load too many webpages quickly or your appid will be paused for a bit
