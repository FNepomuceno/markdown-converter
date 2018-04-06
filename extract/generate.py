#!/usr/bin/env python3

def extract_contents(filename):
	result = ""
	with open(filename, 'r') as infile:
		result = infile.read()
	#print("INPUT:\n{}".format(result))
	return result

def parse_data(data):
	result = {}
	result['data'] = []
	print(data)
	return result

def parse_file(filename):
	data = extract_contents(filename)
	return parse_data(data)
