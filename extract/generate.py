#!/usr/bin/env python3
from string import punctuation

def extract_contents(filename):
	result = ""
	with open(filename, 'r') as infile:
		result = infile.read()
	#print("INPUT:\n{}".format(result))
	return result

def parse_data(data):
	result = {}
	result['data'] = []
	if data == "":
		return result
	token_text = ""
	token_type = "text"
	subtoken = ""
	for letter in data:
		if letter == ' ':
			if subtoken == "\n":
				pass
			elif subtoken == " ":
				subtoken = "\n"
			else:
				subtoken = " "
		elif letter == '\n':
			result['data'].append({'type': token_type, 'content': token_text+subtoken})
			subtoken = ""
			token_text = ""
			token_type = "text"
		else:
			token_text = token_text + subtoken + letter
			subtoken = ""
	result['data'].append({'type': token_type, 'content': token_text+subtoken})
	return result

def clean_data(data):
	old_data = data['data']
	new_data = []
	old_item = None
	for item in old_data:
		if old_item is not None and item['type'] == old_item['type']:
			if item['type'] == "text" :
				separator = " "
				if old_item['content'][-1].isspace():
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
