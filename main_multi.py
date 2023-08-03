import requests
from bs4 import BeautifulSoup as BS
from datetime import datetime
import xlsxwriter
from multiprocessing import Pool


def get_html(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def get_page_links(html):
    links = []
    soup = BS(html,'html.parser')
    container = soup.find('div',{'class':'container body-container'})
    main = container.find('div',{'class':'main-content'})
    listings = main.find('div',{'class':'listings-wrapper'})
    post = listings.find_all('div',{'class':'listing'})
    for post_list in post:
        header = post_list.find('div',{'class':'left-side'})
        link  = header.find('a').get('href')
        full_link = 'https://www.house.kg'+link
        links.append(full_link)
        
        
    return links
        # title = header.find('p',{'class':'title'}).text.strip()
        # address = header.find('div',{'class':'address'}).text.strip()
        # dollar = post_list.find('div',{'class':'sep main'}).find('div',{'class':'price'}).text.strip()
        # som = post_list.find('div',{'class':'sep main'}).find('div',{'class':'price-addition'}).text.strip()
        # desc = post_list.find('div',{'class':'description'})



def get_post_data(html):
    soup = BS(html,'html.parser')
    main = soup.find('div',{'class':'main-content'})
    header = main.find('div',{'class':'details-header'})
    title = header.find('div',{'class':'left'}).find('h1').text.strip()
    address = header.find('div',{'class':'address'}).text.strip()
    dollar = header.find('div',{'class':'sep main'}).find('div',{'class':'price-dollar'}).text.strip()
    som = header.find('div',{'class':'sep main'}).find('div',{'class':'price-som'}).text.strip()
    mobile = main.find('div',{'class':'phone-fixable-block'}).find('div',{'class':'number'}).text.strip()
    desc = main.find('div',{'class':'description'})
    desc = desc.text.strip() if desc else 'Нет Описания'
    
    
    info = main.find('div',{'class':'details-main'}).find_all('div',{'class':'info-row'})
    
    add_info = {}
    
    for infos in info:
        key = infos.find('div',{'class':'label'}).text.strip()
        value = infos.find('div',{'class':'info'}).text.strip()
        add_info.update({key:value})
        
    data = {
        'title':title,
        'address':address,
        'dollar':dollar,
        'som':som,
        'phone':mobile,
        'desc':desc
    }
    return data
    
    
    

def get_last_page(html):
    soup = BS(html,'html.parser')
    page = soup.find('ul',{'class':'pagination'})
    page_list = page.find_all('a',{'class':'page-link'})
    last_page = page_list[-1].get('data-page')
    
    
    return int(last_page)
    
    
def write_excel(data):
    workbook = xlsxwriter.Workbook('house_kg.xlsx')
    worksheet = workbook.add_worksheet()
    row = 0
    column = 0
    for value in data.values():
        worksheet.write(row, column, value )
        
        row+=1
        
    workbook.close()
    
    
    
def multi_pars(page_num):
    URL = 'https://www.house.kg/snyat-kvartiru?region=1&town=2&sort_by=upped_at+desc'
    
    page_url = URL + f'&page={page_num}'
    print(page_num)
    html = get_html(page_num)
    links = get_page_links(html)
    for link in links:
        detail_html = get_html(link)
        data = get_post_data(detail_html)
        write_excel(data)
    
def main():
    start = datetime.now()
    URL = 'https://www.house.kg/snyat-kvartiru?region=1&town=2&sort_by=upped_at+desc'
    last_page = get_last_page(get_html(URL))
    html = get_html(URL)
    
    end = datetime.now()
    result = end - start
    print(result)
        
        
        
        
if __name__ == '__main__':
    main()
    
    

