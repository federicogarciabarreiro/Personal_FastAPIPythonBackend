valid_tables = {
    'actions': ['action_id', 'action_description'],
    'games': ['game_id', 'game_name'],
    'games_sessions': ['game_id', 'session_id'],
    'scores': ['score_id', 'score_name', 'score_value'],
    'sessions': ['session_id'],
    'sessions_actions': ['session_id', 'action_id'],
    'sessions_scores': ['session_id', 'score_id'],
    'users': ['user_id', 'user_name', 'user_email'],
    'users_sessions': ['user_id', 'session_id']
}

def is_valid_table(table: str) -> bool:
    return table in valid_tables

def is_valid_column(table: str, column: str) -> bool:
    return column in valid_tables.get(table, [])

def is_data_valid(table: str, data: dict) -> bool:
    if not is_valid_table(table):
        return False

    return all(key in valid_tables[table] for key in data.keys())
