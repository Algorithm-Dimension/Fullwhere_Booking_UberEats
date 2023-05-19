from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import time
import numpy as np
import undetected_chromedriver as uc


URL = "https://admin.booking.com/"
CREDENTIALS = {"username": "Chloé Maison Bayard", "password": "Bayard02023", "phone_number_digit": "5179"}
X_PATHS = {
    "username_fill": "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[1]/div/div/div/input",
    "username_click": "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[3]/button",
    "password_fill": "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[1]/div/div/div/div/input",
    "password_click": "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[2]/button",
    "choose_sms_verif": "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div[2]/a[1]/div",
    "select_phone": "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div[2]/div/div/select/option[2]",
    "send_code_sms": "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/div/div[3]/button",
    "fill_code": "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[1]/div/div/div/div/input",
    "verify_now": "/html/body/div[1]/div/div/div/div[2]/div[1]/div/div/div/div/div/div/form/div[2]/button",
    "guest_review_button": "/html/body/div[1]/div/div/div/header/div[2]/nav/div[2]/div/ul/li[8]/button",
    "guest_review_dropdown": "/html/body/div[1]/div/div/div/header/div[2]/nav/div[2]/div/ul/li[8]/div/ul/li[1]/a",
    "number_of_pages": "/html/body/div[1]/div/div/div/main/div/div[4]/div[1]/div/div[2]/div[11]/div[1]/ul/li[8]/ul/li/a",
    "next_page_button": "/html/body/div[1]/div/div/div/main/div/div[4]/div[1]/div/div[2]/div[11]/div[1]/ul/li[9]/a"
}
REVIEWS_CLASS_NAME = "gr-review-card bui-panel"


def click_function(x_path):
    time.sleep(1)
    button_to_click = driver.find_element(By.XPATH, value=x_path)
    button_to_click.click()
    return

def fill_function(x_path, fill_value):
    time.sleep(1)
    button_to_click = driver.find_element(By.XPATH, value=x_path)
    button_to_click.send_keys(fill_value)
    return

def login_into_our_account():
    """
    LOGIN INTO OUR ACCOUNT
    :return: Success
    """
    # ENTER USERNAME AND CLICK ON NEXT
    fill_function(X_PATHS["username_fill"], CREDENTIALS["username"])
    click_function(X_PATHS["username_click"])

    # ENTER PASSWORD AND CLICK ON NEXT
    fill_function(X_PATHS["password_fill"], CREDENTIALS["password"])
    click_function(X_PATHS["password_click"])

    # SELECT PHONE SMS VERIFICATION, CHOOSE OUR NUMBER AND REQUEST A SMS CODE
    click_function(X_PATHS["choose_sms_verif"])
    click_function(X_PATHS["select_phone"]) # TODAY THE SMS IN THE LIST HAVE BEEN SELECTED MANUALLY - TO CHANGE
    click_function(X_PATHS["send_code_sms"])

    # ENTER THE CODE AND LOGIN
    code_ = input("WHAT IS THE CODE?") # FOR NOW CODE IS RECEIVED BY INPUT, TO CHANGE WITH FLASK APP
    fill_function(X_PATHS["fill_code"], str(code_))
    click_function(X_PATHS["verify_now"])
    print("Successfully logged in")
    return

def get_on_scrap_page():
    click_function(X_PATHS["guest_review_button"])
    click_function(X_PATHS["guest_review_dropdown"])
    print("Successfully got into the guest page")
    return

def scrapping():
    page_number_value = int(driver.find_element(By.XPATH, value=X_PATHS["number_of_pages"]).text)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    review_elements = soup.find_all(class_=REVIEWS_CLASS_NAME)
    reviews = [elem.text for elem in review_elements]
    final_reviews = [[x.strip() for x in r_.replace("-", "").split("\n") if len(x.strip()) > 0] for r_ in reviews]

    for _ in range(page_number_value):
        time.sleep(2 + np.random.randint(3))
        next_page = X_PATHS["next_page_button"]
        guest_path_button = driver.find_element(By.XPATH, value=next_page)
        guest_path_button.click()
        time.sleep(3 + np.random.randint(4))
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        review_elements = soup.find_all(class_=REVIEWS_CLASS_NAME)
        reviews = [elem.text for elem in review_elements]
        final_reviews.extend(
            [[x.strip() for x in r_.replace("-", "").split("\n") if len(x.strip()) > 0] for r_ in reviews])

        return final_reviews


if __name__ == "__main__":
    driver = uc.Chrome()
    driver.get(URL)
    login_into_our_account()
    time.sleep(10)
    get_on_scrap_page()
    time.sleep(5)
    driver.execute_script("window.scrollTo(0, 1000);") # TO CHECK IF MANDATORY
    reviews = scrapping()

    for review in reviews[:50]:
        for line_ in review:
            print(line_, "\n")
