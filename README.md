# Indeed scraper & Data extraction from description using NLP

## Overview
This project is a web scraping tool designed to extract Specific data from job vacancy leads from the Indeed UK for Private Client Solicitor vacancies and extract data such as Name, Surname and email from the description using the NER NLP technique. Utilizing a blend of powerful web scraping libraries such as Selenium, Requests, BeautifulSoup, and Spacy this tools delivers accurate and efficient data extraction for specific regions.

## Features
- **scrap_indeed**: Efficiently scrapes data depending on the specified elements from the job posts in the indeed platform.
- **description_data_extraction.py**: Take the scraped job description Text data and extracts the Name, Surname, Email, and PQE if found, if not found it stays as None.

## Technologies
- **Selenium**: Automates web browsers, providing the backbone for real-time data scraping and interaction.
- **Requests**: Handles HTTP requests, allowing efficient data retrieval.
- **BeautifulSoup**: Parses HTML and XML documents, making it easier to navigate and search the parse tree.
- **Spacy**: Helps me extract the wanted information from the description text

## Getting Started
To use this scraper, you'll need to have Python installed on your machine along with the Selenium, Requests, and BeautifulSoup libraries. Detailed instructions on setting up the environment and running the scraper are provided below.

### Prerequisites
- Python 3.x
- webdriver-manager
- requests
- beautifulsoup4
- pandas
- selenium
- spacy
- openpyxl

### Installation
1. Clone the repository to your local machine.
2. Install the necessary libraries using `pip install -r requirements.txt`.
3. Set up your web driver for Selenium (e.g., ChromeDriver for Google Chrome).

## Contribution
Contributions to this project are welcome. Please ensure that your code adheres to the project's coding standards and include appropriate tests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.