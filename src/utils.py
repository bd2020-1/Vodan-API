def get_sql_file(file_path_name: str):
    return open(f"sql/{file_path_name}.sql", "r").read()
