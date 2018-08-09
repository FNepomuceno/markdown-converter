#!/usr/bin/env python3
from string import punctuation
from utils.test import DEBUG

def extract_contents(filename):
	result = ""
	with open(filename, 'r') as infile:
		result = infile.read()
	if DEBUG:
		print("INPUT:\n{}".format(result))
	return result

def add_token(data_list, token_type, token_text):
	data_list.append({'type': token_type, 'content': token_text})

# TODO: Clean up this code
class BaseParseState:
	def parse_text(text=""):
		result = {}
		result['data'] = []
		if text == "":
			return result
		token_text = ""
		token_type = "text"
		for letter in text:
			if letter == ' ':
				if token_text == "#":
					token_text = ""
					token_type = "heading1"
				elif token_text == "##":
					token_text = ""
					token_type = "heading2"
				elif token_text == "###":
					token_text = ""
					token_type = "heading3"
				elif token_text == "####":
					token_text = ""
					token_type = "heading4"
				elif token_text == "#####":
					token_text = ""
					token_type = "heading5"
				elif token_text == "######":
					token_text = ""
					token_type = "heading6"
				elif token_text == "\n":
					pass
				elif token_text == " ":
					token_text = "\n"
					token_type = "text"
				elif (token_type == "heading1" or \
						token_type == "heading2" or \
						token_type == "heading3" or \
						token_type == "heading4" or \
						token_type == "heading5" or \
						token_type == "heading6") and \
						token_text == "":
					pass
				else:
					add_token(result['data'], token_type, token_text)
					token_text = " "
			elif letter == '\n':
				if token_text is None:
					pass
				elif token_text == "":
					token_text = None
					token_type = "paragraph"
				else:
					add_token(result['data'], token_type, token_text)
					token_text = ""
					token_type = "text"
			elif token_type != "text" and \
					token_type != "heading1" and \
					token_type != "heading2" and \
					token_type != "heading3" and \
					token_type != "heading4" and \
					token_type != "heading5" and \
					token_type != "heading6":
				add_token(result['data'], token_type, token_text)
				token_text = letter
				token_type = "text"
			else:
				token_text = token_text + letter
		add_token(result['data'], token_type, token_text)
		return result

	def clean_data(data={'data':[]}):
		old_data = data['data']
		new_data = []
		old_item = None
		if DEBUG:
			print(data)
		for item in old_data:
			if DEBUG is True:
				print(item)
			if old_item is not None and item['type'] == old_item['type']:
				if item['type'] == "text" or \
						item['type'] == "heading1" or \
						item['type'] == "heading2" or \
						item['type'] == "heading3" or \
						item['type'] == "heading4" or \
						item['type'] == "heading5" or \
						item['type'] == "heading6":
					separator = " "
					if item['content'] == '' or \
							item['content'][0].isspace() or \
							old_item['content'][-1].isspace():
						separator = ""
					old_item['content'] = old_item['content'] + \
						separator + item['content']
			else:
				if old_item is not None:
					new_data.append(old_item)
				old_item = item
		if old_item is not None:
			new_data.append(old_item)
		data['data'] = new_data
		return data

class Parser:
	def __init__(self, text=""):
		self.text = text
		self.length = len(text)
		self.index = 0
		self.state = BaseParseState

	def parse_data(self):
		parsed_data = self.state.parse_text(self.text)
		return self.state.clean_data(parsed_data)

def parse_file(filename):
	parser = Parser(extract_contents(filename))
	data = parser.parse_data()
	return data
