def create_database():
    return [
        """
        DROP TABLE IF EXISTS record
        """,
        """
        CREATE TABLE IF NOT EXISTS record (
            id integer primary key autoincrement,
            contents text not null
        )
        """
    ]

def make_record(text):
    return f"""
        INSERT INTO record (contents) VALUES ('{text}');
    """
