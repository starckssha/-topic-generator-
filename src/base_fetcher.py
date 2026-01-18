"""
基础抓取器类 - 增强SSL兼容性
"""
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context
import time
import random
import sys
import os
import ssl

# 添加父目录到路径以导入config
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from config import CONFIG
except:
    CONFIG = {}


class SSLAdapter(HTTPAdapter):
    """自定义SSL适配器，使用更宽松的SSL配置"""
    
    def init_poolmanager(self, *args, **kwargs):
        # 创建更宽松的SSL上下文
        context = create_urllib3_context()
        
        # 设置更宽松的选项
        context.options |= 0x4  # OP_LEGACY_SERVER_CONNECT
        
        # 尝试设置最低TLS版本
        try:
            context.minimum_version = ssl.TLSVersion.TLSv1_2
        except:
            context.set_ciphers('DEFAULT@SECLEVEL=1')
        
        kwargs['ssl_context'] = context
        return super().init_poolmanager(*args, **kwargs)


class BaseFetcher(ABC):
    """所有抓取器的基类"""

    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    ]

    def __init__(self):
        self.timeout = CONFIG.get('timeout', 15) if isinstance(CONFIG, dict) else 15
        self.session = requests.Session()
        self._setup_session()

    def _setup_session(self):
        """配置session"""
        user_agent = random.choice(self.USER_AGENTS)

        # 配置代理
        if isinstance(CONFIG, dict) and CONFIG.get('use_proxy', False):
            proxies = {
                'http': CONFIG.get('http_proxy'),
                'https': CONFIG.get('https_proxy')
            }
            # 只设置非空的代理
            proxies = {k: v for k, v in proxies.items() if v}
            if proxies:
                self.session.proxies = proxies
                print(f"[PROXY] Using proxy: {proxies}")
            else:
                print("[PROXY] Proxy disabled - using direct connection")
        else:
            print("[PROXY] Proxy disabled - using direct connection")

        self.session.headers.update({
            'User-Agent': user_agent,
            'Accept': 'application/json, text/plain, */*, text/html, application/xhtml+xml',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })

        # 挂载SSL适配器
        self.session.mount('https://', SSLAdapter())

        # 禁用SSL验证（用于某些网站）
        self.session.verify = False

        # 禁用SSL警告
        import urllib3
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        print("[SSL] Enhanced SSL compatibility mode enabled")

    @abstractmethod
    def fetch(self, count: int = 20) -> List[Dict]:
        pass

    def _get_json(self, url: str, referer: str = None, retry: int = 3) -> Optional[dict]:
        for attempt in range(retry):
            try:
                headers = self.session.headers.copy()
                if referer:
                    headers['Referer'] = referer

                if attempt > 0:
                    time.sleep(random.uniform(0.5, 1.5))

                response = self.session.get(url, headers=headers, timeout=self.timeout)
                
                if response.status_code in [403, 401]:
                    if attempt < retry - 1:
                        self.session.headers['User-Agent'] = random.choice(self.USER_AGENTS)
                        continue
                
                response.raise_for_status()
                return response.json()

            except requests.RequestException as e:
                if attempt == retry - 1:
                    print(f"请求失败: {url}, 错误: {e}")
                else:
                    print(f"重试中 ({attempt + 1}/{retry})...")
            except Exception as e:
                if attempt == retry - 1:
                    print(f"解析JSON失败: {e}")
        
        return None

    def _get_html(self, url: str, referer: str = None, retry: int = 3) -> Optional[str]:
        for attempt in range(retry):
            try:
                headers = self.session.headers.copy()
                if referer:
                    headers['Referer'] = referer
                
                if attempt > 0:
                    time.sleep(random.uniform(0.5, 1.5))

                response = self.session.get(url, headers=headers, timeout=self.timeout)
                
                if response.status_code in [403, 401]:
                    if attempt < retry - 1:
                        self.session.headers['User-Agent'] = random.choice(self.USER_AGENTS)
                        continue
                
                response.raise_for_status()
                response.encoding = response.apparent_encoding
                return response.text

            except requests.RequestException as e:
                if attempt == retry - 1:
                    print(f"请求失败: {url}, 错误: {e}")
            except Exception as e:
                if attempt == retry - 1:
                    print(f"获取HTML失败: {e}")
        
        return None
