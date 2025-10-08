# Empilement de polyèdres dans un polyèdre

## Installation
Le projet utilise [`uv`](https://docs.astral.sh/uv/) pour la gestion des dépendances.

Pour synchroniser les dépendances, installer `uv` et exécuter la commande suivante dans le répertoire du projet :
```bash
uv sync
```

## Sujet

Étant donné un polyèdre P et un ensemble de n polyèdres P₁, P₂, …, Pₙ, il faut trouver un sous-ensemble de ces polyèdres et les placer dans l'espace tels que :

1. Le sous-ensemble de polyèdres se trouve à l'intérieur du polyèdre P
2. Les polyèdres du sous-ensemble ne s'intersectent pas.

Avec ces deux contraintes, il faut trouver l'empilement qui maximise la somme des volumes des polyèdres.

### Précisions

- Tous les polyèdres sont fermés, c'est-à-dire, ils contiennent leur frontière.

- Un polyèdre Pᵢ est contenu dans P si tous ses sommets, arêtes et faces se trouvent à l'intérieur. Un point de Pᵢ peut se retrouver dans la frontière de P (car P est fermé).

- Deux polyèdres Pᵢ et Pⱼ s'intersectent même s'ils ne partagent qu'un seul point (car ils sont fermés). On ne peut donc pas coller deux polyèdres.

- Pour placer un polyèdre Pᵢ, il faut lui donner une position (avec un vecteur 3D) et une orientation (avec un quaternion).

- Données d'entrée : [instance.zip](instance.json)

- Données de sortie : volume total ; liste des polyèdres avec leur position. Exemple :
```json
{
  "volume": 84.32,
  "polyedres": [
    {
      "index": 4,
      "vecteur": {"x": 0.2, "y": 0.3, "z": 1.1},
      "quaternion": {
        "s": 0.2, 
        "u": {"x": 0.2, "y": 0.4, "z": 1.1}
      }
    },
    {
      "index": 6,
      "vecteur": {"x": 1.2, "y": 3.32, "z": 1.1},
      "quaternion": {
        "s": 0.2, 
        "u": {"x": 0.2, "y": 0.4, "z": 1.0}
      }
    }
  ]
}