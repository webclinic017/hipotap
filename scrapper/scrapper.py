from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pandas as pd
import re
import math

FILE_PATH_FOLDER = '.'
search_query = 'https://www.itaka.pl/'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='../chromedriver_win32/chromedriver.exe', options=options)
offers_details = []
driver.get(search_query)
time.sleep(2)
# Choose when - anytime, destination - anywhere, number of tourists - 1 adult
driver.find_element_by_id("participants-count").click()
dropdown = driver.find_elements_by_xpath("//div[@class='dropdown-menu']")[0]
dropdown.find_elements_by_xpath("//a[@class='number-select-action number-select-action-less']")[0].click()
dropdown.find_elements_by_xpath("//span[@class='dropdown-menu-close dropdown-menu-confirm']")[0].click()
driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
time.sleep(2)
# Filter hotel tours only
driver.find_element_by_class_name("single-select").click()
dropdown = driver.find_elements_by_xpath("//div[@class='single-select_content']")[0]
dropdown.find_elements_by_xpath("//div[@class='single-select_item ']")[0].click()
time.sleep(2)

# Open all additional pages
more_offers = driver.find_elements_by_xpath("//div[@class='offer-list_more-offers clearfix']")
while(len(more_offers) > 0):
    driver.execute_script("arguments[0].click();", more_offers[0])
    time.sleep(2)
    more_offers = driver.find_elements_by_xpath("//div[@class='offer-list_more-offers clearfix']")

# Scrap information from the page
offers_list = driver.find_elements_by_xpath("//article[@class='offer clearfix']")
for each_offer in offers_list:
    # Getting offer info
    hotel_elem = each_offer.find_elements_by_xpath(".//h3[@class='header_title']/a")[0]
    period_elem = each_offer.find_elements_by_xpath(".//div[@class='offer_date pull-right']")[1]  #08.05-15.05.22 (8 dni) lub 25.12.22-01.01.23 (8 dni)
    result = re.search(r"^(.*)-(.*) \((.*) dni\)", period_elem.text)
    start_date = result.group(1)
    end_date = result.group(2)
    number_of_days = int(result.group(3))
    if len(start_date)==5:
        # Add year
        start_date+=end_date[5:8]
    price_elem = each_offer.find_elements_by_xpath(".//span[@class='current-price_value']")[1]
    result = re.search(r"^(.*) PLN / os", price_elem.text)
    price = result.group(1);
    price = int(price.replace(" ", ""))
    child_price = math.floor(price/2)
    place_elem = each_offer.find_elements_by_xpath(".//div[@class='header_geo-labels']")[0]
    offer_info = [hotel_elem.text, start_date, end_date, number_of_days, price, child_price, place_elem.text]
    print(offer_info)
    offers_details.append(offer_info)
driver.quit()
print(len(offers_details))
# Write to the csv file
#offers_details_df = pd.DataFrame(offers_details)
#offers_details_df.columns = ['type', 'title', 'number_of_days', 'price', 'place']
#offers_details_df.to_csv('offers_details.csv', index=False)