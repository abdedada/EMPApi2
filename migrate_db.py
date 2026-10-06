"""
Script de migration pour supprimer la colonne 'prenom' de la table 'students'
"""
import os
import sys
from sqlalchemy import inspect
from database import Base, engine
import models

def migrate_database():
    """Migrer la base de données"""
    
    print("=" * 60)
    print("Migration de la base de donnees")
    print("=" * 60)
    
    # Vérifier si la table students existe
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    
    if 'students' not in tables:
        print("[!] La table 'students' n'existe pas. Creation de toutes les tables...")
        Base.metadata.create_all(bind=engine)
        print("[OK] Toutes les tables ont ete creees avec succes!")
        return
    
    # Vérifier les colonnes existantes
    columns = inspector.get_columns('students')
    column_names = [col['name'] for col in columns]
    
    print(f"\nColonnes actuelles de la table 'students': {column_names}")
    
    # Vérifier si la colonne 'prenom' existe et doit être supprimée
    needs_migration = 'prenom' in column_names
    
    if needs_migration:
        print("\n[*] Migration requise. La colonne 'prenom' va etre supprimee...")
        print("Suppression de la colonne 'prenom' de la table 'students'...")
        
        # Utiliser ALTER TABLE pour supprimer la colonne
        from sqlalchemy import text
        
        with engine.connect() as connection:
            try:
                # Supprimer la colonne 'prenom' si elle existe
                connection.execute(text("ALTER TABLE students DROP COLUMN prenom"))
                connection.commit()
                print("[OK] Colonne 'prenom' supprimee")
                
                print("\n[OK] Migration reussie!")
                
            except Exception as e:
                connection.rollback()
                print(f"[!] Erreur lors de la migration: {e}")
                sys.exit(1)
    else:
        print("\n[OK] La colonne 'prenom' n'existe pas. Aucune migration necessaire!")

if __name__ == "__main__":
    migrate_database()
