from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime

app = Flask(__name__)

month = datetime.today().strftime('%m')

options = webdriver.FirefoxOptions()
options.add_argument('-headless')
dr = webdriver.Firefox(options=options)
dr.implicitly_wait(5)

url = "https://consumer.scheduling.athena.io/?locationId=21276-1&practitionerId=21276-1"

dr.get(url)

dropdown = Select(dr.find_element(By.NAME, "visitReason"))
dropdown.select_by_visible_text("Annual Physical")

current_month = dr.find_elements(By.CLASS_NAME, "src-consumer-portal-workflow-filters-calendar-calendar-module__is-available--pz8Db")
dates_this_month = []
for x in current_month:
    date = x.get_attribute('data-date')
    if date[5:7] == month:
        dates_this_month.append(date)

next_button = dr.find_element(By.CSS_SELECTOR, "[aria-label='Next Month']")
next_button.click()

next_month = dr.find_elements(By.CLASS_NAME, "src-consumer-portal-workflow-filters-calendar-calendar-module__is-available--pz8Db")
dates_next_month = []
for x in next_month:
    date = x.get_attribute('data-date')
    if int(date[5:7]) == int(month)+1:
        dates_next_month.append(date)

dr.close()

@app.route("/")
def main():
    return render_template("index.html", current_month=dates_this_month, next_month=dates_next_month)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)