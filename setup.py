from setuptools import setup
import ast
import os


def version():
    """Return version string."""
    with open(os.path.join('lib2or3', '__init__.py')) as input_file:
        for line in input_file:
            if line.startswith('__version__'):
                return ast.parse(line).body[0].value.s

setup(name='2or3',
      version=version(),
      description='Writes a single byte to stdout (either "2" or "3") classifying a Python file using heuristics, giving priority to 3 if unclear',
      url='https://github.com/thomasballinger/2or3',
      author='Thomas Ballinger',
      author_email='thomasballinger@gmail.com',
      license='MIT',
      packages=['lib2or3'],
      scripts=['scripts/2or3', 'scripts/ispy2', 'scripts/ispy3'])
