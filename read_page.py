import requests
from bs4 import BeautifulSoup


page = requests.get('http://destiny.gg/embed/chat')
soup = BeautifulSoup(page.text, 'html.parser')

for tag in soup.find_all('msg-chat msg-user'):
    print(tag.text)
