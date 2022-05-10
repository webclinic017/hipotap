import re
import time
from selenium import webdriver

def test_zero_number_purchase(driver):
    driver.get('http://localhost:17212/offer/1')
    driver.find_element_by_id("adult_count").clear()
    driver.find_element_by_id("adult_count").send_keys('0')
    driver.find_element_by_id("children_count").clear()
    driver.find_element_by_id("children_count").send_keys('0')
    driver.find_element_by_name("purchase_button").click()
    notification = driver.find_elements_by_xpath("//div[@class='notification is-danger']")
    assert notification
    

def test_zero_number_reserve(driver):
    driver.get('http://localhost:17212/offer/1')
    driver.find_element_by_id("adult_count").clear()
    driver.find_element_by_id("adult_count").send_keys('0')
    driver.find_element_by_id("children_count").clear()
    driver.find_element_by_id("children_count").send_keys('0')
    driver.find_element_by_name("reserve_button").click()
    notification = driver.find_elements_by_xpath("//div[@class='notification is-danger']")
    assert notification

def test_big_number_purchase(driver):
    driver.get('http://localhost:17212/offer/1')
    table = driver.find_elements_by_xpath("//table//tbody")[0]
    entry_values = table.find_elements_by_xpath("//tr//td")
    result = re.search(r"^(.*) - (.*)", entry_values[6].text)
    adults_max = result.group(2)
    driver.find_element_by_id("adult_count").clear()
    driver.find_element_by_id("adult_count").send_keys(f"{int(adults_max) + 1}")
    driver.find_element_by_name("purchase_button").click()
    assert driver.current_url == 'http://localhost:17212/offer/1'

def test_purchase(driver):
    driver.get('http://localhost:17212/offer/1')
    table = driver.find_elements_by_xpath("//table//tbody")[0]
    entry_values = table.find_elements_by_xpath("//tr//td")
    result = re.search(r"^(.*) - (.*)", entry_values[6].text)
    adults_max = int(result.group(2))
    result = re.search(r"^(.*) - (.*)", entry_values[7].text)
    children_max = int(result.group(2))
    adult_price = float(entry_values[4].text)
    children_price = float(entry_values[5].text)
    driver.find_element_by_id("adult_count").clear()
    driver.find_element_by_id("adult_count").send_keys(f"{int(adults_max)}")
    driver.find_element_by_id("children_count").clear()
    driver.find_element_by_id("children_count").send_keys(f"{int(children_max)}")
    driver.find_element_by_name("purchase_button").click()
    assert driver.current_url != 'http://localhost:17212/offer/1'

    table = driver.find_elements_by_xpath("//table//tbody")[0]
    entry_values = table.find_elements_by_xpath("//tr//td")
    price = adults_max * adult_price + children_max*children_price
    given_price = float(entry_values[4].text)
    assert given_price == price
    driver.find_element_by_id("card_number").send_keys("1234567890")
    driver.find_elements_by_xpath("//button[@class='button is-secondary']")[0].click()
    notification = driver.find_elements_by_xpath("//div[@class='notification is-success']")
    assert 'payment' not in driver.current_url
    assert notification


def test_purhcase_without_login(driver):
    driver.get('http://localhost:17212/offer/1')
    purchase_button = driver.find_elements_by_xpath("//button[@name='purchase_button']")
    assert not purchase_button

if __name__ == "__main__":
    CHROMEDRIVER_PATH = '../chromedriver_win32/chromedriver.exe'
    options = webdriver.ChromeOptions()
    search_query = 'http://localhost:17212/login'
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    time.sleep(1)
    test_purhcase_without_login(driver)
    #Log in
    driver.get(search_query)
    driver.find_element_by_name("email").send_keys("a@a")
    driver.find_element_by_name("password").send_keys("123")
    driver.find_elements_by_xpath("//button[@class='button is-block is-info is-large is-fullwidth']")[0].click()
    time.sleep(1)
    test_zero_number_purchase(driver)
    test_zero_number_reserve(driver)
    test_big_number_purchase(driver)
    test_purchase(driver)
    driver.quit()
    print("Everything passed")