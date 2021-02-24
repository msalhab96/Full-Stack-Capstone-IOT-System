import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Device, Measures
from datetime import datetime
USER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBHU1kwMzBDT2kxRTJMUzBGbkZ5SiJ9.eyJpc3MiOiJodHRwczovL2RldmljZWlvdC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNWYyM2I4Mzc3Y2MwMDY5ZTUzMzYwIiwiYXVkIjoiZGV2aWNlYXBpIiwiaWF0IjoxNjE0MTU2NTY1LCJleHAiOjE2MTQxNjM3NjUsImF6cCI6IlpTZVNucTM5RnM3cTA4N29lM2NMZzc3YzNNakk0UVhIIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6bGlzdCJdfQ.Sw_uqyQOqOBI6HL6tbFU6_m4dWKlOgOTN6mkBRxSaF2Cksmc-4wdGOOVRUGG1lK9P8W3VHgDtJQYwbcTduJCmpEgVKM6uIxIQmpSBAGIvQiZzTORCjHaMEdrZXv2RVigR8cv9m-uhkWt7sGvini3kv-U88hY2-HdURFqvqt1-SQY_KA4okFkgyqD5seRSk-ogsPrldb-07kE5B5CSUGntJ04YyymMn2FELdRpS-tc3oAiHI_brHcAxdNqMuvHMBOdFRHwgicZ4KLZS9CpHKczhwZl5TCzQs2QyMHuYlfAPLWlypvE-9AaOGWEDwzzd_yF77dAaL8Py2JiQBGMUUxQw"
ADMIN_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjBHU1kwMzBDT2kxRTJMUzBGbkZ5SiJ9.eyJpc3MiOiJodHRwczovL2RldmljZWlvdC5hdS5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjAzNWYxYzA4Mzc3Y2MwMDY5ZTUzMzU5IiwiYXVkIjoiZGV2aWNlYXBpIiwiaWF0IjoxNjE0MTU2NTEyLCJleHAiOjE2MTQxNjM3MTIsImF6cCI6IlpTZVNucTM5RnM3cTA4N29lM2NMZzc3YzNNakk0UVhIIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6ZGV2aWNlIiwiZ2V0Omxpc3QiLCJwYXRjaDpkZXZpY2UiLCJwb3N0Om1lYXN1cmUiXX0.nPOlfn6g27zJufzQspwCeiauOrESZvqtGydUlZUkFTX8Acfks_UKWod9UMKebvJ0TWa2X4a-9NPlgUqqZfrglPq6gRNEpL2UjnGtyY8Us9hljxgnzcYzg2AtpWwM5bEjWgjh9edgmbwYHSn5aziiId-tObS_5CSY728sCQubLOXA3iAXqkOU6e0zZvI-fwrz3rhy31eNEhqG-e-06699dt_WFNAg9LcGtqi9zdjJsIfc9RPxPpQE1z_uJQAscwAdUs54y0qCKD9cL31G0bp2u9wVmz2LPvO092uHYDSqEm4wpxLIh-9vmV5mGbVJ6scrvctwOdBujeAPfZ7UQPdq8A"

class TestApp(unittest.TestCase):
    """
    a class to test the application
    """
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "app_test"
        self.database_path = "postgres://rootuser:rootuser@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        test_dev_1 = Device(
            "TEST DEVICE 1", 
            datetime.now(), 
            datetime.now(), 
            True
            )
        test_dev_2 = Device(
            "TEST DEVICE 2", 
            datetime.now(), 
            datetime.now(), 
            True
            )
        test_dev_1.insert()
        test_dev_2.insert()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_index_success(self):
        response = self.client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_device_success(self):
        response = self.client().get('/devices/1')
        self.assertEqual(response.status_code, 200)

    def test_get_device_failure(self):
        response = self.client().get('/devices/45555555555')
        self.assertEqual(response.status_code, 404)
    
    def test_list_success_1(self):
        headers = {"Authorization": "Bearer " + USER_TOKEN}
        response = self.client().get('/devices/list', headers = headers)
        self.assertEqual(response.status_code, 200)

    def test_list_success_2(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        response = self.client().get('/devices/list', headers = headers)
        self.assertEqual(response.status_code, 200)
    
    def test_list_failure_1(self):
        headers = {"Authorization": f"Be ar er {USER_TOKEN}"}
        response = self.client().get('/devices/list', headers = headers)
        self.assertEqual(response.status_code, 401)

    def test_list_failure_2(self):
        headers = {"Authorization": "Bearer"}
        response = self.client().get('/devices/list', headers = headers)
        self.assertEqual(response.status_code, 401)

    def test_delete_device_success(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        response = self.client().delete('/device/1', headers = headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_device_failure_1(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        response = self.client().delete('/device/1464684654', headers = headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_device_failure_2(self):
        headers = {"Authorization": f"Bearer {USER_TOKEN}"}
        response = self.client().delete('/device/1', headers = headers)
        self.assertEqual(response.status_code, 401)

    def test_change_status_success(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        data = {"id": 2, "status": False}
        response = self.client().patch(
                                     '/status/change', 
                                     headers = headers, 
                                     json = data
                                     )
        self.assertEqual(response.status_code, 200)

    def test_change_status_failure_1(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        data = {"status": False}
        response = self.client().patch(
                                     '/status/change', 
                                     headers = headers, 
                                     json = data
                                     )
        self.assertEqual(response.status_code, 400)

    def test_change_status_failure_2(self):
        headers = {"Authorization": f"Bearer {USER_TOKEN}"}
        data = {"id": 2, "status": False}
        response = self.client().patch(
                                     '/status/change', 
                                     headers = headers, 
                                     json = data
                                     )
        self.assertEqual(response.status_code, 401)

    def test_add_measure_success(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        data = {
            "time": datetime.now(),
            "value": 4.365,
            "rank": 2,
            "device": 2 
        }
        response = self.client().post(
                                     '/add/measure', 
                                     headers = headers, 
                                     json = data
                                     )
        self.assertEqual(response.status_code, 200)

    def test_add_measure_failure_1(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        data = {
            "time": datetime.now(),
            "value": 4.365,
            "rank": 2
        }
        response = self.client().post(
                                     '/add/measure', 
                                     headers = headers, 
                                     json = data
                                     )
        self.assertEqual(response.status_code, 404)

    def test_add_measure_failure_2(self):
        headers = {"Authorization": f"Bearer {USER_TOKEN}"}
        data = {
            "time": datetime.now(),
            "value": 4.365,
            "rank": 2,
            "device": 2 
        }
        response = self.client().post(
                                     '/add/measure', 
                                     headers = headers, 
                                     json = data
                                     )
        self.assertEqual(response.status_code, 401)
    
if __name__ == "__main__":
    unittest.main()