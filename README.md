# Presentation Text Generator

Ce projet utilise Selenium, BeautifulSoup et l'API OpenAI GPT-4 pour extraire des informations sur des entreprises depuis des pages web, puis génère un texte de présentation détaillé pour chaque entreprise. Le script utilise également la bibliothèque `tqdm` pour afficher une barre de progression pendant l'exécution.

## Prérequis

Assurez-vous d'avoir les éléments suivants installés sur votre machine :

- Python 3.x
- pip (Python package installer)

## Installation

1. Clonez ce dépôt sur votre machine locale :

    ```bash
    git clone https://github.com/votre-utilisateur/presentation-text-generator.git
    cd presentation-text-generator
    ```

2. Créez un environnement virtuel et activez-le :

    ```bash
    python -m venv .venv
    source .venv/bin/activate  # Sur Windows, utilisez .venv\Scripts\activate
    ```

3. Installez les dépendances requises :

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1. Remplissez le fichier `config.json` avec votre clé API OpenAI et le chemin absolu vers les fichiers nécessaires :

    ```json
    {
        "API_KEY": "votre_clé_api_openai",
        "company_csv_path": "/chemin/vers/liste-entreprises.csv",
        "prompts_file_path": "/chemin/vers/prompts.txt",
        "proxies_file_path": "/chemin/vers/proxyscrape_premium_http_proxies.txt",
        "output_json_path": "/chemin/vers/company_info.json"
    }
    ```

2. Préparez vos fichiers d'entrée :
   - `liste-entreprises.csv` : Fichier CSV contenant les informations des entreprises, incluant une colonne `URL`.
   - `prompts.txt` : Fichier texte contenant les différents prompts séparés par deux sauts de ligne (`\n\n`).
   - `proxyscrape_premium_http_proxies.txt` : Fichier texte contenant des proxies HTTP.

## Utilisation

1. Activez l'environnement virtuel si ce n'est pas déjà fait :

    ```bash
    source .venv/bin/activate  # Sur Windows, utilisez .venv\Scripts\activate
    ```

2. Exécutez le script :

    ```bash
    python script.py
    ```

Le script traitera les entreprises listées dans le fichier CSV, extraira le texte de présentation des pages web, générera des textes de présentation détaillés en utilisant GPT-4, et affichera une barre de progression pour suivre l'avancement du traitement.

## Structure du projet

- `script.py` : Script principal pour le traitement des entreprises.
- `requirements.txt` : Liste des dépendances Python nécessaires.
- `config.json` : Fichier de configuration contenant les chemins et la clé API.
- `liste-entreprises.csv` : Fichier CSV contenant les informations des entreprises.
- `prompts.txt` : Fichier texte contenant les prompts pour GPT-4.
- `proxyscrape_premium_http_proxies.txt` : Fichier texte contenant les proxies HTTP.

## Dépendances

Le projet utilise les bibliothèques suivantes :

- `pandas`
- `openai`
- `tabulate`
- `beautifulsoup4`
- `selenium`
- `fake_useragent`
- `tqdm`

Ces dépendances sont spécifiées dans le fichier `requirements.txt`.

## Contribuer

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez ce dépôt.
2. Créez une branche pour votre fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalité`).
3. Commitez vos modifications (`git commit -am 'Ajoute une nouvelle fonctionnalité'`).
4. Poussez la branche (`git push origin feature/nouvelle-fonctionnalité`).
5. Ouvrez une Pull Request.

## Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.
