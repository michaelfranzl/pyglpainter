.PHONY: clean
clean:
	rm -rf dist

dist:
	python -m build --sdist .

build_deps:
	python -m pip install build
	python -m pip install twine

.PHONY: deploy_test
deploy_test: dist
	twine check dist/*
	# https://test.pypi.org/project/gcode-machine
	# python3 -m pip install --index-url https://test.pypi.org/simple/ gcode-machine
	twine upload --repository testpypi --sign dist/*

.PHONY: deploy_PRODUCTION
deploy_PRODUCTION: dist
	twine check dist/*
	# https://pypi.org/project/gcode-machine
	# python3 -m pip install gcode-machine
	twine upload --sign dist/*
