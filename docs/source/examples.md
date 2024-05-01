# Exemples

Voici quelques exemple pour réaliser certaines actions spécifiques. N'hésitez pas regarder directement la documentation des classes pour connaître les paramètres que vous pouvez utilisez ainsi que les fonctions disponibles.

## Récupérer les projets accessibles par l'utilisateur

```python
projects=aq.project.get_all()
```

## Créer un dossier dans un projet
```python
# projects is defined on the previous example
project = projects[0]
reference_folder=project.append(type='Group', data={'name': 'References'})
```

## Uploader une image dans un dossier
```python
# reference_folder is defined on the previous example
media = reference_folder.item.append(type='Media', path=r"/mnt/project/image.jpg")
```

## Récupérer les dossiers d'un projet
```python
# project is defined on previous example

folders = project.get_children(types="Group")
```

## Créer un shot dans une séquence
```python
sequence_key = 123456
shot = aq.item(sequence_key).append(type="Shot", data={'name': 's010_p100', frameIn: '101', frameOut: '256'})
```

## Récupérer les tâches assignées de l'utilisateur courant

```python
me=aq.get_current_user()
my_tasks=me.get_tasks()
```

### Récupérer les tâches assignées au sein d'un projet de l'utilisateur courant

```python
projectKey=123456
me=aq.get_current_user()
my_tasks=me.get_tasks(project_key=projectKey)
```

## Récupérer les shots ou assets d'un projet

```python
projectKey=123456
project=aq.project(123456).get()
shots=project.get_shots()
```

```{admonition} Conseil
:class: tip

En fonction de la structure de votre projet, il pourra être plus performant d'utiliser directement un traverse avec une requête personnalisée.
```

## Récupérer les status disponibles pour une tâche

```python
me=aq.get_current_user()
tasks=me.get_tasks()
statuses=tasks[0].get_statuses()
```

## Créer une playlist avec les media uploadés aujourd'hui

```python
# project is defined on the previous example
playlist = project.append(type="Playlist", data={'name': 'My playlist'})
medias = project.traverse(meshql="# -($Child, 5)> $Media AND item.updatedAt > DATE_ROUND(@now, 1, 'day') VIEW item")
medias = [aq.item(media) for media in medias]

for media in medias:
    aq.edge.create(type="Child", from_key=playlist.item._key, to_key=media._key)

imported_media = playlist.item.get_medias()
```

## Ecouter des événements

```python
events = aq.events.listen()
callback = lambda event: print(event)

allEvents = events.subscribe('*', callback)
itemCreated = events.subscribe('item.created', callback)

events.unsubscribe('*', allEvents)

events.start()
```