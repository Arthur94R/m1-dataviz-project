# Projet : Visualiation de données massives
# Analyse des conflits armés mondiaux (1946-2024)

**Auteur :** RONDEAU Arthur  
**Formation :** Master 1 Informatique Big Data - Université Paris 8

---

## Description du projet

Projet de visualisation interactive des conflits armés à l'échelle mondiale utilisant les données de l'**Uppsala Conflict Data Program (UCDP)**. Le projet combine un pipeline Python de préparation des données et un dashboard Tableau avec 8 visualisations complémentaires pour analyser 78 ans de conflits armés.

---

## Le Dataset

**Source :** UCDP PRIO Armed Conflict Dataset v25.1  
**Volume :** 2 752 enregistrements | 303 conflits uniques | 119 pays affectés  
**Période :** 1946 - 2024 (78 ans d'historique)  
**Périmètre :** Conflits impliquant au moins un État (guerres interétatiques, guerres civiles, interventions militaires)

### Types de conflits
- **Interstate** : Guerres entre États (ex: Russie vs Ukraine 2022)
- **Interne** : Guerres civiles
- **Internationalisé** : Guerres civiles avec intervention étrangère
- **Extrasystémique** : Conflits coloniaux

### Variables enrichies
- **Géographie** : `Pays Carte`, `region_label` (Europe, Asie, Afrique, Moyen-Orient, Amériques)
- **Temporalité** : `Decennie Text`, `periode_historique` (Post-WW2, Guerre Froide, Post-URSS...)
- **Typologie** : `type_conflit_label`, `objet_conflit` (Territoire vs Gouvernement)
- **Intensité** : `intensite_label` (Mineur: 25-999 morts, Guerre: 1000+ morts)
- **Statistiques** : `Duree Conflit`, `nb_annees`, `intensite_max`, `conflit_actif`
- **Focus** : `est_ukraine_russie`, `Adversaire Ukraine Simplifié`

---

## Les 7 visualisations

### 1. Carte mondiale interactive
**Principe :** Cercles proportionnels au nombre de conflits par pays, colorés selon l'intensité (orange=mineur, rouge=guerre). Filtrable par année via slider.

### 2. Répartition par régions
**Principe :** Barres horizontales des régions avec leur nombre de conflits à chacune.

### 3. Timeline évolution (1946-2024)
**Principe :** Lignes empilées montrant l'évolution du nombre de conflits dans le temps, par type de conflit.

### 4. Top 10 pays affectés
**Principe :** Barres horizontales des 10 pays avec le plus de conflits, avec gradient de couleur (rouge = plus touché).

### 5. Heatmap décennie × région
**Principe :** Grille colorée (9 décennies × 5 régions) où l'intensité de couleur représente le nombre de conflits. Identifie les zones chaudes à chaque époque.

### 6. Top 5 conflits les plus longs
**Principe :** Barres horizontales des 5 conflits avec la plus grande durée (calculée avec `annee_fin - annee_debut + 1`).

### 7. Heatmap Ukraine-Russie
**Principe :** Grille année × adversaire montrant l'évolution du conflit 2014-2024. Couleur = intensité. Suit l'escalade du conflit.

---

## Résultats et interprétations

### Principaux insights
 
**Géographie :**
- **L'Inde en tête** avec le plus grand nombre de conflits, suivi de la Russie
- **L'Afrique concentre le plus de conflits**, suivie de l'Asie et de l'Europe
 
**Évolution :**
- **Tendance croissante en Asie & Afrique** depuis 1946 : multiplication des conflits au fil des décennies
- **Pic visible** dans les années 2010 en Afrique
- **Nombreux conflits toujours actifs** depuis 2020
 
**Ukraine-Russie :**
- **2014** : début du conflit (multiple adversaires : Maïdan, DPR, LPR)
- **2022-2024** : intensification maximale (guerre totale)
 
**Conflits les plus longs :**
- **Philippines : 79 ans** d'insurrection communiste continue
- **Myanmar : 3 conflits de 76-77 ans** (instabilité chronique)
- **Turquie vs PKK : 41 ans**
 
---

## Installation et lancement

### Prérequis
```bash
Python 3.8+
pandas
numpy
Tableau Desktop
```

### Installation
```bash
cd projet_conflits_armes
pip install pandas numpy
```

### Exécution
```bash
python main.py
```
**Sortie :** `UCDP_Conflicts_Tableau_Ready.csv` dans `/outputs/`

### Visualisation Tableau
- Ouvrir lien [Tableau publique](https://public.tableau.com/app/profile/arthur.rondeau/viz/projet_17745227569860/Timelineconflits?publish=yes) ou télécharger fichier .twb provenant du repo Github (avec jeu de données nettoyé)

---

### Pipeline (17 fonctions modulaires)

**main.py (59 lignes)** : Gestion des chemins, vérification des fichiers, appel du pipeline, gestion d'erreurs.

**pipeline.py (503 lignes)** :

- **Chargement** : `load_data()` - Lecture CSV avec pandas
- **Enrichissement** : `add_conflict_type_labels()`, `add_intensity_labels()`, `add_region_labels()`, `add_incompatibility_labels()` - Labels en français
- **Temporalité** : `add_historical_periods()`, `add_decade()` - Périodes et décennies
- **Géographie** : `extract_primary_country()` - Extraction pays principal
- **Calculs** : `calculate_conflict_duration()`, `add_conflict_statistics()`, `flag_active_conflicts()` - Stats et durées
- **Flags** : `flag_ukraine_russia_conflicts()` - Détection Ukraine/Russie
- **Nettoyage** : `clean_dates()`, `select_final_columns()`, `sort_data()` - Dates, colonnes, tri
- **Export** : `save_to_csv()`, `generate_summary_statistics()` - CSV + stats
- **Orchestration** : `run_full_pipeline()` - Exécution séquentielle