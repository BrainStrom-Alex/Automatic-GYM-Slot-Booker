from selenium import webdriver
import os
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

already_booked_count = 0
booked_count = 0
waitlist_count = 0

no_booked_count = 0
no_waitlist_count = 0

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://appbrewery.github.io/gym/")

wait = WebDriverWait(driver, 10)
login_button = wait.until(ec.element_to_be_clickable(driver.find_element(By.ID, value="login-button")))
login_button.click()

email_input = wait.until(ec.element_to_be_clickable(driver.find_element(By.ID, value="email-input")))
email_input.clear()
email_input.send_keys("testing.brainstrom@gmail.com")

password_input = wait.until(ec.element_to_be_clickable(driver.find_element(By.ID, value="password-input")))
email_input.clear()
password_input.send_keys("Ravish@07")

submit_button = driver.find_element(By.ID, value="submit-button")
submit_button.click()

wait.until(ec.presence_of_element_located((By.ID, "schedule-page")))

class_cards = driver.find_elements(By.CSS_SELECTOR, value="div[id^='class-card-']")

processed_classes = []
for card in class_cards:
    day_group = card.find_element(By.XPATH, value="./ancestor::div[contains(@id, 'day-group-')]")
    day = day_group.find_element(By.TAG_NAME, value="h2").text
    if "Tue" in day or "Thu" in day:
        times = card.find_elements(By.CSS_SELECTOR, value="p[id^='class-time-']")
        for time in times:
            if "6:00" in time.text:
                booking_condition = card.find_element(By.CSS_SELECTOR, value="button[id^='book-button-']").text
                button = card.find_element(By.CSS_SELECTOR, value="button[id^='book-button-']")
                class_name = card.find_element(By.CSS_SELECTOR, value="h3[id^='class-name-").text
                if booking_condition == "Booked":
                    already_booked_count += 1
                    print(f"✓ Already booked: {class_name} on {day}")
                elif booking_condition == "Waitlisted":
                    already_booked_count += 1
                    print(f"✓ Already Waitlisted: {class_name} on {day}")
                elif booking_condition == "Join Waitlist":
                    waitlist_count += 1
                    processed_classes.append(f"[New Waitlist] {class_name} on {day}")
                    button.click()
                    print(f"✓ Already on waitlist: {class_name} on {day}")
                else:
                    booked_count += 1
                    processed_classes.append(f"[New Booking] {class_name} on {day}")
                    button.click()
                    print(f"✓ Booked: {class_name} on {day}")

booking_section = driver.find_element(By.CSS_SELECTOR, value="a[id^='my-bookings-link']")
booking_section.click()

try:
    booked_class = driver.find_elements(By.CSS_SELECTOR, value="div[id^='booking-card-']")
    for i in booked_class:
        no_booked_count += 1
except NoSuchElementException:
    pass
try:
    waitlist_class = driver.find_elements(By.CSS_SELECTOR, value="div[id^='waitlist-card-']")
    for p in waitlist_class:
        waitlist_count += 1
except NoSuchElementException:
    pass

print("\n--- BOOKING SUMMARY ---")
print(f"Classes booked: {booked_count}")
print(f"Waitlists joined: {waitlist_count}")
print(f"Already booked/waitlisted: {already_booked_count}")
print(f"Total Tuesday 6pm classes processed: {booked_count + waitlist_count + already_booked_count}")

for classes in processed_classes:
    print(f"{classes}")

total_booked = booked_count + waitlist_count + already_booked_count
total_in_booking_section = no_booked_count + waitlist_count

print("--- VERIFICATION RESULT ---")
print(f"Expected: {total_booked} booking")
print(f"Found: {total_in_booking_section} booking")

if total_booked == total_in_booking_section:
    print("✅ SUCCESS: All bookings verified!")
elif total_booked > total_in_booking_section:
    print(f"❌ MISMATCH: Missing {int(total_booked)-int(total_in_booking_section)}")

