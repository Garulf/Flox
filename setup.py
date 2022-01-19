from setuptools import setup

URL = 'https://github.com/Garulf/Flox'

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("flox/version", "r") as fh:
    version = fh.read().strip()

setup(name='Flox-lib',
      version=version,
      description='Python library to help build Flow Launcher and Wox plugins.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url=URL,
      project_urls={
              "Bug Tracker": f"{URL}/issues"
      },
      classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
      ],
      author='William McAllister',
      author_email='dev.garulf@gmail.com',
      license='MIT',
      packages=['flox'],
      zip_safe=True,
      include_package_data=True,
      package_data = {
            'flox': ['version']
      })
