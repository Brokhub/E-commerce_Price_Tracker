# Amazon Price Tracker 

Simple and easy to use Python script to track a product price on Amazon

## Featuers
✅ Scrapes product name, price, and rating  \n
✅ Saves data to CSV  \n
✅ Sends a Telegram notification if price drops\n

## How to run
First make sure to install the next modules:\n
`pip install requests beautifulsoup4 pandas`\n

If you want to recieve a telegram notification when the price drops , change these variables:\n

On line 8 `TG_ID = 123` replace `123` with your actual Telegram ID\n
On line 9 `TG_TOKEN = "12345:abcde"` replace `12345:abcde` with an actual Telegram Bot Token (You can make a Telegram Bot from `@BotFather`)\n

Then run the script, when this shows up:\n
![image_2025-03-05_04-14-52](https://github.com/user-attachments/assets/170683f3-6afd-420b-81a4-5865ee768ce4)\n
Enter the URL of the itam that you want to track\n

That's it!

