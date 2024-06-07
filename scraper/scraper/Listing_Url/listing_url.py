import os
import time
import datetime
from selenium import webdriver
import shutil
import json
start_time = time.time()
# username = os.environ['D_USERNAME_SECRET']
# passw = os.environ['D_PASSWORD_SECRET']
username ="Marketing@novavacation.com"
passw = "Novabookings@2024!"


website = "https://app.rankbreeze.com/listings"

# Set up Chrome WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
# options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920x1080")

driver = webdriver.Chrome(options=options)


def ranklistingcheck():
    driver.get(website)

    time.sleep(2)

    driver.find_element("xpath", """(//div[@class="form-group"]/input)[1]""").send_keys(username)
    time.sleep(2)
    driver.find_element("xpath", """(//div[@class="form-group"]/input)[2]""").send_keys(passw)
    log = driver.find_element("xpath", """(//div[@class="form-group"]/input)[3]""")
    time.sleep(2)
    log.click()
    time.sleep(3)

    proxy_links = []
    addresses = []

    while True:
        # Get all the desired links on the current page
        links = driver.find_elements("xpath",
                                     """//a[@class="btn btn-outline-primary card-btn custom-nav-button mr-1"]""")
        for link in links:
            web = link.get_attribute("href")
            proxy_links.append(web)

        address_elements = driver.find_elements("xpath", """//td[1]/div[2]/div[1]/small""")
        for element in address_elements:
            address_text = element.text
            address2 = address_text.replace(' - ', '--').replace(' ', '-')
            addresses.append(address2)

        time.sleep(5)
        # Check if there's a "Next" button on the page
        next_buttons = driver.find_elements("xpath", """//span[@class="next"]""")
        if len(next_buttons) > 0:
            # Click the first "Next" button
            next_buttons[0].click()
        else:

            links = driver.find_elements("xpath",
                                         """//a[@class="btn btn-outline-primary card-btn custom-nav-button mr-1"]""")
            for link in links:
                web = link.get_attribute("href")
                proxy_links.append(web)

            address_elements = driver.find_elements("xpath", """//td[1]/div[2]/div[1]/small""")
            for element in address_elements:
                address_text = element.text
                address2 = address_text.replace(' - ', '--').replace(' ', '-')
                addresses.append(address2)
            break

    data = []
    for i in range(min(len(proxy_links), len(addresses))):
        data.append({
            "proxy_link": proxy_links[i],
            "address": addresses[i]
        })

    unique_values = list(set(tuple(item.items()) for item in data))
    unique_data = [dict(item) for item in unique_values]
    return unique_data

def data_to_json(unique_data):
    rankbreeze_Id = []
    airbnb_link = []
    final_data = []

    for item in unique_data:
        proxy_link = item['proxy_link']
        driver.get(proxy_link)
        time.sleep(1)

        r_Id = proxy_link.strip("https://app.rankbreeze.com/rankings/")
        rankbreeze_Id.append(r_Id)
        arbnb_link = driver.find_element("xpath", """//*[@id="get-email"]/div/main/div[3]/ul/a[1]""").get_attribute(
            "href")
        airbnb_link.append(arbnb_link)

        final_data_item = (
            ('proxy_link', proxy_link),
            ('address', item['address']),
            ('rankbreeze_Id', r_Id),
            ('airbnb_link', airbnb_link[-1]),
        )
        final_data.append(final_data_item)

    airbnb_data = []

    for item in final_data:
        airbnb_entry = {
            'proxy_link': item[0][1],
            'address': item[1][1],
            'rankbreeze_Id': item[2][1],
            'airbnb_link': item[3][1]
        }
        airbnb_data.append(airbnb_entry)

    rb_bnb_json = json.dumps(airbnb_data, indent=4)
    with open('json_file/rb_bnb.json', 'w') as f:
        f.write(rb_bnb_json)


unique_data = ranklistingcheck()
data_to_json(unique_data)

end_time = time.time()

elapsed_time = end_time - start_time
minutes = int(elapsed_time // 60)
seconds = int(elapsed_time % 60)
print(f"Time takes {minutes} minutes and {seconds} seconds")
