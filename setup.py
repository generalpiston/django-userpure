from setuptools import setup, find_packages
import sys

module = __import__('userpure')

readme_file = 'README.md'
try:
    long_description = open(readme_file).read()
except IOError, err:
    sys.stderr.write("[ERROR] Cannot find file specified as "
        "``long_description`` (%s)\n" % readme_file)
    sys.exit(1)

setup(name='django-userpure',
      version=module.get_version(),
      description='Basic user proerties and user ability for django 1.5.',
      long_description=long_description,
      zip_safe=False,
      author='Abraham Elmahrek',
      author_email='abraham@elmahrek.com',
      url='https://github.com/abec/django-userpure',
      download_url='https://github.com/abec/django-userpure/tarball/0.1',
      packages = find_packages(),
      include_package_data=True,
      install_requires = [
        'django>=1.5',
      ],
      classifiers = ['Development Status :: 1 - Planning',
                     'Environment :: Web Environment',
                     'Framework :: Django',
                     'Intended Audience :: Developers',
                     'License :: OSI Approved :: BSD License',
                     'Operating System :: OS Independent',
                     'Programming Language :: Python',
                     'Topic :: Software Development :: Libraries'])
