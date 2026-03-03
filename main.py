import sys
import os
from pathlib import Path

# Ajouter le dossier src au PATH
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from pipeline import run_full_pipeline


def main():
    """
    Point d'entrée principal du programme.
    """
    # Chemins des fichiers
    INPUT_FILE = 'data/UcdpPrioConflict_v25_1.csv'
    OUTPUT_FILE = 'results/UCDP_Conflicts_Tableau_Ready.csv'
    
    # Vérifier que le fichier d'entrée existe
    if not os.path.exists(INPUT_FILE):
        print(f"❌ ERREUR: Le fichier {INPUT_FILE} n'existe pas!")
        print(f"   Veuillez vérifier le chemin du fichier source.")
        return 1
    
    # Exécuter le pipeline
    try:
        df_final, statistics = run_full_pipeline(INPUT_FILE, OUTPUT_FILE)
        
        print(f"\n{'='*80}")
        print("📁 FICHIER GÉNÉRÉ")
        print(f"{'='*80}")
        print(f"📍 Localisation: {OUTPUT_FILE}")
        print(f"📊 Dimensions: {len(df_final)} lignes × {len(df_final.columns)} colonnes")
        print(f"\n✨ Le dataset est prêt pour Tableau !")
        print(f"{'='*80}\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERREUR lors de l'exécution du pipeline:")
        print(f"   {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)