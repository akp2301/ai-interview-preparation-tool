import requests
import os

def tavily_search(query):
    try:
        api_key = os.getenv("TAVILY_API_KEY", "")
        if not api_key:
            return "❌ Missing Tavily API Key. Add TAVILY_API_KEY to your .env."

        url = "https://api.tavily.com/search"
        payload = {
            "api_key": api_key,
            "query": query,
            "n_tokens": 2048
        }

        response = requests.post(url, json=payload)
        data = response.json()

        # If API returns {"error": "..."}
        if "error" in data:
            return f"Search Error: {data['error']}"

        results = data.get("results", [])
        if not results:
            return "No results found."

        output = ""
        for item in results:
            title = item.get("title", "Untitled")
            url = item.get("url", "No link available")
            snippet = item.get("snippet", "No summary available")  # SAFE

            output += f"### 🔗 {title}\n{snippet}\n👉 {url}\n\n"

        return output

    except Exception as e:
        return f"Search Error: {str(e)}"