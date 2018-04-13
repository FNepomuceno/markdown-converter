#!/usr/bin/env python3
from string import punctuation

def extract_contents(filename):
	result = ""
	with open(filename, 'r') as infile:
		result = infile.read()
	#print("INPUT:\n{}".format(result))
	return result

def add_token(data_list, token_type, token_text):
	data_list.append({'type': token_type, 'content': token_text})

def parse_data(data):
	result = {}
	result['data'] = []
	if data == "":
		return result
	token_text = ""
	token_type = "text"
	for letter in data:
		if letter == ' ':
			if token_text == "\n":
				pass
			elif token_text == " ":
				token_text = "\n"
			else:
				add_token(result['data'], token_type, token_text)
				token_text = " "
				token_type = "text"
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
		elif token_type != "text":
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
	#print(data)
	for item in old_data:
		if old_item is not None and item['type'] == old_item['type']:
			if item['type'] == "text" :
				separator = " "
				if item['content'][0].isspace() or old_item['content'][-1].isspace():
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
