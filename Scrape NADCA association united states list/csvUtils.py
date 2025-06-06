import csv
import os

def append_dicts_to_csv(data_batch, fieldnames, filename):
    """
    将一批以字典形式存储的行（data_batch）追加写入 CSV 文件，
    并且让所有字段都用双引号括起来。如果字段内容中包含双引号，
    CSV 模块会将其转义为两个连续的双引号。

    参数：
    - data_batch:   List[Dict]，本次要追加写入的一批数据
    - fieldnames:   List[str]，CSV 的列名顺序
    - filename:     str，目标 CSV 文件名（不含目录，只是文件名，例如 "output.csv"）
    """

    # 确保 data 目录存在，不存在则创建
    data_dir = "data"
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    # 拼接最终的路径：data/filename
    file_path = os.path.join(data_dir, filename)

    file_exists = os.path.exists(file_path)
    write_header = True
    if file_exists and os.path.getsize(file_path) > 0:
        write_header = False

    # 追加模式打开，同时指定 newline=""，并让所有字段都用双引号引用
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
            quoting=csv.QUOTE_ALL,    # 强制对所有字段加双引号
            quotechar='"',            # 使用双引号作为引用字符
            doublequote=True          # True 表示将内部的 " 转成 ""
        )

        if write_header:
            writer.writeheader()

        for row in data_batch:
            writer.writerow(row)


def writeMain():
    fieldnames = ["name", "age", "email"]
    filename = "output_dict.csv"

    # 第一批数据
    data_batch1 = [
        {"name": "Alice", "age": 30, "email": "alice@example.com"},
        {"name": "Bob",   "age": 25, "email": "bob@example.com"},
    ]
    append_dicts_to_csv(data_batch1, fieldnames, filename)
    # 此时 output_dict.csv 会被创建，内容类似：
    # name,age,email
    # Alice,30,alice@example.com
    # Bob,25,bob@example.com


    # 第二批数据（稍后要追加）
    data_batch2 = [
        {"name": "Cathy", "age": 28, "email": "cathy@example.com"},
        {"name": "David", "age": 22, "email": "david@example.com"},
    ]
    append_dicts_to_csv(data_batch2, fieldnames, filename)
    # 此时 output_dict.csv 文件末尾会继续追加两行，不会重复写表头，最终内容：
    # name,age,email
    # Alice,30,alice@example.com
    # Bob,25,bob@example.com
    # Cathy,28,cathy@example.com
    # David,22,david@example.com
    
