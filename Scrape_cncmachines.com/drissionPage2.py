# 导入
from datetime import datetime

from DrissionPage import Chromium, ChromiumOptions
from csvUtils import append_dicts_to_csv
from markdownify import markdownify as md



fieldnames = ["source_link", "product_name", "brand","model","year",
              "category","location","machine_overview_specs",
              "machine_overview_options","machine_overview_description"]
filename = "output.csv"
# # 获取当前时间戳
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

# 循环 1到100
for i in range(14, 100):
    import time
    import random
    # secs = random.uniform(0, 1)
    # time.sleep(secs)

    # 打印当前循环的数字
    print(f'第{i}页数据开始爬取...')
    # 替换 URL 中的页码
    source_link = f"https://cncmachines.com/listings?groupId=2&page={i}&current={i}"
    url = source_link
    # 访问网页
    tab.get(url)
    # 获取文本框元素对象
    links = tab.eles("x:(//a[@class='lot-box-link-wrapper'])", timeout=0)
    if links is None or len(links) == 0:
        print(f'第{i}页没有数据，结束！')
        break
    data = None
    index = 0
    for title in links:
        secs = random.uniform(0, 1)
        time.sleep(secs)
        index += 1
        print(f'第{i}页第{index}条数据开始爬取...')
        # 打印文本框的文本内容
        # 点击文本框
        tab2 = title.click.middle()  # 点击文本框
        tab2.set.activate()
        tab2.wait.ele_displayed("x://h1[@class='seller-needs-card__title']")

        product_name = tab2.ele("x://h1[@class='seller-needs-card__title']", timeout=0)


        data = {}
        data.update({"source_link": "https://cncmachines.com/cnc-machine-brands"})

        try:
            product_name = tab2.ele("x://h1[@class='seller-needs-card__title']", timeout=0)
            if product_name is not None:
                data.update({"product_name": product_name.text})
            else:
                data.update({"product_name": ""})
        except Exception as e:
            data.update({"product_name": ""})


        try:
            # 定位到 Vendor 同级的下一个元素
            brand = tab2.ele("x://span[normalize-space()='Brand:']/following-sibling::span/a", timeout=0)
            # 如果没找到元素，就让 clean_md 直接成为空字符串
            if brand is None:
                brand = ""
            else:
                brand = brand.text
            data.update({"brand": brand})
        except Exception as e:  
            data.update({"brand": ""})

        try:
            # //label[@class='l'][normalize-space()='Main Category']/following-sibling::*[1]
            model = tab2.ele("x://span[normalize-space()='Model:']/following-sibling::span", timeout=0)
            if model is not None:
                data.update({"model": model.text})
            else:
                data.update({"model": ""})
        except Exception as e:
            data.update({"model": ""})

        try:
            # //label[normalize-space()='Category']/following-sibling::div
            year = tab2.ele("x://span[normalize-space()='Year:']/following-sibling::span", timeout=0)
            if year is not None:
                data.update({"year": year.text})
            else:
                data.update({"year": ""})
        except Exception as e:
            data.update({"year": ""})

        # //label[normalize-space()='Type of Machine']/following-sibling::div
        try:
            category = tab2.ele("x://span[normalize-space()='Category:']/following-sibling::span", timeout=0)
            if category is not None:
                data.update({"category": category.text})
            else:
                data.update({"category": ""})
        except Exception as e:
            data.update({"category": ""})

        # //label[normalize-space()='Manufacturer']/following-sibling::div
        try:
            location = tab2.ele("x://span[normalize-space()='Location:']/following-sibling::span", timeout=0)
            if location is not None:
                # 将 HTML 转换为 Markdown，并过滤掉空行
                raw_md = md(location.html, strip=['img'])
                location = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"location": location})
            else:
                data.update({"location": ""})
        except Exception as e:
            data.update({"location": ""})
        # //label[normalize-space()='Technical data']/following-sibling::div
        # try:  
        try:
            machine_overview_specs = tab2.ele("x:(//div[@class='lot-description-content']//div)[1]", timeout=0)
            if machine_overview_specs is not None:
                # 将 HTML 转换为 Markdown，并过滤掉空行
                raw_md = md(machine_overview_specs.html, strip=['img'])
                machine_overview_specs = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"machine_overview_specs": machine_overview_specs})
            else:   
                data.update({"machine_overview_specs": ""})
        except Exception as e:
            data.update({"machine_overview_specs": ""})

            
        # //label[normalize-space()='Description']/following-sibling::div
        try:
            machine_overview_options = tab2.ele("x:(//div[@class='lot-description-content']//div)[2]", timeout=0)
            if machine_overview_options is not None:
                raw_md = md(machine_overview_options.html, strip=['img'])
                machine_overview_options = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"machine_overview_options": machine_overview_options})
            else:
                data.update({"machine_overview_options": ""})
        except Exception as e:
            data.update({"machine_overview_options": ""})

        try:
            machine_overview_description = tab2.ele("x://div[text()='Description:']/following-sibling::div", timeout=0)
            if machine_overview_description is not None:
                raw_md = md(machine_overview_description.html, strip=['img'])
                machine_overview_description = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"machine_overview_description": machine_overview_description})
            else:
                data.update({"machine_overview_description": ""})
        except Exception as e:
            data.update({"machine_overview_description": ""})

        data_batch1.append(data)
        tab2.close()
        tab.set.activate()
    # data
    print('写入数据到 CSV 文件...')
    append_dicts_to_csv(data_batch1, fieldnames, filename)
    print('写入CSV 文件成功！继续下一批次数据...')
    data_batch1= []  # 清空数据批次，准备下一页的数据
print('写入CSV 文件成功！已完成所有数据的爬取。')
browser.quit()



