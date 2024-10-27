valid_tables = {
    'users': ['user_id','user_name', 'user_email']
}

def is_valid_table(table: str) -> bool:
    return table in valid_tables

def is_valid_column(table: str, column: str) -> bool:
    return column in valid_tables.get(table, [])
