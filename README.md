# 🐦 Analyse des Tweets Saegus France

## 🎯 Le Projet
J'ai développé ce projet pour analyser les tweets de Saegus France et comprendre les tendances de communication sur leur compte Twitter. L'objectif était de créer un dashboard interactif permettant de visualiser les patterns d'engagement et les sujets principaux.

## 🚀 Mon Parcours

### 1. La Récupération des Données
J'ai commencé par développer un script Python pour récupérer les tweets via l'API Twitter. Malheureusement, la version gratuite de l'API ne permettait d'accéder qu'aux 100 derniers tweets. C'était une limitation frustrante, mais j'ai décidé de faire avec ce que j'avais !

### 2. Le Traitement des Données
J'ai dû faire face à plusieurs défis techniques :
- La structure complexe des données JSON
- Les valeurs manquantes dans certaines métriques
- La sérialisation des tableaux NumPy

Mais j'ai réussi à surmonter ces obstacles en créant des solutions personnalisées !

### 3. La Visualisation
J'ai choisi Plotly pour créer des visualisations interactives et modernes. J'ai développé un dashboard unique qui regroupe 6 graphiques différents :
- Distribution des tweets par jour
- Distribution des tweets par heure
- Engagement moyen par jour
- Engagement moyen par heure
- Top 15 des sujets principaux
- Top 15 des sujets par engagement

## 🛠️ Technologies Utilisées
- Python 3.x
- API Twitter (X)
- Pandas
- Plotly
- NumPy
- JSON

## 📊 Les Résultats
Malgré la limitation des données (100 derniers tweets), j'ai réussi à extraire des insights intéressants :
- Les moments optimaux pour poster
- Les sujets qui génèrent le plus d'engagement
- Les patterns de publication

## 🔮 Évolutions Futures
Pour améliorer ce projet, je pourrais :
- Passer à une version payante de l'API pour accéder à plus de données
- Ajouter des analyses de sentiment
- Créer un système de suivi en temps réel

## 🎨 Comment Utiliser le Dashboard
1. Clonez le repository
2. Installez les dépendances :
```bash
pip install -r requirements.txt
```
3. Exécutez le script :
```bash
python graph.py
```
4. Ouvrez le fichier `graphs/dashboard.html` dans votre navigateur

## 💡 Ce que J'ai Appris
Ce projet m'a permis de :
- Travailler avec une API externe
- Gérer des données complexes
- Créer des visualisations interactives
- Optimiser le traitement des données

## 🤝 Contribution
N'hésitez pas à contribuer à ce projet en :
- Proposant des améliorations
- Signalant des bugs
- Ajoutant de nouvelles fonctionnalités

## 📝 Licence
Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails. 