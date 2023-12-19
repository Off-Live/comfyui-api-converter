from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
import json


def convert_to_api(json_obj, url):
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--ignore-ssl-errors=yes")
    chrome_options.add_argument("--ignore-certificate-errors")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    wait = WebDriverWait(driver, 10)
    wait.until(lambda web_driver: web_driver.execute_script("return typeof app !== 'undefined' && app !==null"))

    wf_string = json.dumps(json_obj)
    driver.execute_script(f'app.loadGraphData({wf_string})')

    res = driver.execute_async_script(
        """
        var callback = arguments[arguments.length - 1];
        app.graphToPrompt().then( (result)=> callback(result));
        """
    )
    driver.quit()

    return res['output']
