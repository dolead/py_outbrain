from setuptools import setup

setup(
    name='py_outbrain',
    version='0.0.4',
    packages=['py_outbrain', 'py_outbrain.utils', 'py_outbrain.services'],
    url='https://github.com/dolead/py_outbrain',
    keywords='outbrain api',
    license='MIT',
    author='Ioanna Giannopoulou',
    author_email='ioanna.giannopoulou@dolead.com',
    maintainer="Dolead",
    maintainer_email="it@dolead.com",
    description='Python client for Outbrain API',
    classifiers=[
          "Programming Language :: Python :: 3",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "License :: OSI Approved :: MIT License"],
    install_requires=['requests', 'python-dateutil']
)
