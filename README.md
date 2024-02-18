# Fake-Rating

## 介绍

一个使用 Python 编写的模拟用户对商品进行评分的程序。程序会模拟用户对商品进行评轮, 并根据上传的 csv 模版进行导出

## 安装

```bash
# python 3.11
pip install -r requirements.txt
```

## 使用

```bash
python main.py
```

打开浏览器[http://127.0.0.1:7860](http://127.0.0.1:7860)

根据提示进行操作

- 输入产品名称 `Product Name`
- 输入产品特点 `Product Features`
- 输出需要生成的评论数量 `Number of Reviews to Generate`
- 上传 csv 模版 `example_template.csv`
- 点击 `submit` 开始生成评论
- 导出评论下载为 `export.csv`
