from selenium import webdriver
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://appbrewery.github.io/gym/")

wait = WebDriverWait(driver, 10)
login_button = wait.until(ec.element_to_be_clickable(driver.find_element(By.ID, value="login-button")))
login_button.click()

email_input = driver.find_element(By.ID, value="email-input")
email_input.clear()
email_input.send_keys("testing.brainstrom@gmail.com")

password_input = driver.find_element(By.ID, value="password-input")
email_input.clear()
password_input.send_keys("abc")

submit_button = driver.find_element(By.ID, value="submit-button")
submit_button.click()

wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

class_cards = driver.find_elements(By.CSS_SELECTOR, value="div[id^='class-card-']")

for card in class_cards:
    day_group = card.find_element(By.XPATH, value="./ancestor::div[contains(@id, 'day-group-')]")
    day = day_group.find_element(By.TAG_NAME, value="h2").text
    if "Mon" in day:
        times = card.find_elements(By.CSS_SELECTOR, value="p[id^='class-time-']")
        for time in times:
            if "6:00" in time.text:
                button = card.find_element(By.CSS_SELECTOR, value="button[id^='book-button-spin-']")
                button.click()

                class_name = card.find_element(By.CSS_SELECTOR, value="h3[id^='class-name-").text

                print(f"✓ Booked: {class_name} on {day}")

