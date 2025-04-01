# TouchDesigner MCP - Model Context Protocol

Ce projet implémente le protocole MCP (Model Context Protocol) pour TouchDesigner, permettant aux modèles d'IA d'interagir avec les projets TouchDesigner via une API standardisée.

## Qu'est-ce que le MCP?

Le MCP (Model Context Protocol) est un standard ouvert pour l'intégration des modèles d'IA avec différentes applications et sources de données. Souvent décrit comme "l'USB-C pour les intégrations d'IA", il permet aux assistants d'IA d'interagir avec divers logiciels via une interface commune.

## Structure du projet

```
touchdesigner-mcp/
│
├── server/              # Serveur Flask qui expose l'API MCP
│   ├── server.py        # Point d'entrée principal
│   ├── td_connector.py  # Module de communication avec TouchDesigner
│   ├── tools/           # Définitions des outils disponibles
│   │   ├── __init__.py
│   │   ├── operator_tools.py
│   │   ├── parameter_tools.py
│   │   └── project_tools.py
│   └── requirements.txt # Dépendances Python
│
└── touchdesigner/
    └── mcp_client.toe   # Projet TouchDesigner avec client MCP intégré
```

## Installation

1. Clonez ce dépôt:

   ```bash
   git clone https://github.com/votre-nom/touchdesigner-mcp.git
   cd touchdesigner-mcp
   ```

2. Installez les dépendances du serveur:

   ```bash
   cd server
   pip install -r requirements.txt
   ```

3. Ouvrez le fichier `touchdesigner/mcp_client.toe` avec TouchDesigner.

## Configuration

1. **Serveur MCP**:

   - Par défaut, le serveur écoute sur `localhost:5000`
   - Vous pouvez modifier ces paramètres dans `server.py`

2. **Client TouchDesigner**:
   - Le client TouchDesigner écoute par défaut sur le port `7001`
   - Vous pouvez modifier ce port dans le script `mcp_server` dans le fichier TouchDesigner

## Démarrage

1. **Lancer le serveur MCP**:

   ```bash
   cd server
   python server.py
   ```

2. **Ouvrir le projet TouchDesigner**:
   - Ouvrez `touchdesigner/mcp_client.toe` avec TouchDesigner
   - Le projet se connecte automatiquement au serveur MCP

## Utilisation

Une fois que le serveur et TouchDesigner sont en cours d'exécution, vous pouvez utiliser l'API MCP pour interagir avec votre projet TouchDesigner.

### Exemples d'utilisation avec curl

#### Obtenir la liste des outils disponibles:

```bash
curl http://localhost:5000/mcp/tools
```

#### Créer un opérateur Circle dans TouchDesigner:

```bash
curl -X POST http://localhost:5000/mcp/run \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "create_operator", "parameters": {"operator_type": "circle", "name": "myCircle"}}'
```

#### Modifier un paramètre:

```bash
curl -X POST http://localhost:5000/mcp/run \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "set_parameter", "parameters": {"operator_path": "/myCircle", "parameter_name": "radius", "value": 0.8}}'
```

#### Connecter deux opérateurs:

```bash
curl -X POST http://localhost:5000/mcp/run \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "connect_operators", "parameters": {"source_path": "/source", "destination_path": "/destination"}}'
```

### Intégration avec des modèles d'IA

Les modèles d'IA (comme GPT) peuvent interagir avec cette API pour:

1. **Découvrir les capacités**: En interrogeant `/mcp/tools` pour voir quelles actions sont disponibles
2. **Exécuter des actions**: En envoyant des requêtes à `/mcp/run` avec les paramètres appropriés
3. **Récupérer des états**: En utilisant des outils comme `get_parameter` ou `get_project_info`

## Outils disponibles

Ce MCP pour TouchDesigner propose plusieurs catégories d'outils:

### Opérateurs

- `create_operator`: Créer un nouvel opérateur
- `delete_operator`: Supprimer un opérateur
- `connect_operators`: Connecter deux opérateurs entre eux

### Paramètres

- `set_parameter`: Définir la valeur d'un paramètre
- `get_parameter`: Obtenir la valeur d'un paramètre
- `pulse_parameter`: Envoyer une impulsion à un paramètre
- `create_parameter`: Créer un paramètre personnalisé

### Projet

- `save_project`: Sauvegarder le projet
- `load_project`: Charger un projet
- `create_container`: Créer un conteneur COMP
- `take_screenshot`: Prendre une capture d'écran
- `run_script`: Exécuter un script Python
- `get_project_info`: Obtenir des informations sur le projet
- `export_movie`: Exporter une vidéo depuis un TOP

## Dépannage

### Problèmes courants

1. **Erreur de connexion au serveur MCP**:

   - Vérifiez que le serveur Flask est en cours d'exécution
   - Vérifiez que les ports ne sont pas bloqués par un pare-feu

2. **TouchDesigner ne reçoit pas les commandes**:

   - Vérifiez que le script `mcp_server` est bien promu en extension
   - Vérifiez les messages dans la console TouchDesigner

3. **Erreur d'importation des modules**:
   - Assurez-vous que la structure du dossier `tools/` est correcte
   - Vérifiez que `__init__.py` contient bien la fonction `get_all_tools()`

## Extensions possibles

- Ajouter plus d'outils spécifiques à TouchDesigner
- Implémenter une authentification pour l'API
- Créer une interface web pour tester les commandes
- Ajouter des websockets pour les mises à jour en temps réel

## Ressources

- [Documentation MCP](https://modelcontextprotocol.ai/)
- [Documentation TouchDesigner Python](https://docs.derivative.ca/Python_in_TouchDesigner)
- [Documentation de l'API Flask](https://flask.palletsprojects.com/)

## Licence

MIT
