import pandas as pd
import numpy as np
from typing import Dict, Tuple


def load_data(filepath: str) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    print(f"   ✓ {len(df)} enregistrements chargés")
    print(f"   ✓ Période: {df['year'].min()} - {df['year'].max()}")
    return df


def add_conflict_type_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute des labels explicites pour les types de conflits.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec la colonne 'type_conflit_label'
    """
    print("Ajout des labels de type de conflit...")
    
    conflict_type_map = {
        1: "Extrasystémique",
        2: "Interstate",
        3: "Interne",
        4: "Internationalisé"
    }
    
    df['type_conflit_label'] = df['type_of_conflict'].map(conflict_type_map)
    print(f"   ✓ Labels ajoutés: {df['type_conflit_label'].nunique()} types distincts")
    return df


def add_intensity_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute des labels explicites pour l'intensité des conflits.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec la colonne 'intensite_label'
    """
    print("Ajout des labels d'intensité...")
    
    intensity_map = {
        1: "Mineur (25-999 morts)",
        2: "Guerre (1000+ morts)"
    }
    
    df['intensite_label'] = df['intensity_level'].map(intensity_map)
    
    # Intensité cumulée
    df['intensite_cumulee_label'] = df['cumulative_intensity'].map({
        0: "Pas encore de guerre",
        1: "A connu la guerre"
    })
    
    print(f"   ✓ {df['intensite_label'].value_counts().to_dict()}")
    return df


def add_region_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute des labels explicites pour les régions géographiques.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec la colonne 'region_label'
    """
    print("Ajout des labels de région...")
    
    region_map = {
        1: "Europe",
        2: "Moyen-Orient",
        3: "Asie",
        4: "Afrique",
        5: "Amériques"
    }
    
    # Gérer les régions multiples (prendre la première)
    def extract_primary_region(region_value):
        if pd.isna(region_value):
            return np.nan
        first_region = int(str(region_value).split(',')[0].strip())
        return region_map.get(first_region)
    
    df['region_label'] = df['region'].apply(extract_primary_region)
    print(f"   ✓ Régions: {df['region_label'].value_counts().to_dict()}")
    return df


def add_incompatibility_labels(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute des labels pour l'objet du conflit (incompatibilité).
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec la colonne 'objet_conflit'
    """
    print("Ajout des labels d'objet de conflit...")
    
    incompatibility_map = {
        1: "Territoire",
        2: "Gouvernement",
        3: "Territoire + Gouvernement"
    }
    
    df['objet_conflit'] = df['incompatibility'].map(incompatibility_map)
    print(f"   ✓ Objets: {df['objet_conflit'].value_counts().to_dict()}")
    return df


