import requests
import csv
import time
import urllib.parse

appid = "48190"  

url = f"https://store.steampowered.com/appreviews/{appid}"
csv_filename = f"steam_reviews_{appid}.csv"

num_reviews_to_fetch = 5000  # Target number of reviews
reviews_fetched = 0
cursor = "*"
params = {
    "json": 1,
    "num_per_page": 100,
    "language": "english",
    "cursor": cursor,
}

try:
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        writer.writerow(["Username (SteamID)", "Review"])
        
        while reviews_fetched < num_reviews_to_fetch:
            
            # Ensure the cursor is URL-encoded
            params["cursor"] = urllib.parse.quote(cursor)
            response = requests.get(url, params=params)

            if response.status_code == 200:
                reviews_data = response.json()

                if "reviews" in reviews_data and len(reviews_data["reviews"]) > 0:
                    for review in reviews_data["reviews"]:
                        username = str(review["author"]["steamid"])
                        review_text = review["review"]
                        if "---{" in review_text or "}---" in review_text:
                            continue

                        writer.writerow([f"user_{username}", review_text])
                        reviews_fetched += 1

                        if reviews_fetched >= num_reviews_to_fetch:
                            break
                    
                    # Update the cursor for the next page
                    cursor = reviews_data["cursor"]
                    
                    # Sleep to avoid overwhelming the API
                    time.sleep(1)  
                else:
                    print("No more reviews available or unexpected data format.")
                    break
            else:
                print(f"Failed to fetch reviews. HTTP Status Code: {response.status_code}")
                break

    print(f"Successfully fetched {reviews_fetched} reviews and saved to {csv_filename}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
