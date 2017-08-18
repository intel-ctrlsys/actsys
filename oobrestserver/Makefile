
PYLINT_ERR_LEVEL=8
html_coverage_dir=.html
xml_coverage_file=oobrestserver-report.xml
xml_report=oobrestserver-results.xml
pip_install_dir=dist

all: test pylint coverage build

install_dev:
	sudo -E pip install -e .

install:
	python2 setup.py sdist
	sudo -E pip2 install dist/*.tar.gz

uninstall:
	sudo -E pip2 uninstall oob_rest_server

install_requirements:
	sudo -E pip2 install -r requirements.txt

test: install_requirements
	python2 -m pytest . --junit-xml=$(xml_report)

pylint: install_requirements
	pylint --rcfile=pylintrc --ignore-patterns=test* oobrestserver || [[ $$? == 0 || $$? -ge $(PYLINT_ERR_LEVEL) ]]

coverage: install_requirements
	python2 -m pytest . --cov-config .coveragerc --cov=oobrestserver --cov-report term-missing --cov-report xml:$(xml_coverage_file) --cov-report html:$(html_coverage_dir)

rpm:
	python2 setup.py bdist_rpm

build:
	python2 setup.py sdist --dist-dir $(pip_install_dir)
	python2 setup.py bdist_wheel --dist-dir $(pip_install_dir)
	python2 setup.py bdist_rpm

dist: build
	-

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +
	rm -f $(xml_report) $(xml_coverage_file)
	rm -rf $(html_coverage_dir)

help:
	@echo "Supported actions are:"
	@echo "	build/dist"
	@echo "		Build this component and put a *.tar.gz, *.rpm and *.whl file in the dist folder."
	@echo "	test"
	@echo "		Run all tests in this project."
	@echo "	pylint"
	@echo "		Run a pylint check."
	@echo "	coverage"
	@echo "		Perform a coverage analysis."
	@echo "	clean"
	@echo "		Clean all compiled files."

.PHONY: test pylint coverage clean rpm build dist
