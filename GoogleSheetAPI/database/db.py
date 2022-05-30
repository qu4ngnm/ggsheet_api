from sqlite3 import connect

DB_NAME = "database/webserver.db"
conn = connect(DB_NAME)
cursor = conn.cursor()

def create_table():
    table_script = '''CREATE TABLE IF NOT EXISTS user_table(
                    user_name VARCHAR(30) UNIQUE,
                    pass_wd NVARCHAR(150) NOT NULL
                );
                '''
    cursor.executescript(table_script)
    conn.commit()
def signup(user_name, pass_wd):
    cursor.execute("INSERT INTO user_table(user_name, pass_wd) VALUES(?, ?);",(user_name, pass_wd))
    conn.commit()
def delete_user(user_name):
    cursor.execute("DELETE FROM user_table WHERE user_name = ?;",(user_name))
    conn.commit()
def check_login(username, password):
    data = cursor.execute("SELECT * FROM user_table WHERE user_name = ? and pass_wd = ?;",(username, password))
    result = data.fetchall()
    if result:
        return 1
    else:
        return 0