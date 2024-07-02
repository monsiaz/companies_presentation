import time
import random
import json
import pandas as pd
from openai import OpenAI
from tabulate import tabulate
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from tqdm import tqdm  # Importer tqdm pour la barre de progression

# Clé API pour GPT-4o
API_KEY = 'sk-proj-RZ0LiDtZsP3yuMOk9mSHT3BlbkFJ85KBlBotL0iox0wDxGGv'
client = OpenAI(api_key=API_KEY)

# Charger les informations des entreprises depuis le fichier CSV
def load_company_info(csv_path):
    try:
        df = pd.read_csv(csv_path, sep=';', on_bad_lines='skip')  # Ignore les lignes mal formatées
        return df.to_dict(orient='records')
    except pd.errors.ParserError as e:
        print(f"Error parsing CSV file at {csv_path}: {e}")
        with open(csv_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                print(f"Line {i + 1}: {line.strip()}")
        raise

# Générer un texte avec GPT-4o
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

# Charger les prompts depuis un fichier texte
def load_prompts(prompts_file_path):
    with open(prompts_file_path, 'r') as file:
        prompts = file.read().split("\n\n")
    return prompts

# Charger les proxies depuis un fichier texte
def load_proxies(proxies_file_path):
    with open(proxies_file_path, 'r') as file:
        proxies = [line.strip() for line in file if line.strip()]
    return proxies

# Extraire le texte de présentation existant d'une page web
def extract_intro_text(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')
    element = soup.select_one('#about > div.px-3.px-lg-4.pb-3.pb-lg-4.pt-3.pt-md-0 > div.company-presentation')
    if element:
        return element.text.strip()
    return "Présentation non disponible."

# Obtenir un user agent aléatoire
def get_random_user_agent():
    ua = UserAgent()
    return ua.random

# Configurer Selenium pour utiliser un proxy et un user agent aléatoire
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
    driver.set_page_load_timeout(90)  # Augmenter le délai d'attente pour le chargement des pages
    return driver

# Scraper les informations de la page web
def scrape_page(url, proxies):
    driver = get_driver(proxies)
    try:
        driver.get(url)
        time.sleep(15)  # Attendre le chargement de la page
        page_source = driver.page_source
    except Exception as e:
        print(f"Failed to load page {url}: {e}")
        page_source = ""
    driver.quit()
    return page_source

# Fonction principale
def main(mode_test=False):
    company_csv_path = '/Users/simonazoulay/Presentation_Text/liste-entreprises.csv'  # Chemin absolu vers le fichier CSV
    prompts_file_path = '/Users/simonazoulay/Presentation_Text/prompts.txt'
    proxies_file_path = '/Users/simonazoulay/Presentation_Text/proxyscrape_premium_http_proxies.txt'
    output_json_path = '/Users/simonazoulay/Presentation_Text/company_info.json'
    
    companies = load_company_info(company_csv_path)
    prompts = load_prompts(prompts_file_path)
    proxies = load_proxies(proxies_file_path)
    
    if mode_test:
        companies = companies[:10]  # Traiter uniquement les 10 premières entreprises en mode test

    final_info = {}
    
    # Initialiser la barre de progression
    with tqdm(total=len(companies), desc="Progression") as pbar:
        for company in companies:
            url = company['URL']
            print(f"Traitement de l'URL: {url}")
            
            # Extract introductory text using existing web scraping method
            page_source = scrape_page(url, proxies)
            if page_source:
                presentation_text = extract_intro_text(page_source)
                print(f"Texte de présentation extrait: {presentation_text}")
            else:
                presentation_text = "Présentation non disponible."
                print(f"Échec de l'extraction du texte de présentation pour {url}")
            
            # Choisir un prompt aléatoire
            prompt_template = random.choice(prompts)
            print(f"Using prompt: {prompt_template}")  # Afficher le prompt choisi pour vérification
            
            # Construire le prompt avec les informations de l'entreprise
            prompt = f"{presentation_text}\n\n{prompt_template}"
            
            # Générer le texte avec GPT-4
            generated_text = generate_text(prompt)
            print("Texte généré par GPT-4")
            
            final_info[url] = {
                "Informations clés": company,
                "Texte de présentation existant": presentation_text,
                "Texte généré": generated_text
            }
            
            # Mettre à jour la barre de progression
            pbar.update(1)

            # Afficher les résultats
            print(f"\n--- Résultats pour {url} ---")
            print(f"\nInformations clés extraites :\n{tabulate(company.items(), headers=['Clé', 'Valeur'], tablefmt='pretty')}")
            print(f"\nTexte de présentation extrait :\n{presentation_text}")
            print(f"\nTexte généré :\n{generated_text}")

    # Sauvegarder les informations dans un fichier JSON
    with open(output_json_path, 'w') as json_file:
        json.dump(final_info, json_file, indent=2)

if __name__ == "__main__":
    main(mode_test=True)
