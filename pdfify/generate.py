#!/usr/bin/env python3
import json

def extract_json(filename):
	result = ""
	with open(filename, 'r') as infile:
		result = json.load(infile)
	return result

def generate_output(json_data):
	result = ""
	start_header = ("\\documentclass{article}\n"
		"\\begin{document}")
	end_header = "\\end{document}"
	placeholder = "\\phantom{1}"
	result = "{}\n{}\n{}".format(start_header, placeholder, end_header)
	return result

def generate_file(in_filename, out_filename):
	json_data = extract_json(in_filename)
	result = generate_output(json_data)
	with open(out_filename, 'w') as outfile:
		outfile.write(result)
