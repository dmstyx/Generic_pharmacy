import re
import requests
from statistics import mode
from bs4 import BeautifulSoup
import save_meds_to_db

global name


def fetch_url(url, name):

    """ Uses requests and Beautiful soup. Receives URL
    from format text. Finds all listings verified as Exportes
    and have price listed"""

    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')
    search_result = soup.findAll('li', {'class': 'mList'})
    price_listing = []

    if r.status_code == 200:
        with open('search_results.txt', 'w') as file:
            for item in search_result:
                result = item.text
                if "Exporter" and "₹" in result:
                    price_listing.append(item)
            file.write(str(price_listing))
            get_mode_listing(price_listing, name)
    else:
        print(f"Error {r.status_code}")


def format_text(name, b_name):

    """Takes name of drug from db. Removes numbers and symbols.
    Returns searchable URL"""

    global formated_name
    global formated_url
    global brand_name

    brand_name = b_name
    regex = re.compile('[^a-zA-Z ]')
    regex_name = (regex.sub('', name)).strip().split()
    formated_name = " ".join([i for i in regex_name if len(i) > 3])
    formated_url = f'https://dir.indiamart.com/search.mp?ss={formated_name}&prdsrc=1&countryiso=GB'
    print(brand_name)
    fetch_url(formated_url, name)


def get_mode_listing(search_result, name):
    
    """Takes verified and priced listings. Creates search results and
    returns listing woth mode price."""

    nums = []

    with open('search_results.txt', 'r') as file:
        html_text = file.read()

    soup = BeautifulSoup(html_text, 'html.parser')

    price = soup.findAll('span', {'class': "prc cp"})
    for i in price:
        n = i.text
        nums.append(n)

    if len(nums) > 1:
        find_mode = [float(i) for i in re.findall(r'[\d\.\d]+', str(nums))]
        price_index = find_mode.index(mode(find_mode))
    else:
        price_index = 0

    with open('best_option.txt', 'w') as file:
        try:
            file.write(str(search_result[price_index]))
        except:
            print('NO RESULTS')
            with open('failed_searches.txt', 'a') as file:
                file.write(f'Generic name: {name}\nFormated name{formated_name}\n{formated_url}')
            save_meds_to_db.med_not_found()

    with open('best_option.txt', 'r') as file:
        html_text = file.read()

    soup_url = BeautifulSoup(html_text, 'html.parser')
    get_url = soup_url.find('a', {"class": "mDb"})
    try:
        get_prod_details(get_url['href'], name)
    except TypeError:
        print('        TYPE ERROR        ')


def get_prod_details(url, name):

    """Uses requests and Beautifulsoup to search product URL.
    Returns product details"""

    r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    soup = BeautifulSoup(r.content, 'html.parser')

    get_title = soup.find('h1', {"class": "bo"})
    get_raw_price = soup.find('span', {"class": "prc-tip bo"})
    try:
        get_price = float(re.findall(r'[\d\.\d]+', get_raw_price.text)[0])
    except:
        get_price = 0
    get_pack_size = soup.findAll('td', {"class": "tdwdt1 color6"})
    get_image = soup.find('img', {"class": "drift-demo-trigger"})

    prod_details = ['Packaging Size', 'Manufacturer', 'Composition', 'Treatment', 'Prescription/Non prescription', 'Form']
    prod_details_list = [i.text for i in get_pack_size]
    product_info = tuple(zip(prod_details, prod_details_list))

    contact = soup.find('div', {"id": "supp_nm"}).text
    company = soup.find('a', {"class": "color6 pd_txu bo"}).text
    address = soup.find('span', {"class": "color1 dcell verT fs13"}).text
    tel = soup.find('span', {"class": "duet"}).text
    web = soup.find('a', {"class": "color1 utd"}).text

    title = f"Name: \n{get_title.text} \n\nPrice:\n₹{get_price}\n\n"
    try:
        pi_1 = f"{product_info[0][0]}, {product_info[0][1]}"
        pi_2 = f"{product_info[1][0]}, {product_info[1][1]}"
        pi_3 = f"{product_info[2][0]}, {product_info[2][1]}"
        pi_4 = f"{product_info[3][0]}, {product_info[3][1]}"
        pi_5 = f"{product_info[4][0]}, {product_info[4][1]}"
        pi_6 = f"{product_info[5][0]}, {product_info[5][1]}"
    except:
        pass

    con_inf = f"Contant: {contact}\nCompany: {company}\nAddress: {address}\ntel: {tel}\nWeb: {web}\n\nIndiaMart Url: {url}\n\nImage: {get_image['src']}"

    # with open('results.txt', 'a') as file:
    #     file.write(title)
    #     file.write(pi_1)
    #     file.write(pi_2)
    #     file.write(pi_3)
    #     file.write(pi_4)
    #     file.write(pi_5)
    #     file.write(pi_6)
    #     file.write(con_inf)

    try:
        test_list = [name, get_title.text, get_price, contact, company, address,
                     brand_name, tel, web, url, get_image['src'],
                     product_info[0][0], product_info[0][1],
                     product_info[1][0], product_info[1][1],
                     product_info[2][0], product_info[2][1],
                     product_info[3][0], product_info[3][1],
                     product_info[4][0], product_info[4][1],
                     product_info[5][0], product_info[5][1]]

        save_meds_to_db.enter_med_info(test_list)
    except:
        pass


if __name__ == "__main__":
    format_text()
