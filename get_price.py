import httpx
from lxml import html

HEADERS     = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0"}
PRICE_XPATH = "//*[@id='centerCol']//span[contains(@class, 'apex-pricetopay-value')]"

def get_price(url: httpx.URL) -> str:
    r = httpx.get(url, headers=HEADERS)
    tree = html.fromstring(r.text)
    results = tree.xpath(PRICE_XPATH)
    if results:
        result = results[0]
        return result.text_content().strip()
    else:
        return 'NotFound'

def main():
    url = httpx.URL('https://www.amazon.com/dp/B0FZRTD2Q9')

    try:
        result = get_price(url)
        print(result)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
