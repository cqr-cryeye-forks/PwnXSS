from core import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from multiprocessing import Process


class Crawler:
    visited = []

    def getLinks(self, base, session_get):
        lst = []

        text = session_get.get(base).text
        isi = BeautifulSoup(text, "html.parser")

        for obj in isi.find_all("a", href=True):
            url = obj["href"]

            if urljoin(base, url) in self.visited:
                continue

            elif url.startswith("mailto:") or url.startswith("javascript:"):
                continue
            # :// will check if there is any subdomain or any other domain, but it will pass directory
            elif url.startswith(base) or "://" not in url:
                lst.append(urljoin(base, url))
                self.visited.append(urljoin(base, url))

        return lst

    def crawl(self, base, depth, session_get):

        urls = self.getLinks(base, session_get)

        for url in urls:
            if url.startswith("https://") or url.startswith("http://"):

                if Core.check_connection(url, session_get):
                    tasks = []

                    p_get = Process(target=Core.get_method(url, session_get))
                    tasks.append(p_get)

                    p_post = Process(target=Core.post_method(url, session_get))
                    tasks.append(p_post)

                    p_else = Process(target=Core.get_method(url, session_get))
                    tasks.append(p_else)

                    for p in tasks:
                        p.start()
                        p.join()

                else:
                    continue

                if depth != 0:
                    self.crawl(url, depth - 1, session_get)

                else:
                    break
