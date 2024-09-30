import requests
import re
import threading
import time
from colorama import Fore
from bs4 import BeautifulSoup

class ProxyScraper:
    def __init__(self, urls, filename="valid_proxies.txt"):
        self.urls = urls
        self.proxies = []
        self.filename = filename

    def pattern_one(self, data):
        ip_port = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,5})", data)
        if ip_port:
            for proxy in ip_port:
                self.proxies.append(proxy)
        else:
            self.pattern_two(data)

    def pattern_two(self, data):
        ip = re.findall(r">(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<", data)
        port = re.findall(r"td>(\d{2,5})<", data)
        if ip and port:
            for i in range(min(len(ip), len(port))):
                self.proxies.append(f"{ip[i]}:{port[i]}")
        else:
            self.pattern_three(data)

    def pattern_three(self, data):
        ip = re.findall(r">\n[\s]+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", data)
        port = re.findall(r">\n[\s]+(\d{2,5})\n", data)
        if ip and port:
            for i in range(min(len(ip), len(port))):
                self.proxies.append(f"{ip[i]}:{port[i]}")
        else:
            self.pattern_four(data)

    def pattern_four(self, data):
        ip = re.findall(r">(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})<", data)
        port = re.findall(r">(\d{2,5})<", data)
        if ip and port:
            for i in range(min(len(ip), len(port))):
                self.proxies.append(f"{ip[i]}:{port[i]}")
        else:
            self.pattern_five(data)

    def pattern_five(self, data):
        ip = re.findall(r"(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", data)
        port = re.findall(r"(\d{2,5})", data)
        if ip and port:
            for i in range(min(len(ip), len(port))):
                self.proxies.append(f"{ip[i]}:{port[i]}")

    def start(self, url):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            self.pattern_one(response.text)
            print(Fore.CYAN + f"Scraped proxies from: {Fore.MAGENTA + url}" + "\n")
        except Exception as e:
            print(f"Failed to scrape {url}: {e}")

    def scrape_proxies(self):
        threads = []
        for url in self.urls.splitlines():
            if url:
                thread = threading.Thread(target=self.start, args=(url,))
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()

    def check(self, proxylist):
        for proxy in proxylist:
            try:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"
                }
                requests.get(
                    "https://httpbin.org/ip",
                    headers=headers,
                    proxies={"http": proxy, "https": proxy},
                    timeout=1
                )
                print(Fore.GREEN + "SUCCESS: " + proxy + "\n")
                with open(self.filename, "a") as f:
                    f.write(proxy + "\n")
            except:
                print(Fore.RED + "FAIL   : " + proxy + "\n")

    def check_proxies(self):
        open(self.filename, "w").close()

        self.scrape_proxies()

        time.sleep(10)
        print(Fore.GREEN + "\n" + f"Scraped {len(self.proxies)} proxies")
        time.sleep(0.5)
        print(Fore.BLUE + "Starting checking process...\n")
        time.sleep(2)

        self.optimize_proxies()

        for chunk in self.proxies:
            threading.Thread(target=self.check, args=(chunk,)).start()

    def optimize_proxies(self):
        n = len(self.proxies) // 100 or 1
        self.proxies = [self.proxies[i:i + n] for i in range(0, len(self.proxies), n)]

    def cleanup(self):
        contents = open(self.filename, "r").readlines()
        new_proxies = []

        for line in contents:
            if line.strip() and line not in new_proxies:
                new_proxies.append(line)

        with open(self.filename, "w") as f:
            f.writelines(new_proxies)

        print(Fore.YELLOW + f"Cleaned up duplicates, remaining {len(new_proxies)} proxies.")


