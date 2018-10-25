# StoneGame

An implementation of [Nine-Men's Morris](https://en.wikipedia.org/wiki/Nine_men%27s_morris).

## Getting Started

From the project directory run:

```sh
# install the game as a local python package
python setup.py install
# run the package
python -m stone_game
```

As a consequence, when working within the project and you want to import a class from another file you need to refer to the file a little differently than normal:

```py
# A file in the same directory
from .my_package import MyModule

# A file in a different directory above the current
from ..other_package import AnotherModule
```

## Tests

Tests are automatically run on [TravisCI](https://travis-ci.com/tristaaan/StoneGame) when you push your branch and before a merge. They can be, and it is encouraged to, run locally. Run all tests:

```sh
python -m unittest tests/*.py
```

Run an individual test file:

```sh
python -m unittest tests/test_my_module.py
```
