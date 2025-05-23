# 🕐 Application de Gestion des Horaires de Travail

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Une application web moderne et intuitive pour gérer vos horaires de travail avec calcul automatique des heures et détection des heures supplémentaires.

## ✨ Fonctionnalités

- ✅ Ajout des horaires du matin et de l'après-midi pour chaque jour
- ✅ Calcul automatique du total d'heures par jour
- ✅ Calcul du total hebdomadaire
- ✅ Alerte quand vous dépassez 36h30 par semaine
- ✅ Export des données en CSV
- ✅ Base de données SQLite intégrée
- ✅ Interface web responsive
- ✅ Déployable avec Docker

## Structure des fichiers

```
gestion-horaires/
├── app.py                  # Application Flask principale
├── templates/
│   └── index.html         # Interface utilisateur
├── requirements.txt       # Dépendances Python
├── Dockerfile            # Configuration Docker
├── docker-compose.yml    # Configuration Docker Compose
└── README.md            # Ce fichier
```

## Installation

### Option 1 : Avec Docker (Recommandé)

1. Clonez ou créez les fichiers dans un dossier
2. Construisez et lancez l'application :

```bash
docker-compose up -d
```

3. Accédez à l'application : http://localhost:5000

### Option 2 : Sans Docker

1. Installez Python 3.11 ou supérieur
2. Créez un environnement virtuel :

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installez les dépendances :

```bash
pip install -r requirements.txt
```

4. Créez le dossier templates et placez-y index.html
5. Lancez l'application :

```bash
python app.py
```

## Utilisation

1. **Ajouter un horaire** :
   - Sélectionnez la date
   - Entrez vos horaires du matin (début et fin)
   - Entrez vos horaires de l'après-midi (début et fin)
   - Cliquez sur "Enregistrer"

2. **Visualiser la semaine** :
   - Les horaires de la semaine courante s'affichent automatiquement
   - Utilisez le sélecteur de semaine pour voir d'autres semaines
   - Le total hebdomadaire est affiché en bas

3. **Heures supplémentaires** :
   - Si vous dépassez 36h30, une alerte s'affiche
   - Les heures supplémentaires sont calculées et affichées en rouge

4. **Export des données** :
   - Cliquez sur "Exporter en CSV" pour télécharger vos horaires

## Gestion Docker

### Arrêter l'application
```bash
docker-compose down
```

### Voir les logs
```bash
docker-compose logs -f
```

### Redémarrer l'application
```bash
docker-compose restart
```

### Sauvegarder la base de données
```bash
docker run --rm -v gestion-horaires_horaires-data:/data -v $(pwd):/backup alpine tar czf /backup/horaires-backup.tar.gz -C /data .
```

## 📱 Captures d'écran

### Interface principale
- Design moderne avec animations fluides
- Navigation intuitive par semaine
- Statistiques en temps réel

### Fonctionnalités
- ✨ Interface moderne et responsive
- 📊 Visualisation claire des heures travaillées
- 🚨 Alertes automatiques pour les heures supplémentaires
- 💾 Export CSV des données
- 🐳 Déployable facilement avec Docker

## 🛠️ Technologies utilisées

- **Backend** : Python 3.11, Flask 3.0.0
- **Base de données** : SQLite avec SQLAlchemy
- **Frontend** : HTML5, CSS3, JavaScript vanilla
- **Icônes** : Font Awesome 6.0
- **Containerisation** : Docker & Docker Compose

## 📈 Roadmap

- [ ] Intégration Google Sheets
- [ ] Mode sombre
- [ ] Graphiques de statistiques
- [ ] Export PDF
- [ ] Application mobile
- [ ] Notifications push
- [ ] Multi-utilisateurs
- [ ] Gestion des congés

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

## 📝 Notes techniques

- La base de données SQLite est stockée dans un volume Docker pour persister les données
- L'application redémarre automatiquement en cas d'erreur
- Les horaires sont calculés en heures décimales (ex: 8h30 = 8.5)
- Format d'affichage : HH:MM
- Limite hebdomadaire : 36h30 (configurable)

## 🔮 Intégration Google Sheets (Future amélioration)

Pour intégrer Google Sheets, vous pourriez ajouter :
1. L'API Google Sheets
2. L'authentification OAuth2
3. Un bouton pour synchroniser avec Google Sheets

Cette fonctionnalité nécessiterait des clés API Google et une configuration supplémentaire.