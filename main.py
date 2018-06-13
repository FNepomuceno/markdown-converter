#!/usr/bin/env python3
import sys, json, os
from extract.generate import parse_file
from pdfify.generate import generate_file
from utils.test import DEBUG

def make_inter_json(input_file, json_file):
	data = parse_file(input_file)
	with open(json_file, 'w') as outfile:
		json.dump(data, outfile)

def make_inter_tex(json_file, tex_file):
	generate_file(json_file, tex_file)
	if not DEBUG:
		os.remove(json_file)

def make_output(tex_file, output_dir, filebase):
	os.system("pdflatex -output-directory " + output_dir + " " + tex_file)
	if not DEBUG:
		os.remove(tex_file)
	os.remove(os.path.join(output_dir, filebase + ".aux"))
	os.remove(os.path.join(output_dir, filebase + ".log"))

def main():
	if len(sys.argv) != 4:
		print("Please input the filename, input directory and output directory")
		return
	filename = sys.argv[1]
	filebase = os.path.splitext(filename)[0]
	input_dir = sys.argv[2]
	output_dir = sys.argv[3]

	input_file = os.path.join(input_dir, filename)
	json_file = filebase+".json"
	tex_file = filebase+".tex"

	make_inter_json(input_file, json_file)
	make_inter_tex(json_file, tex_file)
	make_output(tex_file, output_dir, filebase)
main()
