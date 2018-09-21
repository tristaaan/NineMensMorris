# StoneGame


## Setup

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

## Style

Hundreds of style rules could be imposed, the ones that matter, in order of importance, are:

- 2 spaces per indentation level
- `lowercase_snake_case` for variables and method names
- `TitleCaseNames` for classes
- `ALL_CAPS` for constants
