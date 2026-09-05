.PHONY: test compile verify

test:
	python -m unittest discover -s tests -v
compile:
	python -m compileall -q src
verify: compile test
	ga-lab verify --repo .
