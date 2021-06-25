import requests
from bs4 import BeautifulSoup


def fetch_url(url):
    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')

    if r.status_code == 200:
        find_tags(soup)
    else:
        print(f"Error {r.status_code}")


def find_tags(soup):
    with open('generic_drugs2.txt', 'w') as file:
        try:
            med_names = soup.findAll('td')
            for i in med_names:
                print(i.get_text())
                file.write(i.get_text() + '\n')
        except:
            print("Invalid page!")


def save_file(content_text):
    with open('generic_drugs.txt', 'w') as file:
        file.write(content_text)


if __name__ == "__main__":
    fetch_url('https://www.disabled-world.com/medical/pharmaceutical/generic-equivalents.php')
