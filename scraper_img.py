from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import os
import requests
import time
import random

# Configuration
WEBSITE_URL = "https://www.example.com/"
OUTPUT_DIR = r"D:\OneDrive\WebScraping\images_example"

# Create output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set up Chrome options for headless browsing
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

# Initialize webdriver (let Selenium manage to driver)
driver = webdriver.Chrome(options=chrome_options)

try:
    print(f"Accessing website: {WEBSITE_URL}")
    driver.get(WEBSITE_URL)
    
    # Wait for page to load
    time.sleep(random.uniform(3, 5))
    
    # Set to store all unique image URLs
    all_image_urls = set()
    
    # Scroll configuration
    max_scrolls = 7  # Maximum number of scroll attempts (for testing)
    scroll_delay = 3  # Delay between scrolls (seconds)
    no_new_images_threshold = 3  # Stop if no new images for this many consecutive scrolls
    
    consecutive_no_new_images = 0
    
    print("Starting limited scroll for testing...")
    print(f"Maximum scroll attempts: {max_scrolls}")
    print(f"Stop if no new images for: {no_new_images_threshold} consecutive scrolls")
    
    # Infinite scroll loop
    for scroll_num in range(1, max_scrolls + 1):
        # Get current images
        current_images = driver.find_elements(By.TAG_NAME, "img")
        
        # Extract URLs from current images
        current_urls = set()
        for img in current_images:
            img_url = img.get_attribute("src")
            if img_url:
                current_urls.add(img_url)
        
        # Check for new images
        new_images_count = len(current_urls - all_image_urls)
        
        if new_images_count > 0:
            print(f"Scroll {scroll_num}: Found {new_images_count} new images (Total: {len(current_urls)})")
            all_image_urls.update(current_urls)
            consecutive_no_new_images = 0  # Reset counter
        else:
            consecutive_no_new_images += 1
            print(f"Scroll {scroll_num}: No new images ({consecutive_no_new_images}/{no_new_images_threshold} consecutive)")
            
            # Stop if we've had too many scrolls without new images
            if consecutive_no_new_images >= no_new_images_threshold:
                print(f"\nStopping: No new images for {consecutive_no_new_images} consecutive scrolls")
                print(f"Total unique images found: {len(all_image_urls)}")
                break
        
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for content to load
        time.sleep(scroll_delay)
        
        # Random additional delay to mimic human behavior
        time.sleep(random.uniform(0.5, 1.5))
        
        # Check if we've reached to bottom
        scroll_height = driver.execute_script("return document.body.scrollHeight")
        current_position = driver.execute_script("return window.pageYOffset + window.innerHeight")
        
        if current_position >= scroll_height:
            print(f"\nReached to bottom of page (scroll {scroll_num})")
            print(f"Total unique images found: {len(all_image_urls)}")
            break
    
    print(f"\nScrolling complete! Total unique images: {len(all_image_urls)}")
    
    # Convert set to list for easier handling
    image_url_list = list(all_image_urls)
    print(f"Starting to download {len(image_url_list)} images...")
    
    # Download images
    downloaded_count = 0
    failed_count = 0
    skipped_count = 0
    
    for idx, img_url in enumerate(image_url_list, 1):
        try:
            # Check if image URL is valid
            if not img_url or not img_url.startswith(("http://", "https://")):
                print(f"Skipping invalid URL: {img_url}")
                skipped_count += 1
                continue
            
            # Extract filename from URL
            clean_url = img_url.split("?")[0]
            filename = os.path.basename(clean_url)
            
            # If no extension, add .jpg
            if not os.path.splitext(filename)[1]:
                filename += ".jpg"
            
            # Check if file already exists
            save_path = os.path.join(OUTPUT_DIR, filename)
            if os.path.exists(save_path):
                print(f"Skipping existing file: {filename} ({idx}/{len(image_url_list)})")
                skipped_count += 1
                continue
            
            print(f"Downloading: {filename} ({idx}/{len(image_url_list)})")
            
            # Download image using requests
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Referer": WEBSITE_URL
            }
            
            img_response = requests.get(img_url, headers=headers, timeout=15)
            img_response.raise_for_status()
            
            # Save image
            with open(save_path, "wb") as img_file:
                img_file.write(img_response.content)
            
            print(f"Successfully downloaded: {filename} ({idx}/{len(image_url_list)})")
            downloaded_count += 1
            
            # Add random delay between downloads
            time.sleep(random.uniform(0.5, 2))
        
        except Exception as e:
            print(f"Failed to download image {idx}: {e}")
            failed_count += 1
    
    print(f"\n" + "="*50)
    print(f"Download Summary:")
    print(f"Total images found: {len(image_url_list)}")
    print(f"Successfully downloaded: {downloaded_count}")
    print(f"Failed: {failed_count}")
    print(f"Skipped (existing): {skipped_count}")
    print(f"="*50)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    driver.quit()
    print("Browser closed.")