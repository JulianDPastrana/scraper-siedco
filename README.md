Project Overview
Scraper Siedco is a Python-based web scraper designed to extract data from the Siedco portal using Selenium. The project is structured with its main functionality in the scraper_siedco/scraper.py module, and it is managed with Poetry for dependency management and packaging.

Installation Instructions using Poetry
1. Ensure that you have Python 3.10 or later installed.
2. Install Poetry by following the instructions at https://python-poetry.org/docs/#installation.
3. Clone the repository:
   git clone https://your.repo.url/ScraperSiedco.git
   cd ScraperSiedco
4. Install the project dependencies by running:
   poetry install
5. (Optional) Activate the virtual environment with:
   poetry shell

Usage
To run the scraper manually from the command line, use the following command:
   poetry run python scraper_siedco/scraper.py
This command launches the main scraper script, which navigates the Siedco website, extracts the required data, and processes it according to the project’s logic.

Daily Automation (Bash)
To schedule the scraper to run once a day, you can use a cron job. Here is how to set it up:
1. Open your crontab editor by running:
   crontab -e
2. Add the following line to schedule the scraper to run daily at 2:00 AM (replace /path/to/your/ScraperSiedco with the absolute path to your project directory):
   0 2 * * * cd /path/to/your/ScraperSiedco && poetry run python scraper_siedco/scraper.py >> scraper.log 2>&1
Explanation:
- "0 2 * * *" schedules the job to run at 2:00 AM every day.
- "cd /path/to/your/ScraperSiedco" changes the working directory to your project folder.
- "poetry run python scraper_siedco/scraper.py" executes the scraper script using Poetry.
- ">> scraper.log 2>&1" redirects both standard output and error messages to a file named scraper.log for troubleshooting.
