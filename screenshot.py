from flask import current_app
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from models import db, Screenshot, ScreenshotTask
import os
import glob


def screenshot_task(app, task_id, start_url, num_links):
    with app.app_context():
        # Configure Selenium WebDriver
        options = webdriver.ChromeOptions()
        options.headless = True
        # This is required when running as root (e.g., in a Docker container)
        options.add_argument("--no-sandbox")
        # Overcomes limited resource problems
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(
            ChromeDriverManager().install()), options=options)

        try:
            # Navigate to the start URL and take a screenshot
            driver.get(start_url)
            screenshot_path = f'screenshots/{task_id}_start.png'
            driver.save_screenshot(screenshot_path)
            save_screenshot_to_db(task_id, screenshot_path)

            # Find and follow the first N links
            links = driver.find_elements(By.TAG_NAME, 'a')[:num_links]
            for i, link in enumerate(links):
                href = link.get_attribute('href')
                if href and not href.startswith('javascript:') and not href.startswith('#'):
                    driver.get(href)
                    screenshot_path = f'./screenshots/{task_id}_link_{i}.png'
                    driver.save_screenshot(screenshot_path)
                    save_screenshot_to_db(task_id, screenshot_path)
        finally:
            driver.quit()


def save_screenshot_to_db(task_id, file_path):
    # Create a new Screenshot object and save it to the database
    screenshot = Screenshot(file_path=file_path, task_id=task_id)
    db.session.add(screenshot)
    db.session.commit()
