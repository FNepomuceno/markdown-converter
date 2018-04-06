#!/usr/bin/env python3
import os
from .generate import parse_file
from utils.test import TestManager, TestCaseBase, test_list

class TestExtract(TestCaseBase):
	test_name = 'test.txt'

	def __enter__(self):
		with open(TestExtract.test_name, 'w') as outfile:
			outfile.write(self.data)
		return self

	def __exit__(self, exc_type, exc_value, traceback):
		os.remove(TestExtract.test_name)

	def _generate_output(self):
		self.output = parse_file(TestExtract.test_name)

def test_blank(tester):
	data = ""
	target = {'data':[
	]}
	tester.generate_case(data, target)

def test_text(tester):
	data = "word"
	target = {'data':[
		{
			'type': "text",
			'content': "word"
		},
	]}
	tester.generate_case(data, target)

def test_multiline_text(tester):
	data = "This is a sentence,\nthat is not separated."
	target = {'data':[
		{
			'type': "text",
			'content': "This is a sentence, that is not separated."
		},
	]}
	tester.generate_case(data, target)

def test_extract():
	test_list(TestManager(TestExtract), [
		test_blank,
		test_text,
		test_multiline_text,
		#test_linebreak,
		#test_newline,
	])
