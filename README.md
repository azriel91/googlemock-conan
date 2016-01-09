# Google Mock Conan Build Script

This repository holds the [conan](https://www.conan.io/) build script for the [Google Mock](https://github.com/google/googlemock) framework.

Currently the script is configured to publish version `1.7.0` of Google Mock.

## Usage

Declare the dependency.

If you are using `conanfile.txt`:
```
[requires]
googlemock/1.7.0@azriel91/stable-2
```

If you are using `conanfile.py`:

```python
from conans import *

class MyProjectConan(ConanFile):
    # Either:
    requires = 'googlemock/1.7.0@azriel91/stable-2'
    # Or:
    def requirements(self):
        self.requires('googlemock/1.7.0@azriel91/stable-2')

    # ...
```

## Options

A full list of options and defaults can be found in [`conanfile.py`](conanfile.py)

```bash
# Example
conan install --build=missing \
              -o googlemock:GTEST_USE_OWN_TR1_TUPLE=1 \
              -o googlemock:GTEST_HAS_TR1_TUPLE=0
```
