all:
	@echo "do nothing"

clean:
	rm -f `find . -type f -name '*.py[co]' `
	rm -fr */*.egg-info build dist

rpm: clean
	source /opt/virtualenvs/wheel/bin/activate && python setup.py build_py bdist_wheel && deactivate
	mkdir -p scripts/rpm/build/rpms
	cp dist/*.whl scripts/rpm/build/opt/letv/image-manager
	cd scripts/rpm && python build_rpm.py

build: clean
	python setup.py build_py bdist_wheel
	cp Makefile dist

install: build
	pip install dist/*.whl -U

install_whl: install

uninstall: clean
	pip uninstall -y image_manager 

deploy:
	pip install *.whl -U

.PHONY : all clean build install install_whl
