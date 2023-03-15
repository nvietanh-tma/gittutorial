import requests
from bs4 import BeautifulSoup


def extract_url(url):
    if url.find("amazon") != -1:
        index = url.find("/dp/")
        if index != -1:
            index2 = index + 14
            url = "https://www.amazon.in&quot" + url[index:index2]
        else:
            index = url.find("/gp/")
            if index != -1:
                index2 = index + 22
                url = "https://www.amazon.in&quot" + url[index:index2]
            else:
                url = None
    else:
        url = None
    return url


def get_converted_price(price):
    stripped_price = price.strip("₹ ,")
    replaced_price = stripped_price.replace(",", "")
    find_dot = replaced_price.find(".")
    to_convert_price = replaced_price[0:find_dot]
    converted_price = int(to_convert_price)

    return converted_price


def get_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36"
    }
    details = {"name": "", "price": 0, "deal": True, "url": ""}

    _url = extract_url(url)
    if _url == "":
        details = None
    else:
        page = requests.get(url, headers=headers, verify=False)
        soup = BeautifulSoup(page.content, "lxml")
        title = soup.find(id="productTitle")
        price = soup.find(id="priceblock_dealprice")
        if price is None:
            price = soup.find(id="priceblock_ourprice")
            details["deal"] = False
        if title is not None and price is not None:
            details["name"] = title.get_text().strip()
            details["price"] = get_converted_price(price.get_text())
            details["url"] = _url
        else:
            return None
    return details


print(get_product_details("https://www.amazon.in/dp/B01DZSEK68/ref=s9_acsd_al_bw_c2_x_2_i?pf_rd_m=A1K21FY43GMZF8&pf_rd_s=merchandised-search-5&pf_rd_r=85MRWVWB2ETWKPQKHE83&pf_rd_t=101&pf_rd_p=24f91fd1-b1f9-4c65-9f54-33ffaebeae65&pf_rd_i=1380374031"))
