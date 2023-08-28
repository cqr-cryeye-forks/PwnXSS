import cli
import helper
from crawler import *
import os
import pathlib
from crawler import Crawler


def start():
    get_args = cli.parse.parse_args()
    session_get = helper.session(proxies=get_args.proxy, headers=get_args.user_agent, cookie=get_args.cookie)
    Log.info("Starting PwnXSS...")

    if get_args.u:
        if Core.check_connection(url=get_args.u, session_get=session_get):
            crawler = Crawler()
            crawler.crawl(
                base=get_args.u,
                depth=int(get_args.depth),
                session_get=session_get
            )

    if get_args.output:
        root_path = pathlib.Path(__file__).parent
        file_path = root_path.joinpath(get_args.output)
        file_writer(path=file_path)


def file_writer(path):
    unique_dictionaries = []

    if TEMP_PATH_FOR_DATA.exists():
        data = TEMP_PATH_FOR_DATA.read_text()

        if data:
            dict_strings = data.strip().split("\n")
            dictionaries = [json.loads(d) for d in dict_strings]

            # Remove duplicates:
            unique_dictionaries = list({json.dumps(d): d for d in dictionaries}.values())

        TEMP_PATH_FOR_DATA.unlink(missing_ok=True)

    path.write_text(json.dumps(unique_dictionaries, indent=4))


if __name__ == "__main__":
    start()
