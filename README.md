# Projet Visualisation Big Data - Conflits Armés Mondiaux

**Auteur:** Arthur  
**Formation:** Master 1 - Informatique Big Data 
**Université:** Paris 8  
**Cours:** Visualisation Big Data

## 📋 Description

Projet d'analyse géopolitique des conflits armés à l'échelle mondiale (1946-2024) utilisant les données de l'Uppsala Conflict Data Program (UCDP). Ce projet comprend un pipeline Python de préparation des données et une visualisation interactive sous Tableau.

## 📁 Structure du Projet

```
projet_conflits_armes/
│
├── main.py                 # Script principal d'exécution
├── README.md              # Ce fichier
│
├── src/
│   └── pipeline.py        # Pipeline de transformation des données
│
├── data/                  # Données sources (à placer ici)
│   └── UcdpPrioConflict_v25_1.csv
│
└── outputs/               # Fichiers générés
    └── UCDP_Conflicts_Tableau_Ready.csv
```

## 🚀 Utilisation

### Prérequis

```bash
pip install pandas numpy
```

### Exécution du Pipeline

```bash
python main.py
```

Le script :
1. Charge le dataset UCDP brut
2. Applique toutes les transformations
3. Génère le fichier CSV prêt pour Tableau
4. Affiche les statistiques récapitulatives

## 🔧 Fonctionnalités du Pipeline

Le fichier `pipeline.py` contient 17 fonctions modulaires :

### Chargement
- `load_data()` - Chargement du CSV source

### Enrichissement des labels
- `add_conflict_type_labels()` - Types de conflits (Interstate, Interne, etc.)
- `add_intensity_labels()` - Niveaux d'intensité (Mineur, Guerre)
- `add_region_labels()` - Régions géographiques
- `add_incompatibility_labels()` - Objets du conflit (Territoire, Gouvernement)

### Dimensions temporelles
- `add_historical_periods()` - Périodes historiques contextualisées
- `add_decade()` - Décennies

### Géographie
- `extract_primary_country()` - Extraction du pays principal

### Calculs et statistiques
- `calculate_conflict_duration()` - Durée en années
- `add_conflict_statistics()` - Stats agrégées par conflit
- `flag_active_conflicts()` - Identification des conflits actifs

### Flags spéciaux
- `flag_ukraine_russia_conflicts()` - Flag Ukraine-Russie

### Nettoyage
- `clean_dates()` - Conversion des dates
- `select_final_columns()` - Sélection des colonnes pertinentes
- `sort_data()` - Tri des données

### Export
- `save_to_csv()` - Sauvegarde en CSV
- `generate_summary_statistics()` - Statistiques descriptives

### Pipeline complet
- `run_full_pipeline()` - Exécution orchestrée de toutes les étapes

## 📊 Variables Générées

### Identifiants
- `conflict_id`, `year`, `decennie`, `periode_historique`

### Géographie
- `location`, `pays_principal`, `region`, `region_label`

### Acteurs
- `side_a`, `side_b`, `side_a_2nd`, `side_b_2nd`

### Type de conflit
- `type_of_conflict`, `type_conflit_label`, `incompatibility`, `objet_conflit`

### Intensité
- `intensity_level`, `intensite_label`, `cumulative_intensity`

### Temporalité
- `start_date_clean`, `ep_end_date_clean`, `duree_annees`, `annee_debut`, `annee_fin`

### Statistiques
- `nb_annees`, `intensite_max`, `conflit_actif`

### Flags
- `est_ukraine_russie` (1 si implique Ukraine/Russie, 0 sinon)

## 📈 Données Produites

Le dataset final contient :
- **~2750 enregistrements** de conflits armés
- **34 colonnes** enrichies et prêtes pour l'analyse
- **Période:** 1946-2024 (78 ans d'historique)

## 🎯 Utilisation dans Tableau

Le fichier CSV généré peut être importé directement dans Tableau pour créer :
- Cartes géographiques interactives
- Timelines temporelles
- Analyses typologiques
- Dashboard Ukraine-Russie
- Comparaisons régionales

## 📖 Source des Données

**Uppsala Conflict Data Program (UCDP) v25.1**  
Department of Peace and Conflict Research, Uppsala University  
URL: https://ucdp.uu.se/downloads/

## 📝 Notes

- Les labels sont en français pour faciliter la visualisation
- Les périodes historiques sont pré-définies pour contextualiser les conflits
- Le flag Ukraine-Russie permet un filtrage rapide sur ce conflit majeur
- Toutes les fonctions sont documentées et modulaires pour faciliter la maintenance