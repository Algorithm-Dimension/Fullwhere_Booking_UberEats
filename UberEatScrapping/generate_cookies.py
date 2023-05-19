from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager

URL = "https://auth.uber.com/login/?breeze_local_zone=dca1&next_url=https://restaurant.uber.com/"
EMAIL_ = "accountlogin1@fullwhere.com"
PASSWORD_ = "Crea28Tive45!:1"

LOGIN_XPATH = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[2]/div[1]/bdi/div[2]/div/input"
LOGIN_CLICK_XPATH = "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[2]/button"
PASSWORD_XPATH = "/html/body/div[1]/div[1]/div[2]/div/div/div/div[1]/div[2]/div/div/input"
PASSWORD_CLICK_XPATH = "/html/body/div[1]/div[1]/div[2]/div/div/div/div[3]/div/div/button[2]"

COOKIE_ORDER = ["usl_rollout_id", "sid", "_ua", "selectedRestaurant", "udi-id", "jwt-session",
                "mp_adec770be288b16d9008c964acfba5c2_mixpanel", "_cc", "_cid_cc", "udi-fingerprint"]


def click_function(driver, x_path):
    time.sleep(1)
    button_to_click = driver.find_element(By.XPATH, value=x_path)
    button_to_click.click()
    return


def fill_function(driver, x_path, fill_value):
    time.sleep(1)
    button_to_click = driver.find_element(By.XPATH, value=x_path)
    button_to_click.send_keys(fill_value)
    return


def reformat_cookies(cookie_dict):
    final_cookie = ""
    for cook_ in COOKIE_ORDER:
        final_cookie += cook_ + "=" + cookie_dict[cook_] + "; "

    return final_cookie


def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(URL)
    fill_function(driver, LOGIN_XPATH, EMAIL_)
    click_function(driver, LOGIN_CLICK_XPATH)

    # TODO A INTEGRER ICI LA VERIF GMAIL A LA PLACE DU PASSWORD
    # TODO 1: CHECK SI VERIF DEMANDER
    # TODO 2: SI OUI, RECUP LE CODE SUR GMAIL ET INTEGRER AU SCRAP
    # TODO 3: SI NON, VERIF PASSWORD SI DESSOUS

    fill_function(driver, PASSWORD_XPATH, PASSWORD_)
    click_function(driver, PASSWORD_CLICK_XPATH)

    time.sleep(20)
    cookies = driver.get_cookies()
    cookie_dict = {cookie['name']: cookie['value'] for cookie in cookies}

    final_cookies = reformat_cookies(cookie_dict)

    with open("files/cookies.txt", "w") as file:
        file.write(final_cookies)


if __name__ == "__main__":
    # TODO A FAIRE TEST POUR SAVOIR LA DUREE DE VIE D'UN COOKIE
    main()







