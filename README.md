# Projet : Visualiation de données massives
# Analyse des Conflits Armés Mondiaux (1946-2024)

**Auteur :** RONDEAU Arthur  
**Formation :** Master 1 Informatique Big Data - Université Paris 8

---

## 📋 Description du Projet

Projet de visualisation interactive des conflits armés à l'échelle mondiale utilisant les données de l'**Uppsala Conflict Data Program (UCDP)**. Le projet combine un pipeline Python de préparation des données et un dashboard Tableau avec 8 visualisations complémentaires pour analyser 78 ans de conflits armés.

---

## 📊 Le Dataset

**Source :** UCDP PRIO Armed Conflict Dataset v25.1  
**Volume :** 2 752 enregistrements | 303 conflits uniques | 119 pays affectés  
**Période :** 1946 - 2024 (78 ans d'historique)  
**Périmètre :** Conflits impliquant au moins un État (guerres interétatiques, guerres civiles, interventions militaires)

### Types de conflits
- **Interstate** : Guerres entre États (ex: Russie vs Ukraine 2022) - 5%
- **Interne** : Guerres civiles - 73%
- **Internationalisé** : Guerres civiles avec intervention étrangère - 18%
- **Extrasystémique** : Conflits coloniaux - 4%

### Variables enrichies
- **Géographie** : `Pays Carte`, `region_label` (Europe, Asie, Afrique, Moyen-Orient, Amériques)
- **Temporalité** : `Decennie Text`, `periode_historique` (9 périodes : Post-WW2, Guerre Froide, Post-URSS...)
- **Typologie** : `type_conflit_label`, `objet_conflit` (Territoire vs Gouvernement)
- **Intensité** : `intensite_label` (Mineur: 25-999 morts, Guerre: 1000+ morts)
- **Statistiques** : `Duree Conflit`, `nb_annees`, `intensite_max`, `conflit_actif`
- **Focus** : `est_ukraine_russie`, `Adversaire Ukraine Simplifié`

---

## 🎨 Les 7 Visualisations

### 1. Carte Mondiale Interactive
**Principe :** Cercles proportionnels au nombre de conflits par pays, colorés selon l'intensité (orange=mineur, rouge=guerre). Filtrable par année via slider.

### 2. Timeline Évolution (1946-2024)
**Principe :** Lignes empilées montrant l'évolution du nombre de conflits dans le temps, par type de conflit.

### 3. Top 10 Pays Affectés
**Principe :** Barres horizontales des 10 pays avec le plus de conflits, avec gradient de couleur (rouge = plus touché).

### 4. Heatmap Décennie × Région
**Principe :** Grille colorée (9 décennies × 5 régions) où l'intensité de couleur représente le nombre de conflits. Identifie les zones chaudes à chaque époque.

### 5. Treemap Types de Conflits
**Principe :** Rectangles proportionnels au nombre de conflits par type (Interstate, Interne, Internationalisé, Extrasystémique).

### 6. Top 5 Conflits les Plus Longs
**Principe :** Barres horizontales des 5 conflits avec la plus grande durée (calculée avec `annee_fin - annee_debut + 1`).

### 7. Heatmap Ukraine-Russie
**Principe :** Grille année × adversaire montrant l'évolution du conflit 2014-2024. Couleur = intensité. Suit l'escalade du conflit.

---

## 📈 Résultats et Interprétations

### Principaux Insights

**Géographie :**
- **Myanmar leader** avec ~303 conflits (26% du total), suivi de l'Inde (187) et de l'Éthiopie (132)
- **L'Asie concentre 39%** des conflits, suivie de l'Afrique (33%)
- **Le Moyen-Orient** représente 14% malgré sa petite taille géographique

**Évolution :**
- **Tendance croissante** : +300% de conflits depuis 1946 (72 → 287)
- **Pic historique** dans les années 2010 (456 conflits) lié au Printemps arabe
- **61 conflits actifs en 2024**, dont des guerres majeures (Ukraine, Gaza, Myanmar)

**Typologie :**
- **73% de conflits internes** : domination écrasante des guerres civiles
- **Seulement 5% interétatiques** : déclin des guerres État vs État
- **18% internationalisés** : guerres civiles avec interventions étrangères

**Enjeux :**
- **55% territoriaux** : séparatisme, contrôle de régions, frontières
- **44% gouvernementaux** : qui contrôle l'État, légitimité du régime

**Ukraine-Russie :**
- **2014** : année charnière (Maïdan, Crimée, Donbass)
- **2022** : escalade majeure avec invasion russe
- **2024** : conflit toujours actif avec soutien nord-coréen

**Conflits les plus longs :**
- Philippines : Insurrection communiste **79 ans** (1946-2024, incluant Hukbalahap puis CPP)
- Myanmar vs CPB : **77 ans**
- Myanmar vs KNU : **76 ans**
- Myanmar vs KIO : **76 ans**
- Turquie vs PKK : **41 ans**

---

## 🚀 Installation et Lancement

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
- Ouvrir lien Tableau publique ou télécharger fichier .twb provenant du repo Github (avec jeu de données nettoyé)

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