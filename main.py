import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep

url = input("Enter Product URL : ")

TG_ID = 123
TG_TOKEN = "12345:abcde"

def get_product_details(url):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": "x-amz-captcha-1=1737472354344787; x-amz-captcha-2=igNGYsG2orL///WGz7QYnw==; session-id=146-2838555-9102714; session-id-time=2082787201l; i18n-prefs=USD; sp-cdn=\"L5Z9:IQ\"; ubid-main=134-3806987-6655000; skin=noskin; session-token=0ifB4POWDu/cNezf52n1HEq9vb8KKyECvDUnVrPi4tyx9jy5YaJDz4wQtqWnxH0Rmz4pGYIRsknvA7ztZZ3Y/qIIcQiuD2D3SDgbW5/+G9oZ8GZwshHal6iFo5xA2jM1stBfEPHazw66Pq8qWohqBlDtrELO0j0Uu9xNlq+fKJA3mO6ccc6bSv3eRDgebAT4eTWvC9eXRgliEvlHduo6qKW/Q7QO0N61g5CBWvGpkMLRni5SUvz4ILdvVl2uZY5h7zfbgJjjTzyRtAwQhTHWWqdLke/3DY7jjXllzZcMpg396W7zlJZvix5QndW2e9bgjcw9eIhBJTQJ/tyX6GCoef4Yamc/hMGb; csm-hit=tb:V6TE6NM3MN425EWVD2AT+s-V6TE6NM3MN425EWVD2AT|1741134106322&t:1741134106322&adb:adblk_no",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("span", {"id": "productTitle"}).text.strip()
    price = soup.find("span", {"class": "a-offscreen"}).text.strip()
    rating = soup.find("span", {"class": "a-size-base a-color-base"}).text.strip() + "/5.0 (" + soup.find("span", {"id": "acrCustomerReviewText"}).text.strip() + ")"

    return {
        "title": title, 
        "price": price, 
        "rating": rating
        }

details = get_product_details(url)

title, price, rating = details["title"], details["price"], details["rating"]

df = pd.DataFrame([[title, price, rating]], columns=["Title", "Price", "Rating"])
df.to_csv("amazon_prices.csv", index=False)

print(f"Item Title : {title}\n\nPrice : {price}\n\nSeller Rating : {rating}\n\nThis Script Will Keep Running To Track The Price , If The Current Price Drop You Will Recieve A Notification And The Script Will Automatically Stop.\n")

while True:

    target_price = price.replace("$", "").replace(",", "")
    target_price = float(target_price)

    cprice = get_product_details(url)["price"].replace("$", "").replace(",", "")
    cprice = float(cprice)

    if cprice < target_price:

        msg = f"The Item Price Is Down!\n\nOriginal Price : {target_price}\nCurrent Price {cprice}\n\nItem URL : {url}"
        link = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id={TG_ID}&text={msg}"

        requests.get(link)

        print("The Price has been drop!")
        break
    
    sleep(300)
