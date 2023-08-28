from core import *
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from multiprocessing import Process


class Crawler:
    visited = []

    @staticmethod
    def get_links(base, session_get):
        lst = []

        text = session_get.get(base).text
        isi = BeautifulSoup(text, "html.parser")
        list_of_links_from_base_url = isi.find_all("a", href=True)

        for obj in list_of_links_from_base_url:
            url = obj["href"]
            full_link = urljoin(base, url)

            if full_link in Crawler.visited:
                continue

            elif url.startswith("mailto:") or url.startswith("javascript:"):
                continue
            # Pass only base url or directory, not other domains or subdomains
            elif url.startswith(base) or "://" not in url:
                # TODO: debug this
                lst.append(full_link)
                Crawler.visited.append(full_link)

        return lst

    def crawl(self, base, depth, session_get):

        urls = self.get_links(base, session_get)

        for url in urls:
            if url.startswith("http"):

                if Core.check_connection(url, session_get):
                    tasks = []

                    p_get = Process(target=Core.get_method(url, session_get))
                    tasks.append(p_get)

                    p_post = Process(target=Core.post_method(url, session_get))
                    tasks.append(p_post)

                    p_else = Process(target=Core.get_method_form(url, session_get))
                    tasks.append(p_else)

                    for p in tasks:
                        p.start()
                        p.join()
                # else:
                #     continue

                if depth != 0:
                    self.crawl(url, depth - 1, session_get)

                else:
                    break
