# Quickstart

## Prérequis

Avant d'aller plus loin, vous devez vous assurer d'avoir un compte Aquarium Studio. Si ce n'est pas le cas, rendez-vous sur notre site pour [démarrer votre période d'essai](https://fatfi.sh/aquarium/offres).

En plus du compte, il faut vous munir du point d'accès API de votre instance d'Aquarium Studio. Si vous le ne connaissez pas, vous pouvez [contacter notre support](support.md).

## Installation

Installer le package Aquarium pour python

```python
python -m pip install aquarium-python-api
```
OU
```python
python -m pip install git+https://github.com/fatfish-lab/aquarium-python-api.git
```
## Utilisation simple

Après avoir importer le package aquarium, vous pouvez créer une instance Aquarium, qui vous permettra d'intéragir avec notre API.

```python
from aquarium import Aquarium

aq=Aquarium('https://your-aquarium-server/v1')
aq.connect(AQ_USER, AQ_PASSWORD)

me=aq.get_current_user()

my_tasks=me.get_tasks()

projects=aq.project.get_all()
```