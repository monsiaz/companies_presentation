import time
import random
import json
import pandas as pd
import psutil
from openai import OpenAI
from tabulate import tabulate
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from tqdm import tqdm
from dotenv import load_dotenv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Load environment variables
load_dotenv()

# API key for GPT-4o
API_KEY = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=API_KEY)

# Load company information from a CSV file
def load_company_info(csv_path):
    try:
        df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip')  # Ignore malformed lines
        return df.to_dict(orient='records')
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file at {csv_path}: {e}")
        with open(csv_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                print(f"Line {i + 1}: {line.strip()}")
        raise

# Generate text with GPT-4o
def generate_text(prompt):
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "Tu es un expert de la finance et de la comptabilité qui connait bien le monde de l'entreprise. Chaque section doit avoir un titre descriptif et pas générique (Ex : 'Introduction' ou 'Conclusion') et ne doit pas répéter les informations clés déjà fournies à savoir les Informations clés (nom + date de création + localisation etc.. qui ne te servent que pour le contexte et les reste des parties) Par ailleurs, tu feras attention à ce que le texte ne soit pas redondant avec les informations du {presentation_text}."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response.choices[0].message.content.strip()

# Load prompts from a text file
def load_prompts(prompts_file_path):
    with open(prompts_file_path, 'r') as file:
        prompts = file.read().splitlines()
    return prompts

# Load proxies from a text file
def load_proxies(proxies_file_path):
    with open(proxies_file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

# Extract introductory text from a web page
def extract_intro_text(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    element = soup.select_one('#about > div.px-3.px-lg-4.pb-3.pb-lg-4.pt-3.pt-md-0 > div.company-presentation')
    if element:
        return element.text.strip()
    return "Présentation non disponible."

# Get a random user agent
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Configure Selenium to use a proxy and a random user agent
def get_driver(proxies):
    proxy = random.choice(proxies)
    user_agent = get_random_user_agent()

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument(f'user-agent={user_agent}')

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(90)  # Increase page load timeout
    return driver

# Scrape information from the web page
def scrape_page(url, proxies):
    driver = get_driver(proxies)
    try:
        driver.get(url)
        time.sleep(15)  # Wait for the page to load
        page_source = driver.page_source
    except Exception as e:
        print(f"Failed to load page {url}: {e}")
        page_source = ""
    driver.quit()
    return page_source

# Process a single company
def process_company(company, prompts, proxies):
    url = company['URL']
    print(f"Traitement de l'URL: {url}")
    
    # Extract introductory text using existing web scraping method
    page_source = scrape_page(url, proxies)
    if page_source:
        presentation_text = extract_intro_text(page_source)
    else:
        presentation_text = "Présentation non disponible."
        print(f"Échec de l'extraction du texte de présentation pour {url}")
    
    # Choose a random prompt
    prompt_template = random.choice(prompts)
    print(f"Using prompt for {url}: {prompt_template}")  # Print the chosen prompt for verification
    
    # Build the prompt with the company's information
    fixed_text = "Tu me livreras le texte en html sans doctype et unicode ou markdown ni head ou body avec une mise en forme adaptée et en partant sur des balises à partir du H3 si nécessaire et sans unicode ou markdown - seulement de la mise en page tel que du gras et des titres si c'est nécessaire et pertinent."
    prompt = f"{presentation_text}\n\n{fixed_text}\n\n{prompt_template}"
    
    # Generate the text with GPT-4
    generated_text = generate_text(prompt)
    
    return {
        "Informations clés": company,
        "Texte de présentation existant": presentation_text,
        "Texte généré": generated_text
    }

# Dynamically adjust the number of workers
def adjust_workers():
    cpu_percent = psutil.cpu_percent(interval=1)
    mem_percent = psutil.virtual_memory().percent
    max_workers = min(5, os.cpu_count() - 1)  # Max workers to be between 1 and CPU count - 1
    if cpu_percent < 50 and mem_percent < 70:
        return max_workers
    elif cpu_percent < 70 and mem_percent < 85:
        return max(1, max_workers // 2)
    else:
        return 1

# Main function
def main(mode_test=False):
    company_csv_path = '/Users/simonazoulay/Presentation_Text/liste-entreprises.csv'  # Absolute path to the CSV file
    prompts_file_path = '/Users/simonazoulay/Presentation_Text/prompts.txt'
    proxies_file_path = os.getenv('PROXY_FILE_PATH')  # Use environment variable for proxies path
    output_json_path = '/Users/simonazoulay/Presentation_Text/company_info.json'
    
    companies = load_company_info(company_csv_path)
    prompts = load_prompts(prompts_file_path)
    proxies = load_proxies(proxies_file_path)
    
    if mode_test:
        companies = random.sample(companies, 15)  # Process only 15 random companies in test mode

    final_info = {}
    
    # Initialize progress bar
    with tqdm(total=len(companies), desc="Progression") as pbar:
        with ThreadPoolExecutor(max_workers=adjust_workers()) as executor:
            future_to_company = {executor.submit(process_company, company, prompts, proxies): company for company in companies}
            for future in as_completed(future_to_company):
                company = future_to_company[future]
                try:
                    data = future.result()
                    final_info[company['URL']] = data
                except Exception as e:
                    print(f"Error processing company {company['URL']}: {e}")
                pbar.update(1)

    # Save information to a JSON file
    with open(output_json_path, 'w') as json_file:
        json.dump(final_info, json_file, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main(mode_test=True)
