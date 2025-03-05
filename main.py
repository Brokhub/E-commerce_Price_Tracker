import requests
from bs4 import BeautifulSoup
import sqlite3
import sys

con = sqlite3.connect("products.db")

cur = con.cursor()

try: cur.execute("CREATE TABLE items(title, price, rating, source)")
except: ""

def amazon_product_details(url):

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

    try: title = soup.find("span", {"id": "productTitle"}).text.strip()
    except: title = "Unknown"
    try: price = soup.find("span", {"class": "a-offscreen"}).text.strip()
    except: price = "Unknown"
    try: rating = soup.find_all("span", {"class": "a-size-base a-color-base"})[1].text.strip() + "/5.0 (" + soup.find("span", {"id": "acrCustomerReviewText"}).text.strip() + ")"
    except: rating = "Unknown"

    return {
        "title": title, 
        "price": price, 
        "rating": rating,
        "source": "Amazon"
        }

def ebay_product_details(url):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": "ak_bmsc=02F17572B3D3CC4151841CA56813D957~000000000000000000000000000000~YAAQDCjdF+HIpkGVAQAAbyNrZxuUpm35F3t9JbwrwapTeZjBLOG0EyKR6SawEbhFKZJouN1PtWIbgzcWiATnNsrX/T4MpwT9fTeesQWlUnxQIl0ZC6h5+Js+qK1Qooxaptcn+m2DIzEUje+MkWblWtE4bwpUi+kZtsy4sYK1dacuA3sv3T/kJuhSZ17YxdJ7DhkwEEsNXddRoyZ1OITLYl+TtVCR9WILIxcKv/Iqepx+8vkdQn2wemFPjgjzkKfCwJwtiLRJBotIFsQVI0NVZ0+bV6QuT/zfqLmbSZJ0F61oX4T2UA61YrvyVUfzoXK/ZVkb6TpwXrUdABKHBiKd2tZuq1riCDoHxUdiiY8dkoC8xf39PPFUZgHmkHO0/fqVwgt4Bbj8iw==; __uzma=d7aa39b7-56bb-4466-b719-52c9d2f27867; __uzmb=1741196833; __uzme=5649; s=CgADuAF9nyd+tMwZodHRwczovL3d3dy5lYmF5LmNvbS9zY2gvaS5odG1sP19ua3c9cnR4KzQwNjAmX3NhY2F0PTAmX2Zyb209UjQwJl90cmtzaWQ9cDQ0MzIwMjMubTU3MC5sMTMxMwcA+AAgZ8nfnTY3NmIyMmI2MTk1MGE1NjlhNDA1ZjUyOGZmZmZlOGQ0CCcTKA**; __ssds=2; __ssuzjsr2=a9be0cd8e; __uzmaj2=e84a2342-5626-4071-b4b3-c7502784abd4; __uzmbj2=1741196871; __uzmcj2=947011058320; __uzmdj2=1741196871; __uzmlj2=lq0GBdMn755LY3HyG/TqwuRKp7gvG7hs3B6bYzGwRpc=; __uzmfj2=7f6000239393a8-ce2a-4ecd-ab5f-79e3f9dcad9517411968711540-82dd6b6c1baab05810; ebay=%5Ejs%3D1%5Esbf%3D%23000000%5E; __deba=uzfP-Ry8is4H3AwMLbOtrbixTPHSUdfgUUSgXWp3kfKTZhKqQ_vKWIL6gpAwwEAmXR8UW1J2_XMwSXzXGqPFGNy5eao-yngO4yNbDN9gbwEKsjKMJbIG-D4CAhxdZHM-clw1_qrC-9CaU1wM9V-QyQ==; __uzmc=608202276846; __uzmd=1741196892; __uzmf=7f6000239393a8-ce2a-4ecd-ab5f-79e3f9dcad95174119683392858288-652942c2d390f5b622; __gads=ID=d02413d1a2ea6a08:T=1741196893:RT=1741196893:S=ALNI_MZRiDUMrt4R1WzSrqkBgBR1lD8GbA; __gpi=UID=0000105200cfb5b3:T=1741196893:RT=1741196893:S=ALNI_MZfqVBWKKHrLnCEBGWlgoyJK-M6sA; __eoi=ID=14b217ac413afeaf:T=1741196893:RT=1741196893:S=AA-AfjaYKJiyTZ2eLfnnvirMJcBR; AMP_f93443b04c=JTdCJTIyZGV2aWNlSWQlMjIlM0ElMjIzZTQxZDQ5YS04ZDQ1LTQwMWEtYjY5Mi04N2NhNDUwODk4NzUlMjIlMkMlMjJzZXNzaW9uSWQlMjIlM0ExNzQxMTk2ODk5Njg2JTJDJTIyb3B0T3V0JTIyJTNBZmFsc2UlMkMlMjJsYXN0RXZlbnRUaW1lJTIyJTNBMTc0MTE5NzE2OTA1MiUyQyUyMmxhc3RFdmVudElkJTIyJTNBOCUyQyUyMnBhZ2VDb3VudGVyJTIyJTNBOCU3RA==; ns1=BAQAAAZRXz2gmAAaAANgAU2mpwvVjNjl8NjAxXjE3NDExOTY4Mzc5MjJeXjFeM3wyfDV8NHw3fDEwfDQyfDQzfDExXl5eNF4zXjEyXjEyXjJeMV4xXjBeMV4wXjFeNjQ0MjQ1OTA3NT1ku/q3NEt8orHmfcA7dRdwAvIU; nonsession=BAQAAAZRXz2gmAAaAADMAAWmpwvU/AMoAIGuK9nU2NzZiMjJiNjE5NTBhNTY5YTQwNWY1MjhmZmZmZThkNADLAAJnyJZ9MTEyOnLjtuUkmndNQoEPeSXWd7Hg7Q**; dp1=bpbf/%2320000000000000000069a9c2f5^bl/IQ6b8af675^; bm_sv=09F920E1A7AD5B1B6D6EB7C976D718FD~YAAQzRXfrR5Qv1yVAQAAiGJwZxuy5zDF5t6MlBICGzDKcVszNAN2CAHnbYJ2UH48spu5Ea4MtjpEFJPTGcEeujo6UuBHUB4X3jPKhbG2Z7jooZnOIdnLCZyvi0nqEtfFtjk+O9CjXmFetEOLid5JBcSdgjPHXdhKRjabb1YDeGoEvySzHlzJ6/3n9P2UOYXB54UmDdHCKgDSLmAH1T7Wn+flIZ/XebxMZdYAZzskabjea5DcG/9IrOHBWYFoS28=~1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try: title = soup.find("h1", {"class": "x-item-title__mainTitle"}).text.strip()
    except: title = "Unknown"
    try: price = soup.find("div", {"class": "x-price-primary"}).text.strip()
    except: price = "Unknown"
    try: rating = soup.find_all("button", {"class": "ux-action fake-link fake-link--action"})[1].text.strip()
    except: rating = "Unknown"

    return {
        "title": title, 
        "price": price, 
        "rating": rating,
        "source": "eBay"
        }

