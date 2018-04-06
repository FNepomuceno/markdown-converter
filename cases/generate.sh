#!/usr/bin/env bash
for file in *.tex; do
	pdflatex $file
done
rm *.log *.aux
