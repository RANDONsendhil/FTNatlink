# Guide de l'Interface Graphique FTNatlink

## 🎯 Vue d'ensemble

L'interface graphique FTNatlink fournit un moyen convivial de gérer les grammaires de reconnaissance vocale et d'installer des addons. Cette interface utilise un système d'onglets pour une navigation facile.

## 🚀 Lancement de l'Application

### Démarrage Normal

```powershell
python -m gui
```

### Démarrage avec Installation d'Addon

```powershell
python -m gui chemin/vers/addon.natlink-addon
```

### Écran de Chargement

Au démarrage, l'application affiche un écran de chargement qui montre :
- Initialisation des composants
- Chargement des grammaires
- Création de l'interface
- Configuration finale

## 🗂️ Interface à Onglets

L'interface principale est organisée en deux onglets principaux :

### 1. 📚 Onglet "Grammaires Disponibles"

Cet onglet permet de gérer toutes les grammaires de reconnaissance vocale.

#### Disposition

- **Panneau Gauche** - Liste des grammaires et boutons de gestion
- **Panneau Droit** - Informations détaillées sur la grammaire sélectionnée
- **Diviseur Ajustable** - Permet de redimensionner les panneaux

#### Fonctionnalités Principales

**Liste des Grammaires**
- Affiche toutes les grammaires disponibles
- Inclut les grammaires des dossiers `grammars/` et `addons/`
- Actualisation automatique lors des changements

**Boutons de Gestion Globale**
- **"Actualiser"** - Met à jour la liste des grammaires
- **"Charger Toutes"** - Charge toutes les grammaires disponibles
- **"Recharger Toutes"** - Décharge et recharge toutes les grammaires
- **"Décharger Toutes"** - Décharge toutes les grammaires actives

**Contrôles Individuels**
- **"Charger"** - Charge la grammaire sélectionnée uniquement
- **"Décharger"** - Décharge la grammaire sélectionnée uniquement
- **"Recharger"** - Recharge la grammaire sélectionnée uniquement

#### Affichage des Détails

Quand vous sélectionnez une grammaire, le panneau droit affiche :

- **📄 Nom du Fichier** - Nom et emplacement du fichier
- **📏 Taille du Fichier** - Taille en octets
- **📝 Description** - Extraite de la docstring du module
- **🔷 Classes** - Noms des classes et leurs méthodes
- **🎤 Commandes Vocales** - Commandes définies dans la grammaire
- **📊 Statut** - Indique si la grammaire est chargée ou non

#### Utilisation Typique

1. **Voir les Grammaires Disponibles**
   - Cliquer sur "Actualiser" pour voir toutes les grammaires
   - Les grammaires apparaissent dans la liste de gauche

2. **Examiner une Grammaire**
   - Cliquer sur n'importe quelle grammaire dans la liste
   - Les détails apparaissent dans le panneau de droite

3. **Charger les Grammaires**
   - Utiliser "Charger Toutes" pour activer toutes les grammaires
   - Ou sélectionner une grammaire spécifique et cliquer "Charger"

4. **Modifier et Recharger**
   - Après avoir modifié un fichier de grammaire
   - Utiliser "Recharger Toutes" ou "Recharger" pour appliquer les changements

### 2. 📦 Onglet "Gestion des Addons"

Cet onglet permet d'installer et de gérer les packages d'addons.

#### Fonctionnalités

**Installation d'Addons**
- **"Installer un Addon depuis un Fichier"** - Ouvre un navigateur de fichiers
- Support pour les fichiers `.natlink-addon`
- Installation automatique avec extraction et rechargement

**Instructions d'Utilisation**
- Guide étape par étape pour l'installation
- Explication des formats de fichiers supportés
- Conseils de dépannage

#### Processus d'Installation

1. **Sélection du Fichier**
   - Cliquer sur "Installer un Addon depuis un Fichier"
   - Naviguer vers le fichier `.natlink-addon`
   - Sélectionner et confirmer

2. **Installation Automatique**
   - L'addon est extrait automatiquement
   - Les fichiers sont copiés aux bons emplacements
   - Les métadonnées sont enregistrées

3. **Rechargement**
   - Les grammaires sont automatiquement rechargées
   - Les nouvelles commandes vocales deviennent disponibles

