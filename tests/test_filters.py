import re
import time
from selenium import webdriver

ADULTS_NUM_KEY = 25
CHILDREN_NUM_KEY = 15
ADULTS_MAX_PRICE = 4000
CHILDREN_MAX_PRICE = 1500
HOTEL_STRING_TO_FIND = "Blue" 
PLACE_STRING_TO_FIND = "Korfu" 
DATE_START_KEY = "05162022"
DATE_END_KEY = "05232022"

def test_adults_num(driver):
    driver.find_element_by_id("allowed_adult_count").send_keys(ADULTS_NUM_KEY)
    driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
    table = driver.find_elements_by_xpath("//table//tbody")[0]
    table_entries = table.find_elements_by_xpath("//tr")
    entry_values = table.find_elements_by_xpath("//tr//td")
    i = 0
    adults_nums = []
    while(i < len(table_entries) - 1):
        result = re.search(r"^(.*) - (.*)", entry_values[6 + i * 11].text)
        adults_nums.append(result.group(2))
        i+=1
    for num in adults_nums:
        assert int(num) >= ADULTS_NUM_KEY

def test_children_num(driver):
    driver.find_element_by_id("allowed_children_count").send_keys(CHILDREN_NUM_KEY)
    driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
    table = driver.find_elements_by_xpath("//table//tbody")[0]
    table_entries = table.find_elements_by_xpath("//tr")
    entry_values = table.find_elements_by_xpath("//tr//td")
    i = 0
    children_nums = []
    while(i < len(table_entries) - 1):
        result = re.search(r"^(.*) - (.*)", entry_values[7 + i * 11].text)
        children_nums.append(result.group(2))
        i+=1
    for num in children_nums:
        assert int(num) >= CHILDREN_NUM_KEY

def test_adults_max_price(driver):
    driver.find_element_by_id("max_adult_price").send_keys(ADULTS_MAX_PRICE)
    driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
    table = driver.find_elements_by_xpath("//table//tbody")[0]
    table_entries = table.find_elements_by_xpath("//tr")
    entry_values = table.find_elements_by_xpath("//tr//td")
    i = 0
    prices = []
    while(i < len(table_entries) - 1):
        prices.append(entry_values[4 + i * 11].text)
        i+=1
    for price in prices:
        assert float(price) <= ADULTS_MAX_PRICE

def test_children_max_price(driver):
    driver.find_element_by_id("max_children_price").send_keys(CHILDREN_MAX_PRICE)
    driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
    table = driver.find_elements_by_xpath("//table//tbody")[0]
    table_entries = table.find_elements_by_xpath("//tr")
    entry_values = table.find_elements_by_xpath("//tr//td")
    i = 0
    prices = []
    while(i < len(table_entries) - 1):
        prices.append(entry_values[5 + i * 11].text)
        i+=1
    for price in prices:
        assert float(price) <= CHILDREN_MAX_PRICE

def test_hotel(driver):
    driver.find_element_by_id("hotel").send_keys(HOTEL_STRING_TO_FIND)
    driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
    table = driver.find_elements_by_xpath("//table//tbody")[0]
    table_entries = table.find_elements_by_xpath("//tr")
    entry_values = table.find_elements_by_xpath("//tr//td")
    i = 0
    names = []
    while(i < len(table_entries) - 1):
        names.append(entry_values[3 + i * 11].text)
        i+=1
    for name in names:
        # case insensitive
        assert HOTEL_STRING_TO_FIND in name or HOTEL_STRING_TO_FIND.lower() in name

def test_place(driver):
    driver.find_element_by_id("place").send_keys(PLACE_STRING_TO_FIND)
    driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
    table = driver.find_elements_by_xpath("//table//tbody")[0]
    table_entries = table.find_elements_by_xpath("//tr")
    entry_values = table.find_elements_by_xpath("//tr//td")
    i = 0
    names = []
    while(i < len(table_entries) - 1):
        names.append(entry_values[2 + i * 11].text)
        i+=1
    for name in names:
        # case insensitive
        assert PLACE_STRING_TO_FIND in name or PLACE_STRING_TO_FIND.lower() in name

def test_date_start(driver):
    driver.find_element_by_id("date_start").send_keys(DATE_START_KEY)
    driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
    table = driver.find_elements_by_xpath("//table//tbody")[0]
    table_entries = table.find_elements_by_xpath("//tr")
    entry_values = table.find_elements_by_xpath("//tr//td")
    i = 0
    dates = []
    while(i < len(table_entries) - 1):
        result = re.search(r"^(.*)-(.*)-(.*)", entry_values[8 + i * 11].text)
        dates.append(result.group(2) + result.group(3) + result.group(1))
        i+=1
    for date in dates:
        assert date == DATE_START_KEY

def test_date_end(driver):
    driver.find_element_by_id("date_end").send_keys(DATE_END_KEY)
    driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
    table = driver.find_elements_by_xpath("//table//tbody")[0]
    table_entries = table.find_elements_by_xpath("//tr")
    entry_values = table.find_elements_by_xpath("//tr//td")
    i = 0
    dates = []
    while(i < len(table_entries) - 1):
        result = re.search(r"^(.*)-(.*)-(.*)", entry_values[9 + i * 11].text)
        dates.append(result.group(2) + result.group(3) + result.group(1))
        i+=1
    for date in dates:
        assert date == DATE_END_KEY

if __name__ == "__main__":
    CHROMEDRIVER_PATH = '../chromedriver_win32/chromedriver.exe'
    search_query = 'http://localhost:17212/offers'
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)
    driver.get(search_query)
    time.sleep(1)
    test_adults_num(driver)
    test_children_num(driver)
    test_adults_max_price(driver)
    test_children_max_price(driver)
    test_hotel(driver)
    test_place(driver)
    test_date_start(driver)
    test_date_end(driver)
    driver.quit()
    print("Everything passed")