import UrbanRutesLocators
import data
from UrbanRutesLocators import UrbanRoutesPage
from selenium import webdriver
from selenium.webdriver.common.by import By
from helpers import retrieve_phone_code


from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


#Pruebas
class TestUrbanRoutes:

    driver = None

    @classmethod
    def setup_class(cls):
        # Configurar las opciones del navegador
        options = Options()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        # Iniciar el servicio de Chrome
        service = Service()  # Puedes pasar el path del driver aquí si es necesario

        # Inicializar el driver con opciones
        cls.driver = webdriver.Chrome(service=service, options=options)
        cls.driver.implicitly_wait(10)
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRutesLocators.UrbanRoutesPage(cls.driver)

    # 1.Configurar la dirección
    def test_set_route(self):
        self.driver.get(data.urban_routes_url)
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        routes_page.set_from(address_from)
        routes_page.set_to(address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    # 2.Seleccionar la tarifa Comfort.
    def test_select_comfort_tariff(self):
        self.routes_page.click_order_taxi_button()
        self.routes_page.click_comfort_tariff_button()
        assert self.routes_page.is_comfort_tariff_selected(), 'Comfort tariff not selected'

    # 3.Rellenar el número de teléfono.
    def test_fill_phone_number(self):
        self.routes_page.click_add_phone_number()
        self.routes_page.set_phone_number()
        self.routes_page.click_next_button()
        code = UrbanRutesLocators.retrieve_phone_code(self.driver)
        self.routes_page.click_confirm_button(code)
        phone_input_value = self.driver.find_element(*self.routes_page.phone_number_field).get_attribute("value")
        assert phone_input_value == data.phone_number


    # 4.Agregar una tarjeta de crédito.
    def test_add_credit_card(self):
        self.routes_page.click_payment_method_button()
        self.routes_page.click_add_card_button()
        self.routes_page.click_card_number_field()
        self.routes_page.set_card_number_field(data.card_number)
        self.routes_page.click_card_code_field()
        self.routes_page.set_card_code_field(data.card_code)
        self.routes_page.click_focus_click()
        self.routes_page.click_add_button()

#CORRECION
        self.routes_page.validate_card_number(data.card_number)


    # 5.Escribir un mensaje para el controlador.
    def test_write_comment_for_driver(self):
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)
        self.routes_page.set_comment_field(data.message_for_driver)

        assert self.routes_page.get_comment_field() == data.message_for_driver


    # 6.Pedir una manta y pañuelos
    def test_select_blanket_and_scarves(self):
        self.driver.get(data.urban_routes_url)
        self.routes_page = UrbanRoutesPage(self.driver)
        self.routes_page.click_requirements_button()
        self.routes_page.click_blanket_and_scarves_slider()
        # Asegúrarse de que la opción haya sido seleccionada
        assert self.driver.find_element(*self.routes_page.blanket_and_scarves_slider).is_selected()

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

    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
