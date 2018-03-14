#!/usr/bin/env python3
import json, os
from .generate import generate_file
from utils.test import TestManager, TestCaseBase, test_list

class TestPdfify(TestCaseBase):
	test_input_name = 'input.txt'
	test_output_name = 'output.txt'

	def __enter__(self):
		with open(TestPdfify.test_input_name, 'w') as outfile:
			json.dump(self.data, outfile)
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		os.remove(TestPdfify.test_input_name)
		os.remove(TestPdfify.test_output_name)

	def _generate_output(self):
		generate_file(TestPdfify.test_input_name,
			TestPdfify.test_output_name)
		with open(TestPdfify.test_output_name, 'r') as infile:
			self.output = infile.read()

def test_blank(tester):
	data = {'data':[
	]}
	target = (
		"\\documentclass{article}\n"
		"\\begin{document}\n"
		"\\phantom{1}\n"
		"\\end{document}"
	)
	tester.generate_case(data, target)

def test_text(tester):
	data = {'data':[
		{
			'type': "text",
			'content': "word"
		},
	]}
	target = (
		"\\documentclass{article}\n"
		"\\begin{document}\n"
		"word\n"
		"\\end{document}"
	)
	tester.generate_case(data, target)

def test_pdfify():
	test_list(TestManager(TestPdfify), [
		test_blank,
		test_text,
	])
