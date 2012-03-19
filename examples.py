#!/usr/bin/env python3

import translate

tarkus = translate.Translator()

print("Input Language is "+tarkus.detect("hello world"))
print("Input Language is "+tarkus.detect("bonjour"))
print("Translate 'bonjour' of language of 'bonjour' to language of 'hello world' "+tarkus.translate("bonjour", tarkus.detect("bonjour"), tarkus.detect("hello world")))
