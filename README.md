# trakt
Generate csv files from my trakt lists, to import to Notion

## Actresses
Export a list with people

TODO
- [ ] Move configs to json so I can commit it
- [ ] Option to update/insert directly to notion

## lists
Export a list with movie and shows

TODO
- [ ] Move configs to json so I can commit it
- [ ] Option to update/insert directly to notion

## migrate_list
Migrate Watchlist or Finished to a new list, as PyTrakt don't return all information for those trakt lists.

# Reddit
Export saved posts to json. Has commented code to unsave

# Goodreads
For a json exported from the site (csv converted to json), add cover URLs and save to csv so it can be imported into notion.

Todo:
- [ ] Move configs to json so I can commit it
- [ ] Option to update/insert directly to notion

# Notion

NOTE: consider using https://github.com/ramnes/notion-sdk-py in the future

Not commited yet:

## notion_to_blog

Load books from notion and export to markdown file so it can be used on my hugo blog.

TODO:
- [ ] Move configs to json so I can commit it
- [ ] Move configs to json so I can commit it


# Twitter
From https://github.com/jarulsamy/twitter-bookmark-downloader.

### Setup

This software is only compatible with **Python 3.6+**.

Install the required dependencies using the `requirements.txt` file.

    pip install -r requirements.txt

> **Selenium** is required for this application when running with python. Please install selenium and the **Firefox Gecko Webdriver**. Add it to your platform specific PATH based on the [Selenium Documentation](https://selenium-python.readthedocs.io/index.html).

### Run

Run `main.py` to start. Enter your username, password, and if enabled, 2fa code when prompted.

Optionally, use the command line arguments:

    usage: main.py [-h][-d DOWNLOAD_DIR] [-u USERNAME][-p PASSWORD] [--headless]

    optional arguments:
      -h, --help            show this help message and exit
      -d DOWNLOAD_DIR, --download_dir DOWNLOAD_DIR
                            Output folder of downloads
      -u USERNAME, --username USERNAME
                            Specify user as argument to circumvent prompt
      -p PASSWORD, --password PASSWORD
                            Specify password as argument
      --headless            Run without user input and firefox window display.