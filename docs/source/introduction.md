# Introduction

```{admonition} Introduction générale
:class: important

Cette documentation se concentre sur l'utilisation du package python.

Nous vous conseillons de lire notre [introduction générale dans notre documentation développeur](https://docs.fatfish.app/#/dev/introduction).
```

## Connexion à Aquarium

L'ensemble des fonctions sont regroupés au sein de la classe Aquarium(). Cette classe est en charge de gérer l'authentification ainsi que les différentes requêtes vers le serveur Aquarium.

En créant une instance, vous allez pouvoir réutiliser votre identification sans avoir besoin de la spécifier à chaque fois.

```python
from aquarium import Aquarium

aq=Aquarium('https://your-aquarium-server/v1')
aq.connect(AQ_USER, AQ_PASSWORD)
```

```{admonition} Sécurité
:class: danger
Si vous voulez permettre à vos utilisateurs de se reconnecter facilement sans avoir besoin de rentrer tous les jours un mot de passe, vous pouvez sauvegarder le token d'authentification. Une fois le token sauvegardé de manière sécurisée, vous pouvez le réutiliser au moment de l'initialisation de la classe Aquarium() :

```python
aq=Aquarium('https://your-aquarium-server/v1', token=secured_token)
```

## Les classes Item() et Edge()

Au sein du package, 2 classes principales sont disponibles pour travailler avec les items et les edges. Ces classes sont accessibles directement au sein de la classe Aquarium()

```python
projectKey=1234567
project=aq.item(projectKey).get()
```

Des sous-classes issues de la classe Item() sont également disponibles pour faciliter les requêtes :

- Asset
- Project
- Shot
- Task
- Template
- User
- Usergroup

Lorsque vous faites une requête, le package va essayé au maximum de vous retourner des instances de classe Item() ou Edge().

```{admonition} Détails
:class: info
En effet, certaines fonctions ne retournent pas nécessairement des items ou des edges. Notre documentation indique les différents types qui sont retournés par les fonctions.
```

### Créer une instance Item() ou Edge()
Pour créer une instance d'item, vous avez 2 possiblités :

#### Via la _key
Si vous connaissez la `_key` de l'item ou de l'edge, vous pouvez l'initialiser de cette manière là :
```python
projectKey=1234567
project=aq.project(projectKey)
```

#### Via les données complètes
Si vous avez toutes les données de l'item (ou d'un edge), vous pouvez utiliser la fonction `cast()` pour créer automatiquement une instance d'une classe :

```python
item={
            "_id": "items/1234",
            "_key": "1234",
            "_rev: "b234553",
            "type": "Group",
            "data": {
                "name": "My group"
            },
            "createdBy": "567",
            "updatedBy": "567",
            "createdAt": "2017-1...8.580Z",
            "updatedAt": "2017-1...8.580Z"
        }
group=aq.cast(item)
child=group.get_children()
```

```{admonition} Détail sur la fonction cast()
:class: info
La fonction `cast()` va automatiquement créer une instance avec le bon type d'item. **Exemple** : Si l'item que vous castez est de type `Project`, la fonction cast va vous retourner une instance de la classe `item.Project()`. Si le type n'est pas disponible en tant que sous-classe, une instance de la classe `Item()` sera retourné.
```

## Allez plus loin


### Découvrir meshQL
Des sous-classes ont été ajoutées pour vous faciliter l'accès à certaines données au sein d'Aquarium.

Comme par exemple récupérer tous les projets accessibles à l'utilisateur actif, récupérer les tâches assignées à un utilisateur, ou encore uploader une nouvelle version de media dans un shot, ...

```{admonition} Nous sommes là pour vous
:class: note
Si certaines fonctions vous manque, n'hésitez pas à [nous contacter](support.md) pour que nous puissions les ajouter.
```

Ces fonctions vous permettent de gagner du temps en évitant de vous plonger dans [meshQL](https://docs.fatfish.app/#/dev/meshql), le langage qui permet d'écrire les requêtes dans Aquarium.

Mais si vous êtes curieux, vous pouvez [activer le mode DEBUG du package](troubleshoot.md), afin de visualiser les requêtes meshQL qui sont utilisés dans ces fonctions.

De cette manière là, vous pourrez voir que la fonction suivante :

```python
projects=aq.project.get_all()
```
est équivalent à cette requête :
```python
projects=aq.query(meshql="# ($Project AND item.data.completion != 1 AND NOT <($Trash)- *) ) SORT item.data.name ASC")
```

C'est un outil pratique pour apprendre petit à petit meshQL. Si vous avez des questions, n'hésitez pas à [nous contacter](support.md) !

### Quels sont les fonctions les plus utiles ?

Vous avez besoin d'écrire des requêtes plus avancés ? Nous vous conseillons de vous pencher sur les fonctions item.traverse() et aquarium.query(). Ces 2 fonctions seront les plus utiles pour filtrer, naviguer et récupérer les données que vous voulez au sein de vos projets.

Ces 2 fonctions utilisent meshQL.