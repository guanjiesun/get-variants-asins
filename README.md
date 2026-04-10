### 项目描述
> 给定一个asin，获取所有变体的asin

### 实现方式
    1. 使用 httpx 并且构造 `User-Agent` 请求头，然后请求 `asin` 详情页
    2. 使用 zendriver 浏览器自动化工具获取 `asin` 详情页
### 运行方法
    1. uv sync
    2. uv run python main.py

### 输出文件
    1. f'{asin}-httpx.xlsx'
    2. f'{asin}-zendriver.xlsx'