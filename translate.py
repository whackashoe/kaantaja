#!/usr/bin/env python3

"""
Interface to Microsoft Translator API
"""
import os
import sys
import urllib.parse
import urllib.request
import codecs
try:    import json
except: import simplejson as json

class Translator:
	app_id = ''	#substitute for your own appid from microsofts bing website
	translate_api_url = "http://api.microsofttranslator.com/V2/Ajax.svc/Translate"
	detect_api_url = "http://api.microsofttranslator.com/V2/Ajax.svc/Detect"

	langCodes = {
		'ar' : 'Arabic',
		'cz' : 'Czech',
		'da' : 'Danish',
		'de' : 'German',
		'en' : 'English',
		'et' : 'Estonian',
		'fi' : 'Finnish',
		'fr' : 'French',
		'nl' : 'Dutch',
		'el' : 'Greek',
		'he' : 'Hebrew',
		'ht' : 'Haitian Creole',
		'hu' : 'Hungarian',
		'id' : 'Indonesian',
		'it' : 'Italian',
		'ja' : 'Japanese',
		'ko' : 'Korean',
		'lt' : 'Lithuanian',
		'lv' : 'Latvian',
		'no' : 'Norweigian',
		'pl' : 'Polish',
		'pt' : 'Portuguese',
		'ro' : 'Romanian',
		'es' : 'Spanish',
		'ru' : 'Russian',
		'sk' : 'Slovak',
		'sl' : 'Slovene',
		'sv' : 'Swedish',
		'th' : 'Thai',
		'tr' : 'Turkish',
		'uk' : 'Ukrainian',
		'vi' : 'Vietnamese',
		'zh-CHS' : 'Simplified Chinese',		
		'zh-CHT' : 'Traditional Chinese'
	}
		
	def __init__(self, appid=app_id):
		self.app_id = appid
		if self.app_id == '' or not self.app_id:
			raise ValueError("AppId needs to be set when instantiating Translator")
							
	
	#A unicode aware version of urllib.urlencode.
	#Borrowed from pyfacebook :: http://github.com/sciyoshi/pyfacebook/
	def unicode_urlencode(self, params):
		if isinstance(params, dict):
			params = params.items()
			
		return urllib.parse.urlencode([(k, v) for k, v in params])

	
	#takes arguments and optional language argument and runs query on server
	def query(self, api_url, args):
		data = self.unicode_urlencode(args)
		sock = urllib.request.urlopen(api_url + '?' + data)
		result = sock.read()
		result = self.applyDecoding(result)
			
		return json.loads(result)
	
	#translates text or html
	def translate(self, text, source=None, target="en"):
		if self.app_id == '' or not self.app_id:
			raise Exception("Manually enter an appId from\"https://ssl.bing.com/webmaster/Developers/\"")
		
		if  target not in self.langCodes:
			raise Exception("Output Language is not supported, type \"translate.py  -l\" to view language codes")
		
		if source != None and source not in self.langCodes:
			raise Exception("Input  Language is not supported, type \"translate.py  -l\" to view language codes")


		html = False
		if text.startswith("http"):
			html = True
			text = str(urllib.request.urlopen(text).read())
		
		#safe length is 1024
		#a more optimal solution would be to split on sentence/word end
		if(len(text) >= 1024):
			longList = self.splitCount(text, 1024)
			finalText = ''
			
			for i in range(0, len(longList)):
				query_args = {
					'appId': self.app_id,
					'text': longList[i],
					'to': target,
					'contentType': 'text/plain' if not html else 'text/html',
					'category': 'general'
				}
				if source:
					query_args['from'] = source
					
				finalText += self.query(self.translate_api_url, query_args)
				
			return finalText
			
		query_args = {
			'appId': self.app_id,
			'text': text,
			'to': target,
			'contentType': 'text/plain' if not html else 'text/html',
			'category': 'general'
		}
		
		if source:
			query_args['from'] = source
			
		return self.query(self.translate_api_url, query_args)
	
	#detects language of input, returns abbreviation that can be used to translate
	#on bings end there seems to be an issue with parsing html to detect
	#todo: work around this shiz
	def detect(self, text):
		if self.app_id == '' or not self.app_id:
			raise Exception("Manually enter an appId from\"https://ssl.bing.com/webmaster/Developers/\"")
		
		html = False
		if text.startswith("http"):
			html = True
			text = str(urllib.request.urlopen(text).read())
		
		if(len(text) >= 1024):
			longList = self.splitCount(text, 1024)
			finalText = []
			for i in range(0, 2 if(len(longList) >= 2) else len(longList)):
				query_args = {
					'appId': self.app_id,
					'text': longList[i],
					'contentType': 'text/plain' if not html else 'text/html',
				}
					
				finalText.append(self.query(self.detect_api_url, query_args))
			
			
			return most_common(finalText)
			
				
		query_args = {
			'appId': self.app_id,
			'text': text,
			'contentType': 'text/plain' if not html else 'text/html',
		}
			
		return self.query(self.detect_api_url, query_args)
		
	#taken from http://code.activestate.com/recipes/496784-split-string-into-n-size-pieces/
	#code splits string into n sized pieces
	def splitCount(self, s, count):
		return [''.join(x) for x in zip(*[list(s[z::count]) for z in range(count)])]
	
	
	def most_common(lst):
		cur_length = 0
		max_length = 0
		cur_i = 0
		max_i = 0
		cur_item = None
		max_item = None
		for i, item in sorted(enumerate(lst), key=lambda x: x[1]):
			if cur_item is None or cur_item != item:
				if cur_length > max_length or (cur_length == max_length and cur_i < max_i):
					max_length = cur_length
					max_i = cur_i
					max_item = cur_item
				cur_length = 1
				cur_i = i
				cur_item = item
			else:
				cur_length += 1
		if cur_length > max_length or (cur_length == max_length and cur_i < max_i):
			return cur_item
		return max_item
	
	
	#attempts to decode items from web
	def applyDecoding(self, data):
		if data.startswith(codecs.BOM_UTF8):
			return data.lstrip(codecs.BOM_UTF8).decode('utf-8')
		elif data.startswith(codecs.BOM_UTF16_LE):
			return data.lstrip(codecs.BOM_UTF16_LE).decode('utf-16-le')
		elif data.startswith(codecs.BOM_UTF16_BE):
			return data.lstrip(codecs.BOM_UTF16_BE).decode('utf-16-be')
			
		return None


