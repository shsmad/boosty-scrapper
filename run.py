import os
import time
import httpx
from bs4 import BeautifulSoup
import json
import sys

from config import settings

boostyProfileTemplate = "https://boosty.to/{}"
boostyPostTemplate = "https://boosty.to/{}/posts/{}"
boostyJsonTemplate = "https://api.boosty.to/v1/blog/{}/post/?limit=100&comments_limit=2&reply_limit=1"

def start_crawler(username: str):
    print("Starting crawler")
    cookies_dict = {cookie.split('=')[0]: cookie.split('=')[1] for cookie in settings.AUTH_COOKIES.split('; ')}

    with httpx.Client(
        cookies=httpx.Cookies(cookies_dict),
        headers={"User-Agent": settings.USER_AGENT},
    ) as client:
        url = boostyJsonTemplate.format(username)
        response = client.get(url)
        post_list = json.loads(response.text)['data']

        os.makedirs(f'posts/{username}', exist_ok=True)
        for post_idx, post in enumerate(post_list):
            print(f"post {post_idx} of {len(post_list)} ({post['id']})")
            os.makedirs(f'posts/{username}/{post["id"]}', exist_ok=True)

            url = boostyPostTemplate.format(username, post['id'])
            response = client.get(url)
            if response.status_code != 200:
                print(f"!!! {response.status_code=} {response.text}")
                return

            html_content = response.text

            soup = BeautifulSoup(html_content, 'html.parser')
            script_tag = soup.find('script', {'type': 'text/plain', 'id': 'initial-state'})

            if not script_tag:
                print("!!! No script tag")
                continue

            initial_state = json.loads(script_tag.string)
            posts = initial_state['posts']['postsList']['data']['posts']
            post_info = posts[0]
            data = post_info['data']

            with open(f'posts/{username}/{post["id"]}/metadata.json', 'w') as f:
                json.dump(post_info, f)

            with open(f'posts/{username}/{post["id"]}/dump.html', 'w') as f:
                f.write(html_content)

            time.sleep(1)

            for att_idx, attachment in enumerate(data):
                print(f"\t{att_idx} of {len(data)} for {post['id']}")
                if attachment['type'] != 'image':
                    print(f"!!! {attachment}")
                    continue

                if os.path.exists(f'posts/{username}/{post["id"]}/{attachment["id"]}.jpg'):
                    continue

                response = client.get(f"https://images.boosty.to/image/{attachment['id']}")
                with open(f'posts/{username}/{post["id"]}/{attachment["id"]}.jpg', 'wb') as f:
                    f.write(response.content)

                time.sleep(1)

start_crawler(username=sys.argv[1])
