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
	data = ("This is a sentence,\n"
		"that is not separated.")
	target = {'data':[
		{
			'type': "text",
			'content': "This is a sentence, that is not separated."
		},
	]}
	tester.generate_case(data, target)

def test_linebreak(tester):
	data = ("This is a sentence,  \n"
		"that is separated by a linebreak.")
	target = {'data':[
		{
			'type': "text",
			'content': "This is a sentence,\nthat is separated by a linebreak."
		},
	]}
	tester.generate_case(data, target)

def test_newline(tester):
	data = ("This is a sentence,\n"
		"\n"
		"that is separated by a newline.")
	target = {'data':[
		{
			'type': "text",
			'content': "This is a sentence,"
		},
		{
			'type': "paragraph",
			'content': None
		},
		{
			'type': "text",
			'content': "that is separated by a newline."
		},
	]}
	tester.generate_case(data, target)

def test_section(tester):
	data = ("# This is a section\n"
		"This is some text.")
	target = {'data':[
		{
			'type': "header1",
			'content': "This is a section"
		},
		{
			'type': "text",
			'content': "This is some text."
		},
	]}
	tester.generate_case(data, target)

def test_simple(tester):
	data = ("This is some text in a paragraph.\n"
		"\n"
		"This is some text in another paragraph,  \n"
		"but this other text is only in another line.\n"
		"\n"
		"This is some text in yet another paragraph\n"
		"and this text is not on another line.")
	target = {'data':[
		{
			'type': "text",
			'content': "This is some text in a paragraph."
		},
		{
			'type': "paragraph",
			'content': None
		},
		{
			'type': "text",
			'content': "This is some text in another paragraph,\nbut this other text is only in another line."
		},
		{
			'type': "paragraph",
			'content': None
		},
		{
			'type': "text",
			'content': "This is some text in yet another paragraph and this text is not on another line."
		},
	]}
	tester.generate_case(data, target)

def test_subsection(tester):
	data = ("# This is a header-1\n"
		"## This is a header-2\n"
		"### This is a header-3\n"
		"#### This is a header-4\n"
		"##### This is a header-5\n"
		"###### This is a header-6\n"
		"This is some text.")
	target = {'data':[
		{
			'type': "header1",
			'content': "This is a header-1"
		},
		{
			'type': "header2",
			'content': "This is a header-2"
		},
		{
			'type': "header3",
			'content': "This is a header-3"
		},
		{
			'type': "header4",
			'content': "This is a header-4"
		},
		{
			'type': "header5",
			'content': "This is a header-5"
		},
		{
			'type': "header6",
			'content': "This is a header-6"
		},
		{
			'type': "text",
			'content': "This is some text."
		},
	]}
	tester.generate_case(data, target)

def test_extract():
	test_list(TestManager(TestExtract), [
		test_blank,
		test_text,
		test_multiline_text,
		test_linebreak,
		test_newline,
		test_section,
		test_simple,
	])
