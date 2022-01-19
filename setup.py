from setuptools import setup

URL = 'https://github.com/Garulf/Flox'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("./flox/version", "r") as f:
    version = f.read().strip()

setup(name='Flox-lib',
      version=version,
      description='Python library to help build Flow Launcher and Wox plugins.',
      long_description=long_description,
      url=URL,
      project_urls={
              "Bug Tracker": f"{URL}/issues"
      },
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Windows",
      ],
      author='William McAllister',
      author_email='dev.garulf@gmail.com',
      license='MIT',
      packages=['flox'],
      zip_safe=False)
