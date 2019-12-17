import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

data = {"社会组织名称": "", "统一社会信用代码": "", "社会组织类型": "", "法定代表人": "", "成立登记日期": "", "状态": ""}
data_list = []

url = "http://bmfw.www.gov.cn/qgshzzcx/index.html#zyf"
option = webdriver.ChromeOptions()
# 不加载图片,css
prefs = {'profile.default_content_setting_values': {'images': 2, 'stylesheet': 2}}
option.add_experimental_option('prefs', prefs)

desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

BROWSER = webdriver.Chrome(options=option)

BROWSER.get(url)
BROWSER.implicitly_wait(1)

pages = int(BROWSER.find_element_by_id("sumpage").text.replace('共', '').replace('页', ''))
print(pages)

index = BROWSER.find_element_by_id("wxx")

for num in range(0, 5):
    for i in range(1, 10):
        data["社会组织名称"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[1].text
        data["统一社会信用代码"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[2].text
        data["社会组织类型"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[3].text
        data["法定代表人"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[4].text
        data["成立登记日期"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[5].text
        data["状态"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[6].text
        print(data)

        a_info = BROWSER.find_element_by_id('pagination3').find_elements_by_name('a')[4 + num].click()

    BROWSER.implicitly_wait(0.5)


BROWSER.close()
BROWSER.quit()





