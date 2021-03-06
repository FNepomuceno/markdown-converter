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
		"This is a sentence,\n"
		"\n"
		"separated by a newline."
	)
	target = "{}\n{}\n{}".format(_start_header(), content, _end_header())
	tester.generate_case(data, target)

def test_section_heading(tester):
	data = {'data':[
		{
			'type': "heading1",
			'content': "This is a section"
		},
		{
			'type': "text",
			'content': "This is some text."
		},
		
	]}
	content = (
		"\\section*{This is a section}\n"
		"This is some text."
	)
	target = "{}\n{}\n{}".format(_start_header(), content, _end_header())
	tester.generate_case(data, target)

def test_simple(tester):
	data = {'data':[
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
	content = (
		"This is some text in a paragraph.\n"
		"\n"
		"This is some text in another paragraph,\\\\\n"
		"but this other text is only in another line.\n"
		"\n"
		"This is some text in yet another paragraph "
		"and this text is not on another line."
	)
	target = "{}\n{}\n{}".format(_start_header(), content, _end_header())
	tester.generate_case(data, target)

def test_subsection_heading(tester):
	data = {'data':[
		{
			'type': "heading1",
			'content': "This is a heading-1"
		},
		{
			'type': "heading2",
			'content': "This is a heading-2"
		},
		{
			'type': "heading3",
			'content': "This is a heading-3"
		},
		{
			'type': "heading4",
			'content': "This is a heading-4"
		},
		{
			'type': "heading5",
			'content': "This is a heading-5"
		},
		{
			'type': "heading6",
			'content': "This is a heading-6"
		},
		{
			'type': "text",
			'content': "This is some text."
		},
		
	]}
	content = (
		"\\section*{This is a heading-1}\n"
		"\\subsection*{This is a heading-2}\n"
		"\\subsubsection*{This is a heading-3}\n"
		"\\subsubsection*{This is a heading-4}\n"
		"\\subsubsection*{This is a heading-5}\n"
		"\\subsubsection*{This is a heading-6}\n"
		"This is some text."
	)
	target = "{}\n{}\n{}".format(_start_header(), content, _end_header())
	tester.generate_case(data, target)

def test_emphasis(tester):
	data = {'data':[
		{
			'type': "text",
			'content': ("This is a sample text with words that are "
				"emphasised. Some words are ")
		},
		{
			'type': "bold",
			'content': "bold"
		},
		{
			'type': "text",
			'content': ", some words are "
		},
		{
			'type': "italic",
			'content': "italic"
		},
		{
			'type': "text",
			'content': ", and some words are "
		},
		{
			'type': "bolditalic",
			'content': "both bold and italic"
		},
		{
			'type': "text",
			'content': "."
		},
	]}
	content = (
		"This is a sampletext with words that are emphasized. "
		"Some words are \\textbf{bold}, some words "
		"are \\textit{italic}, and some words are "
		"\\textbf{\\textit{both bold and italic}}."
	)
	target = "{}\n{}\n{}".format(_start_header(), content, _end_header())
	tester.generate_case(data, target)

def test_pdfify():
	test_list(TestManager(TestPdfify), [
		test_blank,
		test_text,
		test_newline,
		test_section_heading,
		test_simple,
		test_subsection_heading,
		test_emphasis,
	])
