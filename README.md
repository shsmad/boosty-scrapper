# Boosty Scrapper

## Install

1. `git clone https://github.com/shsmad/boosty-scrapper.git`
2. `cd boosty-scrapper`
3. `python3.12 -m venv venv`
4. `source venv/bin/activate`
5. `pip install -r requirements.txt`

## Setup

1. Log in to your Boosty account in web-browser
2. Get your Boosty cookies (see `document.cookie` in devtools). It
   shoud be a string like "auth=… _clientId=…"
3. create file `.secrets.toml` with structure `auth_cookies = %your
   cookies from 2%:

   ```toml
   auth_cookies = "auth=… _clientId=…"
   ```

## Usage

1. ensure your venv is activated
2. `python run.py %desired_boosty_author_to_scrape%`
3. see `posts/%desired_boosty_author_to_scrape%` folder for posts
