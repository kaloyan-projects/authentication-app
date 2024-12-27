import sqlite3
import hashlib
import getpass
import gettext
import os
import locale

def set_language(lang_code):
    locales_dir = os.path.join(os.path.dirname(__file__), 'locale')
    translation = gettext.translation('messages', locales_dir, languages=[lang_code], fallback=True)
    translation.install()
    global _
    _ = translation.gettext


while True:
    lang = input("(1) Български (2) English: ")
    if lang == '1':
        set_language('bg')
        break
    elif lang == '2':
        set_language('en_US')
        break

# Function to create a database and a users table
def create_database():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to create a new user
def create_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hash_password(password)))
        conn.commit()
        print(_("User created successfully!"))
    except sqlite3.IntegrityError:
        print(_("Username already exists."))
    conn.close()

# Function to log in a user
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hash_password(password)))
    user = c.fetchone()
    conn.close()
    if user:
        print(_("Login successful!") % username)
    else:
        print(_("Invalid username or password."))

# Main program loop
def main():
    create_database()
    while True:
        action = input(_("Do you want to (1) create an account or (2) log in? (q to quit): "))
        if action == '1':
            username = input(_("Enter a username: "))
            password = getpass.getpass(_("Enter a password: "))
            create_user(username, password)
        elif action == '2':
            username = input(_("Enter your username: "))
            password = getpass.getpass(_("Enter your password: "))
            login_user(username, password)
        elif action.lower() == 'q':
            break
        else:
            print(_("Invalid option. Please try again."))

if __name__ == "__main__":
    main()
