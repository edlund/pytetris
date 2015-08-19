#!/bin/bash

run_tests() {
	echo ""
	echo "$1:"
	python "$1"
	echo ""
}

run_tests "geometry.py"

