from setuptools import setup, find_packages

setup(name='rests',
      version='0.1',
      description='rests',
      author='Peter Woyzbun',
      author_email='peter.woyzbun@gmail.com',
      packages=find_packages(),
      install_requires=['psycopg2',
                        'pandas',
                        'pyparsing',
                        'sqlalchemy',
                        'mysqlclient',
                        'networkx',
                        'PyMySQL',
                        'mysqlclient',
                        'sqlalchemy_utils',
                        'pyyaml',
                        'django>=2.1',
                        'djangorestframework',
                        'jinja2'
                        ],
      zip_safe=False)