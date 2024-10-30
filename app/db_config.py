valid_tables = {
    'actions': ['action_id', 'action_description', 'created_at'],
    'games': ['game_id', 'game_name', 'created_at'],
    'games_sessions': ['game_id', 'session_id', 'created_at'],
    'scores': ['score_id', 'score_name', 'score_value', 'created_at'],
    'sessions': ['session_id', 'created_at'],
    'sessions_actions': ['session_id', 'action_id', 'created_at'],
    'sessions_scores': ['session_id', 'score_id', 'created_at'],
    'users': ['user_id', 'user_name', 'user_email', 'created_at'],
    'users_sessions': ['user_id', 'session_id', 'created_at']
}

def is_valid_table(table: str) -> bool:
    return table in valid_tables

def is_valid_column(table: str, column: str) -> bool:
    return column in valid_tables.get(table, [])

def is_data_valid(table: str, data: dict) -> bool:
    if not is_valid_table(table):
        return False

    return all(key in valid_tables[table] for key in data.keys())
