from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
import time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import re

os.system("clear")
download_dir = "/home/usuario/Documents/policia_files/"
time_wait = 60
options_list = [
    # "Abigeato",
    # "Amenazas",
    "Delitos sexuales",
    "Homicidios",
    # "Homicidios en accidentes de tránsito",
    "Hurto a residencias",
    "Hurto a comercio",
    "Hurto a personas",
    "Hurto automotores",
    "Hurto motocicletas",
    # "Hurto entidades financieras",
    "Lesiones personales",
    # "Piratería terrestre",
    # "Terrorismo",
    "Violencia intrafamiliar",
    "Capturas",
    "Incautación armas de fuego",
    "Extorsión",
    # "Lesiones en accidentes de tránsito",
    "Secuestro extorsivo",
    "Secuestro simple",
    "Incautación de estupefacientes",
    # "Automotores recuperados",
    # "Motocicletas recuperadas",
]

options = Options()
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", os.path.abspath(download_dir))
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
options.set_preference("browser.download.useDownloadDir", True)



for option in options_list:
    driver = webdriver.Firefox(options=options)
    driver.get("https://portalsiedco.policia.gov.co:4443/extensions/PortalPublico/index.html#/home")
    WebDriverWait(driver, time_wait).until(EC.invisibility_of_element_located((By.CLASS_NAME, "flex-loader-cover")))
    year_selector = Select(driver.find_element(By.ID, "añosCombo"))
    year_selector.select_by_visible_text("2025")
    topic_selector = Select(driver.find_element(By.ID, "tematicasCombo"))
    topic_selector.select_by_visible_text(option)
    view_button = driver.find_element(By.XPATH, "//button[text()='Ver indicadores']")
    view_button.click()
    municipio_container = WebDriverWait(driver, time_wait).until(
        EC.presence_of_element_located((By.XPATH, "//h6[@aria-label='Municipio' and text()='Municipio']"))
    )
    WebDriverWait(driver, time_wait).until(EC.invisibility_of_element_located((By.CLASS_NAME, "flex-loader-cover")))
    municipio_container.click()
    search_municipio = WebDriverWait(driver, time_wait).until(
    	EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Buscar en cuadro de lista']"))
    )
    search_municipio.send_keys("Pereira")
    pereira_option = WebDriverWait(driver, time_wait).until(
        EC.presence_of_element_located((By.XPATH, "//div[@title='PEREIRA (CT)']"))
    )
    pereira_option.click()
    confirm_button_municipio = driver.find_element(By.XPATH, "//button[@title='Confirmar selección']")
    confirm_button_municipio.click()
    footer_element = WebDriverWait(driver, time_wait).until(
        EC.presence_of_element_located((By.XPATH, "//footer[contains(text(), '2024')]"))
    )
    footer_text = footer_element.text
    file_date = re.search(r"Hasta:\s(\d{2}/\d{2}/\d{4})", footer_text).group(1).replace("/", "-")
    download_button = WebDriverWait(driver, time_wait).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-excel")))
    download_button.click()
    timeout = time_wait
    start_time = time.time()
    downloaded_file = None
    while time.time() - start_time < timeout:
        files = os.listdir(download_dir)
        for file in files:
            if file.endswith(".xlsx"):
                downloaded_file = os.path.join(download_dir, file)
                break
        if downloaded_file:
            break
        time.sleep(1)
    if not downloaded_file:
        raise Exception("Download did not complete within the timeout period")
    new_file_name = f"{file_date}_{option.replace(' ', '_')}.xlsx"
    new_file_path = os.path.join("/home/usuario/Downloads/files_police", new_file_name)
    os.rename(downloaded_file, new_file_path)
    print(f"File downloaded and renamed to: {new_file_path}")

    driver.quit()

