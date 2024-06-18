import requests
from bs4 import BeautifulSoup

# URLs for the product pages
amazon_url = 'https://www.amazon.com/Apple-iPhone-128GB-Blue-Titanium/dp/B0CMZ8ZBVN/ref=sr_1_3?crid=30DU06AL1W2AG&dib=eyJ2IjoiMSJ9.TKMfsDdzp2QNVDSdRILQcwqIhGGmVK6IahX81lYsFuysfLI8v49ktFezYSEx_i0ZT8wKXAmqmrsqDZdqPHfMKRFXFTVlv7KEr5gOOwtURkv_XzsBhfHS_3M27kHGtvSbxaBCB9lCbxwF2M5t2Mzz74llh1IberMqFDTJ-KcW8yRe4zdyHkpdnDbdukxjW3wG6ys1-kqaJdCIJ-G23SnsM90FrfqCKKSvFu2Ri-d_dg_IrRWDpVAhwEMbKz0rRjzMagIbHZzSGm8qe5BdAd2_v0ViV7ZSrjEP-PiScm1mLg4.ohjzWUmI5aRxum0YV3ArcmG_HmKpFtmtVIxzSAF_ifQ&dib_tag=se&keywords=iphone%2B15%2Bpro%2Bmax&qid=1718752411&refinements=p_n_feature_thirty-two_browse-bin%3A108501313011&rnid=25926948011&s=wireless&sprefix=iphone%2B15%2Bpro%2Bmax%2Caps%2C402&sr=1-3&th=1'
ebay_url = 'https://www.ebay.com/itm/285915570275?itmmeta=01J0PSZV81E2P1EN9PVXB7286Q&hash=item4291e56063:g:ixcAAOSwBAtma~xb&itmprp=enc%3AAQAJAAAA4A0b2kTeX54CaO9U9BHi5Z53TvT7SGCpkYbe7JtPWCbm2lMtt7fdyDHbHDZVgRujyVaCVq8l3nGzzMO94SSO1uxZIxlDYqbLvgqkxBSGwLOEGzkxAeqIo2y1T1A0%2BPNDcwQx9YO9zuviqYGS--f%2BR2QG%2FFwbO3a0BViQf15KefOnHfJMduQRoP%2FRNHG5U4J8bpEYGmdLfGqFBX5Cqg%2BcMePgKWxJ5vTn0%2Bf0G4grfqjJypOrcv3r9r15AOR8u3fa0gYLVXPFIItyLERcvx1wWdL%2BqRie5v2kg%2Bxypow4KJiK%7Ctkp%3ABk9SR460_9mFZA'
walmart_url = 'https://www.walmart.com/ip/Open-Box-Apple-iPhone-15-Pro-Max-A2849-512GB-White-Titanium-US-Model-Factory-Unlocked-Cell-Phone/5372212120?from=/search'

# Headers to mimic a browser visit
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_amazon_price(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        price = soup.find('span', {'id': 'priceblock_ourprice'}) or soup.find('span', {'id': 'priceblock_dealprice'})
        if price:
            return float(price.get_text().strip().replace('$', '').replace(',', ''))
    except Exception as e:
        print(f"Error getting price from Amazon: {e}")
    return None

def get_ebay_price(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        price = soup.find('span', {'id': 'prcIsum'}) or soup.find('span', {'id': 'prcIsum_bidPrice'})
        if price:
            return float(price.get_text().strip().replace('$', '').replace(',', ''))
    except Exception as e:
        print(f"Error getting price from eBay: {e}")
    return None

def get_walmart_price(url):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        price = soup.find('span', {'class': 'price-characteristic'})
        if price and price.has_attr('content'):
            return float(price['content'])
    except Exception as e:
        print(f"Error getting price from Walmart: {e}")
    return None

def compare_prices():
    amazon_price = get_amazon_price(amazon_url)
    ebay_price = get_ebay_price(ebay_url)
    walmart_price = get_walmart_price(walmart_url)

    prices = {
        'Amazon': amazon_price,
        'eBay': ebay_price,
        'Walmart': walmart_price
    }

    # Filter out None values
    valid_prices = {k: v for k, v in prices.items() if v is not None}

    if not valid_prices:
        print("No valid prices found.")
        return

    best_deal = min(valid_prices, key=valid_prices.get)
    print(f"Best deal is at {best_deal} with price ${valid_prices[best_deal]:.2f}")

compare_prices()
