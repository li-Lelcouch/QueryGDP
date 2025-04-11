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
        """加载可用的国家列表"""
        self.status_var.set("正在加载国家列表...")
        self.root.update()
        
        countries = self.data_fetcher.get_available_countries()
        
        if countries:
            self.country_combo['values'] = countries
            self.status_var.set(f"已加载 {len(countries)} 个国家")
        else:
            self.status_var.set("加载国家列表失败")
            messagebox.showerror("错误", "无法加载国家列表，请检查网络连接")

    def fetch_and_display_data(self):
        """获取并显示选定国家的数据"""
        country_name = self.country_combo.get()
        
        if not country_name:
            messagebox.showwarning("警告", "请选择一个国家")
            return
            
        # 获取国家代码
        country_code = self.data_fetcher.get_country_code(country_name)
        if not country_code:
            messagebox.showwarning("警告", f"未找到 {country_name} 的国家代码")
            return
        
        try:
            start = int(self.start_year.get())
            end = int(self.end_year.get())
            
            if start > end:
                messagebox.showwarning("警告", "起始年份不能大于结束年份")
                return
                
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的年份")
            return
        
        self.status_var.set(f"正在获取 {country_name} 的数据...")
        self.root.update()
        
        # 获取数据
        data = self.data_fetcher.get_country_data(country_code, start, end)
        
        if not data["GDP"] or not data["GDP_per_capita"]:
            self.status_var.set("获取数据失败")
            messagebox.showerror("错误", f"无法获取 {country_name} 的数据")
            return
            
        # 显示图表
        self.plot_data(country_name, data, start, end)
        self.status_var.set(f"已显示 {country_name} 从 {start} 到 {end} 年的数据")

    def plot_data(self, country, data, start_year, end_year):
        """绘制数据图表"""
        self.figure.clear()
        
        # 创建GDP子图
        ax1 = self.figure.add_subplot(211)
        years = sorted([int(y) for y in data["GDP"].keys() if start_year <= int(y) <= end_year])
        values = [data["GDP"][str(y)] for y in years]
        
        # 将GDP值从美元转换为十亿美元，以便更好地显示
        values = [v / 1e9 for v in values]
        
        ax1.plot(years, values, 'b-o', linewidth=2)
        ax1.set_title(f"{country}的GDP ({start_year}-{end_year})")
        ax1.set_xlabel("年份")
        ax1.set_ylabel("GDP (十亿美元)")
        ax1.grid(True)
        
        # 创建人均GDP子图
        ax2 = self.figure.add_subplot(212)
        pc_years = sorted([int(y) for y in data["GDP_per_capita"].keys() if start_year <= int(y) <= end_year])
        pc_values = [data["GDP_per_capita"][str(y)] for y in pc_years]
        
        ax2.plot(pc_years, pc_values, 'r-o', linewidth=2)
        ax2.set_title(f"{country}的人均GDP ({start_year}-{end_year})")
        ax2.set_xlabel("年份")
        ax2.set_ylabel("人均GDP (美元)")
        ax2.grid(True)
        
        self.figure.tight_layout()
        self.plot_canvas.draw()






def main():
    root = tk.Tk()
    app = GDPVisualizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()