import streamlit as st
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException


#------------------------------------------Streamlit------------------------------------------


st.set_page_config(layout="wide")
st.sidebar.title("Start Here")

st.sidebar.write("What products should we compare?")

user_input = st.sidebar.text_input("Product name","Tefal")


# Getting URL for product

# ---------------Generating Product for Shopee--------------

def get_url_shopee(product):
    product = product.replace(' ', '%20')
    template = 'https://shopee.com.my/search?keyword={}'
    url = template.format(product)
    return url

def get_shopee_products(card):
    pImg = card.find('img')
    product_image = pImg['src']
    product_name = card.find('div', '_10Wbs- _2STCsK _3IqNCf').text.strip()
    # This to ignore special characters/emoji --> change into bytecode
    product_name = product_name.encode('ascii', 'ignore')
    # This to remove bytecode(B) in product_name
    product_name = str(product_name, 'utf-8')
    product_price = card.find('div', 'zp9xm9 kNGSLn l-u0xK').text.strip()
    anchor_tag = card.a.get('href')
    product_buy_link = 'https://shopee.com.my' + anchor_tag

    product_info = {"product_image": product_image,
                    "product_name": product_name,
                    "product_price": product_price,
                    "product_buy_link": product_buy_link}

    return product_info

#------------------Generating Product for Lazada

def get_url_lazada(product):
    product = product.replace(' ', '+')
    template = 'https://www.lazada.com.my/catalog/?q={}'
    url = template.format(product)
    return url

def get_lazada_products(card):
    pImg = card.find('img', 'jBwCF')
    product_image = pImg['src']
    product_name = card.find('div', 'RfADt').text.strip()

    # This to ignore special characters/emoji --> change into bytecode
    product_name = product_name.encode('ascii', 'ignore')

    # This to remove bytecode(B) in product_name
    product_name = str(product_name, 'utf-8')
    product_price = card.find('span', 'ooOxS').text.strip()
    anchor_tag = card.a.get('href')
    product_buy_link = anchor_tag.lstrip("/")

    product_info = (product_image, product_name, product_price, product_buy_link)
    product_info = {"product_image": product_image,
                    "product_name": product_name,
                    "product_price": product_price,
                    "product_buy_link": product_buy_link}

    return product_info


# ---------------Main Function--------------

def main(product):
    shopee_progress = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.1)
        st.write("Initializing Shopee Crawler..")
        shopee_progress.progress(percent_complete + 10)
        url = get_url_shopee(product)

        options = Options()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--log-level=3')

        #-------------------Shopee------------
        st.write("Web Crawler Initialized")
        shopee_progress.progress(percent_complete + 10)
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get(url)
        driver.maximize_window()
        time.sleep(5)
        btn = driver.find_element(By.XPATH, '//*[@id="modal"]/div[1]/div[1]/div/div[3]/div[1]/button')
        btn.click()
        time.sleep(5)
        st.write("Scraping..")
        shopee_progress.progress(percent_complete + 20)
        # Define an initial value
        temp_height = 0
        while True:
            # Looping down the scroll bar
            driver.execute_script("window.scrollBy(0,1000)")
            # sleep and let the scroll bar react
            time.sleep(5)
            # Get the distance of the current scroll bar from the top
            check_height = driver.execute_script(
                "return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            # If the two are equal to the end
            if check_height == temp_height:
                break
            temp_height = check_height
        st.write("Scraping finished! Compiling data..")
        shopee_progress.progress(percent_complete + 20)
        time.sleep(3)

        # Creating a BSoup object
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        product_cards = soup.find_all('div', 'col-xs-2-4')
        # Fetching single product
        singleCard = product_cards[0]
        productDetails = get_shopee_products(singleCard)
        st.write("Shopee data is ready!")
        shopee_progress.progress(percent_complete + 40)
        break

#-------------Lazada----------------
    lazada_progress = st.progress(0)

    for completion in range(100):
        time.sleep(0.1)
        st.write("Initializing Lazada Crawler..")
        lazada_progress.progress(completion + 10)
        lazada_url = get_url_lazada(product)

        options = Options()
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        options.add_argument('--log-level=3')

        st.write("Web Crawler Initialized")
        lazada_progress.progress(completion + 10)

        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get(lazada_url)
        driver.maximize_window()
        time.sleep(5)
        try:
            slider = driver.find_element(By.XPATH, '/ html / body / div / div[2] / div / div[1] / div[2] / center / div[1] / div / div[1] / div[2]')
            ActionChains(driver).drag_and_drop_by_offset(slider, 400, 0).perform()
            time.sleep(10)
        except NameError:
            pass
        except NoSuchElementException:
            pass

        st.write("Scraping..")
        lazada_progress.progress(completion + 20)

        # Define an initial value
        temp_height = 0
        while True:
            # Looping down the scroll bar
            driver.execute_script("window.scrollBy(0,1000)")
            # sleep and let the scroll bar react
            time.sleep(5)
            # Get the distance of the current scroll bar from the top
            check_height = driver.execute_script("return document.documentElement.scrollTop || window.pageYOffset || document.body.scrollTop;")
            # If the two are equal to the end
            if check_height == temp_height:
                break
            temp_height = check_height
        st.write("Scraping finished! Compiling data..")
        lazada_progress.progress(completion + 20)
        time.sleep(3)

        # Creating a BSoup object
        soup2 = BeautifulSoup(driver.page_source, 'html.parser')
        product_cards_lz = soup2.find_all('div', 'Bm3ON')

        # Fetching single product
        lazadaCard = product_cards_lz[0]
        lazadaDetails = get_lazada_products(lazadaCard)

        st.write("Lazada data is ready!")
        lazada_progress.progress(completion + 40)
        break


    #Table Setting

    col1, col2 = st.columns(2)
    with col1:
        st.header("Shopee")
        st.write(str(productDetails["product_name"]))
        st.write(str(productDetails["product_price"]))
        st.write(productDetails["product_buy_link"],unsafe_allow_html=True)

    with col2:
        st.header("Lazada")
        st.write(str(lazadaDetails["product_name"]))
        st.write(str(lazadaDetails["product_price"]))
        st.write(lazadaDetails["product_buy_link"], unsafe_allow_html=True)

if st.sidebar.button("Compare"):
    main(user_input)































