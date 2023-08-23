import argparse
from helper import agent

parse = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, usage="PwnXSS -u <target> [options]",
                                add_help=False)

pos_opt = parse.add_argument_group("Options")
pos_opt.add_argument("--help", action="store_true", default=False, help="Show usage and help parameters")

pos_opt.add_argument("-u", metavar="", help="Target url (e.g. http://testphp.vulnweb.com)")
pos_opt.add_argument("--depth", metavar="", help="Depth web page to crawl. Default: 2", default=2)

# Leave as default:

pos_opt.add_argument("--payload", metavar="",
                     help="Load custom payload directly (e.g. <script>alert(2005)</script>)", default=None)

pos_opt.add_argument("--user-agent", metavar="", help="Request user agent (e.g. Chrome/2.1.1/...)", default=agent)
pos_opt.add_argument("--single", metavar="", help="Single scan. No crawling just one address")
pos_opt.add_argument("--proxy", default=None, metavar="",
                     help="Set proxy (e.g. {'https':'https://10.10.1.10:1080'})")
pos_opt.add_argument("--about", action="store_true", help="Print information about PwnXSS tool")
pos_opt.add_argument("--cookie", help="Set cookie (e.g {'ID':'1094200543'})", default='''{"ID":"1094200543"}''',
                     metavar="")

# Add output to json file
pos_opt.add_argument("--output", help="Set JSON file output", default="result.json")


# Delete later (won't use)
pos_opt.add_argument("--payload-level", metavar="",
                     help="Level for payload Generator, 7 for custom payload. {1...6}. Default: 6", default=6)
pos_opt.add_argument("--method", metavar="",
                     help="Method setting(s): \n\t0: GET\n\t1: POST\n\t2: GET and POST (default)", default=2,
                     type=int)
