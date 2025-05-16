import unittest, threading, time
from app import create_app, db
from app.config import TestingConfig
from app.models import User
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from werkzeug.serving import make_server

class ServerThread(threading.Thread):
    def __init__(self, app):
        threading.Thread.__init__(self)
        self.srv = make_server('127.0.0.1', 5001, app)
        self.ctx = app.app_context()
        self.ctx.push()

    def run(self):
        self.srv.serve_forever()

    def shutdown(self):
        self.srv.shutdown()

class SeleniumTests(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestingConfig)
        with self.app.app_context():
            db.create_all()
            u = User(username="Literally any username works")
            u.set_password("Any password too")
            db.session.add(u)
            db.session.commit()

        self.server = ServerThread(self.app)
        self.server.start()

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(3)

    def tearDown(self):
        self.driver.quit()
        self.server.shutdown()
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def login(self, username, password):
        self.driver.get("http://127.0.0.1:5001/")
        self.driver.find_element(By.ID, "loginBtn").click()
        WebDriverWait(self.driver, 5).until(
            EC.element_to_be_clickable((By.NAME, "username"))
        ).send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.NAME, "submit_login").click()
        time.sleep(1)

    def test_login_valid_credentials(self):
        self.login("Literally any username works", "Any password too")
        self.assertIn("Homepage", self.driver.page_source)

    def test_login_invalid_credentials(self):
        self.login("New username", "Random password")
        self.assertIn("User does not exist", self.driver.page_source)

    def test_navigate_pages(self):
        self.login("Literally any username works", "Any password too")
        self.driver.get("http://127.0.0.1:5001/Stats")
        self.assertIn("Movie Analytics", self.driver.page_source)
        self.driver.get("http://127.0.0.1:5001/Collection")
        self.assertIn("Add", self.driver.page_source)

    def test_display_dashboard_user(self):
        self.login("Literally any username works", "Any password too")
        self.assertIn("Literally any username works", self.driver.page_source)

    def test_visit_collection_page(self):
        self.login("Literally any username works", "Any password too")
        self.driver.get("http://127.0.0.1:5001/Collection")
        self.assertIn("Collections", self.driver.page_source)
