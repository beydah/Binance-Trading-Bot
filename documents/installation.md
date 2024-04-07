# Binance Trading Bot

<div style="text-align: center;">
  <a href="https://github.com/beydah/Binance-Trading-Bot">  
    <img src="https://raw.githubusercontent.com/beydah/asset/main/button/home_off.png" style="width: 10%;"  alt="<< Return to Home Page <<">
  </a>
</div>

<div style="text-align:center;">
    <a href="#binance-trading-bot">
        <img src="https://i.imgur.com/waxVImv.png" alt="Colorful Stick">
    </a>
</div>

## Download
### Get API Binance & Telegram
First, log in via the [Binance Website](https://www.binance.com/). Then `Settings -> Account -> API Management`
gel in the part.

Create an API in the opened location. The API name you create doesn't matter. You can give any name you want
(Preferred: Binance-Trading-Bot). Make sure to place the **API Key and Secret Key you have created in a place where no one can access it.
Save** (Since you save, these two effects will definitely be permanent later).

With these flags in API restrictions:
- Enable Reading
- Enable Spot and Margin Trading

Now that we have our Binance APIs, we need to create a bot on Telegram so that our bot can talk to us and
Let's get our person's Token and ID information. First, log in to [Telegram](https://web.telegram.org/)
(If you don't have an account, sign up).

Then send this command to the `userinfobot` bot from the search section: `/start`. After sending this command you will get Id,
It will send Name and Grammar message. Note the Id information in the message content where you noted the API information.
This information will be needed later for our bot to talk to us.

Finally, search for `BotFather` bot in the search section and search for BotFather, which is approved by Telegram, respectively.
Send these messages:
- `/start`
- `/newbot`
- `Binance Trading Bot` (Here you can give your bot any name you want.)
- `{YOUR_USERNAME}_Binance_Trading_Bot` (Here you specify the username of your bot and the username is unique
should be. For this reason, you can specify a username by typing your own username in the {YOUR_USERNAME} section.
If you get an error here, try another name. Example: **Beydah_Binance_Trading_Bot**)

Congratulations! Your bot is ready. In the last message that BotFather sent you, you have noted the HTTP API and your APIs.
Make a note on the ground. This will come in handy later.

### Get Python & PyCharm
First of all, you need to install [Python 3.10.0](https://www.python.org/downloads/release/python-3100/). This version of the bot I created works with Python.

Then install [PyCharm Community Edition](https://www.jetbrains.com/pycharm/download/) and restart the computer.

### Download Binance Trading Bot
You can download Binance Trading Bot to your computer from this link. Then download the zip file you downloaded
Extract the zip file to the folder on your computer where you want it to work.

[v Click For Download To Binance Trading Bot v](https://github.com/beydah/Binance-Trading-Bot/archive/refs/heads/main.zip)

<div style="text-align: center;">
    <a href="https://github.com/beydah/Binance-Trading-Bot/archive/refs/heads/main.zip">
        <img src="https://raw.githubusercontent.com/beydah/asset/main/button/download_focus.png" style="width: 15%;"  alt=">> Continue Reading >>">
    </a>
</div>

## Installation
### Installation on PyCharm
Open the bot you downloaded and extracted to the folder you want it to run in the PyCharm application.

### Create Venv on PyCharm
requirements.txt dosyasındaki kütüphanelerin de indirileceği bir venv dosyası oluştur (PyCharm uygulamayı ilk açtığında
size soracak. Eğer bu soruya evet yanıtını vermediyseniz kendiniz kurmanız gerekir. Bunun için Settings > 
Python Interpreter > Add Interpreter > Add Local Interpreter kısmına gidin ve açılan yerde Virtual Enverionment 
seçeneği ile venv dosyanızı oluşturun [DEVAMI GELECEK]).

### Enter Your APIs

<div style="text-align:center;">
    <a href="#binance-trading-bot">
        <img src="https://i.imgur.com/waxVImv.png" alt="Colorful Stick">
    </a>
</div>

<div style="text-align: center;">
    <a href="#binance-trading-bot">
        <img src="https://raw.githubusercontent.com/beydah/asset/main/button/scroll_off.png" style="width: 15%;"  alt="^ Scroll UP ^">
    </a>
    <a href="https://github.com/beydah/Binance-Trading-Bot/blob/main/documents/installation.md">
        <img src="https://raw.githubusercontent.com/beydah/asset/main/button/next_on.png" style="width: 15%;"  alt=">> Continue Reading >>">
    </a>
</div>
