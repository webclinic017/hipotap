from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time
import pandas as pd

FILE_PATH_FOLDER = '.'
search_query = 'https://www.itaka.pl/'
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path='../chromedriver_win32/chromedriver.exe', options=options)
offers_details = []
driver.get(search_query)
time.sleep(5)
# Choose when - anytime, destination - anywhere, number of tourists - 1 adult
driver.find_element_by_id("participants-count").click()
dropdown = driver.find_elements_by_xpath("//div[@class='dropdown-menu']")[0]
dropdown.find_elements_by_xpath("//a[@class='number-select-action number-select-action-less']")[0].click()
dropdown.find_elements_by_xpath("//span[@class='dropdown-menu-close dropdown-menu-confirm']")[0].click()
driver.find_elements_by_xpath("//button[@type='submit']")[0].click()
time.sleep(5)
# Scrap information from the pages
offers_list = driver.find_elements_by_xpath("//article[@class='offer clearfix']")
print(f"offers_list: {offers_list}")
for each_offer in offers_list:
    # Getting offer info
    offer_title = each_offer.find_elements_by_xpath(".//h3[@class='header_title']/a")[0]
    number_of_days = each_offer.find_elements_by_xpath(".//div[@class='offer_date pull-right']")[1]
    price = each_offer.find_elements_by_xpath(".//span[@class='current-price_value']")[1]
    offer_type = each_offer.find_elements_by_xpath(".//span[@class='offer_type_title']")[0]
    place = each_offer.find_elements_by_xpath(".//div[@class='header_geo-labels']")[0]
    offer_info = [offer_type.text, offer_title.text, number_of_days.text, price.text, place.text]
    #print(offer_info)
    offers_details.append(offer_info)
driver.quit()
print(offers_details)
# Write to the csv file
offers_details_df = pd.DataFrame(offers_details)
offers_details_df.columns = ['type', 'title', 'number_of_days', 'price', 'place']
offers_details_df.to_csv('offers_details.csv', index=False)