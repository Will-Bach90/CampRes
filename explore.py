## https://washington.goingtocamp.com/create-booking/results?resourceLocationId=-2147483624&mapId=-2147483388&searchTabGroupId=0&bookingCategoryId=0

import re
from playwright.sync_api import Playwright, sync_playwright, expect
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
import time
from time import perf_counter

MONTH = "May"

START_DATE = MONTH + " 28,"
END_DATE = MONTH + " 31,"

LOOP = "Site Lower Loop A"

CAMP_SITE = 86

USE_BACKUP = True
BACKUP_SITE = 88

OPEN_YEAR = 2026
OPEN_MONTH = 8
OPEN_DAY = 28
OPEN_HOUR = 7          # military time
OPEN_MINUTE = 0
OPEN_SECOND = 0

target = datetime(
    OPEN_YEAR, 
    OPEN_MONTH, 
    OPEN_DAY, 
    OPEN_HOUR, 
    OPEN_MINUTE, 
    OPEN_SECOND,
    tzinfo=ZoneInfo("America/Los_Angeles")
)

def format_clock_time(dt):
    hour = dt.hour % 12
    if hour == 0:
        hour = 12

    return f"{hour}:{dt.minute:02d}:{dt.second:02d} {'AM' if dt.hour < 12 else 'PM'}"

def print_sys_time(page):
    clock = page.locator("#systemTime > div").first
    park_str = clock.inner_text().strip()
    park_time = datetime.strptime(
        park_str,
        "%I:%M:%S %p"
    ).replace(
        year=target.year,
        month=target.month,
        day=target.day,
        tzinfo=target.tzinfo
    )

    print(f"Park time:       {park_time}")

def wait_for_park_time(page, target):
    page.get_by_label("Check parks local time").click()

    clock = page.locator("#systemTime > div").first

    current_str = clock.inner_text().strip()

    current_time = datetime.strptime(
        current_str,
        "%I:%M:%S %p"
    ).replace(
        year=target.year,
        month=target.month,
        day=target.day,
        tzinfo=target.tzinfo
    )

    next_time = current_time + timedelta(seconds=1)
    next_time_str = next_time.strftime("%I:%M:%S %p").lstrip("0")

    print(f"Park clock: {current_str}")
    print(f"Synchronizing on: {next_time_str}")

    # Wait for the exact next second using the mechanism
    page.wait_for_function(
        """target => {
            const el = document.querySelector("#systemTime > div");
            return el && el.textContent.trim() === target;
        }""",
        arg=next_time_str,
        timeout=5000
    )

    # Synchronization point.
    transition_perf = perf_counter()

    # Calculate target relative to the observed park-clock second.
    remaining = (target - next_time).total_seconds()

    if remaining < 0:
        raise ValueError("Target time has already passed.")

    target_perf = transition_perf + remaining

    print(f"Target in {remaining:.3f} seconds")

    # Coarse sleep until close to target.
    while True:
        remaining_local = target_perf - perf_counter()

        if remaining_local <= 0.050:
            break

        time.sleep(min(remaining_local - 0.025, 0.25))

    # Final ~50 ms: don't sleep, just wait.
    while perf_counter() < target_perf:
        pass

    print("TARGET REACHED")

def load_more_sites(page):
    load_more = page.locator("#loadMoreButton")

    for i in range(2):
        start = perf_counter()

        load_more.wait_for(state="visible")
        load_more.click()

def reserve_site(page, site_number):
    site = page.get_by_label(f"Site {site_number}", exact=True)
    site.click()

    panel = site.locator("xpath=..")

    reserve = panel.locator('[id^="reserveButton-"]')
    reserve.wait_for(state="visible")

    reserve.click()

    print(f"Site {site_number}:")
    

def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://washington.goingtocamp.com/")
    page.locator(".mat-mdc-select-arrow > svg > path").first.click()
    page.get_by_role("option", name="Deception Pass").click()
    page.locator(".svg-inline--fa.fa-calendar-days > path").click()
    page.get_by_role("button", name="August 2026, Select to change").click()
    page.get_by_role("button", name="View next year, September").click()
    page.get_by_role("button", name=MONTH).click()
    page.get_by_role("button", name=START_DATE).click()
    page.get_by_role("button", name=END_DATE).click()
    page.get_by_label("Party Size").click()
    page.get_by_label("Party Size").fill("8")
    page.locator("div:nth-child(2) > .mat-mdc-select-arrow > svg > path").click()
    page.get_by_role("option", name="3 Tents").click()
    page.get_by_label("Search for availability").click()
    page.get_by_label("List view of results").click()
    page.get_by_label(LOOP).click()
    page.get_by_label("Show available sites only").uncheck()
    page.locator("#loadMoreButton").click()

    wait_for_park_time(page, target)

    # page.reload(wait_until="commit")

    reserve_site(page, CAMP_SITE)
    page.get_by_role("button", name="Confirm").click()
    page.get_by_label("All reservation details are").check()
    page.locator("#confirmReservationDetails").click()

    if USE_BACKUP:
        page.get_by_label("Make a Reservation (Home)").click()
        page.get_by_label("Search for availability").click()
        page.get_by_label("List view of results").click()
        page.locator("#loadMoreButton").click()

        reserve_site(page, BACKUP_SITE)
        page.get_by_label("All reservation details are").check()
        page.locator("#confirmReservationDetails").click()
  
    page.locator("#proceedToCheckout").click()

    input("Press Enter after you reach the results page...")

    browser.close()

with sync_playwright() as playwright:
    run(playwright)