from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
import random


def get_house_attributes(address):


    # Format the address for the URL
    formatted_address = '-'.join(address.split(' '))
    url = f"https://www.zillow.com/homes/{formatted_address}_rb/"

    # Path to your ChromeDriver executable
    # chrome_driver_path = r"C:\Program Files\JetBrains\PyCharm Community Edition 2024.2\chrome-win64" # Replace with the path to your chromedriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    # Set up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode if you don't need a browser UI


    # Navigate to the URL
    driver.get(url)

    # Optionally, you can wait for a few seconds to ensure the page loads
    next_data_script = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "__NEXT_DATA__"))
    )

    # Print the title of the page to confirm successful navigation

    # Locate the <script> tag with id='__NEXT_DATA__'
    script_tag = driver.find_element(By.ID, '__NEXT_DATA__')

    # Extract the content of the script tag
    script_content = script_tag.get_attribute('innerHTML')  # or .text for raw text content

    # Optionally parse the content if it's JSON
    r_json = json.loads(script_content)

    try:
        r_json = json.loads(r_json['props']['pageProps']['componentProps']['gdpClientCache'])
        r_json = r_json[next(iter(r_json.keys()))]['property']

    except:
        print(f"No search results were found for {address}")
        driver.quit()
        return None

    # set desired attributes for extraction
    attributes = ['streetAddress',
                  'city',
                  'state',
                  'zipcode',
                  'longitude',
                  'latitude',
                  'homeType',
                  'yearBuilt',
                  'livingArea',
                  'lotSize',
                  'hoaFee',
                  ['resoFacts', 'bathroomsFloat'],
                  ['resoFacts', 'bedrooms'],
                  ['resoFacts', 'parkingCapacity'],
                  ['resoFacts', 'hasHeating'],
                  ['resoFacts', 'hasPrivatePool']
                  ]

    # construct DataFrame with desired attributes
    df = pd.DataFrame()
    for att in attributes:
        if type(att) is list:
            df[att[1]] = [r_json[att[0]][att[1]]]
        else:
            df[att] = [r_json[att]]

    driver.quit()
    return df

if __name__ == "__main__":
    pass
