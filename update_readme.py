import requests
import re
import sys

def fetch_medium_posts(username):
    feed_url = f'https://medium.com/feed/@chiragnemani'  # Replace '@{username}' with your Medium username
    response = requests.get(feed_url)
    if response.status_code != 200:
        raise Exception(f'Failed to fetch Medium posts for {username}')

    posts = re.findall(r'<item>(.*?)</item>', response.text, re.DOTALL)[:5]  # Fetching latest 5 posts
    post_list = [{'title': re.search(r'<title>(.*?)</title>', post).group(1),
                  'link': re.search(r'<link>(.*?)</link>', post).group(1)}
                 for post in posts]
    return post_list

def update_readme(posts):
    with open('README.md', 'r+') as file:
        readme_content = file.read()
        marker = '<!-- MEDIUM-POSTS-LIST:START -->'  # Start marker in your README
        end_marker = '<!-- MEDIUM-POSTS-LIST:END -->'  # End marker in your README
        post_md = '\n'.join([f'- [{post["title"]}]({post["link"]})' for post in posts])
        new_readme = re.sub(f'{marker}.*?{end_marker}', f'{marker}\n{post_md}\n{end_marker}', readme_content, flags=re.DOTALL)
        file.seek(0)
        file.write(new_readme)
        file.truncate()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide your Medium username as an argument.')
        sys.exit(1)
    
    medium_username = sys.argv[1]  # Replace None with your Medium username
    posts = fetch_medium_posts(medium_username)
    update_readme(posts)
