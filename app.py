def get_search_results(api_key, query, location=None, domain=None, gl=None, hl=None, device=None):
    base_url = "https://api.spaceserp.com/google/search"
    params = {
        "apiKey": api_key,
        "q": query,
        "location": location,
        "domain": domain,
        "gl": gl,
        "hl": hl,
        "device": device
    }
    response = requests.get(base_url, params=params)
    return response.json()

def parse_search_results(response):
    results = []
    for item in response.get("organic", []):
        result = {
            "title": item.get("title"),
            "link": item.get("url"),
            "snippet": item.get("snippet")
        }
        results.append(result)
    return results

def extract_html_content(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        return soup.prettify()
    except Exception as e:
        print(f"Error extracting HTML content: {e}")
        return None

def save_to_csv(results, file_name):
    with open(file_name, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["keyword", "title", "link", "snippet", "html_content"])
        for result in results:
            writer.writerow([
                result["keyword"],
                result["title"],
                result["link"],
                result["snippet"],
                result["html_content"]
            ])