import time

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.EdgeOptions()
options.headless = True
options.add_argument("--mute-audio")

driver = webdriver.Edge(options=options)
video_url = "https://www.oba.gov.tr/egitim/oynatma/uzman-ogretmenlik-egitim-programi-semineri-meb-personeli-286/"
main_url = "https://www.oba.gov.tr/"

driver.get(main_url)
driver.add_cookie({"name": "PHPSESSID", "value": "SECRET"})

while True:
    try:
        driver.get(video_url)
        time.sleep(5)
        items = driver.find_elements(By.CLASS_NAME, "course-player-object-list-item")
        for item in items:
            icon = item.find_element(By.CLASS_NAME, "mdi")
            if icon.get_attribute("class").find("mdi-circle-slice-3") > 0:
                print(f"{item.text} dersi izlenmeye başlandı.")

        play_button = driver.find_element(By.XPATH, '//*[@id="video"]/button')
        play_button.click()

        time.sleep(1500)

    except Exception as e:
        print("Bir hata oluştu, tekrar deneniyor.")
        print(f"Hata kodu: {e}")
