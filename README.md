# ``chromex``

An asynchronous interface for chrome automations built on ``bs4``, ``selenium``, and ``pydantic`` libraries.



# Development Reference

Use ``venv`` to install editable clone, in the `python-chromex` working directory run:

```shell
python -m pip install --upgrade pip
python -m venv .venv
source .venv/bin/activate
pip install setuptools wheel
pip install -e '.[cli, test]'
```

Run the test-suite:
```shell
pytest chromex
```