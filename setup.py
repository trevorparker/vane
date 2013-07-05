from distutils.core import setup

setup(
    name='vane',
    version='0.1.0',
    author='Trevor Parker',
    author_email='trevor@trevorparker.com',
    scripts=['bin/weather-now'],
    url='https://github.com/trevorparker/vane',
    license='Modified BSD',
    description='Simple weather utilities in Python',
    install_requires=['requests']
)