urls = """
https://raw.githubusercontent.com/proxifly/free-proxy-list/main/proxies/all/data.txt
https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/all.txt
https://raw.githubusercontent.com/zloi-user/hideip.me/main/https.txt
https://raw.githubusercontent.com/zloi-user/hideip.me/main/http.txt
https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/http.txt
https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks4.txt
https://raw.githubusercontent.com/zloi-user/hideip.me/main/socks5.txt
https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks5.txt
https://raw.githubusercontent.com/roosterkid/openproxylist/main/SOCKS4_RAW.txt
https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=50000&country=all
https://raw.githubusercontent.com/UptimerBot/proxy-list/main/proxies_anonymous/socks4.txt
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/socks4.txt
https://raw.githubusercontent.com/officialputuid/KangProxy/KangProxy/socks4/socks4.txt
https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-socks4.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt
https://www.proxyscan.io/api/proxy?type=socks4&last_check=10000&limit=20&format=txt
https://api.openproxylist.xyz/socks4.txt
https://www.proxy-list.download/api/v1/get?type=socks4
https://raw.githubusercontent.com/XDMEOW/SocksProxy/main/socks4(all).txt
https://raw.githubusercontent.com/B4RC0DE-TM/proxy-list/main/SOCKS4.txt
https://raw.githubusercontent.com/ProxyScraper/ProxyScraper/refs/heads/main/socks4.txt
https://api.proxyscrape.com/v4/free-proxy-list/get?request=display_proxies&proxy_format=protocolipport&format=text
https://raw.githubusercontent.com/saschazesiger/Free-Proxies/master/proxies/http.txt
http://globalproxies.blogspot.com/
http://www.cybersyndrome.net/plz.html
http://www.cybersyndrome.net/plr5.html
http://biskutliat.blogspot.com/
http://freeproxylist-daily.blogspot.com/2013/05/usa-proxy-list-2013-05-15-0111-am-gmt8.html
http://freeproxylist-daily.blogspot.com/2013/05/usa-proxy-list-2013-05-13-812-gmt7.html
http://www.cybersyndrome.net/pla5.html
http://vipprox.blogspot.com/2013_06_01_archive.html
http://vipprox.blogspot.com/2013/05/us-proxy-servers-74_24.html
http://vipprox.blogspot.com/p/blog-page_7.html
http://vipprox.blogspot.com/2013/05/us-proxy-servers-199_20.html
http://vipprox.blogspot.com/2013_02_01_archive.html
http://alexa.lr2b.com/proxylist.txt
http://vipprox.blogspot.com/2013_03_01_archive.html
http://browse.feedreader.com/c/Proxy_Server_List-1/449196260
http://browse.feedreader.com/c/Proxy_Server_List-1/449196258
http://sock5us.blogspot.com/2013/06/01-07-13-free-proxy-server-list.html#comment-form
http://browse.feedreader.com/c/Proxy_Server_List-1/449196251
http://free-ssh.blogspot.com/feeds/posts/default
http://browse.feedreader.com/c/Proxy_Server_List-1/449196259
http://sockproxy.blogspot.com/2013/04/11-04-13-socks-45.html
http://proxyfirenet.blogspot.com/
https://www.javatpoint.com/proxy-server-list
https://openproxy.space/list/http
http://proxydb.net/
https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/http.txt
https://raw.githubusercontent.com/ItzRazvyy/ProxyList/main/https.txt
https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt
https://raw.githubusercontent.com/Natthanon823/steam-account-checker/main/http.txt
http://olaf4snow.com/public/proxy.txt
http://westdollar.narod.ru/proxy.htm
https://openproxy.space/list/socks4
https://openproxy.space/list/socks5
http://tomoney.narod.ru/help/proxi.htm
http://sergei-m.narod.ru/proxy.htm
http://rammstein.narod.ru/proxy.html
http://greenrain.bos.ru/R_Stuff/Proxy.htm
http://inav.chat.ru/ftp/proxy.txt
http://johnstudio0.tripod.com/index1.htm
http://atomintersoft.com/transparent_proxy_list
http://atomintersoft.com/anonymous_proxy_list
http://atomintersoft.com/high_anonymity_elite_proxy_list
http://atomintersoft.com/products/alive-proxy/proxy-list/3128
http://atomintersoft.com/products/alive-proxy/proxy-list/com
http://atomintersoft.com/products/alive-proxy/proxy-list/high-anonymity/
http://atomintersoft.com/products/alive-proxy/socks5-list
http://atomintersoft.com/proxy_list_domain_com
http://atomintersoft.com/proxy_list_domain_edu
http://atomintersoft.com/proxy_list_domain_net
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt
http://atomintersoft.com/proxy_list_domain_org
http://atomintersoft.com/proxy_list_port_3128
http://atomintersoft.com/proxy_list_port_80
http://atomintersoft.com/proxy_list_port_8000
http://atomintersoft.com/proxy_list_port_81
http://hack-hack.chat.ru/proxy/allproxy.txt
https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt
http://hack-hack.chat.ru/proxy/anon.txt
http://hack-hack.chat.ru/proxy/p1.txt
http://hack-hack.chat.ru/proxy/p2.txt
http://hack-hack.chat.ru/proxy/p3.txt
http://hack-hack.chat.ru/proxy/p4.txt
https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt
https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt
https://free-proxy-list.net/
https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt
https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-http.txt
https://www.us-proxy.org/
https://free-proxy-list.com/
https://sunny9577.github.io/proxy-scraper/proxies.txt
https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all
https://api.proxyscrape.com/?request=getproxies&proxytype=socks4&timeout=10000&country=all
https://api.proxyscrape.com/?request=getproxies&proxytype=socks5&timeout=10000&country=all
https://spys.one/
https://api.proxyscrape.com/?request=getproxies&proxytype=https&timeout=10000&country=all&ssl=all&anonymity=all
https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks4&timeout=10000&country=all
https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/proxy.txt
https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all
https://api.proxyscrape.com/v2/?request=getproxies&protocol=socks5&timeout=10000&country=all
"""

proxy_scraper = ProxyScraper(urls)
proxy_scraper.check_proxies()
proxy_scraper.cleanup()
