from os import system, chdir
from os.path import isfile
from setuptools import setup


# globals
requirements_list = []


def get_requirements():
    if not isfile('requirements.txt'):
        chdir('../')
    else:
        pass

    with open('requirements.txt') as req_file:
        for x in req_file.readlines():
            requirements_list.append(x)
    return requirements_list


if isfile('../requirements.txt') or isfile('./requirements.txt'):
    get_requirements()

if not isfile('./requirements.txt') and not isfile('../requirements.txt'):
    try:
        raise FileNotFoundError("requirements.txt not found, quitting!")
    except NameError as e:
        raise IOError("requirements.txt file not found, quitting!")

setup(
    name='PiMailbox',
    version='1.0',
    packages=['python_files', 'python_files.dev_tests', 'python_files.dependencies'],
    install_requires=requirements_list,
    url='',
    license='',
    author='Andrew McSparron',
    author_email='amcsparron@albanyny.gov',
    description='Monitors AWDGISPlans for new mail. When new mail is received, the pi activates a servo and raises the flag/lights an LED.'
)

