import os
import re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

def create_download_folder(download_dir):
    today_date = time.strftime("%Y-%m-%d")
    folder_path = os.path.join(download_dir, today_date)
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

def download_files(options_list, download_dir, verbose=False):
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", os.path.abspath(download_dir))
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
    options.set_preference("browser.download.useDownloadDir", True)
    
    for option in options_list:
        driver = webdriver.Firefox(options=options)
        driver.get("https://portalsiedco.policia.gov.co:4443/extensions/PortalPublico/index.html#/home")
        
        WebDriverWait(driver, 60).until(EC.invisibility_of_element_located((By.CLASS_NAME, "flex-loader-cover")))
        
        year_selector = Select(driver.find_element(By.ID, "añosCombo"))
        year_selector.select_by_visible_text("2025")
        
        topic_selector = Select(driver.find_element(By.ID, "tematicasCombo"))
        topic_selector.select_by_visible_text(option)
        
        view_button = driver.find_element(By.XPATH, "//button[text()='Ver indicadores']")
        view_button.click()
        
        try:
            # Wait for municipio_container to be clickable
            municipio_container = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//h6[@aria-label='Municipio' and text()='Municipio']"))
            )
            municipio_container.click()
        except Exception as e:
            print(f"Error clicking municipio_container for option '{option}': {str(e)}")
            driver.quit()
            continue
        
        search_municipio = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Buscar en cuadro de lista']"))
        )
        search_municipio.send_keys("Pereira")
        
        pereira_option = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@title='PEREIRA (CT)']"))
        )
        pereira_option.click()
        
        confirm_button_municipio = driver.find_element(By.XPATH, "//button[@title='Confirmar selección']")
        confirm_button_municipio.click()
        
        footer_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//footer[contains(text(), '2024')]"))
        )
        footer_text = footer_element.text
        file_date = re.search(r"Hasta:\s(\d{2}/\d{2}/\d{4})", footer_text).group(1).replace("/", "-")
        
        download_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "btn-excel")))
        download_button.click()
        
        downloaded_file = None
        start_time = time.time()
        timeout = 60
        
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
            print(f"Download did not complete within the timeout period for option '{option}'")
        else:
            new_file_name = f"{file_date}_{option.replace(' ', '_')}.xlsx"
            new_file_path = os.path.join(download_dir, new_file_name)
            
            os.rename(downloaded_file, new_file_path)
            print(f"File downloaded and renamed to: {new_file_path}")
        
        driver.quit()

# Usage example:
if __name__ == "__main__":
    download_dir = "/home/usuario/Downloads/files_police"
    options_list = [
        "Delitos sexuales",
        "Homicidios",
        "Hurto a residencias",
        "Hurto a comercio",
        "Hurto a personas",
        "Hurto automotores",
        "Hurto motocicletas",
        "Lesiones personales",
        "Violencia intrafamiliar",
        "Capturas",
        "Incautación armas de fuego",
        "Extorsión",
        "Secuestro extorsivo",
        "Secuestro simple",
        "Incautación de estupefacientes",
    ]
    
    download_folder = create_download_folder(download_dir)
    download_files(options_list, download_folder, verbose=True)

