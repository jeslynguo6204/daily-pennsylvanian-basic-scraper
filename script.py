"""
Scrapes the latest multimedia headline from The Daily Pennsylvanian website 
and saves it to a JSON file that tracks headlines over time.
"""

import os
import sys
import daily_event_monitor
import bs4
import requests
import loguru

def scrape_data_point():
    """
    Scrapes the latest multimedia headline from The Daily Pennsylvanian Multimedia page.
    """
    headers = {
        "User-Agent": "cis3500-scraper"
    }
    
    multimedia_url = "https://www.thedp.com/multimedia"
    req = requests.get(multimedia_url, headers=headers)
    loguru.logger.info(f"Request URL: {req.url}")
    loguru.logger.info(f"Request status code: {req.status_code}")

    if req.ok:
        soup = bs4.BeautifulSoup(req.text, "html.parser")
        
        # Extract the Multimedia section
        multimedia_section = soup.find("div", class_="featured-media")
        
        if multimedia_section:
            latest_story = multimedia_section.find("a", class_="medium-link")
            data_point = latest_story.get_text(strip=True) if latest_story else "No multimedia headline found"
        else:
            data_point = "No multimedia section found"

        loguru.logger.info(f"Extracted headline: {data_point}")
        return data_point

    loguru.logger.error("Failed to retrieve multimedia page")
    return ""



if __name__ == "__main__":

    # Setup logger to track runtime
    loguru.logger.add("scrape.log", rotation="1 day")

    # Create data dir if needed
    loguru.logger.info("Creating data directory if it does not exist")
    try:
        os.makedirs("data", exist_ok=True)
    except Exception as e:
        loguru.logger.error(f"Failed to create data directory: {e}")
        sys.exit(1)

    # Load daily event monitor
    loguru.logger.info("Loading daily event monitor")
    dem = daily_event_monitor.DailyEventMonitor(
        "data/daily_pennsylvanian_headlines.json"
    )

    # Run scrape
    loguru.logger.info("Starting scrape")
    try:
        data_point = scrape_data_point()
    except Exception as e:
        loguru.logger.error(f"Failed to scrape data point: {e}")
        data_point = None

    # Save data
    if data_point:
        dem.add_today(data_point)
        dem.save()
        loguru.logger.info("Saved daily event monitor")

    def print_tree(directory, ignore_dirs=[".git", "__pycache__"]):
        loguru.logger.info(f"Printing tree of files/dirs at {directory}")
        for root, dirs, files in os.walk(directory):
            dirs[:] = [d for d in dirs if d not in ignore_dirs]
            level = root.replace(directory, "").count(os.sep)
            indent = " " * 4 * (level)
            loguru.logger.info(f"{indent}+--{os.path.basename(root)}/")
            sub_indent = " " * 4 * (level + 1)
            for file in files:
                loguru.logger.info(f"{sub_indent}+--{file}")

    print_tree(os.getcwd())

    loguru.logger.info(f"Printing contents of data file {dem.file_path}")
    with open(dem.file_path, "r") as f:
        loguru.logger.info(f.read())

    # Finish
    loguru.logger.info("Scrape complete")
    loguru.logger.info("Exiting")
