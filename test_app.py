import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Device, Measures
from datetime import datetime
import os
USER_TOKEN = open('user_auth.txt').read().strip()
ADMIN_TOKEN = open('admin_auth.txt').read().strip()


class TestApp(unittest.TestCase):
    """
    a class to test the application
    """
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "app_test"
        self.database_path = "postgres://rootuser:rootuser@{}/{}".format(
            'localhost:5432',
            self.database_name
            )
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
        response = self.client().get('/devices/list', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_list_success_2(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        response = self.client().get('/devices/list', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_list_failure_1(self):
        headers = {"Authorization": f"Be ar er {USER_TOKEN}"}
        response = self.client().get('/devices/list', headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_list_failure_2(self):
        headers = {"Authorization": "Bearer"}
        response = self.client().get('/devices/list', headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_delete_device_success(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        response = self.client().delete('/device/1', headers=headers)
        self.assertEqual(response.status_code, 200)

    def test_delete_device_failure_1(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        response = self.client().delete('/device/1464684654', headers=headers)
        self.assertEqual(response.status_code, 404)

    def test_delete_device_failure_2(self):
        headers = {"Authorization": f"Bearer {USER_TOKEN}"}
        response = self.client().delete('/device/1', headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_change_status_success(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        data = {"id": 2, "status": False}
        response = self.client().patch(
                                     '/status/change',
                                     headers=headers,
                                     json=data
                                     )
        self.assertEqual(response.status_code, 200)

    def test_change_status_failure_1(self):
        headers = {"Authorization": f"Bearer {ADMIN_TOKEN}"}
        data = {"status": False}
        response = self.client().patch(
                                     '/status/change',
                                     headers=headers,
                                     json=data
                                     )
        self.assertEqual(response.status_code, 400)

    def test_change_status_failure_2(self):
        headers = {"Authorization": f"Bearer {USER_TOKEN}"}
        data = {"id": 2, "status": False}
        response = self.client().patch(
                                     '/status/change',
                                     headers=headers,
                                     json=data
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
                                     headers=headers,
                                     json=data
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
                                     headers=headers,
                                     json=data
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
                                     headers=headers,
                                     json=data
                                     )
        self.assertEqual(response.status_code, 401)


if __name__ == "__main__":
    unittest.main()
