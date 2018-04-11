#!/usr/bin/env python3
import json, os
from .generate import generate_file, _start_header, _end_header
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
	content = (
		"\\phantom{1}"
	)
	target = "{}\n{}\n{}".format(_start_header(), content, _end_header())
	tester.generate_case(data, target)

def test_text(tester):
	data = {'data':[
		{
			'type': "text",
			'content': "word"
		},
	]}
	content = (
		"\\paragraph{}\n"
		"word"
	)
	target = "{}\n{}\n{}".format(_start_header(), content, _end_header())
	tester.generate_case(data, target)

def test_newline(tester):
	data = {'data':[
		{
			'type': "text",
			'content': "This is a sentence,"
		},
		{
			'type': "paragraph",
			'content': None,
		},
		{
			'type': "text",
			'content': "separated by a newline."
		},
		
	]}
	content = (
		"\\paragraph{}\n"
		"This is a sentence,\n"
		"\\paragraph{}\n"
		"separated by a newline."
	)
	target = "{}\n{}\n{}".format(_start_header(), content, _end_header())
	tester.generate_case(data, target)

def test_section_header(tester):
	data = {'data':[
		{
			'type': "header1",
			'content': "This is a section"
		},
		{
			'type': "text",
			'content': "This is some text."
		},
		
	]}
	content = (
		"\\section*{This is a section}\n"
		"\\paragraph{}\n"
		"This is some text."
	)
	target = "{}\n{}\n{}".format(_start_header(), content, _end_header())
	tester.generate_case(data, target)

def test_pdfify():
	test_list(TestManager(TestPdfify), [
		test_blank,
		test_text,
		test_newline,
		test_section_header,
	])
