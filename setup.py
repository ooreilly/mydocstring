from setuptools import setup
 
setup(name='mydocstring',
      version='0.2.5',
      description="""A tool for extracting and converting Google-style docstrings to
      plain-text, markdown, and JSON.""",
      url='http://github.com/ooreilly/mydocstring',
      author="Ossian O'Reilly",
      license='MIT',
      packages=['mydocstring'],
      install_requires=['mako', 'docopt'],
      entry_points = {
             'console_scripts': [
                 'mydocstring=mydocstring.docstring:main',
             ],},
      package_data={'mydocstring': ['templates/google_docstring.md']}, 
         
      zip_safe=False)
