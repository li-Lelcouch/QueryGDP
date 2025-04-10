import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import ttk, messagebox
from gdp_data import GDPDataFetcher

class GDPVisualizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("国家GDP可视化工具")
        self.root.geometry("900x700")
        
        # 设置代理（如需要）
        self.proxy = {
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",
        }
        
        # 创建数据获取对象
        self.data_fetcher = GDPDataFetcher(self.proxy)
        
        # 创建UI
        self.create_ui()
        
        # 获取可用国家列表
        self.load_countries()
    
    def create_ui(self):
        # 创建顶部控制面板
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 国家选择
        ttk.Label(control_frame, text="选择国家:").grid(row=0, column=0, padx=5, pady=5)
        self.country_combo = ttk.Combobox(control_frame, width=20)
        self.country_combo.grid(row=0, column=1, padx=5, pady=5)
        
        # 年份范围选择
        ttk.Label(control_frame, text="起始年份:").grid(row=0, column=2, padx=5, pady=5)
        self.start_year = ttk.Spinbox(control_frame, from_=1990, to=2022, width=5)
        self.start_year.set(1990)
        self.start_year.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(control_frame, text="结束年份:").grid(row=0, column=4, padx=5, pady=5)
        self.end_year = ttk.Spinbox(control_frame, from_=1990, to=2022, width=5)
        self.end_year.set(2022)
        self.end_year.grid(row=0, column=5, padx=5, pady=5)
        
        # 查询按钮
        self.query_button = ttk.Button(control_frame, text="查询数据", command=self.fetch_and_display_data)
        self.query_button.grid(row=0, column=6, padx=10, pady=5)
        
        # 创建图表区域
        self.figure = Figure(figsize=(9, 6), dpi=100)
        self.plot_canvas = FigureCanvasTkAgg(self.figure, self.root)
        self.plot_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 状态栏
        self.status_var = tk.StringVar()
        self.status_var.set("就绪")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_countries(self):
        pass

    def fetch_and_display_data(self):
        pass






def main():
    root = tk.Tk()
    app = GDPVisualizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()