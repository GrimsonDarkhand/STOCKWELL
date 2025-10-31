#!/usr/bin/env python3
"""
StokWELL Desktop Application Test Suite
"""

import unittest
import json
import os
import tempfile
from unittest.mock import patch, MagicMock

# Import our modules
import sys
sys.path.append('.')

from data_manager import load_data, save_data
from user_manager import register_user, login_user, get_user_data
from stokvel_manager import create_stokvel, contribute, get_stokvel_data
from utils import hash_password, verify_password, validate_amount

class TestDataManager(unittest.TestCase):
    def setUp(self):
        self.test_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json')
        self.test_file.close()
        
    def tearDown(self):
        if os.path.exists(self.test_file.name):
            os.unlink(self.test_file.name)
    
    @patch('data_manager.DATA_FILE')
    def test_load_data_new_file(self, mock_data_file):
        mock_data_file = self.test_file.name
        # Remove the file to test new file creation
        os.unlink(self.test_file.name)
        
        with patch('data_manager.DATA_FILE', self.test_file.name):
            data = load_data()
            self.assertEqual(data, {"users": {}, "stokvels": {}})
    
    @patch('data_manager.DATA_FILE')
    def test_save_and_load_data(self, mock_data_file):
        mock_data_file = self.test_file.name
        test_data = {"users": {"test": "data"}, "stokvels": {}}
        
        with patch('data_manager.DATA_FILE', self.test_file.name):
            save_data(test_data)
            loaded_data = load_data()
            self.assertEqual(loaded_data, test_data)

class TestUserManager(unittest.TestCase):
    def setUp(self):
        self.data = {"users": {}, "stokvels": {}}
    
    def test_register_user_success(self):
        success, message = register_user(self.data, "testuser", "password123")
        self.assertTrue(success)
        self.assertIn("testuser", self.data["users"])
        self.assertEqual(self.data["users"]["testuser"]["balance"], 0)
        self.assertEqual(self.data["users"]["testuser"]["transactions"], [])
        self.assertEqual(self.data["users"]["testuser"]["stokvels"], [])
    
    def test_register_user_duplicate(self):
        # First registration
        register_user(self.data, "testuser", "password123")
        # Second registration with same username
        success, message = register_user(self.data, "testuser", "password456")
        self.assertFalse(success)
        self.assertIn("already exists", message)
    
    def test_login_user_success(self):
        register_user(self.data, "testuser", "password123")
        success, message = login_user(self.data, "testuser", "password123")
        self.assertTrue(success)
        self.assertIn("Welcome back", message)
    
    def test_login_user_wrong_password(self):
        register_user(self.data, "testuser", "password123")
        success, message = login_user(self.data, "testuser", "wrongpassword")
        self.assertFalse(success)
        self.assertIn("Invalid credentials", message)
    
    def test_login_user_nonexistent(self):
        success, message = login_user(self.data, "nonexistent", "password123")
        self.assertFalse(success)
        self.assertIn("Invalid credentials", message)

class TestStokvelManager(unittest.TestCase):
    def setUp(self):
        self.data = {"users": {}, "stokvels": {}}
        register_user(self.data, "testuser", "password123")
    
    def test_create_stokvel_success(self):
        success, message = create_stokvel(self.data, "TestStokvel", "testuser")
        self.assertTrue(success)
        self.assertIn("TestStokvel", self.data["stokvels"])
        self.assertIn("testuser", self.data["stokvels"]["TestStokvel"]["members"])
        self.assertIn("TestStokvel", self.data["users"]["testuser"]["stokvels"])
    
    def test_create_stokvel_duplicate(self):
        create_stokvel(self.data, "TestStokvel", "testuser")
        success, message = create_stokvel(self.data, "TestStokvel", "testuser")
        self.assertFalse(success)
        self.assertIn("already exists", message)
    
    def test_contribute_success(self):
        create_stokvel(self.data, "TestStokvel", "testuser")
        success, message = contribute(self.data, "TestStokvel", 100.0, "testuser")
        self.assertTrue(success)
        self.assertEqual(self.data["stokvels"]["TestStokvel"]["balance"], 100.0)
        self.assertEqual(len(self.data["stokvels"]["TestStokvel"]["contributions"]), 1)
        self.assertTrue(len(self.data["users"]["testuser"]["transactions"]) > 0)
    
    def test_contribute_nonexistent_stokvel(self):
        success, message = contribute(self.data, "NonexistentStokvel", 100.0, "testuser")
        self.assertFalse(success)
        self.assertIn("not found", message)
    
    def test_contribute_non_member(self):
        register_user(self.data, "otheruser", "password456")
        create_stokvel(self.data, "TestStokvel", "testuser")
        success, message = contribute(self.data, "TestStokvel", 100.0, "otheruser")
        self.assertFalse(success)
        self.assertIn("not a member", message)

class TestUtils(unittest.TestCase):
    def test_hash_password(self):
        password = "testpassword"
        hashed = hash_password(password)
        self.assertNotEqual(password, hashed)
        self.assertEqual(len(hashed), 64)  # SHA256 produces 64-character hex string
    
    def test_verify_password(self):
        password = "testpassword"
        hashed = hash_password(password)
        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrongpassword", hashed))
    
    def test_validate_amount_valid(self):
        amount, error = validate_amount("100.50")
        self.assertEqual(amount, 100.50)
        self.assertIsNone(error)
    
    def test_validate_amount_negative(self):
        amount, error = validate_amount("-50")
        self.assertIsNone(amount)
        self.assertIn("positive", error)
    
    def test_validate_amount_invalid(self):
        amount, error = validate_amount("not_a_number")
        self.assertIsNone(amount)
        self.assertIn("Invalid", error)

if __name__ == '__main__':
    # Run tests
    unittest.main(verbosity=2)

