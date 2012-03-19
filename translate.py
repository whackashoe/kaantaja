#!/usr/bin/env python3

"""
Interface to Microsoft Translator API
"""
import sys
import urllib.parse
import urllib.request
import codecs
try:    import json
except: import simplejson as json

class Translator():
	app_id = ''	#substitute for your own appid from microsofts bing website
	translate_api_url = "http://api.microsofttranslator.com/V2/Ajax.svc/Translate"
	detect_api_url = "http://api.microsofttranslator.com/V2/Ajax.svc/Detect"

	
	def __init___(self):
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
		html = False
		
		if text.startswith("http"):
			html = True
			webText = str(urllib.request.urlopen(text).read())
			if(len(webText) >= 1024):
				webList = self.splitCount(webText, 1024)
				finalText = ''
				
				for i in range(0, len(webList)):
					query_args = {
						'appId': self.app_id,
						'text': webList[i],
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
				'text': webText,
				'to': target,
				'contentType': 'text/plain' if not html else 'text/html',
				'category': 'general'
			}
			if source:
				query_args['from'] = source
			
			return self.query(self.translate_api_url, query_args)
	
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
		html = False
		
		if text.startswith("http"):
			html = True
			webText = str(urllib.request.urlopen(text).read())
			if(len(webText) >= 1024):
				webList = self.splitCount(webText, 1024)
				finalText = ''
				for i in range(0, 2 if(len(webList) >= 2) else len(webList)):
					query_args = {
						'appId': self.app_id,
						'text': webList[i],
						'contentType': 'text/plain' if not html else 'text/html',
					}
						
					finalText += self.query(self.detect_api_url, query_args)
				return finalText
			
			query_args = {
				'appId': self.app_id,
				'text': webText,
				'contentType': 'text/plain' if not html else 'text/html',
			}
			
			return self.query(self.detect_api_url, query_args)
			
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
		
	#attempts to decode items from web
	def applyDecoding(self, data):
		if data.startswith(codecs.BOM_UTF8):
			return data.lstrip(codecs.BOM_UTF8).decode('utf-8')
		elif data.startswith(codecs.BOM_UTF16_LE):
			return data.lstrip(codecs.BOM_UTF16_LE).decode('utf-16-le')
		elif data.startswith(codecs.BOM_UTF16_BE):
			return data.lstrip(codecs.BOM_UTF16_BE).decode('utf-16-be')
			
		return None