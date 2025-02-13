import streamlit as st
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import altair as alt
from datetime import datetime
from urllib.parse import urlparse
import re
import io
import time
import sqlite3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchWindowException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Define price-fetching functions
def fetch_nykaa_price(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use new headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging support
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(10)  # Allow page to load fully

        # Try to extract the price using class name
        try:
            price_element = driver.find_element(By.CLASS_NAME, "css-1jczs19")
            price = price_element.text.strip().replace('₹', '').replace(',', '')
        except Exception:
            # Fallback to regex if direct extraction fails
            page_source = driver.page_source
            match = re.search(r'₹\s?(\d{1,5}(?:,\d{3})*)', page_source)
            price = match.group(1).replace(',', '') if match else "NA"

    except Exception as e:
        print(f"Error fetching Nykaa price: {e}")
        price = "NA"
    
    finally:
        driver.quit()  # Ensure the browser is closed properly

    return price

def fetch_amazon_price(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use new headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging support
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # Wait for the price element to be visible
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "a-price-whole"))
        )

        # Extract and clean the price
        price = price_element.text.strip().replace(',', '')

        return price if price else "NA"

    except Exception as e:
        print(f"Error fetching Amazon price: {e}")
        return "NA"

    finally:
        driver.quit()  # Close browser session
                
def fetch_flipkart_price(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use new headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging support
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        
        # Wait for the price element to load
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "Nx9bqj.CxhGGd"))
            )
        except:
            try:
                price_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "_30jeq3._16Jk6d"))
                )
            except:
                try:
                    price_element = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, "._25b18c ._30jeq3"))
                    )
                except:
                    return "NA"
        
        price = price_element.text.strip().replace('₹', '').replace(',', '')

        return price

    except Exception as e:
        print(f"Error: {e}")
        return "NA"

    finally:
        driver.quit()  # Close browser instance

def fetch_myntra_price(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use new headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging support
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)
        
        # Wait for the price element to load
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "pdp-discount-container"))
            )
            price_text = price_element.text.strip().replace('₹', '').replace(',', '')

            # Extract only the numeric discounted price
            price = price_text.split()[0]  # Extracts only the first numeric value

            return price

        except Exception as e:
            print(f"Error fetching Myntra price: {e}")
            return "NA"

    finally:
        driver.quit()  # Close browser instance
        
def fetch_zepto_price(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use new headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging support
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # Wait for price element to be visible
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span[itemprop='price']"))
            )
            price = price_element.get_attribute("content")  # Extracts price

            return price if price else "NA"

        except Exception as e:
            print(f"Error fetching Zepto price: {e}")
            return "NA"

    finally:
        driver.quit()  # Close browser session

def fetch_faceshop_price(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use new headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging support
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get(url)

        # Wait for the price element to be visible
        try:
            price_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "price-item--sale"))
            )
            price = price_element.text.strip().replace('₹', '').replace(',', '')  # Extracts price

            return price if price else "NA"

        except Exception as e:
            print(f"Error fetching Faceshop price: {e}")
            return "NA"

    finally:
        driver.quit()  # Close browser session
        
