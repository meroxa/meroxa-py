## How to contribute to Meroxa-py

Thank you for considering contributing to Meroxa-py!

### Submitting patches


If there is not an open issue for what you want to submit, prefer
opening one for discussion before working on a PR. You can work on any
issue that doesn't have an open PR linked to it or a maintainer assigned
to it. These show up in the sidebar. No need to ask if you can work on
an issue that interests you.

Include the following in your patch:

-   Use [Black](https://black.readthedocs.io) to format your code. This and other tools will run
    automatically if you install [pre-commit](https://pre-commit.com) using the instructions
    below.
-   Include tests if your patch adds or changes code. Make sure the test
    fails without your patch.
-   Update any relevant docs pages and docstrings. Docs pages and
    docstrings should be wrapped at 72 characters.



### First time setup


- Create a virtualenv.

    #### Linux/macOS
     ```bash
     $ python3 -m venv env
     $ . env/bin/activate
    ```
    #### Windows
    ```bash
    > py -3 -m venv env
    > env\Scripts\activate
   ```

- Upgrade pip and setuptools.

  ```bash
  $ python -m pip install --upgrade pip setuptools
    ```


- Install the development dependencies, then install Flask in editable
    mode.

  ```bash
  $ make install dev
  ```

- Install the pre-commit hooks.

    ```bash
  $ pre-commit install
  ```
