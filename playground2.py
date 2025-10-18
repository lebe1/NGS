from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import json
import time

class ScheduleScraper:
    def __init__(self, headless=False):
        """Initialize the Selenium WebDriver"""
        options = webdriver.ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 10)
        
    def scrape_schedule(self, base_url, resource_id="16845"):
        """
        Scrape the schedule from the EDT system
        
        Args:
            base_url: The base URL (e.g., "https://edt.grenoble-inp.fr/2025-2026/exterieur")
            resource_id: The resource ID for the schedule
        """
        full_url = f"{base_url}?resources={resource_id}"
        
        print(f"Accessing: {full_url}")
        self.driver.get(full_url)
        
        # Wait for the page to load
        time.sleep(2)
        
        # Check if there's a form that needs to be submitted
        try:
            form = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "form")))
            print("Form detected, submitting...")
            form.submit()
            time.sleep(2)
        except TimeoutException:
            print("No form detected, page already loaded")
        
        # Now find and click on course elements to get detailed information
        # First, let's see what's on the page
        print("\nSearching for course/activity elements...")
        
        all_events = []
        
        # Try to find clickable elements (activities/courses)
        # These might be in various formats, so we'll try multiple approaches
        try:
            # Look for elements with onclick handlers or links
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Find all links with javascript:ev() pattern (event links)
            event_links = soup.find_all('a', href=lambda x: x and 'javascript:ev(' in x)
            
            if event_links:
                print(f"Found {len(event_links)} event links")
                
                # Extract event IDs from the javascript calls
                import re
                event_ids = set()
                for link in event_links:
                    match = re.search(r'ev\((\d+)\)', link.get('href', ''))
                    if match:
                        event_ids.add(match.group(1))
                
                print(f"Found {len(event_ids)} unique event IDs")
                
                # For each event ID, construct the eventInfo.jsp URL and fetch it
                for event_id in sorted(event_ids):
                    print(f"\nFetching event {event_id}...")
                    event_data = self.fetch_event_details(event_id)
                    if event_data:
                        all_events.extend(event_data)
                        
            else:
                # Alternative: look for table with schedule data
                print("Looking for schedule table...")
                tables = soup.find_all('table')
                for table in tables:
                    events = self.parse_schedule_table(table)
                    if events:
                        all_events.extend(events)
                        
        except Exception as e:
            print(f"Error during scraping: {e}")
            # Save page source for debugging
            with open("debug_page_source.html", "w", encoding="utf-8") as f:
                f.write(self.driver.page_source)
            print("Saved page source to debug_page_source.html")
        
        return all_events
    
    def fetch_event_details(self, event_id):
        """Fetch detailed information for a specific event"""
        # Construct the eventInfo.jsp URL
        current_url = self.driver.current_url
        base_url = current_url.rsplit('/', 1)[0]
        
        event_url = f"{base_url}/jsp/custom/modules/plannings/eventInfo.jsp"
        params = (
            f"?week=-1&day=-1&slot=0&eventId={event_id}"
            f"&activityId=-1&resourceId=-1&sessionId=-1"
            f"&repetition=-1&order=slot&availableZone=-1"
        )
        
        full_event_url = event_url + params
        
        try:
            self.driver.get(full_event_url)
            time.sleep(1)
            
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            
            # Parse the table with event details
            tables = soup.find_all('table')
            events = []
            
            for table in tables:
                parsed_events = self.parse_schedule_table(table)
                events.extend(parsed_events)
            
            return events
            
        except Exception as e:
            print(f"Error fetching event {event_id}: {e}")
            return []
    
    def parse_schedule_table(self, table):
        """Parse a schedule table and extract event information"""
        events = []
        
        try:
            rows = table.find_all('tr')
            
            # Find header row to identify column positions
            header_row = None
            for row in rows:
                if row.find('td', class_='subHeader1') or row.find('th'):
                    header_row = row
                    break
            
            if not header_row:
                return events
            
            # Get column headers
            headers = [th.get_text(strip=True) for th in header_row.find_all(['th', 'td'])]
            
            # Parse data rows
            for row in rows:
                cells = row.find_all('td')
                if not cells or len(cells) < 2:
                    continue
                
                # Skip header rows
                if cells[0].find('a') and 'eventInfo.jsp' in str(cells[0]):
                    continue
                
                # Extract cell data
                cell_data = []
                for cell in cells:
                    # Get text, handling links
                    link = cell.find('a')
                    if link and 'javascript:ev(' in str(link.get('href', '')):
                        cell_data.append(link.get_text(strip=True))
                    else:
                        cell_data.append(cell.get_text(strip=True))
                
                # Create event dictionary
                if len(cell_data) >= len(headers):
                    event = {}
                    for i, header in enumerate(headers):
                        if i < len(cell_data):
                            event[header] = cell_data[i]
                    
                    # Only add if it has meaningful data
                    if event.get('Date') or event.get('Name'):
                        events.append(event)
                        
        except Exception as e:
            print(f"Error parsing table: {e}")
        
        return events
    
    def save_results(self, events, output_format='all'):
        """Save the scraped events to files"""
        if not events:
            print("No events to save")
            return
        
        print(f"\nSaving {len(events)} events...")
        
        # Save as JSON
        if output_format in ['json', 'all']:
            with open('schedule_events.json', 'w', encoding='utf-8') as f:
                json.dump(events, f, indent=2, ensure_ascii=False)
            print("✓ Saved to schedule_events.json")
        
        # Save as CSV using pandas
        if output_format in ['csv', 'all']:
            df = pd.DataFrame(events)
            df.to_csv('schedule_events.csv', index=False, encoding='utf-8')
            print("✓ Saved to schedule_events.csv")
        
        # Save as readable text
        if output_format in ['txt', 'all']:
            with open('schedule_events.txt', 'w', encoding='utf-8') as f:
                for i, event in enumerate(events, 1):
                    f.write(f"{'='*60}\n")
                    f.write(f"Event {i}\n")
                    f.write(f"{'='*60}\n")
                    for key, value in event.items():
                        f.write(f"{key}: {value}\n")
                    f.write("\n")
            print("✓ Saved to schedule_events.txt")
        
        # Print summary
        print(f"\n{'='*60}")
        print("SUMMARY")
        print(f"{'='*60}")
        print(f"Total events extracted: {len(events)}")
        
        if events:
            print("\nSample event:")
            for key, value in list(events[0].items())[:5]:
                print(f"  {key}: {value}")
    
    def close(self):
        """Close the WebDriver"""
        self.driver.quit()


# Main execution
if __name__ == "__main__":
    # Configuration
    BASE_URL = "https://edt.grenoble-inp.fr/2025-2026/exterieur"
    RESOURCE_ID = "16845"
    
    # Initialize scraper
    scraper = ScheduleScraper(headless=False)  # Set to True to run without GUI
    
    try:
        # Scrape the schedule
        print("="*60)
        print("Starting schedule scraper...")
        print("="*60)
        
        events = scraper.scrape_schedule(BASE_URL, RESOURCE_ID)
        
        # Save results
        scraper.save_results(events, output_format='all')
        
        print("\n" + "="*60)
        print("Scraping completed successfully!")
        print("="*60)
        
    except Exception as e:
        print(f"\nError during execution: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Clean up
        scraper.close()