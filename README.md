# Euronics-Web-Scraper
A web scraper to extract smart TV products data from www.euronics.it. 

![alt text](https://github.com/mariadancianu/Euronics-Scraper/blob/main/website_page.png)

It extracts the following information:
- TV model 
- Category 
- Price 
- Dimension 
- Discounted 
- Discount rate 
- Brand
- Number of user reviews
- User reviews

Expected output dataset:
![alt text](https://github.com/mariadancianu/Euronics-Scraper/blob/main/output_dataset_example.png)

## Technologies 

Python version: 3.11. 

Python libraries:
- BeautifulSoup
- urllib 
- pandas
- time

## Learning points 
- inspect the structure of the html page from which to scrape the data and identify the required elements
- getting familiar with the BeautifulSoup library 
- extract the number of pages of the website and scrape the data on all pages 
- extract URLs from the main page, open them and extract additional information from these pages 
- using a crawling delay to avoid performance issues for the scraped website 


## Status
Project is: *in progress*. 

## Warnings
The websites structure changes in time and a Web Scraper that was previously working perfectly can break due to these updates. The code must be maintained and updated by running periodical tests. Small adjustments are usually required since the websites changes are small and incremental. I will try to update the code periodically but keep in mind that any errors are part of the Web Scraping process.

## Contact 
Created by mary_0094@hotmail.it, feel free to get in touch! :woman_technologist:
