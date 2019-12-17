from selenium import webdriver
import pymysql
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# 数据存储
def process_insert(db, cursor, data):
    # 向数据库插入获取的数据
    try:
        # 插入json数据
        sql = "insert into qgshzzcx(organization_name,credit_code,organizations_type,legal_person" \
               ",establishment_date,state) values ('%s','%s','%s','%s','%s','%s')" % (data["社会组织名称"],
                data["统一社会信用代码"], data["社会组织类型"], data["法定代表人"], data["成立登记日期"], data["状态"])
        # print(sql)
        # sql = "insert into qgshzzcx(organization_name,credit_code,organizations_type,legal_person" \
        #        ",establishment_date,state) values ('%%s','%%s','%%s','%%s','%s','%%s')"
        # cursor.executemany(sql, data)
        cursor.execute(sql)
        # 提交到数据库
        db.commit()
    except LookupError:
        # 如果发生错误则回滚
        db.rollback()

# 获取数据
def data_get(browser, db, cursor):

    data = {"社会组织名称": "", "统一社会信用代码": "", "社会组织类型": "", "法定代表人": "", "成立登记日期": "", "状态": ""}
    datas = ()
    pages = int(browser.find_element_by_id("sumpage").text.replace('共', '').replace('页', ''))
    print(pages)

    index = browser.find_element_by_id("wxx")

    for num in range(1, pages+1):
        for i in range(0, 10):
            data["社会组织名称"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[1].text
            # data1 = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[1].text
            # data_list.append(data1)
            data["统一社会信用代码"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[2].text
            # data2 = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[2].text
            # data_list.append(data2)
            data["社会组织类型"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[3].text
            # data3 = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[3].text
            # data_list.append(data3)
            data["法定代表人"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[4].text
            # data4 = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[4].text
            # data_list.append(data4)
            data["成立登记日期"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[5].text
            # data5 = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[5].text
            # data_list.append(data5)
            data["状态"] = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[6].text
            # data6 = index.find_elements_by_tag_name("li")[i].find_elements_by_tag_name("p")[6].text
            # data_list.append(data6)
            # print(data_list)
            # 获取一条数据存入
            process_insert(db, cursor, data)

        print('第'+str(num)+'页ok')

        # # 清空数据
        # data_list.clear()
        # 点击下一页
        browser.find_element_by_xpath("//*[text()='下一页']").click()
        browser.implicitly_wait(0.5)
    # 关闭驱动
    browser.close()
    browser.quit()
    # 关闭数据库
    cursor.close()
    db.close()

def start_app():
    """程序控制函数"""
    url = "http://bmfw.www.gov.cn/qgshzzcx/index.html#zyf"
    try:
        browser.get(url)
    except Exception:
        print("无法进入搜索页")

    # 数据库连接信息
    host = '192.168.10.198'
    username = 'zyc'
    password = 'zyc147258'
    database = 'zyc'
    port = 3306

    # 连接数据库
    db = pymysql.connect(host=host, user=username, passwd=password, db=database, port=port, charset="utf8")
    cursor = db.cursor()

    # 数据爬取阶段
    data_get(browser, db, cursor)


if __name__ == '__main__':
    option = webdriver.ChromeOptions()
    prefs = {'profile.default_content_setting_values': {'images': 2}}
    option.add_experimental_option('prefs', prefs)
    option.add_argument('--headless')

    # 不加载图片,css
    prefs = {'profile.default_content_setting_values': {'images': 2, 'stylesheet': 2}}
    option.add_experimental_option('prefs', prefs)

    desired_capabilities = DesiredCapabilities.CHROME  # 修改页面加载策略
    desired_capabilities["pageLoadStrategy"] = "none"  # 注释这两行会导致最后输出结果的延迟，即等待页面加载完成再输出

    browser = webdriver.Chrome(options=option)
    start_app()

