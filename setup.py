from setuptools import setup


with open('README.md', 'r') as fh:
    long_description = fh.read()


setup(
    name='pycharm_debug',
    packages=[''],
    version='0.4.0',
    license='MIT',
    description='Connection helper for PyCharm Python Remote Debugging.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Lee Dunham',
    author_email='leedunham@gmail.com',
    url='https://github.com/ldunham1/pycharm_debug',
    classifiers=[
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities"
    ],
)
