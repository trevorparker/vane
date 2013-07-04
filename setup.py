from distutils.core import setup

setup(
    name='meteo-py',
    version='0.1.0',
    author='Trevor Parker',
    author_email='trevor@trevorparker.com',
    scripts=['bin/weather-now'],
    url='https://github.com/trevorparker/meteo-py',
    license='MIT License',
    description='Simple weather utilities in Python',
    install_requires=['requests']
)
