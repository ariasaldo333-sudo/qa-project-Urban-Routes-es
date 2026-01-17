from selenium.webdriver.chrome.service import Service
import data
from selenium import webdriver
from common_steps import UrbanRoutesPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from template_original import retrieve_phone_code


#aqui iba el class hasta a ca#
        #from selenium.webdriver import DesiredCapabilities
        #capabilities = DesiredCapabilities.CHROME
       # capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
       # cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    #Primer TEST
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        actual_desde = self.routes_page.get_from()
        actual_para = self.routes_page.get_to()
        assert address_from == actual_desde
        assert address_to == actual_para

    # test numero 2
    def test_select_comfort(self) :
        self.routes_page.click_pedir_taxi()
        self.routes_page.click_select_comfort()
        assert self.routes_page.click_select_comfort() == self.routes_page.click_select_comfort()


    def test_rellenar_telefono(self):
        self.routes_page.click_telefono()
        self.routes_page.llenar_numero_telefonico()
        self.routes_page.select_siguiente()
       # assert self.routes_page.llenar_numero_telefonico() == self.routes_page.llenar_numero_telefonico()

    def test_rellenar_codigo(self):
        codigo = retrieve_phone_code(driver=self.driver)
        self.routes_page.set_codigo(codigo)
        print(codigo)

