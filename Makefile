
PYLINT_ERR_LEVEL=8

all: test pylint coverage

test:
	py.test --junit-xml=ctrl-results.xml

pylint:
	python run-pylint.py || [[ $$? == 0 || $$? -ge $(PYLINT_ERR_LEVEL) ]]

coverage:
	python run-coverage.py

clean:
	find . -name '*.pyc' -exec rm --force {} +
	find . -name '*.pyo' -exec rm --force {} +
	find . -name '*~' -exec rm --force {} +
	rm ctrl-results.xml

help:
	@echo "Supported actions are:"
	@echo "	test"
	@echo "		Run all tests."
	@echo "	pylint"
	@echo "		Run a pylint check."
	@echo "	coverage"
	@echo "		Perform a coverage analysis."
	@echo "	clean"
	@echo "		Clean all compiled files."

.PHONY: test pylint coverage clean
