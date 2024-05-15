from playwright.sync_api import sync_playwright, Browser, Page, PlaywrightContextManager
import pandas as pd
import os, time
from utils import extract_numeric_value, remove_numeric_values, itemize_instructions

def login(playwright_sync: PlaywrightContextManager, site:str, user_name: str, password: str, headless: bool = True) -> tuple[Browser, Page]:
    p = playwright_sync
    browser: Browser = p.chromium.launch(headless=headless)
    page = browser.new_page()
    
    # Navigate to the login page
    page.goto(site)

    page.wait_for_load_state('networkidle') 

    # Wait for the fields to be loaded
    page.is_visible('button[type="submit"]')
    
    # Fill in login credentials
    page.fill('input[name="email"]', user_name)
    page.fill('input[name="password"]', password)
    
    # Submit the login form
    page.click('button[type="submit"]')

    return browser, page
        

def click_add_recipe(page: Page) -> None:
    page.wait_for_load_state('networkidle') 
    new_recipe_button = page.locator("xpath=//body/div/div[1]/div[1]/div[2]/button")
    new_recipe_button.is_visible()
    new_recipe_button.click()
    

def populate_fields(page: Page, site:str, data: dict, fill_method: str) -> bool:
    page.wait_for_load_state('networkidle') 
    try:
        if fill_method == 'url':
            url_field = page.locator('xpath=//body/div/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/input')
            save_button = page.locator('xpath=//body/div/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/button')

            url_field.is_visible()
            url_field.fill(data['recipe_name'])

            save_button.is_visible()

            page.wait_for_load_state('networkidle')
            save_button.click()

        elif fill_method == 'manual':
            dump = page.locator('xpath=//body/div/div[1]/div[2]/div/div/div[5]/div/div/div/div/input')
            recipe_name_field = page.locator('xpath=//body/div/div[1]/div[2]/div/div/div[1]/div[1]/div[1]/div/div/div/input')
            description_field = page.locator('xpath=//body/div/div[1]/div[2]/div/div/div[1]/div[1]/div[3]/div/div[2]/div/textarea')
            portion_field = page.locator('xpath=//body/div/div[1]/div[2]/div/div/div[1]/div[1]/div[4]/div/div/div/div')
            portion_field_input = page.locator('xpath=//body/div/div[1]/div[2]/div/div/div[1]/div[1]/div[4]/div/div/div/input')
            ingredient_field = page.locator('xpath=//body/div/div[1]/div[2]/div/div/div[2]/div/div/div/textarea')
            method_field = page.locator('xpath=//body/div/div[1]/div[2]/div/div/div[3]/div/div/div[2]')
            save_ingredient_button = page.locator('xpath=//body/div/div[1]/div[2]/div/div/div[2]/div/div/button')

            # Populate recipe name
            recipe_name_field.is_visible()
            recipe_name_field.wait_for()
            recipe_name_field.fill(str(data['recipe_name']))

            # Populate portion
            portion_field.is_visible()
            portion_field.click()
            portion_field_input = page.locator('#RecipePortions') 
            portion_field_input.fill(str(int(data['portion'])))

            # Populate description
            description_field.is_visible()
            description_field.fill(data['description'])

            # Populate method
            method_field.is_visible()
            method_field.fill(str(itemize_instructions(data['method'])))

            # Populate ingredient
            ingredient_field.is_visible()
            ingredient_field.fill(parse_ingredient(data['ingredients']))

            # Save via ingredient save button
            page.wait_for_load_state('networkidle') 
            save_ingredient_button.is_visible()
            save_ingredient_button.click()

            return True
    except Exception as e:
        return False




def parse_ingredient(ingredients: str) -> str:
    ingredients = ingredients.split('\n')
    ingredients = [i for i in ingredients if i != '']
    ingredient_template = '{qty} {text}'
    out_ingredients = []
    for ingredient in ingredients:
        ingredient = f'0 {ingredient}'
        qty = str(round(extract_numeric_value(ingredient), 2))
        text = remove_numeric_values(ingredient)
        out_ingredients.append(ingredient_template.format(qty=qty, text=text))

    return '\n'.join(out_ingredients)




def close_browser(browser: Browser) -> None:
    # Close the browser
    browser.close()


if __name__ == '__main__':
    site:str = 'https://staging.menuwise.com/'
    site_user_name: str = os.environ.get('SITE_USER_NAME')
    site_password: str = os.environ.get('SITE_PASSWORD')
    data: list[dict] = pd.read_excel('recipes.xlsx').to_dict(orient='records')

    with sync_playwright() as p:
        (browser, page) = login(p, site, site_user_name, site_password, False)
        for n, i in enumerate(data):
            click_add_recipe(page)
            if i['status'] == 0:
                success = populate_fields(page, site, i, i['fill_method'])

                if success:
                    data[n]['status'] = 1
        time.sleep(5)
        close_browser(browser)

    # TODO update excel file so that the status of all the processed records have a value of 1
