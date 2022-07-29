import time
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.EdgeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

cookie_driver = webdriver.Edge(options=options)
oba_login_url = "https://mebbisyd.meb.gov.tr/ssologinBIDB.aspx?id=72&URL=http://giris.eba.gov.tr/EBA_GIRIS/GirisKontrol/oba"
phpsessid_cookie = ""
cookie_driver.get(oba_login_url)

print("Giriş yapmanız bekleniyor. Giriş yaptıktan sonra sekme otomatik olarak kapanacaktır.")

while len(phpsessid_cookie) <= 0:
    for i in cookie_driver.get_cookies():
        if i.get("name") == "PHPSESSID":
            phpsessid_cookie = i.get("value")
    time.sleep(2)

cookie_driver.close()
print("Giriş başarılı!")

options.headless = True
options.add_argument("--mute-audio")

driver = webdriver.Edge(options=options)
video_url = "https://www.oba.gov.tr/egitim/oynatma/uzman-ogretmenlik-egitim-programi-semineri-meb-personeli-286/"
main_url = "https://www.oba.gov.tr/"

driver.get(main_url)
driver.add_cookie({"name": "PHPSESSID", "value": phpsessid_cookie})

while True:
    try:
        wait_second = 1500
        driver.get(video_url)
        time.sleep(5)
        items = driver.find_elements(By.CLASS_NAME, "course-player-object-list-item")
        for item in items:
            icon = item.find_element(By.CLASS_NAME, "mdi")
            if icon.get_attribute("class").find("mdi-circle-slice-3") > 0:
                print(f"[{datetime.now()}] {item.text} dersi izlenmeye başlandı.")
                text = item.text
                wait_second = int(text[text.find("(") + 1:text.find("dk")]) * 60
                wait_second += int(text[text.find("dk ") + 3:text.find("sn")])
                # for network connection stability :)
                wait_second += 60

        play_button = driver.find_element(By.XPATH, '//*[@id="video"]/button')
        play_button.click()

        time.sleep(wait_second)

    except Exception as e:
        print(f"[{datetime.now()}] Bir hata oluştu, tekrar deneniyor.")
        print(f"Hata kodu: {e}")
