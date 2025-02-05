# Scraper Siedco

Scraper Siedco is a Python-based web scraping project that automates the extraction of data from the Siedco portal using Selenium and other Python libraries. This project is managed with [Poetry](https://python-poetry.org/) for dependency management. You can find the repository at [https://github.com/JulianDPastrana/scraper-siedco.git](https://github.com/JulianDPastrana/scraper-siedco.git).

## Installation

This project uses Poetry to manage dependencies. To install the project dependencies, follow these steps:

1. Clone the repository:

       git clone https://github.com/JulianDPastrana/scraper-siedco.git
       cd scraper-siedco

2. Install the dependencies using Poetry:

       poetry install

3. (Optional) Activate the Poetry-managed virtual environment:

       poetry shell

## Usage

To run the scraper manually from the command line, execute the following command:

       poetry run python scraper_siedco/scraper.py

This command uses Poetry to run the scraper script located in the scraper_siedco directory, which performs the web scraping tasks.

## Scheduling Daily Execution with Cron (Bash)

You can automate the daily execution of the scraper using a cron job. To schedule the scraper to run every day at 2:00 AM, follow these steps:

1. Open your crontab editor:

       crontab -e

2. Add the following line to schedule the job (replace /path/to/your/project with the absolute path to your repository):

       0 2 * * * cd /path/to/your/project && poetry run python scraper_siedco/scraper.py >> scraper.log 2>&1

Explanation:
- "0 2 * * *" schedules the job to run at 2:00 AM every day.
- "cd /path/to/your/project" changes the working directory to your project root.
- "poetry run python scraper_siedco/scraper.py" runs the scraper using the Poetry-managed virtual environment.
- ">> scraper.log 2>&1" redirects both standard output and error messages to a file named scraper.log for troubleshooting.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with improvements or bug fixes.
