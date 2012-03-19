#!/usr/bin/env python3

"""
Interface to Microsoft Translator API
"""
import urllib.parse
import urllib.request
import codecs
import json

class Translator():
	app_id = '2EB3615434F1D1401B9E3636840C763D22B15C35'	#substitute for your own appid from microsofts bing website
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
		if result.startswith(codecs.BOM_UTF8):
			result = result.lstrip(codecs.BOM_UTF8).decode('utf-8')
		elif result.startswith(codecs.BOM_UTF16_LE):
			result = result.lstrip(codecs.BOM_UTF16_LE).decode('utf-16-le')
		elif result.startswith(codecs.BOM_UTF16_BE):
			result = result.lstrip(codecs.BOM_UTF16_BE).decode('utf-16-be')
			
		return json.loads(result)
	
	#translates text or html
	def translate(self, text, source=None, target="en", html=False):
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
	def detect(self, text, target="en", html=False):
		query_args = {
			'appId': self.app_id,
			'text': text,
			'to': target,
			'contentType': 'text/plain' if not html else 'text/html',
			'category': 'general'
		}
			
		return self.query(self.detect_api_url, query_args)