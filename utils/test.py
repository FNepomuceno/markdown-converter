#!/usr/bin/env python3
import json, os, traceback

class TestException(Exception):
	def __init__(self, output, target):
		self.output = output
		self.target = target

	def __str__(self):
		return "EXPECTED: {}\nRECEIVED: {}".format(
			self.target, self.output)

	def __repr__(self):
		return self.__str__()

class TestManager:
	def __init__(self, TestCase):
		self.num_cases = 0
		self.num_passes = 0
		self.num_fails = 0
		self.num_errors = 0
		self.TestCase = TestCaseBase
		if(issubclass(TestCase, TestCaseBase)):
			self.TestCase = TestCase

	def generate_case(self, data, target):
		try:
			with self.TestCase(data, target) as test_case:
				test_case.validate_output()
		except TestException as e:
			print("TEST CASE FAILED.\n{}".format(e))
			self.num_fails += 1
		except Exception as e:
			traceback.print_exc()
			print("ERROR:\n{}".format(e))
			self.num_errors += 1
		else:
			print("TEST CASE PASSED.")
			self.num_passes += 1
		finally:
			self.num_cases += 1

	def results(self):
		print(self)

	def __str__(self):
		return ("TOTAL CASES: {}\n"
			"PASSES: {}\n"
			"FAILS: {}\n"
			"ERRORS: {}").format(
			self.num_cases,
			self.num_passes,
			self.num_fails,
			self.num_errors)

	def __repr__(self):
		return self.__str__

class TestCaseBase:
	def __init__(self, data, target):
		self.data = data
		self.target = target
		self.output = None

	def __enter__(self):
		raise NotImplementedError()

	def __exit__(self, exc_type, exc_value, traceback):
		raise NotImplementedError()

	def _generate_output(self):
		raise NotImplementedError()

	def validate_output(self):
		self._generate_output()
		if not self.output == self.target:
			raise TestException(self.output, self.target)

def test_list(tester, test_case_list):
	print("RUNNING TEST CASES...")
	for test_case in test_case_list:
		test_case(tester)
	print("")
	tester.results()
