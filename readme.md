# Gestionnaire de Données Vidéo pour Caméras de Surveillance

## Description

Ce projet a pour objectif de créer un logiciel innovant capable de gérer efficacement les données vidéo enregistrées par les caméras de surveillance. Notre solution permet d’enregistrer sélectivement des séquences vidéo basées sur la détection d’objets spécifiques tels que les humains, les animaux, les véhicules, etc.

## Fonctionnalités

- **Spécification d'objets à détecter** : Les utilisateurs peuvent spécifier les objets à détecter, tels que humains, animaux, et véhicules.
- **Enregistrement sélectif des séquences vidéo** : Le logiciel autorise l'enregistrement sélectif des séquences vidéo en fonction de la détection d'objets spécifiques.
- **Classification automatique des séquences** : Les séquences vidéo sont automatiquement classées dans des dossiers dédiés selon la catégorie détectée.

## Technologies

- **YOLOv8** : Utilisé pour la détection d'objets en temps réel.
- **FastAPI** : Back-end rapide et performant pour gérer les API et les communications avec le système de stockage.
- **Angular 16** : Front-end moderne pour une interface utilisateur fluide et réactive.

## Installation

1. **Cloner le dépôt :**

    ```bash
    git clone https://github.com/AYMEN-MEGBLI/video-surveillance-backup-manager.git
    ```

2. **Installer les dépendances du back-end :**

    ```bash
    cd backend
    yolo_venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Installer les dépendances du front-end :**

    ```bash
    cd frontend
    npm install
    ```

4. **Lancer le serveur FastAPI :**

    ```bash
    cd backend\src\controllers
    uvicorn MainController:app --reload
    ```

5. **Lancer le serveur Angular :**

    ```bash
    cd frontend
    ng serve -o
    ```

## Utilisation

1. Accédez à l'interface utilisateur via votre navigateur à l'adresse `http://localhost:4200`.
2. Spécifiez les objets que vous souhaitez détecter (humains, animaux, véhicules).
3. Surveillez les séquences vidéo enregistrées et classées automatiquement en fonction des objets détectés.

## Contributions

Les contributions sont les bienvenues ! Veuillez soumettre une pull request ou ouvrir une issue pour discuter des changements proposés.

## Licence

Ce projet est sous licence [Licence GPL-3.0 license](LICENSE).
