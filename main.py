import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from data import card_code, phone_number, card_number, message_for_driver

#Localizadores
class UrbanRoutesPage:
    # 1.Configurar la dirección
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # 2.Seleccionar la tarifa Comfort.
    personal_button = (By.CLASS_NAME, 'mode active')
    taxi_icon = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[2]/div[3]/img')
    order_taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    comfort_icon = (By.CSS_SELECTOR, '[data-for="tariff-card-4"]')

    # 3.Rellenar el número de teléfono.
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_number_field = (By.CLASS_NAME, 'input-container error')
    next_button = (By.CLASS_NAME, 'button full')
    sms_code = (By.CLASS_NAME, 'input-container')
    confirm_button = (By.CSS_SELECTOR, 'button[type="submit"].button.full')

    # 4.Agregar una tarjeta de crédito.
    payment_method_button = (By.CLASS_NAME, 'pp-button filled')
    add_card_button = (By.CLASS_NAME, 'pp-title')
    card_number_field = (By.ID, 'number')
    card_code_field = (By.ID, 'code')
    focus_click =(By.CLASS_NAME, 'modal unusual')
    add_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    x_button = (By.CLASS_NAME, 'close-button section-close')

    # 5.Escribir un mensaje para el controlador.
    comment_field = (By.ID, 'comment')

    # 6.Pedir una manta y pañuelos
    requirements_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[1]/div[1]')
    blanket_and_scarves_slider = (By.CSS_SELECTOR, 'input.switch-input[type="checkbox"]')

    # 7.Pedir 2 helados
    ice_cream_plus_counter = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')

    # 8.Aparece el modal para buscar un taxi
    taxi_search_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')

