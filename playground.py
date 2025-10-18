import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, parse_qs, urlparse
import re
import json

session = requests.Session()
session.headers.update({"User-Agent": "Mozilla/5.0"})

BASE_URL = "https://edt.grenoble-inp.fr/2025-2026/exterieur?resources=16845"
RESOURCE_ID = "16845"

# Step 1: Get the redirect page
print("Step 1: Accessing base URL...")
r = session.get(BASE_URL)
soup = BeautifulSoup(r.text, "html.parser")

# Step 2: Extract form action and hidden inputs
form = soup.find("form")
if form:
    action = form["action"]
    inputs = {inp["name"]: inp["value"] for inp in form.find_all("input") if inp.get("name")}
    final_url = urljoin(r.url, action)
    print(f"Redirecting to: {final_url}")
    
    # Step 3: Simulate the JavaScript form submission
    r2 = session.post(final_url, params={"resources": RESOURCE_ID}, data=inputs)
else:
    r2 = r

print(f"Status: {r2.status_code}")

# Step 4: Access imagemap.jsp with reasonable dimensions
print("\n" + "="*60)
print("Step 2: Accessing imagemap.jsp...")
print("="*60)

# Use typical screen dimensions
width = 1200
height = 800

imagemap_url = urljoin(r2.url, "imagemap.jsp")
params = {
    "projectId": "14",
    "clearTree": "false",
    "width": width,
    "height": height
}

r_imagemap = session.get(imagemap_url, params=params)
print(f"Imagemap status: {r_imagemap.status_code}")

# Save for inspection
with open("imagemap_output.html", "w", encoding="utf-8") as f:
    f.write(r_imagemap.text)
print("Saved imagemap to imagemap_output.html")

# Step 5: Parse the imagemap to extract event IDs
soup_map = BeautifulSoup(r_imagemap.text, "html.parser")

# Look for area tags in the image map
event_ids = set()
area_tags = soup_map.find_all("area")

print(f"\nFound {len(area_tags)} area tags")

for area in area_tags:
    href = area.get("href", "")
    onclick = area.get("onclick", "")
    
    # Extract eventId from href or onclick
    # Pattern: eventInfo.jsp?...eventId=12345...
    match = re.search(r'eventId=(\d+)', href + onclick)
    if match:
        event_ids.add(match.group(1))

print(f"Found {len(event_ids)} unique events")

# Step 6: Fetch detailed information for each event
print("\n" + "="*60)
print("Step 3: Fetching event details...")
print("="*60)

events_data = []

for event_id in sorted(event_ids):
    print(f"\nFetching event {event_id}...")
    
    eventinfo_url = urljoin(r2.url, "eventInfo.jsp")
    event_params = {
        "week": "-1",
        "day": "-1",
        "slot": "0",
        "eventId": event_id,
        "activityId": "-1",
        "resourceId": "-1",
        "sessionId": "-1",
        "repetition": "-1",
        "order": "slot",
        "availableZone": "-1"
    }
    
    try:
        r_event = session.get(eventinfo_url, params=event_params)
        
        if r_event.status_code == 200:
            soup_event = BeautifulSoup(r_event.text, "html.parser")
            
            # Parse the event information
            event_info = {
                "event_id": event_id,
                "raw_html": r_event.text
            }
            
            # Extract text content
            text_content = soup_event.get_text(separator="\n", strip=True)
            event_info["text"] = text_content
            
            # Try to extract structured data from tables or divs
            tables = soup_event.find_all("table")
            if tables:
                # Parse table data
                for table in tables:
                    rows = table.find_all("tr")
                    for row in rows:
                        cells = row.find_all(["td", "th"])
                        if len(cells) >= 2:
                            key = cells[0].get_text(strip=True)
                            value = cells[1].get_text(strip=True)
                            if key:
                                event_info[key] = value
            
            events_data.append(event_info)
            
            # Print preview
            print(f"  Preview: {text_content[:200]}")
            
    except Exception as e:
        print(f"  Error fetching event {event_id}: {e}")

# Step 7: Save all events data
print("\n" + "="*60)
print("Step 4: Saving results...")
print("="*60)

# Save as JSON
with open("events_data.json", "w", encoding="utf-8") as f:
    json.dump(events_data, f, indent=2, ensure_ascii=False)
print(f"Saved {len(events_data)} events to events_data.json")

# Save as readable text file
with open("events_summary.txt", "w", encoding="utf-8") as f:
    for event in events_data:
        f.write("="*60 + "\n")
        f.write(f"Event ID: {event['event_id']}\n")
        f.write("="*60 + "\n")
        f.write(event.get("text", "No text content") + "\n\n")

print(f"Saved summary to events_summary.txt")

# Print summary
print("\n" + "="*60)
print("SUMMARY")
print("="*60)
print(f"Total events found: {len(events_data)}")
print("\nFirst event details:")
if events_data:
    print(json.dumps(events_data[0], indent=2, ensure_ascii=False)[:500])

print("\n" + "="*60)
print("Scraping complete!")
print("="*60)
print("Output files:")
print("  - imagemap_output.html (raw imagemap)")
print("  - events_data.json (structured data)")
print("  - events_summary.txt (readable summary)")
print("="*60)