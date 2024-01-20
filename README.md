# Gesture-Library

A game library designed to take webcam data (of a hand) and streamline it into a readable input format.

## Getting Started
This instructions will be for MacOS only.

First, install some dependcies and restart your shell:
```bash
brew update
brew install pyenv
brew install pipx
```

Now navigate to this direction (`gesture-library/`):
```bash
pyenv install 3.12
pyenv local 3.12
```

Now get poetry (our dependency manager), create a virtual environment, and install our dependencies:
```
pipx install poetry
poetry shell
poetry install
```

To close the shell, just run `exit`.

### VSCode Configuration
If you run into an issue with your environment, make sure your interpreter points to `./.venv/bin/python`.

Some extensions:
- [Ruff](https://github.com/astral-sh/ruff-vscode) is the linter of choice
  - Because it's a dependency, you can format manually (when inside poetry's shell) with `ruff format gestures`
  - I recommend adding the following to your `settings.json`: 
  
    ```python
      "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "charliermarsh.ruff"
      }
      ```