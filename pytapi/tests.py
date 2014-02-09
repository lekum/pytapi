import unittest
import pytapi

class TestPytapi(unittest.TestCase):

    def setUp(self):
        self.username = "YOUR_AES_USERNAME_HERE" 
        self.right_password = "YOUR_AES_PASSWORD"
        self.wrong_password = "False_pw"
        self.app_name = "Tests"
        self.AESService = "YOUR_AES_SERVICE"
        self.wrong_AESService = "AAVAYA#AESESP0#CSTA#AESES"
        self.conn = pytapi.CstaConnection(self.username, self.right_password,
                self.app_name)

    def test_AESConnection(self):
        self.assertEqual(self.conn.connect(self.AESService), 0)
        self.conn.abortConnection()
    
    def test_wrong_AESConnection(self):
        self.assertEqual(self.conn.connect(self.wrong_AESService),  -5)

    def test_wrong_password_AESConnection(self):
        self.conn2 = pytapi.CstaConnection(self.username, self.wrong_password,
                self.app_name)
        self.assertEqual(self.conn2.connect(self.AESService), 0)
        self.conn2.abortConnection()
        del self.conn2

if __name__ == '__main__':
    unittest.main()
