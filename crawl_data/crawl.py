from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import json

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options, executable_path="chromedriver")

def format_num(num):
  num = str(num)
  if len(num) < 2:
    return "0" + num
  return num

stock = [["VNINDEX", 202], ["VN30INDEX", 135] ]
data = []

# for page in range (2, 134)
for st in range(2):
  driver.get(f"https://s.cafef.vn/Lich-su-giao-dich-{stock[st][0]}-1.chn")
  time.sleep(2)
  for page in range (2, stock[st][1]):
    for i in range (1, 21):
      row_num = format_num(i)
      if(i%2 == 0):
        row_num += "_altitemTR"
      else:
        row_num += "_itemTR"
      els = driver.find_element('id', f'ctl00_ContentPlaceHolder1_ctl03_rptData2_ctl{row_num}')
      row_data = {}
      row_data["date"] = els.find_element("class name", "Item_DateItem").text
      price_index = els.find_elements("class name", "Item_Price10")
      row_data["open"] = price_index[4].text
      row_data["high"] = price_index[5].text
      row_data["low"] = price_index[6].text
      row_data["close"] = price_index[0].text
      row_data["volume"] = price_index[1].text
      row_data["value"] = price_index[2].text
      data.append(row_data)
      time.sleep(1)
    print(f" Next to Page {page}")
    els = driver.find_element('xpath', f'//a[@title=" Next to Page {page}"]')
    time.sleep(1)
    els.click()
    time.sleep(1)
    if (page - 1) % 40 == 0:
      print(len(data))
      data_string = json.dumps(data, sort_keys=True, indent=4) 
      myjsonfile = open(f"vn30_index{page - 1}.json", "w")
      myjsonfile.write(data_string)
      myjsonfile.close()

print(len(data))
data_string = json.dumps(data, sort_keys=True, indent=4) 
myjsonfile = open("vn30_index.json", "w")
myjsonfile.write(data_string)
myjsonfile.close()

