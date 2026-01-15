from selenium.webdriver.chrome.service import Service
import time

from selenium.webdriver.common.devtools.v141.extensions import remove_storage_items

import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code


class UrbanRoutesPage:
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    pedir_taxi = (By.XPATH, '//button[contains(text(), "Pedir un taxi")]')
    select_comfort = (By.XPATH, '//tcard-title[contains(text(), "Comfort")]')


    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    def set_from(self, from_address):
        self.wait.until(EC.presence_of_element_located(self.from_field)).send_keys(from_address)
       # self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.wait.until(EC.presence_of_element_located(self.to_field)).send_keys(to_address)
        #self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self,address_from, address_to):

        self.set_from(address_from)
        self.set_to(address_to)




    def click_pedir_taxi(self):
        #self.driver.find_element(*self.pedir_taxi).click()
        self.wait.until(EC.presence_of_element_located(self.pedir_taxi)).click()

    def click_select_comfort(self):
        self.wait.until(EC.presence_of_element_located(self.select_comfort)).click()

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability('goog:LoggingPrefs', {'performance':'All'})
        cls.driver = webdriver.Chrome(service=Service(),options=chrome_options)
        #from selenium.webdriver import DesiredCapabilities
        #capabilities = DesiredCapabilities.CHROME
       # capabilities["goog:loggingPrefs"] = {'performance': 'ALL'}
       # cls.driver = webdriver.Chrome(desired_capabilities=capabilities)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        routes_page.click_pedir_taxi()
        routes_page.click_select_comfort()
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to




   # @classmethod
    #def teardown_class(cls):
     #   cls.driver.quit()


