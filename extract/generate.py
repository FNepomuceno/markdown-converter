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

# TODO: Clean up this code
class ParseToken:
	def __init__(self, token_text=None, token_type=None):
		self.text = token_text
		self.type = token_type
		self.finished = False

	def change_content(self, new_text=None, new_type=None):
		if not self.finished:
			self.text = new_text
			self.type = new_type
		else:
			# Finished already, cannot make changes
			pass

	def finalize(self):
		self.finished = True

	def extract_entry(self):
		if self.finished:
			return {'type': self.type, 'content': self.text}
		else:
			# Refuse because content can still change
			return None

	def __str__(self):
		return str({'type': self.type, 'content': self.text})

class BaseParser:
	def parse_text(text="", index = 0, token=None):
		if token is None:
			new_token = ParseToken()
		else:
			new_token = token
		letter = text[index]
		token_text = new_token.text
		token_type = new_token.type
		make_new_token = False
		new_type = None

		#if DEBUG:
		#print(letter)
		if True:
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
				elif token_text is None:
					token_text = " "
				else:
					make_new_token = True
					new_type = token_type
			elif letter == '\n':
				#print("newline")
				if token_text is None and token_type == "text":
					token_type = "paragraph"
				elif token_type is None:
					token_type = "text"
				else:
					make_new_token = True
			elif token_type != "text" and \
					token_type != "heading1" and \
					token_type != "heading2" and \
					token_type != "heading3" and \
					token_type != "heading4" and \
					token_type != "heading5" and \
					token_type != "heading6" and \
					token_type is not None:
				make_new_token = True
			else:
				if token_text is None:
					token_text = letter
					if token_type is None:
						token_type = "text"
				else:
					token_text = token_text + letter
		new_token.change_content(token_text, token_type)

		if make_new_token:
			new_index = index
			new_token.finalize()
			if DEBUG:
				print(new_token)
		else:
			new_index = index + 1

		return new_token, new_index, new_type

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
		self.token_list = []
		#self.parse_group = BaseParseGroup

	def parse_text(self):
		token = None
		while self.index < self.length:
			token, self.index, new_type = BaseParser.parse_text(self.text, self.index, token)
			if token.finished:
				self.token_list.append(token)
				token = ParseToken(token_type=new_type)
		if token is not None:
			token.finalize()
			self.token_list.append(token)

		entry_list = []
		for entry in self.token_list:
			entry_list.append(entry.extract_entry())
		result = {'data':entry_list}
		return result

	def parse_data(self):
		parsed_data = self.parse_text()
		result = BaseParser.clean_data(parsed_data)
		return result

def parse_file(filename):
	parser = Parser(extract_contents(filename))
	data = parser.parse_data()
	return data
