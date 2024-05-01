# Quickstart

## Prérequis

Avant d'aller plus loin, vous devez vous assurer d'avoir un compte Aquarium Studio. Si ce n'est pas le cas, rendez-vous sur notre site pour [démarrer votre période d'essai](https://fatfi.sh/aquarium/offres).

En plus du compte, il faut vous munir du point d'accès API de votre instance d'Aquarium Studio. Depuis Aquarium Studio v4.0, le point d'accès API est votre url Aquarium. En cas de doute, l'URL est disponible au sein de l'interface de Aquarium Studio: dans le menu Aquarium en haut à droite de l'écran, cliquez sur `About`.

Si vous avez des difficultés, n'hésitez pas [contacter notre support](support.md).

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

aq=Aquarium('https://your-aquarium-server')
aq.connect(AQ_USER, AQ_PASSWORD)

me=aq.get_current_user()

my_tasks=me.get_tasks()

projects=aq.project.get_all()
```