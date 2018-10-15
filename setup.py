from setuptools import setup, find_packages

setup(name='rests',
      version='0.1',
      description='rests',
      author='Peter Woyzbun',
      author_email='peter.woyzbun@gmail.com',
      packages=find_packages(),
      install_requires=['django>=2.1',
                        'djangorestframework',
                        'jinja2',
                        'mypy_extensions'
                        ],
      zip_safe=False)