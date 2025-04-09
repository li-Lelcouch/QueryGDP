import requests
import pandas as pd

class GDPDataFetcher:
    def __init__(self, proxy=None):
        self.base_url = "https://api.worldbank.org/v2"
        self.proxies = proxy if proxy else None
        self.country_cache = {}  
        
    def get_country_data(self, country_code, start_year=1990, end_year=2022):
        """获取指定国家的GDP和其他经济指标数据"""
        # 获取GDP数据 (NY.GDP.MKTP.CD 是GDP总量(当前美元))
        gdp_data = self._fetch_indicator("NY.GDP.MKTP.CD", country_code, start_year, end_year)
        
        # 获取人均GDP数据作为第二个指标 (NY.GDP.PCAP.CD 是人均GDP(当前美元))
        gdp_pc_data = self._fetch_indicator("NY.GDP.PCAP.CD", country_code, start_year, end_year)
        
        return {
            "GDP": gdp_data,
            "GDP_per_capita": gdp_pc_data
        }
    
    def _fetch_indicator(self, indicator, country_code, start_year, end_year):
        """获取特定指标的数据"""
        try:
            url = f"{self.base_url}/country/{country_code}/indicator/{indicator}"
            params = {
                "format": "json",
                "date": f"{start_year}:{end_year}",
                "per_page": 100
            }
            response = requests.get(url, params=params, proxies=self.proxies)
            
            if response.status_code != 200:
                print(f"API请求失败，状态码: {response.status_code}")
                return None
                
            data = response.json()
            
            # World Bank API返回的数据是分页的，第一个元素是元数据
            if len(data) < 2 or not data[1]:
                print(f"未找到国家 {country_code} 的 {indicator} 数据")
                return None
                
            # 将数据转换为字典形式 {年份: 值}
            result = {}
            for item in data[1]:
                year = item['date']
                value = item['value']
                if value is not None:  # 有些年份可能没有数据
                    result[year] = value
                    
            return result
                
        except Exception as e:
            print(f"获取数据时出错: {e}")
            return None
            
    def get_available_countries(self):
        """获取可用的国家列表"""
        try:
            url = f"{self.base_url}/country"
            params = {
                "format": "json",
                "per_page": 300  # 获取足够多的国家
            }
            response = requests.get(url, params=params, proxies=self.proxies)
            
            if response.status_code != 200:
                return []
                
            data = response.json()
            
            # 过滤掉非国家的实体(如区域组)并返回国家代码和名称
            countries = []
            for country in data[1]:
                if country['region']['id'] != "NA" and country['incomeLevel']['id'] != "NA":
                    self.country_cache[country['name']] = country['id']
                    countries.append(country['name'])
            
            return sorted(countries)
            
        except Exception as e:
            print(f"获取国家列表时出错: {e}")
            return []
    
    def get_country_code(self, country_name):
        """根据国家名称获取国家代码"""
        return self.country_cache.get(country_name)
