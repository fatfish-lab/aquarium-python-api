# Exemples

Voici quelques exemple pour réaliser certaines actions spécifiques. N'hésitez pas regarder directement la documentation des classes pour connaître les paramètres que vous pouvez utilisez ainsi que les fonctions disponibles.

## Récupérer les projets accessibles par l'utilisateur

```python
projects=aq.project.get_all()
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