#Metodos
    #1.Configurar la dirección
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    #2.Seleccionar la tarifa Comfort.
    def click_personal_button(self):
        self.driver.find_element(*self.personal_button).click()

    def click_taxi_icon(self):
        self.driver.find_element(*self.taxi_icon).click()

    def click_order_taxi_button(self):
        self.driver.find_element(*self.order_taxi_button).click()

    def click_comfort_icon(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'tcard active')))
        self.driver.find_element(*self.comfort_icon).click()

    #3.Rellenar el número de teléfono.
    def click_phone_number_button(self):
        self.driver.find_element(*self.phone_number_button).click()

    def set_phone_number(self, phone_number):
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,'input-container error')))
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_field).get_property(phone_number)

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

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

    def set_sms_code(self, code):
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'input-container')))
        self.driver.find_element(*self.sms_code).send_keys(code)

    def click_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    #4.Agregar una tarjeta de crédito.
    def click_payment_method_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'pp-button filled')))
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'pp-title')))
        self.driver.find_element(*self.add_card_button).click()

    def set_card_number_field(self, card_number):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'number')))
        self.driver.find_element(*self.card_number_field).send_keys(card_number)

    def set_card_code_field(self, card_code):
        self.driver.find_element(*self.card_code_field).send_keys(card_code)

    def get_card_number_field(self):
        return self.driver.find_element(*self.card_number_field).get_property(card_number)

    def get_card_code_field(self):
        return self.driver.find_element(*self.card_code_field).get_property(card_code)

    def click_focus_click(self):
        self.driver.find_element(*self.card_code_field).click()

    def click_add_button(self):
        self.driver.find_element(*self.add_button).click()

    def click_x_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'close-button section-close')))
        self.driver.find_element(*self.x_button).click()

    #5.Escribir un mensaje para el controlador.
    def set_comment_field(self, message_for_driver):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'input-container')))
        self.driver.find_element(*self. comment_field).send_keys(message_for_driver)

    def get_comment_field(self):
        return self.driver.find_element(*self.comment_field).get_property(message_for_driver)

    #6.Pedir una manta y pañuelos
    def click_requirements_button(self):
        self.driver.find_element(*self.requirements_button).click()

    def click_blanket_and_scarves_slider(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')))
        self.driver.find_element(*self.blanket_and_scarves_slider).click()

    # 7.Pedir 2 helados
    def click_ice_cream_plus_counter(self):
        self.driver.find_element(*self. ice_cream_plus_counter).click()

    def get_selected_ice_cream_count(self):
        ice_cream_count_element = self.driver.find_element(By.CSS_SELECTOR, 'div.counter-value')
        ice_cream_count = int(ice_cream_count_element.text)
        return ice_cream_count

    #8.Aparece el modal para buscar un taxi
    def click_taxi_search_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')))
        self.driver.find_element(*self.taxi_search_button).click()
import data
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



from data import card_code, phone_number, card_number, message_for_driver

#Localizadores
class UrbanRoutesPage:
    # 1.Configurar la dirección
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')

    # 2.Seleccionar la tarifa Comfort.
    personal_button = (By.CLASS_NAME, 'mode active')
    taxi_icon = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[2]/div[3]/img')
    order_taxi_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    comfort_icon = (By.CSS_SELECTOR, '[data-for="tariff-card-4"]')

    # 3.Rellenar el número de teléfono.
    phone_number_button = (By.CLASS_NAME, 'np-button')
    phone_number_field = (By.CLASS_NAME, 'input-container error')
    next_button = (By.CLASS_NAME, 'button full')
    sms_code = (By.CLASS_NAME, 'input-container')
    confirm_button = (By.CSS_SELECTOR, 'button[type="submit"].button.full')

    # 4.Agregar una tarjeta de crédito.
    payment_method_button = (By.CLASS_NAME, 'pp-button filled')
    add_card_button = (By.CLASS_NAME, 'pp-title')
    card_number_field = (By.ID, 'number')
    card_code_field = (By.ID, 'code')
    focus_click =(By.CLASS_NAME, 'modal unusual')
    add_button = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    x_button = (By.CLASS_NAME, 'close-button section-close')

    # 5.Escribir un mensaje para el controlador.
    comment_field = (By.ID, 'comment')

    # 6.Pedir una manta y pañuelos
    requirements_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[1]/div[1]')
    blanket_and_scarves_slider = (By.CSS_SELECTOR, 'input.switch-input[type="checkbox"]')

    # 7.Pedir 2 helados
    ice_cream_plus_counter = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')

    # 8.Aparece el modal para buscar un taxi
    taxi_search_button = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')

#Metodos
    #1.Configurar la dirección
    def __init__(self, driver):
        self.driver = driver

    def set_from(self, from_address):
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        self.driver.find_element(*self.to_field).send_keys(to_address)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    #2.Seleccionar la tarifa Comfort.
    def click_personal_button(self):
        self.driver.find_element(*self.personal_button).click()

    def click_taxi_icon(self):
        self.driver.find_element(*self.taxi_icon).click()

    def click_order_taxi_button(self):
        self.driver.find_element(*self.order_taxi_button).click()

    def click_comfort_icon(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'tcard active')))
        self.driver.find_element(*self.comfort_icon).click()

    #3.Rellenar el número de teléfono.
    def click_phone_number_button(self):
        self.driver.find_element(*self.phone_number_button).click()

    def set_phone_number(self, phone_number):
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME,'input-container error')))
        self.driver.find_element(*self.phone_number_field).send_keys(phone_number)

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number_field).get_property(phone_number)

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

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

    def set_sms_code(self, code):
        WebDriverWait(self.driver,10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'input-container')))
        self.driver.find_element(*self.sms_code).send_keys(code)

    def click_confirm_button(self):
        self.driver.find_element(*self.confirm_button).click()

    #4.Agregar una tarjeta de crédito.
    def click_payment_method_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'pp-button filled')))
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'pp-title')))
        self.driver.find_element(*self.add_card_button).click()

    def set_card_number_field(self, card_number):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'number')))
        self.driver.find_element(*self.card_number_field).send_keys(card_number)

    def set_card_code_field(self, card_code):
        self.driver.find_element(*self.card_code_field).send_keys(card_code)

    def get_card_number_field(self):
        return self.driver.find_element(*self.card_number_field).get_property(card_number)

    def get_card_code_field(self):
        return self.driver.find_element(*self.card_code_field).get_property(card_code)

    def click_focus_click(self):
        self.driver.find_element(*self.card_code_field).click()

    def click_add_button(self):
        self.driver.find_element(*self.add_button).click()

    def click_x_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'close-button section-close')))
        self.driver.find_element(*self.x_button).click()

    #5.Escribir un mensaje para el controlador.
    def set_comment_field(self, message_for_driver):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'input-container')))
        self.driver.find_element(*self. comment_field).send_keys(message_for_driver)

    def get_comment_field(self):
        return self.driver.find_element(*self.comment_field).get_property(message_for_driver)

    #6.Pedir una manta y pañuelos
    def click_requirements_button(self):
        self.driver.find_element(*self.requirements_button).click()

    def click_blanket_and_scarves_slider(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')))
        self.driver.find_element(*self.blanket_and_scarves_slider).click()

    # 7.Pedir 2 helados
    def click_ice_cream_plus_counter(self):
        self.driver.find_element(*self. ice_cream_plus_counter).click()

    def get_selected_ice_cream_count(self):
        ice_cream_count_element = self.driver.find_element(By.CSS_SELECTOR, 'div.counter-value')
        ice_cream_count = int(ice_cream_count_element.text)
        return ice_cream_count

    #8.Aparece el modal para buscar un taxi
    def click_taxi_search_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')))
        self.driver.find_element(*self.taxi_search_button).click()



#Pruebas
class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # Configurar las capacidades deseadas
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities["goog:loggingPrefs"] = {"performance": "ALL"}

        # Configurar las opciones del navegador
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])

        # Iniciar el servicio de Chrome (asegurando compatibilidad con tu sistema)
        service = Service()  # Puedes pasar el path del driver aquí si es necesario

        # Inicializar el driver con opciones y capacidades
        cls.driver = webdriver.Chrome(service=service, options=options, desired_capabilities=capabilities)

    # 1.Configurar la dirección
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_route(address_from, address_to)
        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # 2.Seleccionar la tarifa Comfort.
    def test_select_comfort_tariff(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_personal_button()
        routes_page.click_comfort_icon()
        # Verificar si la tarifa Comfort está seleccionada
        comfort_icon_class = self.driver.find_element(*routes_page.comfort_icon).get_attribute('class')
        assert 'active' in comfort_icon_class

    # 3.Rellenar el número de teléfono.
    # CORREGIR
    def test_fill_phone_number(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_phone_number_button()
        routes_page.set_phone_number(data.phone_number)
        assert routes_page.get_phone_number() == data.phone_number
        routes_page.click_next_button()

    # 4.Agregar una tarjeta de crédito.
    #CORREGIR
    def test_add_credit_card(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_payment_method_button()
        routes_page.click_add_card_button()
        routes_page.set_card_number_field(data.card_number)
        routes_page.set_card_code_field(data.card_code)
        routes_page.click_add_button()
        # Asegurarse de que se agregue correctamente la tarjeta
        card_number_field_value = routes_page.get_card_number_field()
        assert data.card_number in card_number_field_value

    # 5.Escribir un mensaje para el controlador.
    def test_write_comment_for_driver(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.set_comment_field(data.message_for_driver)
        assert routes_page.get_comment_field() == data.message_for_driver

    # 6.Pedir una manta y pañuelos
    def test_select_blanket_and_scarves(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_requirements_button()
        routes_page.click_blanket_and_scarves_slider()
        # Asegúrarse de que la opción haya sido seleccionada
        assert self.driver.find_element(*routes_page.blanket_and_scarves_slider).is_selected()

    # 7.Pedir 2 helados
    def test_select_two_ice_creams(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_ice_cream_plus_counter()
        routes_page.click_ice_cream_plus_counter()

        selected_ice_cream_count = routes_page.get_selected_ice_cream_count()
        assert selected_ice_cream_count == 2


    # 8.Aparece el modal para buscar un taxi
    def test_taxi_search_modal(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        routes_page.click_taxi_search_button()
        # Verificar si el modal ha aparecido (usando la presencia de algún elemento del modal)
        modal_displayed = self.driver.find_element(By.CSS_SELECTOR, 'div.order-header-title').is_displayed()
        assert modal_displayed

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
