# Troubleshoot

Afin de vous permettre de débogger votre application, ou d'envoyer des informations au support, nous avis mis en place logging au sein du package Aquarium.

## Activer le débogage du package

Au sein de votre outil, vous pouvez ajouter les lignes de code suivantes :

```python
import logging

logging.basicConfig() # Initialize logging
aq_logger=logging.getLogger('aquarium') # Get the aquarium's package logger
aq_logger.propagate=True # Enable logger propagation
aq_logger.setLevel(logging.DEBUG) # Set the level of logging on DEBUG
```

Une fois ces lignes ajoutées, votre console python affichera les messages.

## Vérifier le type de classe

Pour vérifier si vous utilisez une classe Item() ou Edge(), vous pouvez directement faire un `print()` de votre variable. Si votre variable est une instance de classe, l'output suivant devrait apparaître, vous indiquant le nom de la classe entre parenthèses ainsi que les data de l'item ou l'edge.
```python
print(group)
> (Group) {   '_id': 'items/1234',
            '_key': '1234',
            '_rev_: 'b234553',
            'type': 'Group',
            'data': {
                'name': 'My group'
            },
            'createdBy': '567',
            'updatedBy': '567',
            'createdAt': '2017-1...8.580Z',
            'updatedAt': '2017-1...8.580Z'}
```
