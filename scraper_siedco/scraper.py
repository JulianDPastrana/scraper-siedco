from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import re
from typing import Optional

def download_file_for_option(option: str, driver: webdriver.Firefox, base_url: str, 
                             base_download_dir: str, time_wait: int) -> None:
    """
    Navigates through the page for the given option, extracts the download date,
    checks if the target file already exists, and if not, downloads and moves the file.
    """
    # Reset page state by loading a blank page and then the target URL.
    driver.get("about:blank")
    time.sleep(1)  # Allow a moment for the blank page to load
    
    # Append a query parameter to force a fresh page load.
    current_url: str = f"{base_url}?r={time.time()}"
    driver.get(current_url)
    
    # Wait until any loading overlay disappears.
    WebDriverWait(driver, time_wait).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "flex-loader-cover"))
    )
    
    # Select the year.
    year_selector: Select = Select(driver.find_element(By.ID, "añosCombo"))
    year_selector.select_by_visible_text("2025")
    
    # Select the topic (option).
    topic_selector: Select = Select(driver.find_element(By.ID, "tematicasCombo"))
    topic_selector.select_by_visible_text(option)
    
    # Click the "Ver indicadores" button.
    view_button = driver.find_element(By.XPATH, "//button[text()='Ver indicadores']")
    view_button.click()
    
    # Wait for and click the Municipio container.
    municipio_container = WebDriverWait(driver, time_wait).until(
        EC.presence_of_element_located((By.XPATH, "//h6[@aria-label='Municipio' and text()='Municipio']"))
    )
    # Wait again for the loader to disappear before proceeding.
    WebDriverWait(driver, time_wait).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "flex-loader-cover"))
    )
    municipio_container.click()
    
    # Search for and select "Pereira".
    search_municipio = WebDriverWait(driver, time_wait).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Buscar en cuadro de lista']"))
    )
    search_municipio.send_keys("Pereira")
    
    pereira_option = WebDriverWait(driver, time_wait).until(
        EC.presence_of_element_located((By.XPATH, "//div[@title='PEREIRA (CT)']"))
    )
    pereira_option.click()
    
    confirm_button = driver.find_element(By.XPATH, "//button[@title='Confirmar selección']")
    confirm_button.click()
    
    # Extract the date from the footer text.
    footer_element = WebDriverWait(driver, time_wait).until(
        EC.presence_of_element_located((By.XPATH, "//footer[contains(text(), '2024')]"))
    )
    footer_text: str = footer_element.text
    file_date_match = re.search(r"Hasta:\s(\d{2}/\d{2}/\d{4})", footer_text)
    if not file_date_match:
        raise Exception("Could not extract date from footer.")
    file_date: str = file_date_match.group(1).replace("/", "-")
    
    # Create (or reuse) the target folder named after the extracted date.
    target_folder: str = os.path.join(base_download_dir, file_date)
    os.makedirs(target_folder, exist_ok=True)
    
    # Build the target file name.
    new_file_name: str = f"{option.replace(' ', '_')}.xlsx"
    new_file_path: str = os.path.join(target_folder, new_file_name)
    
    # Check if the file already exists; if so, skip downloading.
    if os.path.exists(new_file_path):
        print(f"File {new_file_path} already exists. Skipping download for '{option}'.")
        return
    
    # Click the download button.
    download_button = WebDriverWait(driver, time_wait).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "btn-excel"))
    )
    download_button.click()
    
    # Wait until the file is downloaded in the base download directory.
    start_time: float = time.time()
    downloaded_file: Optional[str] = None
    while time.time() - start_time < time_wait:
        files = os.listdir(base_download_dir)
        for file in files:
            if file.endswith(".xlsx"):
                downloaded_file = os.path.join(base_download_dir, file)
                break
        if downloaded_file:
            break
        time.sleep(1)
    
    if not downloaded_file:
        raise Exception("Download did not complete within the timeout period.")
    
    # Move the downloaded file into the target folder.
    os.rename(downloaded_file, new_file_path)
    print(f"Downloaded and moved file to: {new_file_path}")

def main(headless: bool = True) -> None:
    """
    Sets up the download directory and browser options (including headless mode),
    and iterates over each option to download the file if it doesn't already exist.
    
    Args:
        headless (bool): If True, runs the browser in headless (background) mode.
                         Default is True.
    """
    # Expand and ensure the base download directory exists.
    base_download_dir: str = os.path.expanduser("~/Documents/siedco_files")
    os.makedirs(base_download_dir, exist_ok=True)
    
    time_wait: int = 60
    options_list: list[str] = [
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
    
    # Configure browser options.
    options = Options()
    # Set the browser to run in headless mode if specified (default is headless).
    # True means the browser will not be shown.
    if headless:
    	print("Headless mode ON")
    	options.add_argument("-headless")
    	
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", os.path.abspath(base_download_dir))
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/vnd.ms-excel")
    options.set_preference("browser.download.useDownloadDir", True)
    
    # Start a single browser session.
    driver: webdriver.Firefox = webdriver.Firefox(options=options)
    
    base_url: str = "https://portalsiedco.policia.gov.co:4443/extensions/PortalPublico/index.html#/home"
    
    for option in options_list:
        try:
            download_file_for_option(option, driver, base_url, base_download_dir, time_wait)
        except Exception as e:
            print(f"Error processing option '{option}': {e}")
    
    driver.quit()

if __name__ == "__main__":
    # By default, run in headless mode. Set headless=False to see the browser.
    main(headless=True)

