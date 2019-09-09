from setuptools import setup, find_packages

def parse_requirements(requirement_file):
    with open(requirement_file) as f:
        return f.readlines()

setup(
    name='entrails',
    version='0.0.1',
    packages=find_packages(exclude=['tests*']),
    license='MIT',
    description='A Python package to save and retrieve data from a mongodb database',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    install_requires=parse_requirements('./requirements.txt'),
    keywords=['phishing', 'phish', 'scraper', 'phishkit'],
    url='https://github.com/swimlane/entrails',
    author='Swimlane',
    author_email='info@swimlane.com'
)