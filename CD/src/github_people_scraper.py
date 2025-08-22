"""
Web scraper for GitHub organization members
------------------------------------------

This script uses Selenium to navigate the "people" tab of a GitHub organization
and extract three pieces of information for each member listed on the page:

1. ``profile_url`` – the full URL to the member's GitHub profile (e.g. ``https://github.com/username``)
2. ``username`` – the short login handle for the user (e.g. ``username``)
3. ``photo_url`` – the URL of the user's avatar image

The scraper is robust to pagination: you can specify how many pages of results
to collect via the ``num_pages`` parameter.  GitHub organisations often break
their member lists into multiple pages, and this script will iterate through
each page in turn until it has collected the desired number of pages or
encounters a page that contains no member rows.

Usage example::

    from github_people_scraper import scrape_org_members
    results = scrape_org_members("https://github.com/orgs/python/people", num_pages=3)
    for item in results:
        print(item)

The ``results`` variable will be a list of dictionaries, one per member,
containing the keys ``profile_url``, ``username``, and ``photo_url``.

Note: This script requires the ``selenium`` package and a compatible
``chromedriver`` available on your system.  You may need to adjust the
``webdriver.ChromeOptions()`` settings (for example, to run in non-headless
mode) depending on your environment.
"""

from __future__ import annotations

import time
from typing import Dict, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def _setup_driver() -> webdriver.Chrome:
    """Initialize a headless Chrome WebDriver.

    Returns
    -------
    webdriver.Chrome
        A configured Selenium WebDriver instance running Chrome in headless
        mode.  Adjust the options here if you need a visible browser window
        during debugging.
    """
    options = webdriver.ChromeOptions()
    # Run in headless mode so the browser window does not pop up.
    options.add_argument("--headless=new")
    # These options help Selenium run more reliably in containerised
    # environments.
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # Increase window size to ensure all elements are within view.
    options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=options)


def scrape_org_members(org_url: str, num_pages: int = 1) -> List[Dict[str, str]]:
    """Scrape member information from a GitHub organisation's People page.

    Parameters
    ----------
    org_people_url : str
        The URL of the organisation's People tab (e.g. ``https://github.com/orgs/python/people``).
    num_pages : int, optional
        How many pages of results to scrape.  If the organisation has fewer
        pages than requested, the scraper will stop at the last available
        page.  Defaults to 1.

    Returns
    -------
    list of dict
        A list where each element corresponds to a member and contains
        ``profile_url``, ``username``, and ``photo_url`` keys.

    Notes
    -----
    - This function uses Selenium WebDriver.  Ensure you have both the
      ``selenium`` Python package and a compatible ``chromedriver`` installed.
    - GitHub may limit the number of results you can see without being
      authenticated.  If you need to access private member lists, you must
      authenticate with GitHub before scraping, which is beyond the scope of
      this function.
    """
    # Validate ``num_pages`` input
    if num_pages < 1:
        raise ValueError("num_pages must be at least 1")

    # Prepare the WebDriver
    driver = _setup_driver()
    results: List[Dict[str, str]] = []

    try:
        for page in range(1, num_pages + 1):
            # Build the URL for the current page.  GitHub paginates with
            # ``?page=``; if the base URL already contains query parameters
            # simply append ``&page=N`` instead.
            if "?" in org_url:
                page_url = f"{org_url}&page={page}"
            else:
                page_url = f"{org_url}?page={page}"

            driver.get(page_url)

            # Wait until at least one member row is present or timeout after 10
            # seconds.  If no row appears, we assume there are no more pages.
            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "li.member-list-item"))
                )
            except Exception:
                # No members found on this page; exit the loop.
                break

            # Collect all member rows on the current page.
            rows = driver.find_elements(By.CSS_SELECTOR, "li.member-list-item")
            if not rows:
                # If the list is empty, stop pagination early.
                break

            for row in rows:
                # Extract the avatar image URL
                try:
                    img_element = row.find_element(By.CSS_SELECTOR, "img.avatar-user")
                    photo_url = img_element.get_attribute("src")
                except Exception:
                    photo_url = ""

                # Extract the member's profile link from the name element.
                try:
                    name_anchor = row.find_element(By.CSS_SELECTOR, "a.f4.d-block")
                    profile_href = name_anchor.get_attribute("href")
                except Exception:
                    # Fallback: try the avatar link if the name anchor is missing.
                    try:
                        avatar_anchor = row.find_element(By.CSS_SELECTOR, "a.d-inline-block")
                        profile_href = avatar_anchor.get_attribute("href")
                    except Exception:
                        profile_href = ""

                # Extract the username (login handle).  The handle appears inside
                # a span with a colour class.
                try:
                    username_span = row.find_element(By.CSS_SELECTOR, "span.color-fg-default")
                    username = username_span.text.strip()
                except Exception:
                    # Fallback to deriving from the URL path
                    username = profile_href.rstrip("/").split("/")[-1] if profile_href else ""

                # Only append if we have at least a profile URL
                if profile_href:
                    results.append(
                        {
                            "profile_url": profile_href,
                            "username": username,
                            "photo_url": photo_url,
                        }
                    )

            # Polite delay between page requests to avoid hammering GitHub servers
            time.sleep(1)
    finally:
        # Always close the browser session to free resources
        driver.quit()

    return results


if __name__ == "__main__":
    # import argparse
    import json

    org_url = "https://github.com/orgs/python/people"
    output = "output.json"

    data = scrape_org_members(org_url="https://github.com/orgs/python/people", num_pages=1)
    if output:
        with open(output, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        for entry in data:
            print(entry)