def walmart_product_details(url):

    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Cookie": 'ak_bmsc=7E7167434C64F68387F91C49D0B39524~000000000000000000000000000000~YAAQWQcQAr+MBlaVAQAAo9d3ZxtL7+8CAosgMNz2lPdRG1dCq5659Nz8s+Bgdum6DDuA0qeYdFsPS7DWNn2GmlhRplqrH6X6Vo6jCJtRH4HDbWbJQqsboO3RX1CuyeeyFdUtRtG2FS+hSFtPSfZVKPxNN7HSYCQ+kI25lwGeBdAcyrmEBrCZJWF8c9UH+MJ6lrwB2wyJeFtznigAIZX4kxwLXIcsIMZUnZEE1TxO3W1+5w4x4DPTTRaD51HCLGgYo61FJ08LkMLib18UtfpW+KnlN5WEk8UiG3S9BmVs6elfMJ7DQysAgNrkVcNxJd5DDRVX9OQjAoUAg5J2p2W6ZFBwFQnyWviXZjU2acBvuPFhcOQfpbrwoUWFnVqCPbBRKcGdHaYjPESq3w==; vtc=Z3bwl5yRGSoU2w68OEYjZM; bstc=Z3bwl5yRGSoU2w68OEYjZM; pxcts=ce491d26-f9eb-11ef-8d8b-29134c85a66c; _pxvid=ce4909f4-f9eb-11ef-8d8b-2af560ad69ba; ACID=82323243-736a-4917-bbef-998445b7173a; _m=9; auth=MTAyOTYyMDE4rBhyGY4IIqxuPWl09S2YFsja4TaOWHPvw%2BCiU%2FZc%2BzbXZUnNKPL9BfVOLRy5eaClw9LSfDio%2FqKIRJWTo7NdxCpYN0JRZtTizhJ9BRPGsU3mOHEkh8%2Bhxb%2Bd8LI7bk6U767wuZloTfhm7Wk2KcjygsAEeU%2BeKCMhfP9XV060SY%2B4dqEcKmy8jIoDwTbzjP4wboM5G2XZbnRw4fkaSurwbQR1aNywrtI1d4pSTtryRzoUMk70P8glgOEpLOprhDfMWpzMbgzyqWg6MoSOREDGWkfIbbyU8RtJpA6t80WdVyYAMHU7h0g4KkYacjcHZ7uA9yNbQuhlpALb0mp6%2BfeGoYVqYeWW%2FEwOdBkkD1WmyjO5lIKvooc1kKl%2B4SYkiY5O29YHXDDXqFqMarTzZXkX1RAbajmc3a6HQbHZlS9HWyI%3D; hasACID=true; userAppVersion=us-web-1.185.0-7133cb55595c366852e1cfb6582f8a439b88b667-030410; abqme=true; mobileweb=0; xpth=x-o-mart%2BB2C~x-o-mverified%2Bfalse; xpa=0vWkn|7xMaT|8TFb0|9wpmY|EwUen|IpnX6|LINWl|Mf3gz|NC__g|OQe8n|PzMdd|QphTZ|RUIbZ|fdm-7|gZWrW|j2xiy|jM1ax|jQ0HQ|kGLhR|ktZl1|ouDo3|q92Hs|u4KO1|uYSVU|w6NXd|xf36q|yAoIi; exp-ck=9wpmY1EwUen3NC__g1OQe8n2PzMdd2QphTZ1RUIbZ1fdm-71gZWrW1jQ0HQ1kGLhR3u4KO11uYSVU1w6NXd3xf36q2yAoIi3; _pxhd=7edb872206678c9f98a12bb711740c6d0bf5189dcb24a19e26ccf1364719c3af:ce4909f4-f9eb-11ef-8d8b-2af560ad69ba; bm_mi=71DD3957B1C97DD3DE2713CEF8E5EEA4~YAAQhz4WAuoAoUqVAQAAav93Zxvt24wO8CIO7/P7xrkIpYCLMOYlRMGqHkWhewzYtTAn8AOOEU+rkz9gRRf6bFk/iIxsFx/F0C7AUNIKaG1+F+I3WuRw5WEJT+6OqRO5JP6kQPdl3Sr7YqzJOCnKBBYqefnpj82ywf0pIQUaATbEKX2FbW6OGPLoOCbORDRHCl+/ZT5QOfv6cO3QqfuKXBsx5kXCMP6BnGMNJ6X6cb7wY8VWFzUZiKn+cRfG7JmhaNMz91yhCLmGTK9uLs7Iu45quz7e6YOAQY4ucqBoKNc52gJX5NYuvUBRO8UZsYH7sO9IeZQ=~1; AID=wmlspartner=0:reflectorid=0000000000000000000000:lastupd=1741197679923; _intlbu=false; _shcc=US; assortmentStoreId=3081; hasLocData=1; xptwj=uz:139bb8a464fe64cd855a:hVLLeCBNH/vozWY+6Culb1QtuXm8qxDAhAd0OaJSCQXcuIn2UAQVY4KtlWI92rx5ytk5WS9MyWx8VI2B5vWgS1q6htUB30yhE1yjoARj//TOohSKR2C1bGeFtqVMh3XPdNbW96xYT3OQvdsb762nguhu1/xl/lV/r6byH/JMoZE=; ipSessionTrafficType=Internal; _astc=9143768bda742ae6fc141678db91506d; locDataV3=eyJpc0RlZmF1bHRlZCI6dHJ1ZSwiaXNFeHBsaWNpdCI6ZmFsc2UsImludGVudCI6IlNISVBQSU5HIiwicGlja3VwIjpbeyJub2RlSWQiOiIzMDgxIiwiZGlzcGxheU5hbWUiOiJTYWNyYW1lbnRvIFN1cGVyY2VudGVyIiwiYWRkcmVzcyI6eyJwb3N0YWxDb2RlIjoiOTU4MjkiLCJhZGRyZXNzTGluZTEiOiI4OTE1IEdFUkJFUiBST0FEIiwiY2l0eSI6IlNhY3JhbWVudG8iLCJzdGF0ZSI6IkNBIiwiY291bnRyeSI6IlVTIn0sImdlb1BvaW50Ijp7ImxhdGl0dWRlIjozOC40ODI2NzcsImxvbmdpdHVkZSI6LTEyMS4zNjkwMjZ9LCJzY2hlZHVsZWRFbmFibGVkIjp0cnVlLCJ1blNjaGVkdWxlZEVuYWJsZWQiOnRydWUsInN0b3JlSHJzIjoiMDY6MDAtMjM6MDAiLCJhbGxvd2VkV0lDQWdlbmNpZXMiOlsiQ0EiXSwic3VwcG9ydGVkQWNjZXNzVHlwZXMiOlsiUElDS1VQX1NQRUNJQUxfRVZFTlQiLCJQSUNLVVBfSU5TVE9SRSIsIlBJQ0tVUF9DVVJCU0lERSJdLCJ0aW1lWm9uZSI6IkFtZXJpY2EvTG9zX0FuZ2VsZXMiLCJzdG9yZUJyYW5kRm9ybWF0IjoiV2FsbWFydCBTdXBlcmNlbnRlciIsInNlbGVjdGlvblR5cGUiOiJERUZBVUxURUQifV0sInNoaXBwaW5nQWRkcmVzcyI6eyJsYXRpdHVkZSI6MzguNDgyNjc3LCJsb25naXR1ZGUiOi0xMjEuMzY5MDI2LCJwb3N0YWxDb2RlIjoiOTU4MjkiLCJjaXR5IjoiU2FjcmFtZW50byIsInN0YXRlIjoiQ0EiLCJjb3VudHJ5Q29kZSI6IlVTIiwibG9jYXRpb25BY2N1cmFjeSI6ImxvdyIsImdpZnRBZGRyZXNzIjpmYWxzZSwiYWxsb3dlZFdJQ0FnZW5jaWVzIjpbIkNBIl19LCJhc3NvcnRtZW50Ijp7Im5vZGVJZCI6IjMwODEiLCJkaXNwbGF5TmFtZSI6IlNhY3JhbWVudG8gU3VwZXJjZW50ZXIiLCJpbnRlbnQiOiJQSUNLVVAifSwiaW5zdG9yZSI6ZmFsc2UsImRlbGl2ZXJ5Ijp7Im5vZGVJZCI6IjMwODEiLCJkaXNwbGF5TmFtZSI6IlNhY3JhbWVudG8gU3VwZXJjZW50ZXIiLCJhZGRyZXNzIjp7InBvc3RhbENvZGUiOiI5NTgyOSIsImFkZHJlc3NMaW5lMSI6Ijg5MTUgR0VSQkVSIFJPQUQiLCJjaXR5IjoiU2FjcmFtZW50byIsInN0YXRlIjoiQ0EiLCJjb3VudHJ5IjoiVVMifSwiZ2VvUG9pbnQiOnsibGF0aXR1ZGUiOjM4LjQ4MjY3NywibG9uZ2l0dWRlIjotMTIxLjM2OTAyNn0sInNjaGVkdWxlZEVuYWJsZWQiOmZhbHNlLCJ1blNjaGVkdWxlZEVuYWJsZWQiOmZhbHNlLCJhY2Nlc3NQb2ludHMiOlt7ImFjY2Vzc1R5cGUiOiJERUxJVkVSWV9BRERSRVNTIn1dLCJpc0V4cHJlc3NEZWxpdmVyeU9ubHkiOmZhbHNlLCJhbGxvd2VkV0lDQWdlbmNpZXMiOlsiQ0EiXSwic3VwcG9ydGVkQWNjZXNzVHlwZXMiOlsiREVMSVZFUllfQUREUkVTUyJdLCJ0aW1lWm9uZSI6IkFtZXJpY2EvTG9zX0FuZ2VsZXMiLCJzdG9yZUJyYW5kRm9ybWF0IjoiV2FsbWFydCBTdXBlcmNlbnRlciIsInNlbGVjdGlvblR5cGUiOiJERUZBVUxURUQifSwiaXNnZW9JbnRsVXNlciI6ZmFsc2UsIm1wRGVsU3RvcmVDb3VudCI6MCwicmVmcmVzaEF0IjoxNzQxMjE5Mjc5OTg2LCJ2YWxpZGF0ZUtleSI6InByb2Q6djI6ODIzMjMyNDMtNzM2YS00OTE3LWJiZWYtOTk4NDQ1YjcxNzNhIn0%3D; locGuestData=eyJpbnRlbnQiOiJTSElQUElORyIsImlzRXhwbGljaXQiOmZhbHNlLCJzdG9yZUludGVudCI6IlBJQ0tVUCIsIm1lcmdlRmxhZyI6ZmFsc2UsImlzRGVmYXVsdGVkIjp0cnVlLCJwaWNrdXAiOnsibm9kZUlkIjoiMzA4MSIsInRpbWVzdGFtcCI6MTc0MTE5NzY3OTk4Miwic2VsZWN0aW9uVHlwZSI6IkRFRkFVTFRFRCJ9LCJzaGlwcGluZ0FkZHJlc3MiOnsidGltZXN0YW1wIjoxNzQxMTk3Njc5OTgyLCJ0eXBlIjoicGFydGlhbC1sb2NhdGlvbiIsImdpZnRBZGRyZXNzIjpmYWxzZSwicG9zdGFsQ29kZSI6Ijk1ODI5IiwiZGVsaXZlcnlTdG9yZUxpc3QiOlt7Im5vZGVJZCI6IjMwODEiLCJ0eXBlIjoiREVMSVZFUlkiLCJ0aW1lc3RhbXAiOjE3NDExOTc2Nzk5NzYsImRlbGl2ZXJ5VGllciI6bnVsbCwic2VsZWN0aW9uVHlwZSI6IkRFRkFVTFRFRCIsInNlbGVjdGlvblNvdXJjZSI6bnVsbH1dLCJjaXR5IjoiU2FjcmFtZW50byIsInN0YXRlIjoiQ0EifSwicG9zdGFsQ29kZSI6eyJ0aW1lc3RhbXAiOjE3NDExOTc2Nzk5ODIsImJhc2UiOiI5NTgyOSJ9LCJtcCI6W10sIm1zcCI6eyJub2RlSWRzIjpbXSwidGltZXN0YW1wIjpudWxsfSwibXBEZWxTdG9yZUNvdW50IjowLCJ2YWxpZGF0ZUtleSI6InByb2Q6djI6ODIzMjMyNDMtNzM2YS00OTE3LWJiZWYtOTk4NDQ1YjcxNzNhIn0%3D; xpm=1%2B1741197726%2BZ3bwl5yRGSoU2w68OEYjZM~%2B0; akavpau_p2=1741198347~id=26def54ec8095e6d3b8c43d3f16aa49d; adblocked=false; io_id=bc8a8ebe-41ea-4591-bb87-630450f5dcb5; xptwg=2382940675:1968FDA77B1F480:3EADB11:5FA158B6:4692D4AE:B61B191B:; TS012768cf=01203d59cb9d06a9f7d4def32c64d62f20e66419ba4647b65f429026352d1f6f40bcf8de092941b7a05f9282839b4a82914c958b0d; TS01a90220=01203d59cb9d06a9f7d4def32c64d62f20e66419ba4647b65f429026352d1f6f40bcf8de092941b7a05f9282839b4a82914c958b0d; if_id=FMEZARSFyuolrJFKLRCnLz9Gz9D+kWRaV/n2KiLZ9uLeqBmLPAdy3xZAOGtj5k5oqDnC0S+7RRVN0Nv/PLE7uygeVndltAE10W1rkWMy5qlUfelKaXzLeGNdiYNzwUTnVaKqb+1M6+mECdaOwMHdXbLe99I+RKMoPEseazJ5M8uzB11pyQl1CK/haCTQEF7fneJI/GuqVPiXAWkKK3dTWx7XscJ8j6z1WWp6wvHEP9PT8zOyR65BWVlTOj5MEKGOfkWqslnWBP/qZx45tEWP7BPBM3KUFfwG26pR+UOn6ClVVtOow2eK7hr6ffblXawZ23k1hDa9Lp8yDpLyN/AQww==; TS016ef4c8=01bd9bc72210fbc2ac320f7f3ea3393b35d757cce900828ee631d634da41698e19a2b0d3a94698379fd8bdd1e238f1812391cdbd34; TS01f89308=01bd9bc72210fbc2ac320f7f3ea3393b35d757cce900828ee631d634da41698e19a2b0d3a94698379fd8bdd1e238f1812391cdbd34; TS8cb5a80e027=08f6425442ab20008d71b1d0126eadd6231996c1b338532bb51de12859756ab4e752def3e40dc40608fc996732113000880d559d8c683680b74065e2d8c4ebf319dadb0950e09fc086de97b081d2ee959d62e16392e1599c09dc0b0ee3ce8328; com.wm.reflector="reflectorid:0000000000000000000000@lastupd:1741198026000@firstcreate:1741197671006"; xptc=_m%2B9~assortmentStoreId%2B3081; TS2a5e0c5c027=08bff2591fab2000d8de6359cd66f7842fcba7ddb1a18d9a4c21446ba9404bb07ed28f9af114bafd087546591d113000f9e42a24c821c59ee9cc4402a1a7a85c3b52736c7ec86cfe4d2037d1f1499774d3afb828d79af57691340c27149e7866; bm_sv=CFB12147C33FD1015AC22C643B88D7A2~YAAQhz4WAjFFoUqVAQAAT2h9Zxt36p5ZQbShnIwrANKPC0ZeQ2RXP99ZXJntZicUTokgcL07enEStAVC/k7DgX1uwAAaTRMl8U/mnNayFb6+YB2tLXXZBtDf9kA5VR7X5QAshlpb7zSgNcNeCmgFskwyiyKnXPmyC+/M+L5AC7YXjHy97BwyJ+0R3iTTvh3gwIqtOTkSE2832QEFbGCPK991iCqUKzENFdAhqcCaw+RRaQxqfq9QoOBoFSia+yhQ/Tw=~1',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    try: title = soup.find("h1", {"id": "main-title"}).text.strip()
    except: title = "Unknown"
    try: price = soup.find("span", {"itemprop": "price"}).text.strip()
    except: price = "Unknown"
    try: rating = soup.find("span", {"class": "f7 ph1"}).text.strip().replace("(", "").replace(")", "") + "/5.0 (" + soup.find("a", {"class": "pl1 bg-transparent bn lh-solid pa0 sans-serif tc underline inline-button dark-gray pointer f7"}).text.strip() + ")"
    except: rating = "Unknown"

    return {
        "title": title, 
        "price": price, 
        "rating": rating,
        "source": "Walmart"
        }

command = int(input("\n\nChoose What Do You Want To Do :\n\n[1] => Track Itme Price.\n[2] => Check Items Database.\n[3] => Exit.\n\nEnter The Command Number : "))

if command == 1:

    url = input("Enter Item URL [Amazon, eBay, Walmart] : ")

    if "amazon.com" in url:

        details = amazon_product_details(url)
    elif "ebay.com" in url:

        details = ebay_product_details(url)
    elif "walmart.com" in url:

        details = walmart_product_details(url)
    else:

        details = "none"

    if details != "none":

        title = details["title"]
        price = details["price"]
        rating = details["rating"]
        source = details["source"]

        print(f"Title : {title}\n\nPrice : {price}\n\nRating : {rating}")

        cur.execute(f"""
        INSERT INTO items VALUES
            ('{title}', '{price}', '{rating}', '{source}')
    """)
        con.commit()
    else:

        print("This site isn't supported.")
elif command == 2:

    items = cur.execute("SELECT title, price, rating, source FROM items")
    for row in items.fetchall():
        print(f"Title : {row[0]}\nPrice : {row[1]}\nRating : {row[2]}\nSource : {row[3]}\n\n====================\n")
else:

    sys.exit()
