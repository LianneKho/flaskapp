import unittest
from app import app
import sqlite3

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        """
        Setup een testclient voor de Flask-app.
        Voeg testgebruikers toe aan de database.
        """
        self.app = app.test_client()
        self.app.testing = True

        # Maak een schone database aan voor de tests
        self._create_test_db()

        # Voeg een testgebruiker toe voor de tests
        self.add_test_user('emp1', 'password123')
        self.add_test_user('emp2', 'password456')

    def _create_test_db(self):
        """ Maak een schone database voor de tests. """
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")  # Verwijder bestaande tabel
        cursor.execute('''CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)''')
        connection.commit()
        connection.close()

    def add_test_user(self, username, password):
        """ Voeg een testgebruiker toe aan de database. """
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        connection.commit()
        connection.close()

    def test_home_page(self):
        """
        Test of de homepagina succesvol laadt.
        """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welkom', response.data)  # Controleer op een relevante term

    def test_login_page(self):
        """
        Test of de loginpagina succesvol laadt.
        """
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username', response.data)  # Controleer of het formulier aanwezig is

    def test_valid_login(self):
        """
        Test een geldige login voor een geregistreerde gebruiker.
        """
        # Eerst een POST request voor login
        response = self.app.post('/login', data={'username': 'emp1', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Controleer op redirect
        self.assertIn('/voortgang', response.headers['Location'])  # Controleer of de redirect naar voortgang gaat

        # De gebruiker zou nu ingelogd moeten zijn, test de voortgangspagina
        with self.app.session_transaction() as sess:
            self.assertIn('username', sess)  # Controleer of de sessie de gebruiker heeft

    def test_invalid_login(self):
        """
        Test een ongeldige login.
        """
        response = self.app.post('/login', data={'username': 'invalid', 'password': 'wrongpass'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Invalid username or password', response.data)

    def test_voortgang_without_login(self):
        """
        Test toegang tot voortgang zonder in te loggen.
        """
        response = self.app.get('/voortgang')
        self.assertEqual(response.status_code, 302)  # Controleer op redirect naar login
        self.assertIn('/login', response.headers['Location'])

    def test_FAQ_page(self):
        """
        Test of de FAQ-pagina succesvol laadt.
        """
        # Login eerst om toegang te krijgen
        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'emp1'  # Simuleer een ingelogde gebruiker

            response = client.get('/FAQ')
            self.assertEqual(response.status_code, 200)  # Controleer of de pagina laadt
            self.assertIn(b'FAQ', response.data)  # Controleer op een relevante term in de FAQ-pagina

    def test_contact_page(self):
        """
        Test of de contactpagina succesvol laadt.
        """
        response = self.app.get('/contact')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'contact', response.data)  # Controleer op een relevante term

    def test_logout(self):
        """
        Test de logout-functionaliteit.
        """
        with self.app as client:
            with client.session_transaction() as sess:
                sess['username'] = 'emp1'
            response = client.get('/logout')
            self.assertEqual(response.status_code, 302)  # Controleer op redirect naar home

    def tearDown(self):
        """ Maak de database schoon na elke test. """
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS users")
        connection.commit()
        connection.close()

if __name__ == '__main__':
    unittest.main()