def fetch_blinkit_price(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # Use new headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid bot detection
    chrome_options.add_argument("--remote-debugging-port=9222")  # Debugging support
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")
    
    driver = webdriver.Chrome(options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(10)  # Give time for JavaScript content to load

        # Get the full page source
        page_source = driver.page_source

        # Extract the price using regex (₹ followed by numbers)
        match = re.search(r'₹\s?(\d{1,5}(?:,\d{3})*)', page_source)

        if match:
            price = match.group(1).replace(',', '')  # Remove commas
        else:
            price = "NA"

    except NoSuchWindowException:
        print("Error: Browser window closed unexpectedly.")
        price = "NA"
    
    except Exception as e:
        print(f"Error fetching price: {e}")
        price = "NA"
    
    finally:
        driver.quit()  # Close the driver properly
    
    return price

def identify_sales_channel(url):
    if not isinstance(url, str):
        return 'Unknown'

    channels = {
        'nykaa': 'Nykaa',
        'amazon': 'Amazon',
        'myntra': 'Myntra',
        'flipkart': 'Flipkart',
        'zepto': 'Zepto',
        'faceshop': 'Faceshop',
        'blinkit': 'Blinkit'
    }

    parsed_url = urlparse(url).netloc.lower()  # Extract domain

    for keyword, channel in channels.items():
        if keyword in parsed_url:
            return channel
    return 'NA'

def fetch_price(channel, url):
    log=[]
    if channel == 'Amazon':
        return fetch_amazon_price(url)
    elif channel == 'Nykaa':
        return fetch_nykaa_price(url)
    elif channel == 'Flipkart':
        return fetch_flipkart_price(url)
    elif channel == 'Myntra':
        return fetch_myntra_price(url)
    elif channel == 'Zepto':
        return fetch_zepto_price(url)
    elif channel == 'Faceshop':
        return fetch_faceshop_price(url)
    elif channel == 'Blinkit':
        return fetch_blinkit_price(url)
    else:
        return "NA"
    
# Function to run price fetching in parallel
def fetch_price_parallel(row):
    return fetch_price(row['Sales Channel'], row['Channel wise URL'])    
    
DB_FILE = "dataset.db"

# Function to fetch and format data
def fetch_data():
    conn = sqlite3.connect("dataset.db")
    df = pd.read_sql_query("SELECT * FROM products", conn)
    conn.close()

    # Convert SKU_CODE to a string to prevent automatic comma formatting
    if "SKU_CODE" in df.columns:
        df["SKU_CODE"] = df["SKU_CODE"].astype(str)  

    return df

# Function to add a row to the database
def add_row(sku_code, sales_channel, channel_url):
    conn = sqlite3.connect("dataset.db")  # Ensure correct path
    cursor = conn.cursor()

    # Insert new row into `products` table
    cursor.execute(
        """
        INSERT INTO products (SKU_CODE, Product_Description, Channel_wise_URL, Sales_Channel, Price_INR, Timestamp) 
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (sku_code, "Default Description", channel_url, sales_channel, None, None),
    )
     
    conn.commit()
    conn.close()
    
# ----------------- Initialize Query Parameters -----------------
query_params = st.query_params  # Fetch query parameters

# Ensure "Home" is the default page if no page is selected
if "page" not in query_params:
    query_params["page"] = "Home"

# ----------------- Sidebar Navigation -----------------
st.sidebar.title("📌 Navigation")

# Sidebar buttons to change query parameters (navigation)
if st.sidebar.button("🏠 Home"):
    query_params["page"] = "Home"

if st.sidebar.button("📂 Manage Data"):
    query_params["page"] = "ManageData"

if st.sidebar.button("🔍 Fetch Prices"):
    query_params["page"] = "FetchPrices"

if st.sidebar.button("📜 Historical Reads"):
    query_params["page"] = "HistoricalReads"    

# ----------------- Page Rendering Logic -----------------
page = query_params["page"]

# ---------------- HOME PAGE ----------------
if page == "Home":
    st.title("📊 Welcome to Price Scraper Tool")
    st.markdown("This tool helps you **store product details, fetch prices**, and **analyze trends** across different sales channels.")
    st.write("📌 Use the sidebar to navigate.")

# ---------------- MANAGE DATA PAGE ----------------
elif page == "ManageData":
    # Display data directly without a button
    st.subheader("📊 Current Data")
    
    data = fetch_data()
    if not data.empty:
        st.dataframe(data.style.format({"SKU_CODE": "{}"}))  # Ensures no commas
    else:
        st.warning("No data available in the database.")
        st.markdown("---")  # Separator

    st.subheader("➕ Add Data in Database")

    # Input fields for adding data
    sku_code = st.text_input("SKU Code")
    product_description = st.text_input("Product Description")
    channel_url = st.text_input("Channel URL")

    # Function to add a row
    def add_row(sku_code, product_description, channel_url):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO products (SKU_CODE, Product_Description, Channel_wise_URL) VALUES (?, ?, ?)", 
            (sku_code, product_description, channel_url)
        )
        conn.commit()
        conn.close()

    # Function to delete a row
    def delete_row(sku_code):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE SKU_CODE = ?", (sku_code,))
        conn.commit()
        conn.close()

    # Add Row Button
    if st.button("Add Row"):
        if sku_code and product_description and channel_url:
            add_row(sku_code, product_description, channel_url)
            st.success(f"Row with SKU_CODE {sku_code} added successfully!")
        else:
            st.warning("Please fill all fields.")

    st.markdown("---")  # Adds a separator line

    # Delete Row Section
    st.subheader("❌ Delete Data from Database")
    delete_sku_code = st.text_input("Enter SKU Code to Delete")
    
    if st.button("Delete Row"):
        if not delete_sku_code:
            st.warning("Please enter an SKU Code to delete.")
        elif not re.fullmatch(r"\d+", delete_sku_code):  # Ensure only digits (no commas)
            st.error("Invalid format! Enter SKU Code without commas (e.g., 30000, not 30,000).")
        else:
            delete_row(delete_sku_code)
            st.success(f"Row with SKU_CODE {delete_sku_code} deleted successfully!")
            
# ---------------- FETCH PRICES PAGE ----------------
elif page == "FetchPrices":
    st.title("🔍 Fetch Prices from Dataset")
    st.markdown("Click below to fetch the latest prices.")

    # Load existing data (Only SKU_CODE, Product_Description, and Channel_wise_URL)
    data = fetch_data()

    # Function to insert fetched prices into historical.db
    def save_to_historical_db(sku_code, product_desc, sales_channel, price):
        conn = sqlite3.connect("historical.db")
        cursor = conn.cursor()
        
        # Ensure table exists
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS historical_prices (
                SKU_CODE INT NOT NULL,
                Product_Description TEXT NOT NULL,
                Sales_Channel TEXT NOT NULL,
                Price REAL NOT NULL,
                Timestamp TEXT NOT NULL
            )
        ''')

        # Insert data
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO historical_prices (SKU_CODE, Product_Description, Sales_Channel, Price, Timestamp) VALUES (?, ?, ?, ?, ?)", 
                    (sku_code, product_desc, sales_channel, price, timestamp))
        
        conn.commit()
        conn.close()

    if not data.empty:
        if st.button("Fetch the Prices"):
            with st.spinner("Fetching prices..."):
                results = []

                with ThreadPoolExecutor() as executor:
                    for row in data.itertuples():
                        sales_channel = identify_sales_channel(row.Channel_wise_URL)
                        st.write(f"Detected Channel: {sales_channel}")  # Debugging log
                        if sales_channel == "Unknown":
                            st.warning(f"Channel not recognized for URL: {row.Channel_wise_URL}")
                        
                        price = fetch_price(sales_channel, row.Channel_wise_URL)
                        st.write(f"Fetched Price: {price}")  # Debugging log
                        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                        results.append({
                            "SKU_CODE": row.SKU_CODE,
                            "Product_Description": row.Product_Description,
                            "Channel_wise_URL": row.Channel_wise_URL,
                            "Sales_Channel": sales_channel,
                            "Price_INR": price,
                            "Timestamp": timestamp
                        })

                        save_to_historical_db(row.SKU_CODE, row.Product_Description, sales_channel, price)  # Save to historical.db

                result_df = pd.DataFrame(results)
                if result_df.empty or result_df["Price_INR"].isnull().all():
                    st.error("No prices were fetched. Check scraper functions.")
                else:
                    st.success("Prices fetched successfully!")
                    st.write("### 📊 Fetched Prices", result_df)

                    # Download button
                    csv = result_df.to_csv(index=False)
                    st.download_button(label="Download CSV", data=csv, file_name="fetched_prices.csv", mime="text/csv")

                    # Plot price trends
                    st.markdown("### 📈 Price Trends")
                    result_df["Price_INR"] = pd.to_numeric(result_df["Price_INR"], errors="coerce").fillna(0)
                    chart = alt.Chart(result_df).mark_line().encode(
                        x="SKU_CODE:N",
                        y="Price_INR:Q",
                        color="Sales_Channel:N",
                        tooltip=["Sales_Channel", "Price_INR", "Timestamp"]
                    ).properties(width=600, height=400, title="Price Trends Across Channels")
                    st.altair_chart(chart, use_container_width=True)

# ---------------- HISTORICAL READS PAGE ----------------
elif page == "HistoricalReads":
    st.title("📜 Overview the Historical Data")

    # Function to fetch data from historical.db
    def fetch_historical_data():
        conn = sqlite3.connect("historical.db")
        df = pd.read_sql("SELECT * FROM historical_prices", conn)
        conn.close()
        return df

    if st.button("Fetch Historical Data"):
        historical_data = fetch_historical_data()
        if not historical_data.empty:
            st.write("Historical Data:", historical_data)

            # Download historical data
            csv = historical_data.to_csv(index=False)
            st.download_button(label="Download CSV", data=csv, file_name="historical_data.csv", mime="text/csv")
        else:
            st.warning("No historical data found.")
