import time

from dataclasses import dataclass, field

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


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


def _safe_find(driver, *args, method: str = "find_elements", timeout: int = 20):
    WebDriverWait(driver, timeout).until(EC.presence_of_element_located(args))
    return getattr(driver, method)(*args)


def find_game_title(game: WebElement):
    try:
        _title = game.find_element(By.CLASS_NAME, "game-item-title")
        title = _title.text
    except NoSuchElementException as err:
        _usernames = game.find_elements(By.CLASS_NAME, "game-item-username")
        title = ' - '.join(u.text for u in _usernames)
    return title


def find_game_pgn(driver: WebDriver, game_details_box: WebElement):
    share_button = game_details_box.find_element(By.CSS_SELECTOR, '[aria-label="Share"]')
    share_button.click()
    embed_component = _safe_find(driver, By.CLASS_NAME, "share-menu-tab-embed-component", method="find_element")
    pgn = embed_component.get_attribute("pgn")
    close_share_modal = _safe_find(driver, By.CLASS_NAME, "ui_outside-close-component", method="find_element")
    close_share_modal.click()
    return pgn


def load_games_from_page(driver: WebDriver, games: list[WebElement]) -> list[Game]:
    game_objects = []
    for game in games:
        game.click()   # Expands _game_details_box
        _game_details_box = game.parent.find_element(By.CLASS_NAME, "game-details-more")
        link = _game_details_box.find_element(By.CSS_SELECTOR, "a.game-details-btn-component")
        obj = Game(
            title=find_game_title(game),
            link=link.get_attribute("href"),
            pgn=find_game_pgn(driver, _game_details_box)
        )
        game_objects.append(obj)
        game.click()  # Closes _game_details_box
    return game_objects


def get_next_page_button(driver) -> None | WebElement:
    try:
        _next_page_button = driver.find_element(By.CSS_SELECTOR,'.ui_pagination-item-component[aria-label="Next Page"]')
        if not _next_page_button.get_attribute("disabled"):
            return _next_page_button
    except NoSuchElementException:
        return None


class Scrapper:
    def __init__(self):
        self.driver: WebDriver = webdriver.Chrome()
        self.collections: list[Collection] = []

    def scrape(self, username: str, password: str):
        self._login(username, password)
        self._retrieve_collections_lazy()
        self._populate_games_into_collections()
        self._end()
        
    def _login(self, username, password):
        self.driver.get("https://www.chess.com/home")
        username_input = self.driver.find_element(By.ID, "username")
        username_input.send_keys(username)
        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.RETURN)
        WebDriverWait(self.driver, 20).until_not(EC.presence_of_element_located((By.ID, "password")))
        
    def _retrieve_collections_lazy(self):
        self.driver.get("https://www.chess.com/library")
        self._retrieve_collections_in_page()
        next_page_button = get_next_page_button(self.driver)
        while next_page_button:
            next_page_button.click()
            time.sleep(1)   # FIXME: Instead of sleeping an arbitrary ammount, some kind of check
                            # should be performed on the UI. (maybe tracking the current page and checking
                            # the specific page selector styling)
            self._retrieve_collections_in_page()
            next_page_button = get_next_page_button(self.driver)
            
    def _retrieve_collections_in_page(self):
        collections = _safe_find(self.driver, By.CLASS_NAME, "library-collection-item-component")
        for collection in collections:
            title = collection.find_element(By.CLASS_NAME, "library-collection-item-link")
            obj = Collection(title=title.text, link=title.get_attribute("href"))
            self.collections.append(obj)
            print(f"Found collection: '{obj.title}' ({obj.link})")
                            
    def _populate_games_into_collections(self):
        for collection in self.collections:
            print(f"Retrieving games from: '{collection.title}' ({collection.link})")
            self.driver.get(collection.link)
            self._populate_page_into_collection(collection)
            next_page_button = get_next_page_button(self.driver)
            while next_page_button:
                next_page_button.click()
                time.sleep(1)  # FIXME: Instead of sleeping an arbitrary ammount, some kind of check
                               # should be performed on the UI. (maybe tracking the current page and checking
                               # the specific page selector styling)
                self._populate_page_into_collection(collection)
                next_page_button = get_next_page_button(self.driver)
                
    def _populate_page_into_collection(self, collection):
        try:
            self.driver.find_element(By.CLASS_NAME, "collection-games-wrapper-no-games")
            return
        except NoSuchElementException:
            games = _safe_find(self.driver, By.CLASS_NAME, "game-item-component")
            game_objects = load_games_from_page(self.driver, games)
            collection.games.extend(game_objects)
        
    def _end(self):
        self.driver.close()
        
    
if __name__ == "__main__":
    from getpass import getpass
    from pprint import pprint
    
    username = input("Username: ")
    password = getpass()
    scrapper = Scrapper()
    scrapper.scrape(username, password)
    pprint(scrapper.collections)


        