if __name__ == "__main__":
	trans = Translator()

	detect      = False
	sourceLang  = None
	toLang      = 'en'
	displayHelp = False
	text 	    = ''

	for a in sys.argv:
		if a == '-h' or a == 'help':
			displayHelp = True
		elif a == '-l':
			for k, v in  trans.langCodes.items():
				print(k+" : "+v)

			sys.exit(0)
		elif a == '-d':
			detect = True
		elif a.startswith('-f'):
			try:
				text = open(a[2:], 'r').read()
			except IOError as e:
				raise Exception("Invalid file name")
		elif a.startswith('-t'):
			toLang = a[2:]
		elif a.startswith('-s'):
			sourceLang = a[2:]
		elif not a.startswith('translate.py'):
			text = text+a+' '

	if text == '':
		displayHelp = True
	
	if displayHelp == True:
		print("kraataja: python translation library")
		print("")
		print("-h displays this help text")
		print("usage: translate.py -h")
		print("")
		print("-l displays language codes")
		print("usage: translate.py -l")
		print("")
		print("-d detects language and returns language code")
		print("usage: translate.py -d words to be detected")
		print("")
		print("-f(filename) loads file as input text")
		print("usage: translate.py -ffrancaiswords.txt")
		print("")
		print("-t(langCode) translates text to language, ommitting it defaults to english")
		print("usage: translate.py -tfr hello")
		print("")
		print("-s(inputLangCode) specifies what language of input, omitting this will attempt to detect language")
		print("usage: translate.py -ses si")


	elif detect == True:
		print(trans.detect(text))
	else:
		print(trans.translate(text, sourceLang, toLang))
