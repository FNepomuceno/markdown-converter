#!/usr/bin/env python3
import json

def _start_header():
	return ("\\documentclass{article}\n"
		"\\usepackage[margin=1.0in]{geometry}\n"
		"\\usepackage[parfill]{parskip}\n"
		"\\begin{document}")

def _end_header():
	return "\\end{document}"

def extract_json(filename):
	result = ""
	with open(filename, 'r') as infile:
		result = json.load(infile)
	return result

def generate_output(json_data):
	result = ""
	placeholder = "\\phantom{1}"
	
	data = json_data['data']
	output = []
	
	paragraph_started = False
	for item in data:
		if item['type'] == 'text':
			if not paragraph_started:
				paragraph_started = True
			item_string = item['content']
			item_string = "\\\\\n".join(item_string.split("\n"))
			output.append(item_string)
		elif item['type'] == 'header1':
			template = "\\section*{{\Huge {}}}"
			item_string = item['content']
			item_string = template.format(item_string)
			output.append(item_string)
			paragraph_started = False
		elif item['type'] == 'paragraph':
			output.append("")
	if not output:
		output = [placeholder]
	content = "\n".join(output)

	result = "{}\n{}\n{}".format(_start_header(), content, _end_header())
	return result

def generate_file(in_filename, out_filename):
	json_data = extract_json(in_filename)
	result = generate_output(json_data)
	with open(out_filename, 'w') as outfile:
		outfile.write(result)
