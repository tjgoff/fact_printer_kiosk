import requests

def fetch_quote():
    #get 50 quotes at a time, format them, and print them to the screen
    api_url = "https://zenquotes.io/api/quotes"
    response = requests.get(api_url)

    if response.status_code == 200:
        for quote in response.json():
            formattedQuote = "\"" + quote["q"] + "\" -" + quote["a"]
            print(formattedQuote)
    else:
        print(f"Failed to fetch quote. Status Code: {response.status_code}")

if __name__ == "__main__":
    fetch_quote()