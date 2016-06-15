all:
	@echo "do nothing"

clean:
	rm -f `find . -type f -name '*.py[co]' `
	rm -fr */*.egg-info build dist

build: clean
	python setup.py build_py bdist_wheel
	cp Makefile dist
	cd scripts/rpm/build && mkdir -p rpms 
	cp dist/*.whl scripts/rpm/build/opt/letv/image-manager

install: build
	pip install dist/*.whl -U

install_whl: install

uninstall: clean
	pip uninstall -y image_manager 

deploy:
	pip install *.whl -U

.PHONY : all clean build install install_whl
