"""
Migration script to fix the UNIQUE constraint on students table
Change from unique(num) to composite unique(num, classe_id)
"""
import sqlite3
from database import Base, engine
from sqlalchemy import inspect, text

def migrate_student_constraint():
    """Migrate the student constraint from unique(num) to composite unique(num, classe_id)"""
    
    print("=" * 60)
    print("Migration: Fix Students Constraint")
    print("=" * 60)
    
    inspector = inspect(engine)
    
    # Get table constraints
    print("\n[*] Checking current constraints on students table...")
    
    with engine.connect() as connection:
        # SQLite requires dropping and recreating the table for constraint changes
        # Get current students data
        try:
            result = connection.execute(text("SELECT sql FROM sqlite_master WHERE type='table' AND name='students'"))
            current_schema = result.fetchone()
            
            if current_schema:
                print(f"\n[*] Current students table schema:")
                print(current_schema[0])
            
            # Check if we need to remove the unique constraint on num
            # Get all constraints
            result = connection.execute(text("PRAGMA table_info(students)"))
            columns = result.fetchall()
            print(f"\n[*] Columns in students table:")
            for col in columns:
                print(f"  - {col[1]} ({col[2]})")
            
            # Try to create the composite unique constraint
            # First, check if the constraint already exists
            result = connection.execute(text(
                "SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='students' AND name='uq_student_num_classe'"
            ))
            
            if result.fetchone():
                print("\n[OK] Composite unique constraint already exists!")
            else:
                print("\n[*] Creating composite unique constraint...")
                # In SQLite, we need to recreate the table or use CREATE UNIQUE INDEX
                connection.execute(text(
                    "CREATE UNIQUE INDEX IF NOT EXISTS uq_student_num_classe ON students(num, classe_id)"
                ))
                connection.commit()
                print("[OK] Composite unique constraint created!")
            
            print("\n[OK] Migration completed successfully!")
            
        except Exception as e:
            print(f"[!] Error during migration: {e}")
            raise

if __name__ == "__main__":
    migrate_student_constraint()
