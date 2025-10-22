# Guide des Addons FTNatlink

## 🎯 Vue d'ensemble

Les addons FTNatlink permettent d'étendre les fonctionnalités de reconnaissance vocale en ajoutant de nouvelles commandes personnalisées. Ce guide couvre l'installation, la gestion et le développement d'addons.

## 📦 Installation des Addons

### Méthode 1 : Via l'Interface Graphique

1. **Lancer le Gestionnaire de Grammaires**
   ```powershell
   python -m gui
   ```

2. **Aller à l'onglet "Gestion des Addons"**

3. **Cliquer sur "Installer un Addon depuis un Fichier"**
   - Cela ouvre une boîte de dialogue de sélection de fichier

4. **Sélectionner votre fichier `.natlink-addon`**
   - Naviguer vers l'emplacement du fichier addon
   - Sélectionner le fichier (ex: `Notepad_Control_Addon.natlink-addon`)
   - Cliquer sur "Ouvrir"

5. **Attendre l'Installation**
   - L'addon sera extrait automatiquement
   - Les grammaires seront rechargées
   - Un message de succès apparaîtra

6. **Vérifier l'Installation**
   - Aller à l'onglet "Grammaires Disponibles"
   - La nouvelle grammaire devrait apparaître dans la liste

### Méthode 2 : Ligne de Commande

```powershell
python -m gui chemin/vers/addon.natlink-addon
```

### Méthode 3 : Glisser-Déposer

Faire glisser un fichier `.natlink-addon` sur le fichier `main.py` dans l'Explorateur Windows.

## 🔍 Processus d'Installation

Lors de l'installation d'un addon :

1. **Extraction** - Le fichier `.natlink-addon` (qui est un ZIP) est extrait
2. **Validation** - Le fichier `addon.json` est vérifié
3. **Copie des Fichiers** - Les fichiers Python sont copiés vers le dossier approprié
4. **Enregistrement** - L'addon est enregistré dans `installed_addons/`
5. **Rechargement** - Les grammaires sont automatiquement rechargées

## 📂 Structure des Addons

Un addon FTNatlink doit avoir la structure suivante :

```
mon_addon/
├── addon.json          # Métadonnées de l'addon
├── _global_mirror.py   # Fichier de grammaire principal
└── README.md          # Documentation (optionnel)
```

### Fichier addon.json

```json
{
    "name": "Mon Addon",
    "version": "1.0.0",
    "description": "Description de mon addon",
    "author": "Nom de l'auteur",
    "grammar_files": ["_global_mirror.py"],
    "dependencies": []
}
```

### Fichier de Grammaire (_global_mirror.py)

```python
from dragonfly import Grammar, CompoundRule, Text

class MonAddonRule(CompoundRule):
    spec = "dis bonjour"
    
    def _process_recognition(self, node, extras):
        Text("Bonjour depuis mon addon !").execute()

# Créer et charger la grammaire
grammar = Grammar("mon_addon")
grammar.add_rule(MonAddonRule())
grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None
```

## 🛠️ Développement d'Addons

### Étapes de Création

1. **Créer le Dossier de l'Addon**
   ```
   mkdir mon_nouvel_addon
   cd mon_nouvel_addon
   ```

2. **Créer addon.json**
   - Définir les métadonnées de l'addon
   - Spécifier les fichiers de grammaire

3. **Écrire les Règles de Grammaire**
   - Utiliser la bibliothèque Dragonfly
   - Définir les commandes vocales et leurs actions

4. **Tester l'Addon**
   - Créer un package `.natlink-addon`
   - Installer via l'interface graphique
   - Tester les commandes vocales

### Bonnes Pratiques

- **Noms de Commandes Uniques** - Éviter les conflits avec d'autres addons
- **Gestion des Erreurs** - Inclure une gestion d'erreurs robuste
- **Documentation** - Fournir un README.md avec les instructions d'utilisation
- **Tests** - Tester toutes les commandes avant la distribution

## 📋 Gestion des Addons Installés

### Voir les Addons Installés

Les addons installés sont stockés dans :
- `installed_addons/` - Fichiers de configuration
- `grammars/` - Fichiers de grammaire extraits

### Désinstaller un Addon

Actuellement, la désinstallation se fait manuellement :
1. Supprimer le dossier de l'addon dans `grammars/`
2. Supprimer le fichier JSON correspondant dans `installed_addons/`
3. Redémarrer l'application

## 🔧 Dépannage

### Problèmes Courants

**L'addon ne s'installe pas**
- Vérifier que le fichier a l'extension `.natlink-addon`
- Vérifier que `addon.json` est valide
- Consulter les logs pour les erreurs détaillées

**Les commandes vocales ne fonctionnent pas**
- S'assurer que Dragon NaturallySpeaking est en cours d'exécution
- Vérifier que la grammaire est chargée dans l'onglet Grammaires
- Redémarrer l'application si nécessaire

**Conflits entre Addons**
- Vérifier que les noms de commandes ne se chevauchent pas
- Consulter les logs pour les erreurs de chargement

### Fichiers de Log

Les logs sont disponibles dans l'interface graphique et contiennent des informations détaillées sur :
- L'installation des addons
- Le chargement des grammaires
- Les erreurs éventuelles

## 🚀 Exemples d'Addons

### Addon Simple - Commandes de Texte

```python
from dragonfly import Grammar, CompoundRule, Text

class CommandesTexte(CompoundRule):
    spec = "(nouveau paragraphe | nouvelle ligne | date actuelle)"
    
    def _process_recognition(self, node, extras):
        if "nouveau paragraphe" in str(node):
            Text("\n\n").execute()
        elif "nouvelle ligne" in str(node):
            Text("\n").execute()
        elif "date actuelle" in str(node):
            from datetime import datetime
            Text(datetime.now().strftime("%d/%m/%Y")).execute()

grammar = Grammar("commandes_texte")
grammar.add_rule(CommandesTexte())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
```

### Addon Avancé - Contrôle d'Application

```python
from dragonfly import Grammar, CompoundRule, Key, AppContext

# Contexte spécifique à Notepad++
notepad_context = AppContext(executable="notepad++")

class NotepadCommands(CompoundRule):
    spec = "(nouveau fichier | sauvegarder | fermer onglet)"
    
    def _process_recognition(self, node, extras):
        if "nouveau fichier" in str(node):
            Key("c-n").execute()
        elif "sauvegarder" in str(node):
            Key("c-s").execute()
        elif "fermer onglet" in str(node):
            Key("c-w").execute()

grammar = Grammar("notepad_control", context=notepad_context)
grammar.add_rule(NotepadCommands())
grammar.load()

def unload():
    global grammar
    if grammar: grammar.unload()
    grammar = None
```

## 📄 Format des Fichiers

### Extension .natlink-addon

Les fichiers d'addon utilisent l'extension `.natlink-addon` et sont des archives ZIP contenant :
- Tous les fichiers Python de l'addon
- Le fichier `addon.json` avec les métadonnées
- Fichiers de documentation optionnels

### Création d'un Package

```powershell
# Créer l'archive depuis le dossier de l'addon
zip -r mon_addon.natlink-addon mon_addon/
```

Ou utiliser l'outil de packaging intégré :
```powershell
python -m addon_manager.addon_packager mon_addon/
```

Ce guide couvre tous les aspects des addons FTNatlink, de l'installation à la création d'addons personnalisés.