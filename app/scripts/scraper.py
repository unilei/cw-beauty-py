import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import json
from datetime import datetime
import time
import random

class CursorDirectoryScraper:
    def __init__(self, max_retries: int = 3, delay: tuple = (1, 3)):
        self.base_url = "https://cursor.directory"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
        }
        self.max_retries = max_retries
        self.delay = delay

    def fetch_page(self, url: str, retry_count: int = 0) -> Optional[str]:
        """获取页面内容，支持重试"""
        try:
            # 随机延迟，避免请求过快
            time.sleep(random.uniform(*self.delay))
            
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            if retry_count < self.max_retries:
                print(f"Error fetching {url}: {e}. Retrying... ({retry_count + 1}/{self.max_retries})")
                time.sleep(2 ** retry_count)  # 指数退避
                return self.fetch_page(url, retry_count + 1)
            else:
                print(f"Failed to fetch {url} after {self.max_retries} retries: {e}")
                return None

    def parse_tags(self, html: str) -> List[Dict]:
        """解析标签数据"""
        soup = BeautifulSoup(html, 'html.parser')
        tags = []
        
        # 查找所有标签元素
        tag_elements = soup.find_all('a', href=True)
        for tag in tag_elements:
            # 获取标签名和数量
            name = tag.text.strip()
            print(f"Found tag: {name!r} with href: {tag['href']!r}")  # Debug output
            
            if not name or name in ['Subscribe', 'Live', 'Learn', 'About', 'All', 'Popular']:
                continue
            
            # 简化标签处理逻辑
            tag_name = name
            count = 1
            
            # 确保URL正确
            href = tag['href']
            if not href.startswith('http'):
                href = f"{self.base_url}{href}"
            
            tags.append({
                'name': tag_name,
                'count': count,
                'url': href
            })
        
        # 过滤掉重复的标签
        unique_tags = []
        seen_names = set()
        for tag in tags:
            if tag['name'] not in seen_names:
                seen_names.add(tag['name'])
                unique_tags.append(tag)
        
        return unique_tags

    def save_to_json(self, data: List[Dict], filename: str = None):
        """保存数据到JSON文件"""
        if filename is None:
            filename = f"cursor_directory_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print(f"Data saved to {filename}")

    def parse_prompt(self, html: str) -> Dict:
        """解析提示词详细内容"""
        soup = BeautifulSoup(html, 'html.parser')
        prompt = {}
        
        # 获取标题
        title_elem = soup.find('h1')
        if title_elem:
            prompt['title'] = title_elem.text.strip()
        
        # 获取内容
        content_elem = soup.find('div', class_='prose')
        if content_elem:
            prompt['content'] = content_elem.text.strip()
        
        # 获取标签
        tags = []
        tag_elements = soup.find_all('a', class_='tag')
        for tag in tag_elements:
            tags.append(tag.text.strip())
        prompt['tags'] = tags
        
        # 获取元数据（作者、日期等）
        meta_elem = soup.find('div', class_='meta')
        if meta_elem:
            author_elem = meta_elem.find('a')
            if author_elem:
                prompt['author'] = author_elem.text.strip()
            
            date_elem = meta_elem.find('time')
            if date_elem:
                prompt['created_at'] = date_elem.get('datetime')
        
        return prompt

    def fetch_prompts(self, tag_url: str) -> List[Dict]:
        """获取某个标签下的所有提示词，支持分页"""
        prompts = []
        page = 1
        
        while True:
            page_url = f"{tag_url}?page={page}" if page > 1 else tag_url
            html = self.fetch_page(page_url)
            
            if not html:
                break
                
            soup = BeautifulSoup(html, 'html.parser')
            prompt_links = soup.find_all('a', class_='prompt-link', href=True)
            
            if not prompt_links:
                break
                
            for link in prompt_links:
                prompt_url = f"{self.base_url}{link['href']}"
                prompt_html = self.fetch_page(prompt_url)
                if prompt_html:
                    prompt = self.parse_prompt(prompt_html)
                    prompt['url'] = prompt_url
                    prompts.append(prompt)
                    print(f"Scraped prompt: {prompt.get('title', 'Untitled')}")
            
            # 检查是否有下一页
            next_button = soup.find('a', string='Next')
            if not next_button:
                break
                
            page += 1
        
        return prompts

    def run(self, output_file: str = None):
        """运行爬虫"""
        print("Starting to scrape cursor.directory...")
        
        # 获取主页内容
        html = self.fetch_page(self.base_url)
        if not html:
            print("Failed to fetch the main page")
            return
        
        # 解析标签数据
        tags = self.parse_tags(html)
        all_data = {'tags': tags, 'prompts': []}
        
        # 获取每个标签下的提示词
        total_tags = len(tags)
        for i, tag in enumerate(tags, 1):
            print(f"\nProcessing tag {i}/{total_tags}: {tag['name']}")
            prompts = self.fetch_prompts(tag['url'])
            all_data['prompts'].extend(prompts)
            
            # 定期保存数据，避免丢失
            if i % 5 == 0:
                temp_file = f"cursor_directory_data_temp_{i}.json"
                self.save_to_json(all_data, temp_file)
        
        # 最终保存
        if output_file:
            self.save_to_json(all_data, output_file)
        else:
            self.save_to_json(all_data)
        
        print(f"\nScraped {len(tags)} tags and {len(all_data['prompts'])} prompts successfully")
        return all_data

if __name__ == "__main__":
    scraper = CursorDirectoryScraper(max_retries=3, delay=(2, 5))
    scraper.run("cursor_directory_full_data.json") 