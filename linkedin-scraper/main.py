from time import sleep

from linkedin_scraper import actions
from selenium import webdriver

from lib.clean_html import get_headline
from lib.g_excel import create_sheet
from lib.prompts import location, password, position, username

# The ID Spreadsheet
# Initialize chrome driver
PATH = './chromedriver'
driver = webdriver.Chrome(PATH)

# General Website to scrape
WEBSITE = "https://www.linkedin.com/"

actions.login(driver, username, password)


def pull_linkedin():
    main_url = f"https://duckduckgo.com/?q=site%3Alinkedin.com%2Fin%2F+AND+%22{position}%22+AND+%22{location}%22&atb=v295-2__&ia=web"
    driver.get(
        main_url
    )

    linkedin_urls = driver.find_elements_by_class_name('result__url')
    linkedin_urls = [url.text for url in linkedin_urls]

    sleep(4)
    for i, value in enumerate(linkedin_urls):
        url = value.replace('› in ›', '/in/').replace(' ', '')
        driver.get(url)
        j = i
        sleep(6)
        check_profile_null = get_headline(driver.page_source)

        if check_profile_null is not None:
            append_sheet2 = create_sheet(j, driver.page_source)
            print("Success Person----", append_sheet2)

        if check_profile_null is None:
            driver.get("https://www.google.com")
            driver.get(url)
            i += 1
            sleep(2)
            create_sheet(j, driver.page_source)
            print("Success Back Person [Saved]----", append_sheet2)


if __name__ == '__main__':
    pull_linkedin()
