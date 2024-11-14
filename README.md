# event_planner_cli
Plannificateur d'événements en ligne de commende python avec détection des conflits entre les événement

## Prérequis
 
python 3 (tester avec python 3.9)

## comment utiliser l'application en ligne de commande

### lancement
Depuis le répertoire contenant event_planner.py, lancer la console python :
```shell
python
```

Dans la console python, importer et initialiser event_planner
```python
import event_planner
planner = event_planner.EventPlanner()
```

### Ajout d'événements
Un événement se compose d'un nom, d'une heure de début et d'une heure de fin.
L'heure de début et de fin peuvent être passer en string au format '%H:%M' ou directement en type time.
L'heure de début doit forcément être inférieur à l'heure de fin.
En cas de conflit avec un événement déjà présent vous pourrez forcer l'insertion de l'événement en rentrant 'o'.
```python
planner.add_event('test', '1:00', '2:00')
```
ou
```python
from datetime import time
planner.add_event('test', time(hour=0, minute=0, second=0), time(hour=1, minute=0, second=0))
```

### Liste les événements
Lister les événements dans l'ordre de l'heure de début
```python
planner.list_event()
```

### Lister les conflits
Lister les conflits présent dans la liste
```python
planner.find_conflicts()
```

## Les tests
### Lancer les tests unitaires
Depuis le répertoire contenant tests.py, lancer la console python :
```shell
python -m unittest tests.TestEventPlanner
```