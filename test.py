#!/usr/bin/env python3
from extract.test import test_extract
from pdfify.test import test_pdfify

print("EXTRACT TESTS:")
test_extract()
print("\n")
print("PDFIFY TESTS:")
test_pdfify()
