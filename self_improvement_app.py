import json
import os

DATA_FILE = 'data.json'

CATEGORIES = ['emotional', 'rational', 'spirituell', 'transformational']
SUBCATEGORIES = ['ich', 'du', 'wir', 'alles']

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {'users': {}}


def save_data(data):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def ensure_user(data, username):
    users = data.setdefault('users', {})
    if username not in users:
        users[username] = {
            'scores': {cat: {sub: 0 for sub in SUBCATEGORIES} for cat in CATEGORIES}
        }


def add_points(data, username, category, subcategory, points):
    ensure_user(data, username)
    data['users'][username]['scores'][category][subcategory] += points


def display_profile(user_data, username):
    print(f"Profil von {username}:")
    scores = user_data['scores']
    for cat in CATEGORIES:
        print(f"  {cat.capitalize()}:")
        for sub in SUBCATEGORIES:
            print(f"    {sub}: {scores[cat][sub]} Punkte")


def main():
    data = load_data()
    current_user = None
    while True:
        print('\nSelbstverbesserungs-Dashboard')
        print('1. Benutzer auswählen')
        print('2. Aufgabe hinzufügen')
        print('3. Profil anzeigen')
        print('4. Beenden')
        choice = input('Auswahl: ')

        if choice == '1':
            user = input('Benutzername: ')
            ensure_user(data, user)
            current_user = user
            print(f'Benutzer {user} ausgewählt.')
        elif choice == '2':
            if not current_user:
                print('Bitte zuerst einen Benutzer auswählen.')
                continue
            print('Kategorien:', ', '.join(CATEGORIES))
            category = input('Kategorie: ')
            if category not in CATEGORIES:
                print('Ungültige Kategorie.')
                continue
            print('Unterkategorien:', ', '.join(SUBCATEGORIES))
            sub = input('Unterkategorie: ')
            if sub not in SUBCATEGORIES:
                print('Ungültige Unterkategorie.')
                continue
            try:
                pts = int(input('Punkte: '))
            except ValueError:
                print('Bitte eine Zahl eingeben.')
                continue
            add_points(data, current_user, category, sub, pts)
            save_data(data)
            print('Punkte hinzugefügt!')
        elif choice == '3':
            if not current_user:
                print('Bitte zuerst einen Benutzer auswählen.')
                continue
            display_profile(data['users'][current_user], current_user)
        elif choice == '4':
            print('Auf Wiedersehen!')
            break
        else:
            print('Ungültige Auswahl.')


if __name__ == '__main__':
    main()
