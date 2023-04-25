"""
Web Scraper to extract companies data from www.euronics.it/tv-e-audio/tv/smart-tv/.

Author: Maria Dancianu
"""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd 
from time import sleep 


def get_url_soup(url, 
                 crawling_delay=5):
    """Opens the website and returns a BeautifulSoup object.
    
    Args:
      homepage_url: string
          URL of the website to be scraped. 
      crawling_delay: int, optional, Default = 5 
          Waiting time, in seconds, before crawling the website page. 
          This is required to avoid causing performance issues to the 
          website. 
      
    Returns: 
      soup: BeautifulSoup object
          BeautifulSoup object representing the page to be scraped. 
    """
    
    sleep(crawling_delay)

    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    
    return soup


def get_website_num_pages(homepage_url):
    """Gets the number of pages of the website.
      
    Args:
      homepage_url: string
          URL of the website to be scraped. 
    
    Returns:
      number_of_pages: int
          Number of pages of the website. 
    """
    
    soup = get_url_soup(homepage_url)
    
    pages = soup.find('select', attrs={'class': 'form-control change-pages'})
    
    all_options = pages.findAll('option')
    
    number_of_pages = len(all_options)

    return number_of_pages


def get_pages_url_list(homepage_url):
    """Gets the list of all the URL pages of the website. 
    
    Args:
      homepage_url: string
          URL of the website to be scraped. 
    
    Returns:
      urls_list: list of strings
          List of all the URL pages of the website. 
    """
    
    urls_list = []

    number_of_pages = get_website_num_pages(homepage_url)
    
    for page in range(1, number_of_pages + 1):
        if page == 1:
            page_url = homepage_url
        else:
            page_url = f'{homepage_url}?p={page}'
        
        urls_list.append(page_url)
    
    return urls_list


def scrape_one_smart_tv_data(product):
    """Extracts the data of a single company. 
    
    Args:
      product: BeautifulSoup object
          BeautifulSoup object of one single smart TV. 
          
    Returns:
      output_dict: dictionary 
          Dictionary with the company data. 
    """
    
    output_dict = {}
    
    title = product.find('div', attrs={'class': 'col-4 tile-body py-3'}).text.split('\n')[1]
    category = product.find('p', attrs={'class': 'tile-category'}).text   
    dimension = product.find('p', attrs={'class': 'body-medium mb-0'}).text
    
    price = product.findAll('div', attrs={'class': 'sales text-center mb-3'})
    
    # if no price was found, get discounted prices
    if len(price) == 0:
        price = product.findAll('span', attrs={
            'class': 'value font-bold text-nowrap h2'})
        
        discount = product.find('small', attrs={
            'class': 'font-bold txt-light-blue discount text-center mt-auto mb-0 mr-3'}).text
        
        discount_rate = discount.replace("Risparmi il ", "")
        discounted = True
    else:
        discounted = False
        discount_rate = None
        
    price = price[0].text.replace('\n', '')
      
    output_dict['tv_model'] = title
    output_dict['category'] = category
    output_dict['price'] = price
    output_dict['dimension'] = dimension
    output_dict['discounted'] = discounted
    output_dict['discount_rate'] = discount_rate
    
    return output_dict


def scrape_smart_tv_reviews(product):
    """Opens a smart TV URL and extracts all the user reviews. 
    
    Args:
      product: BeautifulSoup object
          BeautifulSoup object of one single smart TV. 
        
    Returns:
      smart_tv_reviews: list 
          List of all the user reviews present for one smart TV. 
    """
            
    url = product.find('a', href=True)
    url = url['href']
    
    new_url = f'https://www.euronics.it/{url}'
    
    soup = get_url_soup(new_url)
            
    div = soup.findAll('div', class_="bv-content-summary-body-text")

    smart_tv_reviews = [l.text for l in div]
   
    return smart_tv_reviews
    

def scrape_page_smart_tvs(soup, scrape_reviews=True):
    """Extract the smart TVs data from one single page. 
    
    Args:
      soup: BeautifulSoup object
          BeautifulSoup object representing the page to be scraped. 
      scrape_reviews: boolean, optional, Default=False
          If True scrape also the reviews. 
      
    Returns:
      page_smart_tvs_list: list
          List of dictionaries with the data of all the 
          companies of the page. 
    """
    
    page_smart_tvs_list = []
   
    products = soup.findAll('div', attrs={'class': 'col-md-3 col-sm-3 col-xs-6 product-layout grid-mode'})
    
    for product in products:
        smart_tv_data_dict = scrape_one_smart_tv_data(product)
  
        if scrape_reviews:
            reviews_list = scrape_smart_tv_reviews(product)
            
            smart_tv_data_dict['reviews'] = reviews_list
     
        page_smart_tvs_list.append(smart_tv_data_dict)
        
    return page_smart_tvs_list


def EuronicsSmartTVDataScraper():
    """Extracts smart TV products data.
    
    Returns:
        None but saves a csv named with the extracted data.
    """

    all_smart_tvs_list = []
    
    homepage_url = "https://www.euronics.it/tv-e-audio/tv/smart-tv/"
    
    pages_url_list = get_pages_url_list(homepage_url)
    
    for page_url in pages_url_list:
        soup = get_url_soup(page_url)
        
        page_smart_tvs_list = scrape_page_smart_tvs(soup)
        
        all_smart_tvs_list.extend(page_smart_tvs_list)
        
    results_df = pd.DataFrame(all_smart_tvs_list)  
    
    if not results_df.empty:
        results_df['brand'] = results_df.tv_model.apply(lambda x: x.split('-')[0])
        
        if 'reviews' in results_df.columns:
            results_df['num_of_reviews'] = results_df.reviews.apply(lambda x: len(x))
        
    results_df.to_csv("euronics_smart_tvs.csv")
   
    
if __name__ == '__main__':
    EuronicsSmartTVDataScraper()




