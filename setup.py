from setuptools import setup, find_packages


with open("README.md", "r") as fh:
    long_description = fh.read()

kwargs = {
      'name':'cynamedtuple',
      'version':'0.1.0',
      'description':'Memory efficient and fast namedtuple implementation using Cython',
      'long_description':long_description,
      'long_description_content_type':"text/markdown",
      'author':'Egor Dranischnikow',
      'url':'https://github.com/realead/cynamedtuple',
      'packages':find_packages(where='src'),
      'package_dir':{"": "src"},
      'license': 'MIT',
      'classifiers': [
            "Programming Language :: Python :: 3",
       ],
      'install_requires':["Cython"],
}
setup(**kwargs)
