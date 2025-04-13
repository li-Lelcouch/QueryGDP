# QueryGDP
This application provides an interactive visualization tool for exploring GDP and GDP per capita data across different countries. The tool leverages the World Bank API to fetch real-time economic data and presents it through an intuitive graphical user interface.

## 功能特性

- 查询并展示任意国家的GDP总量、人均GDP和人口总数数据
- 支持自定义年份范围(1990-2022)
- 直观的图形界面，易于操作
- 自动获取可用国家列表
- 数据以十亿美元(GDP总量)、美元(人均GDP)和百万人(人口总数)为单位显示

## 安装要求

```bash
pip install requests matplotlib
```

## 使用方法

1. 运行主程序：

```bash
python main.py
```

2. 在应用程序界面中：
   - 从下拉列表中选择一个国家
   - 设置起始年份和结束年份
   - 点击"查询数据"按钮
   - 程序将在图表区域显示选定国家的GDP、人均GDP和人口数据

## 代理设置

如果您在中国大陆或其他需要代理访问World Bank API的地区，可以在`main.py`中修改代理设置：

```python
self.proxy = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}
```

## 项目结构

- `main.py`: 主程序，包含GUI界面和可视化逻辑
- `gdp_data.py`: 数据获取模块，负责从World Bank API获取GDP数据

## 注意事项

- 该程序需要网络连接才能获取数据
- 可能需要设置代理以访问World Bank API
- 程序使用SimHei字体显示中文，确保您的系统安装了该字体

## 技术实现

本项目使用以下技术：
- `tkinter`: 创建图形用户界面
- `matplotlib`: 数据可视化
- `requests`: 访问World Bank API