import requests
from bs4 import BeautifulSoup
from typing import List, Dict
import json
import time
import random
from urllib.parse import urljoin

class LanguageScraper:
    def __init__(self):
        self.base_url = "https://cursor.directory"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        
    def fetch_page(self, url: str, retries: int = 3) -> str:
        """获取页面内容，支持重试"""
        for i in range(retries):
            try:
                time.sleep(random.uniform(1, 3))  # 随机延迟
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                if i == retries - 1:
                    print(f"Error fetching {url}: {e}")
                    raise
                print(f"Retry {i + 1}/{retries} for {url}")
                time.sleep(2 ** i)  # 指数退避
                
    def parse_languages(self, html: str) -> List[Dict]:
        """解析所有编程语言标签"""
        soup = BeautifulSoup(html, 'html.parser')
        languages = []
        seen = set()
        
        # 查找所有标签元素
        for tag in soup.find_all('a', href=True):
            name = tag.text.strip()
            if not name:
                continue
                
            # 过滤非编程语言的标签
            if name.lower() in {'subscribe', 'live', 'learn', 'about', 'all', 'popular', 
                              'submit', 'type', 'framework', 'library', 'tool'}:
                continue
                
            # 获取标签数量
            count = 1
            if '(' in name:
                try:
                    name, count_str = name.rsplit('(', 1)
                    count = int(count_str.rstrip(')'))
                    name = name.strip()
                except (ValueError, IndexError):
                    pass
            
            # 避免重复
            if name.lower() in seen:
                continue
            seen.add(name.lower())
            
            # 生成slug
            slug = name.lower().replace('.', '').replace(' ', '').replace('-', '').replace('/', '')
            
            languages.append({
                'name': name,
                'name_zh': name,  # 可以后续添加中文名称
                'slug': slug,
                'count': count
            })
        
        # 按count降序排序
        languages.sort(key=lambda x: x['count'], reverse=True)
        return languages
        
    def save_to_json(self, languages: List[Dict], filename: str = 'languages.json'):
        """保存语言数据到JSON文件"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(languages, f, ensure_ascii=False, indent=2)
        print(f"Saved {len(languages)} languages to {filename}")
        
    def run(self):
        """运行爬虫"""
        try:
            print("Fetching languages from cursor.directory...")
            html = self.fetch_page(self.base_url)
            languages = self.parse_languages(html)
            
            print(f"\nFound {len(languages)} languages:")
            for lang in languages[:10]:  # 只显示前10个
                print(f"{lang['name']}: {lang['count']} prompts")
            if len(languages) > 10:
                print("...")
                
            self.save_to_json(languages)
            return languages
            
        except Exception as e:
            print(f"Error running scraper: {e}")
            return []

if __name__ == "__main__":
    scraper = LanguageScraper()
    scraper.run() 