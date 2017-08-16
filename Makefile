
PYLINT_ERR_LEVEL=8
html_coverage_dir=.html
xml_coverage_file=coverage-report.xml
xml_report=test-results.xml
pip_install_dir=dist

all: test pylint coverage build

install_requirements:
	$(MAKE) -C actsys install_requirements
	$(MAKE) -C datastore install_requirements

test: install_requirements
	$(MAKE) -C actsys test xml_report=$(xml_report)
	$(MAKE) -C datastore test xml_report=$(xml_report)

pylint: install_requirements
	$(MAKE) -C actsys pylint PYLINT_ERR_LEVEL=$(PYLINT_ERR_LEVEL)
	$(MAKE) -C datastore pylint PYLINT_ERR_LEVEL=$(PYLINT_ERR_LEVEL)

coverage: install_requirements
	$(MAKE) -C actsys coverage xml_coverage_file=$(xml_coverage_file) html_coverage_dir=$(html_coverage_dir)
	$(MAKE) -C datastore coverage xml_coverage_file=$(xml_coverage_file) html_coverage_dir=$(html_coverage_dir)

rpm:
	$(MAKE) -C actsys rpm
	$(MAKE) -C datastore rpm

build:
	$(MAKE) -C actsys build pip_install_dir=$(pip_install_dir)
	$(MAKE) -C datastore build pip_install_dir=$(pip_install_dir)

dist: build
	-

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +
	rm $(xml_report) $(xml_coverage_file)
	rm -r $(html_coverage_dir)

help:
	@echo "Supported actions are:"
	@echo "	build/dist"
	@echo "		Build this component and put a *.tar.gz, *.rpm and *.whl file in the dist folder."
	@echo "	test"
	@echo "		Run a all tests in this project."
	@echo "	pylint"
	@echo "		Run a pylint check."
	@echo "	coverage"
	@echo "		Perform a coverage analysis."
	@echo "	clean"
	@echo "		Clean all compiled files."

.PHONY: test pylint coverage clean rpm build dist
