# Image_Scraper

A Python web scraper that automatically downloads images from websites using Selenium and requests libraries.

## Features

- 🤖 Headless Chrome browsing for stealthy scraping
- 📸 Downloads images from dynamic web pages
- 🔄 Infinite scroll support to load more content
- 📊 Detailed download statistics
- 🎯 Avoids duplicate downloads
- 🕵️ Mimics human behavior with random delays

## Prerequisites

Before running the scraper, you need to install these dependencies:

```bash
pip install selenium requests
```

You also need to have Chrome browser installed on your system. The scraper uses ChromeDriver which is automatically managed by Selenium.

## Usage

### Basic Usage

1. **Configure the scraper**: Edit the `scraper_img.py` file to set your target website and output directory:

```python
# Configuration
WEBSITE_URL = "https://www.example.com/"
OUTPUT_DIR = r"D:\path\to\save\images"
```

2. **Run the scraper**:

```bash
python scraper_img.py
```

### Customization Options

You can customize these parameters in the script:

- `max_scrolls`: Maximum number of scroll attempts (default: 7)
- `scroll_delay`: Delay between scrolls (default: 3 seconds)
- `no_new_images_threshold`: Stop if no new images for this many consecutive scrolls (default: 3)
- `random delays`: Between 0.5-2 seconds between downloads to mimic human behavior

## How It Works

1. **Initialization**: Sets up headless Chrome browser with stealthy user agent
2. **Page Access**: Navigates to the target website
3. **Infinite Scroll**: Scrolls down to load more content
4. **Image Collection**: Extracts all unique image URLs
5. **Download**: Downloads images to the specified directory
6. **Cleanup**: Properly closes the browser

## Example Output

```
Accessing website: https://www.example.com/
Starting limited scroll for testing...
Maximum scroll attempts: 7
Stop if no new images for: 3 consecutive scrolls
Scroll 1: Found 25 new images (Total: 25)
Scroll 2: Found 18 new images (Total: 43)
Scroll 3: No new images (1/3 consecutive)
Scroll 4: No new images (2/3 consecutive)
Scroll 5: No new images (3/3 consecutive)

Stopping: No new images for 3 consecutive scrolls
Total unique images found: 43

Scrolling complete! Total unique images: 43
Starting to download 43 images...
Downloading: image1.jpg (1/43)
Successfully downloaded: image1.jpg (1/43)
Downloading: image2.jpg (2/43)
Successfully downloaded: image2.jpg (2/43)

==================================================
Download Summary:
Total images found: 43
Successfully downloaded: 41
Failed: 2
Skipped (existing): 0
==================================================
Browser closed.
```

## Notes

- Respect website's robots.txt file and terms of service
- Use appropriate delays to avoid overwhelming servers
- The scraper may not work on websites with strong anti-bot measures
- Always use this tool responsibly and ethically

## License

MIT License - feel free to use this tool for learning purposes.
