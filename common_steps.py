from selenium.webdriver.chrome.service import Service
import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time

# no modificar, MODIFICADO
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

    #LOCALIZADORES//////////////////////////////////////////////////////////////////////

    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    pedir_taxi = (By.XPATH, '//button[contains(text(), "Pedir un taxi")]')
    select_comfort =  (By.XPATH,'//div[text()= "Comfort"]')
    click_numero_telefonico = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div')
    llenar_telefono_field=(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[1]/div[1]/label')
    campo_telefono =(By.ID,'phone')
    siguiente = (By.XPATH,'//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    zona_code = (By.XPATH,'//*[ @ id = "root"]/div/div[1]/div[2]/div[2]/form/div[1]/div')
    click_intro_code = (By.XPATH,'//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[1]/div[1]/label')
    llenar_sms= (By.XPATH, '//*[@id="code"]')
    code_field= (By.ID, 'code')
    confirmar_codigo = (By.XPATH, '//button[contains(text(), "Confirmar")]')
    metodo_pago = (By.XPATH, '// div[ @class ="pp-text"]')
    agregar_tarjeta= (By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]/div[2]')
    campo_mensaje_conductor=(By.XPATH,'//div[@class="form"]//div//div[@class="input-container"]')
    mensaje_conductor_1= (By.XPATH, '//*[@id = "comment"]')
    click_campo_cc=(By.XPATH,'//input[@id = "number"]')
    campo_digitos_cc=(By.XPATH, '//*[@id="number"]')
    campo_ccv=(By.XPATH,'//div[@class="card-code-input"]')
    ccv=(By.XPATH, '//*[@id="code"])[2]')
    cvv2= (By.XPATH, '//div[@class="card-code-input"]//input')
    out_box=(By.XPATH, '// *[@id = "root"]/div/div[2]/div[2]/div[2]/div')
    agregar=(By.XPATH, '//*[@id = "root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    cerrar_tarjeta=(By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    manta_y_pañuelos= (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    pedir_helados= (By.XPATH,'//div[@class="r-group"]//div[1]//div[1]//div[2]//div[1]//div[3]')
    pedir_hela2= (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    modal_pedir_taxi=(By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')
#/////////////////////////////////////////////////////////////////////////////////////////

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
        return self.wait.until(EC.presence_of_element_located(self.from_field)).get_attribute('value')
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

    def click_select_tarifa(self):
        self.wait.until(EC.presence_of_element_located(self.select_comfort))
    def click_telefono(self):
        self.wait.until(EC.presence_of_element_located(self.click_numero_telefonico)).click()
    def llenar_numero_telefonico(self):
        self.wait.until(EC.presence_of_element_located(self.llenar_telefono_field)).click()
        self.wait.until(EC.presence_of_element_located(self.campo_telefono)).send_keys(data.phone_number)

    def select_siguiente(self):
        self.wait.until(EC.presence_of_element_located(self.siguiente)).click()


    def click_code_field(self) :
        self.wait.until(EC.presence_of_element_located(self.zona_code)).click()
    def set_codigo(self,codigo):
        self.wait.until(EC.presence_of_element_located(self.code_field)).send_keys(codigo)
    def click_siguiente(self):
        self.wait.until(EC.presence_of_element_located(self.confirmar_codigo)).click()

#Seleccionar metodo de pago
    def click_metodo_de_pago(self):
        self.wait.until(EC.presence_of_element_located(self.metodo_pago)).click()
#Agregar tarjeta
    def click_agregar_tarjeta(self):
        self.wait.until(EC.presence_of_element_located(self.agregar_tarjeta)).click()


    def introducir_datos_tarjeta(self):
        self.wait.until(EC.presence_of_element_located(self.campo_digitos_cc)).send_keys(data.card_number)
#Introducir CVV
    def click_cvv(self):
        self.wait.until(EC.presence_of_element_located(self.campo_ccv)).click()

    def introducir_ccv(self):
        self.wait.until(EC.presence_of_element_located(self.cvv2)).send_keys(data.card_code)

    def click_out_box(self):
        self.wait.until(EC.presence_of_element_located(self.out_box)).click()


    def click_agregar(self):
        self.wait.until(EC.presence_of_element_located(self.agregar)).click()
    def click_cerrar(self):
        self.wait.until(EC.presence_of_element_located(self.cerrar_tarjeta)).click()

    def mensaje_conductor(self):
        self.wait.until(EC.presence_of_element_located(self.campo_mensaje_conductor)).click()
        self.wait.until(EC.presence_of_element_located(self.mensaje_conductor_1)).send_keys(data.message_for_driver)


    def click_m_p(self):
        self.wait.until(EC.presence_of_element_located(self.manta_y_pañuelos)).click()


    def helados(self):
        self.wait.until(EC.presence_of_element_located(self.pedir_hela2)).click()
        self.wait.until(EC.presence_of_element_located(self.pedir_hela2)).click()

    def hace_click_modal(self):
        self.wait.until(EC.presence_of_element_located(self.modal_pedir_taxi)).click()

class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
         # no lo modifiques, ya que necesitamos un registro adicional habilitado para recuperar el código de confirmación del teléfono
        chrome_options = webdriver.ChromeOptions()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        address_from = data.address_from
        address_to = data.address_to
        self.routes_page.set_route(address_from, address_to)
        actual_desde = self.routes_page.get_from()
        actual_para = self.routes_page.get_to()
        assert address_from == actual_desde
        assert address_to == actual_para

    def test_select_comfort(self):
        self.routes_page.click_pedir_taxi()
        self.routes_page.click_select_comfort()
        assert self.routes_page.click_select_comfort() == self.routes_page.click_select_comfort()

    def test_rellenar_telefono(self):
        self.routes_page.click_telefono()
        self.routes_page.llenar_numero_telefonico()
        self.routes_page.select_siguiente()
        self.routes_page.click_code_field()

    def test_click_code_field(self):
        self.routes_page.click_code_field()


    def test_introducir_codigo(self):
        codigo_sms = retrieve_phone_code(driver=self.driver)
        self.routes_page.set_codigo(codigo_sms)


    def test_siguiente(self):
        self.routes_page.click_siguiente()
        self.routes_page.click_metodo_de_pago()

    def test_pago_tarjeta_credito(self):
        self.routes_page.click_agregar_tarjeta()



    def test_llenar_tarjeta(self):
        #self.routes_page.click_outbox()
        self.routes_page.introducir_datos_tarjeta()


    def test_click_cvv(self):
        self.routes_page.click_cvv()

    def test_llenar_campo_cvv(self):
        self.routes_page.introducir_ccv()
        self.routes_page.click_out_box()
        self.routes_page.click_agregar()
        self.routes_page.click_cerrar()

    def test_mandar_mensaje(self):
        self.routes_page.mensaje_conductor()

    def test_pedir_manta_y_pañuelos(self):
        self.routes_page.click_m_p()

    def test_pedir_helados(self):
        self.routes_page.helados()


    def test_hacer_click_modal_pedir_taxi(self):
        self.routes_page.hace_click_modal()

   # @classmethod
    #def teardown_class(cls):
     # cls.driver.quit()



