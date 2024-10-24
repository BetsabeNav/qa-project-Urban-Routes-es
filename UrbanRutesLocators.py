from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import data
from helpers import retrieve_phone_code 


class UrbanRoutesPage:
    # 1.Configurar la dirección
    from_field = (By.ID,'from')
    to_field = (By.ID,'to')

    # 2.Seleccionar la tarifa Comfort.
    order_taxi_button = (By.XPATH, '//*[contains(text(), "Pedir un taxi")]')
    comfort_button = (By.XPATH, "//div[@class='tcard-title' and normalize-space()='Comfort']")
    comfort_tariff_button = (By.XPATH, "*//div[contains(@class, ' tcard active') and .//dic[text()='Comfort']*)")


    # 3.Rellenar el número de teléfono.
    add_phone_number = (By.CLASS_NAME, 'np-text')
    phone_number_field = (By.ID, 'phone')
    next_button = (By.XPATH, '//*[contains(text(), "Siguiente")]')
    sms_code = (By.ID, 'code')
    confirm_button = (By.XPATH, '//*[contains(text(), "Confirmar")]')

    # 4.Agregar una tarjeta de crédito.
    payment_method_button = (By.CLASS_NAME, 'pp-text')
    add_card_button = (By.XPATH, '//*[contains(text(), "Agregar tarjeta")]')
    card_number_field = (By.ID, 'number')
    card_code_field = (By.ID, 'code')
    focus_click =(By.CLASS_NAME, 'modal unusual')
    add_button = (By.XPATH, "//button[@type='submit' and text()='Agregar']")
    card_added = (By.CLASS_NAME, 'pp-row')
    x_button = (By.CSS_SELECTOR, '.payment-picker.open .modal .section.active .close-button')

    # 5.Escribir un mensaje para el controlador.
    comment_field = (By.ID, 'comment')

    # 6.Pedir una manta y pañuelos
    requirements_button = (By.CLASS_NAME, 'reqs-header')
    blanket_and_scarves_slider = (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[contains(@class, 'r-sw')]//span[@class='slider round']")

    # 7.Pedir 2 helados
    ice_cream_plus_counter = (By.XPATH, "(//div[@class='counter-plus'])[1]")

    # 8.Aparece el modal para buscar un taxi
    taxi_search_button = (By.CLASS_NAME, 'smart-button-wrapper')


#Metodos
    # 1.Configurar la dirección
    def __init__(self, driver):
        self.driver = driver
        self.locators = UrbanRoutesPage

    def set_from(self, from_address):
        WebDriverWait(self.driver, 15).until(EC.visibility_of_element_located(self.from_field))
        self.driver.find_element(*self.from_field).send_keys(from_address)

    def set_to(self, to_address):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.to_field))
        self.driver.find_element(*self.to_field).send_keys(to_address)

#CORRECCION
    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    # 2.Seleccionar la tarifa Comfort.
    def click_order_taxi_button(self):
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Pedir un taxi")]')))
        self.driver.find_element(*self.order_taxi_button).click()

#CORRECION
    def click_comfort_tariff_button(self):
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[contains(@class, 'r-sw')]//span[@class='slider round']" )))
        self.driver.find_element(*self.comfort_button).click()

    def is_comfort_tariff_selected(self):
        try:
            self.driver.find_element(*self.comfort_button)
            return True
        except:
            return False

    # 3.Rellenar el número de teléfono.
    def click_add_phone_number(self):
        self.driver.find_element(*self.add_phone_number).click()

    def set_phone_number(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'phone')))
        self.driver.find_element(*self.phone_number_field).send_keys(data.phone_number)

    def click_next_button(self):
        self.driver.find_element(*self.next_button).click()

    def set_sms_code(self, code):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'input-container')))
        self.driver.find_element(*self.sms_code).send_keys(code)

    def click_confirm_button(self, code):
        self.driver.find_element(*self.confirm_button).click()

#CORRECION
    def validate_phone_number(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.add_phone_number))
        displayed_number = self.driver.find_element(*self.add_phone_number).text
        assert displayed_number == data.phone_number


    # 4.Agregar una tarjeta de crédito.
    def click_payment_method_button(self):
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CLASS_NAME, 'pp-text')))
        self.driver.find_element(*self.payment_method_button).click()

    def click_add_card_button(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(), "Agregar tarjeta")]')))
        self.driver.find_element(*self.add_card_button).click()

    def click_card_number_field(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'number')))
        self.driver.find_element(*self.card_number_field).click()

    def set_card_number_field(self, card_number):
        self.driver.find_element(*self.card_number_field).send_keys(data.card_number)

    def click_card_code_field(self):
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.ID, 'code')))
        self.driver.find_element(*self.card_code_field).click()

    def set_card_code_field(self, card_code):
        self.driver.find_element(*self.card_code_field).send_keys(card_code)

    def click_focus_click(self):
        self.driver.find_element(*self.focus_click).click()

    def click_add_button(self):
        self.driver.find_element(*self.add_button).click()

    def click_x_button(self):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, 'close-button section-close')))
        self.driver.find_element(*self.x_button).click()

#CORRECION
    def validate_card_number(self, expected_card_number):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.card_added))
        actual_card_number = self.driver.find_element(*self.card_added).text
        assert actual_card_number == expected_card_number

    # 5.Escribir un mensaje para el controlador.
    def set_comment_field(self, message_for_driver):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located((By.ID, 'comment')))
        self.driver.find_element(*self.comment_field).send_keys(message_for_driver)

#CORRECION
    def get_comment_field(self):
            return self.driver.find_element(*self.comment_field).get_attribute('value')

        # 6.Pedir una manta y pañuelos
    def click_requirements_button(self):
            self.driver.find_element(*self.requirements_button).click()

    def click_blanket_and_scarves_slider(self):
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(
                (By.XPATH, "//div[@class='r-sw-label' and text()='Manta y pañuelos']/following-sibling::div[contains(@class, 'r-sw')]//span[@class='slider round']")))
            self.driver.find_element(*self.blanket_and_scarves_slider).click()

        # 7.Pedir 2 helados
    def click_ice_cream_plus_counter(self):
            self.driver.find_element(*self.ice_cream_plus_counter).click()

    def get_selected_ice_cream_count(self):
            ice_cream_count_element = self.driver.find_element(By.XPATH, "(//div[@class='counter-plus'])[1]")
            ice_cream_count = int(ice_cream_count_element.text)
            return ice_cream_count

        # 8.Aparece el modal para buscar un taxi
    def click_taxi_search_button(self):
            WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')))
            self.driver.find_element(*self.taxi_search_button).click()