4. **Confirmation**
   - Message de succès affiché
   - L'addon apparaît dans l'onglet Grammaires

## 📋 Zone de Log

### Affichage des Messages

La partie inférieure de l'interface contient une zone de log qui affiche :

- **Messages de Bienvenue** - Au démarrage de l'application
- **Statut des Opérations** - Chargement, déchargement, installation
- **Messages d'Erreur** - Problèmes rencontrés et solutions
- **Informations de Debug** - Détails techniques pour le dépannage

### Types de Messages

**Messages d'Information**
- "Grammaires chargées" - Confirme le chargement réussi
- "Addon installé avec succès" - Confirme l'installation d'addon
- "X grammaire(s) trouvée(s)" - Nombre de grammaires détectées

**Messages d'Erreur**
- "Aucune grammaire sélectionnée" - Aide pour l'utilisation
- "Échec du chargement" - Problèmes de grammaire
- "Erreur d'installation" - Problèmes d'addon

**Messages de Debug**
- Détails sur les chemins de fichiers
- Informations sur le chargement des modules
- Traces d'exécution pour le diagnostic

## ⚙️ Paramètres et Configuration

### Horodatage

Tous les messages de log incluent un horodatage au format :
```
[AAAA-MM-JJ HH:MM:SS] Message
```

### Actualisation Automatique

L'interface se met à jour automatiquement lors :
- Du chargement/déchargement de grammaires
- De l'installation d'addons
- Des changements dans les dossiers de grammaires

### Gestion des Erreurs

L'interface gère gracieusement :
- Les fichiers de grammaires corrompus
- Les addons mal formés
- Les erreurs de chargement Dragon NaturallySpeaking
- Les problèmes de permissions de fichiers

## 🔧 Dépannage de l'Interface

### Problèmes Courants

**L'interface ne se lance pas**
- Vérifier que Python et les dépendances sont installés
- Consulter les logs de démarrage
- S'assurer que wxPython est correctement installé

**Les grammaires n'apparaissent pas**
- Cliquer sur "Actualiser" dans l'onglet Grammaires
- Vérifier que les fichiers sont dans les bons dossiers
- S'assurer que les fichiers Python sont syntaxiquement corrects

**L'installation d'addons échoue**
- Vérifier que le fichier a l'extension `.natlink-addon`
- S'assurer que le fichier n'est pas corrompu
- Consulter les messages d'erreur dans la zone de log

**L'interface est lente**
- Fermer et relancer l'application
- Vérifier l'utilisation mémoire de Dragon NaturallySpeaking
- Réduire le nombre de grammaires chargées

### Messages d'Erreur Fréquents

**"Aucune grammaire trouvée"**
- Vérifier que les dossiers `grammars/` et `addons/` contiennent des fichiers
- S'assurer que les fichiers Python sont valides

**"Échec d'initialisation de l'application"**
- Problème de configuration ou de dépendances
- Relancer avec des privilèges administrateur si nécessaire

**"Erreur lors du chargement de la grammaire"**
- Problème de syntaxe dans le fichier de grammaire
- Dépendance manquante (ex: Dragonfly)

## 🎨 Personnalisation de l'Interface

### Disposition des Panneaux

- **Redimensionnement** - Faire glisser le diviseur central
- **Taille de Police** - Héritée des paramètres système Windows
- **Thème** - Suit le thème Windows par défaut

### Préférences Utilisateur

Actuellement, l'interface utilise des paramètres par défaut, mais les améliorations futures pourraient inclure :
- Sauvegarde de la disposition des panneaux
- Thèmes personnalisables
- Préférences de log
- Raccourcis clavier

## 📱 Intégration Système

### Barre des Tâches

L'application apparaît dans la barre des tâches Windows avec :
- Icône FTNatlink personnalisée
- Titre descriptif
- Support pour les notifications système

### Glisser-Déposer

Support pour :
- Glisser des fichiers `.natlink-addon` sur l'interface
- Installation automatique lors du glisser-déposer
- Feedback visuel pendant l'opération

### Gestion des Fichiers

L'interface interagit avec :
- Explorateur Windows pour la sélection de fichiers
- Système de fichiers pour l'installation d'addons
- Registry Windows pour les associations de fichiers

Ce guide couvre tous les aspects de l'interface graphique FTNatlink pour une utilisation efficace et un dépannage réussi.