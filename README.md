
# Company Information Scraper and GPT-4o Text Generator

This script scrapes company information from a provided URL list, processes the data, and generates text using OpenAI's GPT-4o model. It leverages several libraries for web scraping, data manipulation, and concurrent processing to efficiently handle large datasets.

## Prerequisites

Ensure you have the following installed:

- Python 3.7+
- ChromeDriver
- Required Python packages (listed below)

## Installation

1. Clone the repository or download the script files.

2. Install the required packages using pip:

   ```bash
   pip install time random json pandas psutil openai tabulate beautifulsoup4 selenium fake-useragent tqdm python-dotenv
   ```

3. Ensure ChromeDriver is installed and available in your PATH. You can download it from [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads).

4. Create a `.env` file in the root directory and add your OpenAI API key and proxies file path:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   PROXY_FILE_PATH=path_to_your_proxies_file.txt
   ```

## Usage

1. Prepare your input files:
   - A CSV file with company information (`liste-entreprises.csv`).
   - A text file with GPT-4o prompts (`prompts.txt`).
   - A text file with proxy addresses (`proxies.txt`).

2. Adjust the paths in the script accordingly:
   
   ```python
   company_csv_path = '/path/to/your/liste-entreprises.csv'
   prompts_file_path = '/path/to/your/prompts.txt'
   proxies_file_path = os.getenv('PROXY_FILE_PATH')
   output_json_path = '/path/to/your/company_info.json'
   ```

3. Run the script:

   ```bash
   python your_script.py
   ```

4. The script will generate a JSON file (`company_info.json`) with the processed company information and the generated text.

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key.
- `PROXY_FILE_PATH`: Path to your proxies file.

### Script Parameters

- `mode_test` (boolean): Set to `True` to process a sample of 15 companies for testing.

## Functions

### `load_company_info(csv_path)`

Loads company information from a CSV file and returns a list of dictionaries.

### `generate_text(prompt)`

Generates text using the GPT-4o model with the provided prompt.

### `load_prompts(prompts_file_path)`

Loads prompts from a text file.

### `load_proxies(proxies_file_path)`

Loads proxy addresses from a text file.

### `extract_intro_text(page_source)`

Extracts introductory text from a web page.

### `get_random_user_agent()`

Returns a random user agent string.

### `get_driver(proxies)`

Configures and returns a Selenium WebDriver with a proxy and a random user agent.

### `scrape_page(url, proxies)`

Scrapes the given URL using Selenium and returns the page source.

### `process_company(company, prompts, proxies)`

Processes a single company's information and generates text using GPT-4o.

### `adjust_workers()`

Dynamically adjusts the number of workers based on CPU and memory usage.

### `main(mode_test=False)`

Main function to load data, process companies, and save the results.

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss your ideas.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.# companies_presentation
