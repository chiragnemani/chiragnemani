import requests
import re

USERNAME = 'chiragnemani'
FEED_URL = f'https://medium.com/feed/@{USERNAME}'

def fetch_posts():
    response = requests.get(FEED_URL)
    posts = re.findall(r'<item>(.*?)</item>', response.text, re.DOTALL)[:5]
    return [{'title': re.search(r'<title>(.*?)</title>', post).group(1), 'link': re.search(r'<link>(.*?)</link>', post).group(1)} for post in posts]

def update_readme(posts):
    with open('README.md', 'r+') as file:
        readme = file.read()
        marker = '<!-- BLOG-POST-LIST:START -->'
        end_marker = '<!-- BLOG-POST-LIST:END -->'
        post_md = '\n'.join([f'- [{post["title"]}]({post["link"]})' for post in posts])
        new_readme = re.sub(f'{marker}.*?{end_marker}', f'{marker}\n{post_md}\n{end_marker}', readme, flags=re.DOTALL)
        file.seek(0)
        file.write(new_readme)
        file.truncate()

posts = fetch_posts()
update_readme(posts)
