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
def parse_data(data):
	result = {}
	result['data'] = []
	if data == "":
		return result
	token_text = ""
	token_type = "text"
	for letter in data:
		if letter == ' ':
			if token_text == "#":
				token_text = ""
				token_type = "header1"
			elif token_text == "##":
				token_text = ""
				token_type = "header2"
			elif token_text == "###":
				token_text = ""
				token_type = "header3"
			elif token_text == "####":
				token_text = ""
				token_type = "header4"
			elif token_text == "#####":
				token_text = ""
				token_type = "header5"
			elif token_text == "######":
				token_text = ""
				token_type = "header6"
			elif token_text == "\n":
				pass
			elif token_text == " ":
				token_text = "\n"
				token_type = "text"
			elif (token_type == "header1" or \
					token_type == "header2" or \
					token_type == "header3" or \
					token_type == "header4" or \
					token_type == "header5" or \
					token_type == "header6") and \
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
				token_type != "header1" and \
				token_type != "header2" and \
				token_type != "header3" and \
				token_type != "header4" and \
				token_type != "header5" and \
				token_type != "header6":
			add_token(result['data'], token_type, token_text)
			token_text = letter
			token_type = "text"
		else:
			token_text = token_text + letter
	add_token(result['data'], token_type, token_text)
	return result

def clean_data(data):
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
					item['type'] == "header1" or \
					item['type'] == "header2" or \
					item['type'] == "header3" or \
					item['type'] == "header4" or \
					item['type'] == "header5" or \
					item['type'] == "header6":
				separator = " "
				if item['content'] == '' or \
						item['content'][0].isspace() or \
						old_item['content'][-1].isspace():
					separator = ""
				old_item['content'] = old_item['content'] + separator + item['content']
		else:
			if old_item is not None:
				new_data.append(old_item)
			old_item = item
	if old_item is not None:
		new_data.append(old_item)
	data['data'] = new_data
	return data

def parse_file(filename):
	data = extract_contents(filename)
	parsed_data = parse_data(data)
	result = clean_data(parsed_data)
	return result