def add_historical_periods(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crée des périodes historiques pour contextualiser les conflits.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec la colonne 'periode_historique'
    """
    print("Création des périodes historiques...")
    
    def get_periode(year):
        if year < 1950:
            return "1946-1949: Post-WW2"
        elif year < 1960:
            return "1950-1959: Guerre de Corée"
        elif year < 1970:
            return "1960-1969: Décolonisation"
        elif year < 1980:
            return "1970-1979: Guerre Froide"
        elif year < 1990:
            return "1980-1989: Fin Guerre Froide"
        elif year < 2000:
            return "1990-1999: Post-URSS"
        elif year < 2010:
            return "2000-2009: Guerre contre terrorisme"
        elif year < 2020:
            return "2010-2019: Printemps arabe"
        else:
            return "2020-2024: Conflits contemporains"
    
    df['periode_historique'] = df['year'].apply(get_periode)
    print(f"   ✓ {df['periode_historique'].nunique()} périodes créées")
    return df


def add_decade(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute la décennie pour chaque enregistrement.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec la colonne 'decennie'
    """
    print("Ajout de la décennie...")
    
    df['decennie'] = (df['year'] // 10) * 10
    print(f"   ✓ Décennies: {df['decennie'].min()} - {df['decennie'].max()}")
    return df


def flag_ukraine_russia_conflicts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifie les conflits impliquant Ukraine et/ou Russie.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec la colonne 'est_ukraine_russie'
    """
    print("Identification des conflits Ukraine-Russie...")
    
    df['est_ukraine_russie'] = (
        (df['location'].str.contains('Ukraine', na=False, case=False)) | 
        (df['side_a'].str.contains('Ukraine|Russia', na=False, case=False)) |
        (df['side_b'].str.contains('Ukraine|Russia', na=False, case=False))
    ).astype(int)
    
    ukraine_russia_count = df['est_ukraine_russie'].sum()
    print(f"   ✓ {ukraine_russia_count} enregistrements Ukraine/Russie identifiés")
    return df


def extract_primary_country(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extrait le pays principal de la colonne location.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec la colonne 'pays_principal'
    """
    print("Extraction du pays principal...")
    
    df['pays_principal'] = df['location'].str.split(',').str[0].str.strip()
    print(f"   ✓ {df['pays_principal'].nunique()} pays distincts")
    return df


def clean_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Nettoie et convertit les dates au format datetime.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec les colonnes de dates nettoyées
    """
    print("Nettoyage des dates...")
    
    df['start_date_clean'] = pd.to_datetime(df['start_date'], errors='coerce')
    df['ep_end_date_clean'] = pd.to_datetime(df['ep_end_date'], errors='coerce')
    
    valid_start = df['start_date_clean'].notna().sum()
    valid_end = df['ep_end_date_clean'].notna().sum()
    print(f"   ✓ Dates de début valides: {valid_start}")
    print(f"   ✓ Dates de fin valides: {valid_end}")
    return df


def calculate_conflict_duration(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcule la durée des conflits en années.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec la colonne 'duree_annees'
    """
    print("Calcul de la durée des conflits...")
    
    df['duree_annees'] = df.groupby('conflict_id')['year'].transform('count')
    
    max_duration = df['duree_annees'].max()
    print(f"   ✓ Durée maximale: {max_duration} années")
    return df


def flag_active_conflicts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Identifie les conflits toujours actifs (sans date de fin).
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec la colonne 'conflit_actif'
    """
    print("Identification des conflits actifs...")
    
    df['conflit_actif'] = df['ep_end'].fillna(0).astype(int) == 0
    
    active_count = df['conflit_actif'].sum()
    print(f"   ✓ {active_count} conflits actifs (sans date de fin)")
    return df


def add_conflict_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute des statistiques agrégées par conflict_id.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame enrichi avec statistiques par conflit
    """
    print("Calcul des statistiques par conflit...")
    
    conflict_stats = df.groupby('conflict_id').agg({
        'year': ['min', 'max', 'count'],
        'intensity_level': 'max'
    }).reset_index()
    
    conflict_stats.columns = ['conflict_id', 'annee_debut', 'annee_fin', 'nb_annees', 'intensite_max']
    
    df = df.merge(conflict_stats, on='conflict_id', how='left')
    
    print(f"   ✓ Statistiques calculées pour {df['conflict_id'].nunique()} conflits uniques")
    return df


def select_final_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Sélectionne et réorganise les colonnes finales pour Tableau.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame avec uniquement les colonnes pertinentes
    """
    print("Sélection des colonnes finales...")
    
    colonnes_finales = [
        # Identifiants
        'conflict_id',
        'year',
        'decennie',
        'periode_historique',
        
        # Géographie
        'location',
        'pays_principal',
        'region',
        'region_label',
        'gwno_loc',
        
        # Acteurs
        'side_a',
        'side_b',
        'side_a_2nd',
        'side_b_2nd',
        
        # Type et nature du conflit
        'type_of_conflict',
        'type_conflit_label',
        'incompatibility',
        'objet_conflit',
        'territory_name',
        
        # Intensité
        'intensity_level',
        'intensite_label',
        'cumulative_intensity',
        'intensite_cumulee_label',
        
        # Dates
        'start_date',
        'start_date_clean',
        'ep_end_date',
        'ep_end_date_clean',
        'ep_end',
        
        # Statistiques
        'duree_annees',
        'annee_debut',
        'annee_fin',
        'nb_annees',
        'intensite_max',
        'conflit_actif',
        
        # Flags spéciaux
        'est_ukraine_russie'
    ]
    
    df_final = df[colonnes_finales]
    print(f"   ✓ {len(colonnes_finales)} colonnes sélectionnées")
    return df_final


def sort_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trie les données par année décroissante et conflict_id.
    
    Args:
        df: DataFrame source
        
    Returns:
        DataFrame trié
    """
    print("Tri des données...")
    
    df = df.sort_values(['year', 'conflict_id'], ascending=[False, True])
    print(f"   ✓ Données triées par année (décroissant) et conflict_id")
    return df


def save_to_csv(df: pd.DataFrame, output_path: str) -> None:
    """
    Sauvegarde le DataFrame en CSV optimisé pour Tableau.
    
    Args:
        df: DataFrame à sauvegarder
        output_path: Chemin de sortie du fichier CSV
    """
    print(f"Sauvegarde vers {output_path}...")
    
    df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"   ✓ Fichier sauvegardé avec succès")
    print(f"   ✓ {len(df)} lignes × {len(df.columns)} colonnes")


def generate_summary_statistics(df: pd.DataFrame) -> Dict:
    """
    Génère des statistiques descriptives du dataset final.
    
    Args:
        df: DataFrame final
        
    Returns:
        Dictionnaire avec les statistiques clés
    """
    print("\n" + "="*80)
    print("📊 STATISTIQUES RÉCAPITULATIVES")
    print("="*80)
    
    stats = {
        'total_records': len(df),
        'total_conflicts': df['conflict_id'].nunique(),
        'countries': df['pays_principal'].nunique(),
        'period': f"{df['year'].min()} - {df['year'].max()}",
        'active_conflicts': df['conflit_actif'].sum(),
        'ukraine_russia': df['est_ukraine_russie'].sum(),
        'conflicts_2024': len(df[df['year'] == 2024])
    }
    
    print(f"Enregistrements totaux    : {stats['total_records']}")
    print(f"Conflits uniques          : {stats['total_conflicts']}")
    print(f"Pays affectés             : {stats['countries']}")
    print(f"Période couverte          : {stats['period']}")
    print(f"Conflits actifs           : {stats['active_conflicts']}")
    print(f"Conflits Ukraine-Russie   : {stats['ukraine_russia']}")
    print(f"Conflits en 2024          : {stats['conflicts_2024']}")
    
    print(f"\n📈 Répartition par type de conflit:")
    print(df['type_conflit_label'].value_counts().to_string())
    
    print(f"\n🌍 Répartition par région:")
    print(df['region_label'].value_counts().to_string())
    
    print("\n" + "="*80)
    
    return stats


def run_full_pipeline(input_path: str, output_path: str) -> Tuple[pd.DataFrame, Dict]:
    """
    Exécute le pipeline complet de transformation des données.
    
    Args:
        input_path: Chemin vers le fichier CSV source
        output_path: Chemin vers le fichier CSV de sortie
        
    Returns:
        Tuple contenant le DataFrame final et les statistiques
    """
    print("\n" + "="*80)
    print("🚀 DÉMARRAGE DU PIPELINE DE PRÉPARATION DES DONNÉES")
    print("="*80 + "\n")
    
    # Chargement
    df = load_data(input_path)
    
    # Transformations
    df = add_conflict_type_labels(df)
    df = add_intensity_labels(df)
    df = add_region_labels(df)
    df = add_incompatibility_labels(df)
    df = add_historical_periods(df)
    df = add_decade(df)
    df = flag_ukraine_russia_conflicts(df)
    df = extract_primary_country(df)
    df = clean_dates(df)
    df = calculate_conflict_duration(df)
    df = flag_active_conflicts(df)
    df = add_conflict_statistics(df)
    df = select_final_columns(df)
    df = sort_data(df)
    
    # Sauvegarde
    save_to_csv(df, output_path)
    
    # Statistiques finales
    stats = generate_summary_statistics(df)
    
    print("\n✅ PIPELINE TERMINÉ AVEC SUCCÈS !\n")
    
    return df, stats