
# Package python for Aquarium

![aquarium-python-api](https://github.com/fatfish-lab/aquarium-python-api/blob/main/docs/source/_static/logo.png?raw=true)

> Aquarium python API is a tool that allows [Aquarium Studio](https://fatfi.sh/aquarium) users to interact with there data from directly from Python.

Aquarium Studio is developed by [Fatfish Lab](https://fatfi.sh)

```python
# -*- coding: utf-8 -*-
from aquarium import Aquarium

aq = Aquarium('https://your-aquarium-server/v1')
aq.connect(AQ_USER, AQ_PASSWORD)

me = aq.get_current_user()
my_tasks = me.get_tasks()
```

## Installation
This package is compatible with Python 2.7 and 3.7+

```python
python -m pip install aquarium-python-api
```
OR
```python
python -m pip install git+https://github.com/fatfish-lab/aquarium-python-api.git
```

## Documentation

Check our [documentation](https://docs.fatfish.app/dev/python/index.html) to find all the information you need.

## Maintainer

The repository is maintained by [Fatfish Lab](https://fatfi.sh)

## Support

You can contact our team at [support@fatfi.sh](mailto:support@fatfi.sh).

## Development

> Rather the package is compatible with python 2.7 and 3, the Sphinx documentation is using python 3.

1. Clone this repository
2. Setup a virtual env : `virtualenv pyaq`
3. Setup a virtual env : `virtualenv pyaq`
   1. If needed, you can specify the version of python used in your virtual env : `virtualenv --python=/usr/bin/python3 pyaq3`
4. Enable your virtual env : `source pyaq/bin/activate`
5. Install local Aquarium package to your virtual env : `pip install -e /path/to/package/aquarium-python-api`

### Build the documation

1. `cd /path/to/package/aquarium-python-api/doc`
2. `make html`

## Licence

This project uses the following license: GPL-3.0-only.
See the license file to read it.

