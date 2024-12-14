import unittest
from app import app, init_db
import sqlite3

class AthleteManagementTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        init_db()

    def tearDown(self):
        conn = sqlite3.connect('athletes.db')
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS athletes')
        cursor.execute('DROP TABLE IF EXISTS competitions')
        cursor.execute('DROP TABLE IF EXISTS athlete_competitions')
        conn.commit()
        conn.close()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_add_athlete(self):
        response = self.app.post('/athletes', data=dict(
            add=1,
            name='John Doe',
            age=25
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'John Doe', response.data)

    def test_add_competition(self):
        response = self.app.post('/competitions', data=dict(
            add=1,
            name='Marathon',
            date='2023-12-01'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Marathon', response.data)

    def test_add_athlete_competition(self):
        # Add an athlete
        self.app.post('/athletes', data=dict(
            add=1,
            name='Jane Doe',
            age=30
        ))
        # Add a competition
        self.app.post('/competitions', data=dict(
            add=1,
            name='Sprint',
            date='2023-12-02'
        ))
        # Add athlete-competition entry
        response = self.app.post('/athlete_competitions', data=dict(
            athlete_id=1,
            competition_id=1
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Jane Doe', response.data)
        self.assertIn(b'Sprint', response.data)

if __name__ == '__main__':
    unittest.main()
