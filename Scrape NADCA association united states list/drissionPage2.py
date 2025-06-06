# 导入
from datetime import datetime

from DrissionPage import Chromium, ChromiumOptions
from DrissionPage._elements.none_element import NoneElement

from csvUtils import append_dicts_to_csv
from markdownify import markdownify as md

fieldnames = ["source_link", "country", "company_name","location","company_information",
              "telephone","fax","email", "website","company_profile","capabilities_description",
               "post_casting"]
filename = "Scrape NADCA association united states list.csv"
#获取当前时间戳
# dt_obj = datetime.now()
# dt_str = dt_obj.strftime('%Y%m%d%H%M%S')
# # filename是完整文件名字符串，我想要的是文件名 + 时间戳的形式
# filename = filename.split('.')[0] + '_' + dt_str + '.csv'

# 第一批数据
data_batch1 = []
co = ChromiumOptions()
co.incognito()  # 匿名模式
co.headless()  # 无头模式
co.set_argument('--no-sandbox')  # 无沙盒模式
# 设置不加载图片、静音
co.no_imgs(True).mute(True)
# 连接浏览器
browser = Chromium(addr_or_opts = co)
# 获取标签页对象
tab = browser.latest_tab

url = "https://www.diecasting.org/web/Directories/Find_a_Die_Caster/Web/Resources/Directories/CompanySearch.aspx"
# 访问网页
tab.get(url)

import time
import random

tab.ele("x:(//label[text()='Country:']/following::input)[1]").click(by_js=True)

tab.wait.eles_loaded("x://ul[@class='rcbList']/li[226]")


country_name_list = tab.eles("x://ul[@class='rcbList']/li")

start = 233
for i, country_name in enumerate(country_name_list[start:300]):
    if i != 0:
        tab.ele("x:(//label[text()='Country:']/following::input)[1]").click(by_js=True)
        tab.wait.eles_loaded(f"x://ul[@class='rcbList']/li[{i+1}]", timeout=20)
    i = i+ start
    # 获取国家名称
    country = country_name.text.strip()
    # 打印当前循环的数字
    print(f'正在处理第{i + 1}个国家：{country}')

    tab.ele(f"x://ul[@class='rcbList']/li[{i+1}]", timeout=20).click()
    time.sleep(1)
    tab.ele("x://input[@value='Search']").click(by_js=True)
    tab.wait.eles_loaded("x://tbody/tr[1]/td[2]",timeout=5)



    # 获取文本框元素对象
    lists = tab.eles("x://tbody/tr", timeout=0)
    if lists and len(lists) == 1:
        first_text = tab.ele("x://tbody/tr[1]//div", timeout=0)
        if not isinstance(first_text, NoneElement):
            if "No records to display." == first_text.text:
                print(f'没有数据，跳过国家：{country}')
                continue

    data = None
    index = 0
    for index, row in enumerate(lists):
        data = {}
        data.update({"source_link": "https://www.diecasting.org/web/Directories/Find_a_Die_Caster/Web/Resources/Directories/CompanySearch.aspx"})
        secs = random.uniform(0, 1)
        time.sleep(secs)
        print(f'正在处理第{i + 1}个国家：{country},第{index + 1}条数据开始爬取...')
        # 打印文本框的文本内容
        # 点击文本框
        a = row.ele("x://a", timeout=0)
        if isinstance(a,NoneElement):
            row.ele("x:/td[1]", timeout=0)
            company_name = row.ele("x:/td[1]", timeout=0)
            location = row.ele("x:/td[2]", timeout=0)
            data.update({"country": country})
            data.update({"company_name": company_name.text.strip()})
            data.update({"location": location.text.strip()})
        else :
            company_name = row.ele("x:/td[1]", timeout=0)
            location = row.ele("x:/td[2]", timeout=0)
            data.update({"country": country})
            data.update({"company_name": company_name.text.strip()})
            data.update({"location": location.text.strip()})

            # 获取新标签页对象
            tab2 = a.click.middle()  # 点击文本框
            tab2.set.activate()
            tab2.wait.load_start(timeout=20)
            company_information = tab2.ele("x:(//div[@class='panel ']//div)[1]/following-sibling::div", timeout=0)
            if isinstance(company_information, NoneElement):
                data.update({"company_information": ""})
            else:
                # 将 HTML 转换为 Markdown，并过滤掉空行
                raw_md = md(company_information.html, strip=['img'])
                company_information = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"company_information": company_information})
            telephone = tab2.ele("x://span[text()='Telephone:']/following-sibling::span", timeout=0)
            if isinstance(telephone, NoneElement):
                data.update({"telephone": ""})
            else:
                # 将 HTML 转换为 Markdown，并过滤掉空行
                raw_md = md(telephone.html, strip=['img'])
                telephone = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"telephone": telephone})
            fax = tab2.ele("x://span[text()='Fax:']/following-sibling::span", timeout=0)
            if isinstance(fax, NoneElement):
                data.update({"fax": ""})
            else:
                # 将 HTML 转换为 Markdown，并过滤掉空行
                raw_md = md(fax.html, strip=['img'])
                fax = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"fax": fax})
            email = tab2.ele("x://span[text()='Email:']/following-sibling::span", timeout=0)
            if isinstance(email, NoneElement):
                data.update({"email": ""})
            else:
                email = email.ele("x://a", timeout=0)
                data.update({"email": email.text.strip()})
            website = tab2.ele("x://span[text()='Website:']/following-sibling::span", timeout=0)
            if isinstance(website, NoneElement):
                data.update({"website": ""})
            else:
                website = website.ele("x://a", timeout=0)
                data.update({"website": website.text.strip()})
            company_profile = tab2.ele("x://h2[normalize-space()='Company Profile']/parent::div/following-sibling::div", timeout=0)
            if isinstance(company_profile, NoneElement):
                data.update({"company_profile": ""})
            else:
                # 将 HTML 转换为 Markdown，并过滤掉空行
                raw_md = md(company_profile.html, strip=['img'])
                company_profile = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"company_profile": company_profile})
            capabilities_description = tab2.ele("x://h2[normalize-space()='Capabilities Description']/parent::div/following-sibling::div",
                                       timeout=0)
            if isinstance(capabilities_description, NoneElement):
                data.update({"capabilities_description": ""})
            else:
                # 将 HTML 转换为 Markdown，并过滤掉空行
                raw_md = md(capabilities_description.html, strip=['img'])
                capabilities_description = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"capabilities_description": capabilities_description})
            # //h2[normalize-space()='Post Casting']/parent::div/following-sibling::div
            post_casting = tab2.ele(
                "x://h2[normalize-space()='Post Casting']/parent::div/following-sibling::div",
                timeout=0)
            if isinstance(post_casting, NoneElement):
                data.update({"post_casting": ""})
            else:
                # 将 HTML 转换为 Markdown，并过滤掉空行
                raw_md = md(post_casting.html, strip=['img'])
                post_casting = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"post_casting": post_casting})
            print("data:", data)
            tab2.close()
            tab.set.activate()
        data_batch1.append(data)
    # data
    print(f'第{i + 1}个国家：{country}写入数据到 CSV 文件...')
    append_dicts_to_csv(data_batch1, fieldnames, filename)
    print(f'第{i + 1}个国家：{country}写入CSV文件成功！继续下一批次数据...')
    data_batch1= []  # 清空数据批次，准备下一页的数据
# print('写入CSV 文件成功！已完成所有数据的爬取。')
# browser.quit()



