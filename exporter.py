from dataclasses import dataclass, field
from getpass import getpass

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException


@dataclass
class Game:
    title: str
    link: str
    pgn: str
    

@dataclass
class Collection:
    title: str
    link: str
    games: list[Game] = field(default_factory=list)


def _safe_find(driver, *args, func: str = "find_elements"):
    WebDriverWait(driver, 20).until(EC.presence_of_element_located(args))
    return getattr(driver, func)(*args)


COLLECTIONS: list[Collection] = []

# Request user info
username = input("Username: ")
password = getpass()

# Init
print("Starting...")
driver = webdriver.Chrome()
driver.get("https://www.chess.com/home")

# Login
print("Logging in...")
username_input = driver.find_element(By.ID, "username")
username_input.send_keys(username)
password_input = driver.find_element(By.ID, "password")
password_input.send_keys(password)
password_input.send_keys(Keys.RETURN)
WebDriverWait(driver, 20).until_not(EC.presence_of_element_located((By.ID, "password")))

# Retrieve all collections metadata 
print("Parsing library...")
driver.get("https://www.chess.com/library")
collections = _safe_find(driver, By.CLASS_NAME, "library-collection-item-component")
print(f"Found {len(collections)} collections")
for collection in collections:
    title = collection.find_element(By.CLASS_NAME, "library-collection-item-link")
    obj = Collection(title=title.text, link=title.get_attribute("href"))
    COLLECTIONS.append(obj)
    print(f"Found collection: '{obj.title}' ({obj.link})")


for collection in COLLECTIONS:
    print(f"Retrieving games from: '{collection.title}' ({collection.link})")
    driver.get(collection.link)
    games = _safe_find(driver, By.CLASS_NAME, "game-item-component")
    for game in games:
        game.click()
        try:
            _title = game.find_element(By.CLASS_NAME, "game-item-title")
            title = _title.text
        except NoSuchElementException as err:
            _usernames = game.find_elements(By.CLASS_NAME, "game-item-username")
            title = ' - '.join(u.text for u in _usernames)
        _more = game.parent.find_element(By.CLASS_NAME, "game-details-more")
        link = _more.find_element(By.CSS_SELECTOR, "a.game-details-btn-component")
        share_button = _more.find_element(By.CSS_SELECTOR, '[aria-label="Share"]')
        share_button.click()
        embed_component = _safe_find(driver, By.CLASS_NAME, "share-menu-tab-embed-component", func="find_element")
        obj = Game(
            title=title,
            link=link.get_attribute("href"),
            pgn=embed_component.get_attribute("pgn")
        )
        collection.games.append(obj)
        close_share_modal = _safe_find(driver, By.CLASS_NAME, "ui_outside-close-component", func="find_element")
        close_share_modal.click()
        game.click()


        
from pprint import pprint
pprint(COLLECTIONS)
driver.close()