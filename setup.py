# -*- coding: utf-8 -*-
import setuptools

def _setup():
    setuptools.setup(
        name='image_manager',
        version='0.0.1',
        description='a client of manage docker images',
        license='Apache',
        install_requires=['tornado==4.3', 'docker-py==1.8.1'],
        packages=['image_manager', 'image_manager.appdefine',
                  'image_manager.handlers', 'image_manager.logic',
                  'image_manager.utils'],
        package_dir={'': 'src'},
        entry_points={
            'console_scripts': [
                'image_manager_start=image_manager.main:main',
                ]
            },
        classifiers=[ 
            'Environment :: Console',
        ],
    )

def main():
    _setup()


if __name__ == '__main__':
    main()
