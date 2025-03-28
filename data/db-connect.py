import sqlite3

def copy_table(source_db, target_db, table_name):
    # Connect to both databases
    source_conn = sqlite3.connect(source_db)
    target_conn = sqlite3.connect(target_db)
    
    source_cursor = source_conn.cursor()
    target_cursor = target_conn.cursor()

    try:
        # Get the table schema from the source database
        source_cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        schema = source_cursor.fetchone()[0]

        # Create the table in the target database if it doesn't exist
        target_cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        target_cursor.execute(schema)

        # Copy data from source to target
        source_cursor.execute(f"SELECT * FROM {table_name}")
        rows = source_cursor.fetchall()

        target_cursor.executemany(f"INSERT INTO {table_name} VALUES ({','.join(['?' for _ in rows[0]])})", rows)

        # Commit changes and close connections
        target_conn.commit()
        print(f"Successfully copied {len(rows)} rows from {table_name}")

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        source_conn.close()
        target_conn.close()

# Usage
source_database = "/home/fazlur/Desktop/Projects/soft-engg-project-jan-2025-se-Jan-7/se-team7-db.db"
target_database = "/home/fazlur/Desktop/Projects/soft-engg-project-jan-2025-se-Jan-7/backend/instance/se-team7-db.db"
table_to_copy = "test_cases"

copy_table(source_database, target_database, table_to_copy)
