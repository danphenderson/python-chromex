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


**Sources**:
- [Search Algorithms Overview](https://www.section.io/engineering-education/understanding-search-algorithms-in-ai/#:~:text=A%20search%20problem%20consists%20of,state%20to%20the%20goal%20state)
- [Async/Await PEP standard](https://peps.python.org/pep-0492)
