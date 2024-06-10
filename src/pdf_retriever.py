import os
import requests
import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


BASE_URL = "https://www.fia.com"

def get_season_urls(base_url):
    response = requests.get(base_url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    select_element = soup.find('select', id='facetapi_select_facet_form_3')
    if not select_element:
        raise ValueError("Could not find the season select element on the page.")
    season_urls = {}
    for option in select_element.find_all('option'):
        season_name = option.text.strip()
        season_url = option.get('value')
        if season_url != "0":
            full_season_url = BASE_URL + season_url
            season_urls[season_name] = full_season_url
    return season_urls

def retrieve_fia_pdfs(url, download_dir='data/raw_pdfs', force=False, gp=None, season_year=None):
    # Create a new directory path that includes the season year and GP name
    if season_year and gp:
        download_dir = os.path.join(download_dir, season_year, gp.replace(' ', '_'))

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all links to PDF files
    pdf_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        logger.debug(f'Found FIA HREF {href}')
        if href and href.endswith('.pdf'):
            pdf_name = href.split('/')[-1]
            logger.debug(f'FIA PDF Name: {pdf_name}')
            if gp:
                gp_formatted = [gp.lower().replace(' ', variant) for variant in [' ', '-', '_']]
                logger.debug(f'GP name variants {gp_formatted}')
                if not any(variant in pdf_name.lower() for variant in gp_formatted):
                    continue
            if href.startswith('http'):
                pdf_links.append(href)
            else:
                pdf_links.append(BASE_URL + href)

    for pdf_link in pdf_links:
        pdf_name = pdf_link.split('/')[-1]
        pdf_path = os.path.join(download_dir, pdf_name)
        if os.path.exists(pdf_path) and not force:
            logger.info(f"Skipping already downloaded: {pdf_name}")
            continue
        pdf_response = requests.get(pdf_link)
        pdf_response.raise_for_status()
        with open(pdf_path, 'wb') as pdf_file:
            pdf_file.write(pdf_response.content)
        logger.info(f'Downloaded: {pdf_name}')
    return pdf_links

def retrieve_all_season_pdfs(base_url, download_dir='data/raw_pdfs', force=False, season=None, gp=None):
    season_urls = get_season_urls(base_url)
    for season_name, url in season_urls.items():
        season_year = season_name.split()[-1]  # Extract the year component
        if season and season_year != season:
            continue
        logger.info(f"Retrieving PDFs for {season_name} from {url}")
        # Pass the season_year to the retrieve_fia_pdfs function
        retrieve_fia_pdfs(url, download_dir, force, gp, season_year)