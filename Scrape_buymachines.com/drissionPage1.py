# 导入
from datetime import datetime

from DrissionPage import Chromium, ChromiumOptions
from csvUtils import append_dicts_to_csv
from markdownify import markdownify as md


fieldnames = ["source_link", "name", "vendor","main_category","category","type_of_machine","manufacturer","technical_data","description"]
filename = "output.csv"

#获取当前时间戳
dt_obj = datetime.now()  # 获取当前时间
dt_str = dt_obj.strftime('%Y%m%d%H%M%S')
# filename是完整文件名字符串，我想要的是文件名 + 时间戳的形式
filename = filename.split('.')[0] + '_' + dt_str + '.csv'

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

source_link = "https://www.buymachines.com/"
# 循环 1到100
for i in range(1, 2):
    import time
    import random
    secs = random.randint(1, 2)
    time.sleep(secs)

    # 打印当前循环的数字
    print(f'第{i}页数据开始爬取...')
    # 替换 URL 中的页码
    url = 'https://www.buymachines.com/offers?isRoomActive=1&isRoomOnline=1&has_pictures=&page=' + str(i)
    # 访问网页
    tab.get(url)
    # 获取文本框元素对象
    titles = tab.eles('x:(//div[@class="ellipsis-a"]//b)', timeout=0)# x: xpath 前缀，表示使用 XPath 选择器
    if titles is None or len(titles) == 0:
        print(f'第{i}页没有数据，结束')
        break
    data = None
    index = 0
    for title in titles[:4]:
        index += 1
        print(f'第{i}页第{index}条数据开始爬取...')
        # 打印文本框的文本内容
        # 点击文本框
        title.click(by_js=True)  # 点击文本框

        try:
            # 等待标签加载完成
            tab.wait.ele_displayed("x://span[@class='a']")
        except Exception as e:
            print(f'第{i}页第{index}条数据加载失败，跳过')
            continue

        data = {}
        data.update({"source_link": source_link})

        try:
            # 获取当前标签页的 URL
            name = tab.ele("x://span[@class='a']", timeout=0)
            if name is not None:
                data.update({"name": name.text})
            else:
                data.update({"name": ""})
        except Exception as e:
            print(f'第{i}页第{index}条数据加载失败，跳过')
            data = None
            continue


        try:
            # 定位到 Vendor 同级的下一个元素
            vendor = tab.ele("x://label[text()='Vendor']/following-sibling::*[1]", timeout=0)
            # 如果没找到元素，就让 clean_md 直接成为空字符串
            if vendor is None:
                vendor = ""
            else:
                # 找到了元素，先把它的 HTML 转成 Markdown
                raw_md = md(vendor.html, strip=['a', 'img'])
                # 再过滤掉空行
                vendor = "\n".join(line for line in raw_md.splitlines() if line.strip())
            data.update({"vendor": vendor})
        except Exception as e:  
            data.update({"vendor": ""})

        try:
            # //label[@class='l'][normalize-space()='Main Category']/following-sibling::*[1]
            main_category = tab.ele("x://label[@class='l'][normalize-space()='Main Category']/following-sibling::*[1]", timeout=0)
            if main_category is not None:
                data.update({"main_category": main_category.text})
            else:
                data.update({"main_category": ""})
        except Exception as e:
            data.update({"main_category": ""})

        try:
            # //label[normalize-space()='Category']/following-sibling::div
            category = tab.ele("x://label[normalize-space()='Category']/following-sibling::div", timeout=0)
            if category is not None:
                data.update({"category": category.text})
            else:
                data.update({"category": ""})
        except Exception as e:
            data.update({"category": ""})

        # //label[normalize-space()='Type of Machine']/following-sibling::div
        try:
            type_of_machine = tab.ele("x://label[normalize-space()='Type of Machine']/following-sibling::div", timeout=0)
            if type_of_machine is not None:
                data.update({"type_of_machine": type_of_machine.text})
            else:
                data.update({"type_of_machine": ""})
        except Exception as e:
            data.update({"type_of_machine": ""})

        # //label[normalize-space()='Manufacturer']/following-sibling::div
        try:
            manufacturer = tab.ele("x://label[normalize-space()='Manufacturer']/following-sibling::div", timeout=0)
            if manufacturer is not None:
                data.update({"manufacturer": manufacturer.text})
            else:
                data.update({"manufacturer": ""})
        except Exception as e:
            data.update({"manufacturer": ""})
        # //label[normalize-space()='Technical data']/following-sibling::div
        # try:  
        try:
            technical_data = tab.ele("x://label[normalize-space()='Technical data']/following-sibling::div", timeout=0)
            if technical_data is not None:
                # 将 HTML 转换为 Markdown，并过滤掉空行
                raw_md = md(technical_data.html, strip=['a', 'img'])
                technical_data = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"technical_data": technical_data})
            else:   
                data.update({"technical_data": ""})
        except Exception as e:
            data.update({"technical_data": ""})

            
        # //label[normalize-space()='Description']/following-sibling::div
        try:
            description = tab.ele("x://label[normalize-space()='Description']/following-sibling::div", timeout=0)
            if description is not None:
                raw_md = md(description.html, strip=['a', 'img'])
                description = "\n".join(line for line in raw_md.splitlines() if line.strip())
                data.update({"description": description})
            else:
                data.update({"description": ""})
        except Exception as e:
            data.update({"description": ""})

        data_batch1.append(data)
        #print(f'第{i}页数据爬取完成，当前数据{data}')
        #close = tab.ele("x://a[@id='cnc-lightbox-close']")
        #close.click()  # 关闭当前标签页

    # data
    append_dicts_to_csv(data_batch1, fieldnames, filename)
    data_batch1= []  # 清空数据批次，准备下一页的数据
browser.quit()





