"""
Comprehensive migration to fix the students table constraint
Handles duplicate records and updates the constraint
"""
import sqlite3
from database import Base, engine
from sqlalchemy import inspect, text

def migrate_students_comprehensive():
    """Comprehensively migrate students table to allow same num in different classes"""
    
    print("=" * 60)
    print("Comprehensive Students Table Migration")
    print("=" * 60)
    
    with engine.connect() as connection:
        try:
            # 1. Check current state
            print("\n[*] Step 1: Checking current constraints...")
            
            # Get all indexes on students table
            result = connection.execute(text(
                "SELECT name, sql FROM sqlite_master WHERE type='index' AND tbl_name='students' AND sql IS NOT NULL"
            ))
            indexes = result.fetchall()
            
            if indexes:
                print(f"\n[*] Current unique indexes on students:")
                for idx_name, idx_sql in indexes:
                    print(f"  - {idx_name}: {idx_sql}")
                    
                # Check if there's a unique constraint on num alone
                for idx_name, idx_sql in indexes:
                    if 'num' in idx_sql and 'classe_id' not in idx_sql:
                        print(f"\n[*] Removing old unique constraint on 'num' alone...")
                        connection.execute(text(f"DROP INDEX IF EXISTS {idx_name}"))
                        print(f"[OK] Dropped {idx_name}")
            else:
                print("\n[OK] No unique indexes found")
            
            connection.commit()
            
            # 2. Check for duplicates across all classes
            print("\n[*] Step 2: Checking for duplicate student numbers...")
            result = connection.execute(text(
                """
                SELECT num, COUNT(*) as count 
                FROM students 
                GROUP BY num 
                HAVING count > 1
                """
            ))
            duplicates = result.fetchall()
            
            if duplicates:
                print(f"\n[!] Found {len(duplicates)} student numbers with duplicates:")
                for num, count in duplicates:
                    print(f"  - num='{num}': {count} instances")
                    
                    # Show these duplicates
                    result2 = connection.execute(text(
                        f"SELECT id, num, classe_id, nom FROM students WHERE num = '{num}' ORDER BY classe_id"
                    ))
                    for row in result2:
                        print(f"    - id={row[0]}, classe_id={row[3]}, nom={row[4]}")
            else:
                print("\n[OK] No duplicate student numbers found")
            
            # 3. Create composite unique constraint
            print("\n[*] Step 3: Creating composite unique constraint...")
            
            # Check if composite constraint already exists
            result = connection.execute(text(
                "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='students' AND name='uq_student_num_classe'"
            ))
            
            if result.fetchone():
                print("[OK] Composite unique constraint already exists!")
            else:
                connection.execute(text(
                    "CREATE UNIQUE INDEX uq_student_num_classe ON students(num, classe_id)"
                ))
                print("[OK] Composite unique constraint created!")
            
            connection.commit()
            
            print("\n" + "=" * 60)
            print("[OK] Migration completed successfully!")
            print("=" * 60)
            
        except Exception as e:
            connection.rollback()
            print(f"\n[!] Error during migration: {e}")
            raise

if __name__ == "__main__":
    migrate_students_comprehensive()
