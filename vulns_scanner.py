import sys
import urllib3
from scanner import Scanner

if sys.version_info < (3, 0):
    sys.stderr.write("\nYou need python 3.0 or later to run this script\n")
    sys.stderr.write("Please update and make sure you use the command python3 vulns_scanner.py <url>\n\n")
    sys.exit(0)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  # disable warnings related to insecure requests
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/102.0.0.0 Safari/537.36'}  # It will send the request like browser
credentials = {"username": "admin", "password": "password", "Login": "submit"}
links_to_ignore = ["http://192.168.152.129/dvwa/logout.php"]


def main():
    if len(sys.argv) != 2:
        print("(+) Usage: %s <url>" % sys.argv[0])
        print("(+) Example: %s http://www.target-website.com" % sys.argv[0] + "\n")
        sys.exit(-1)
    url = sys.argv[1]
    vuln_scan = Scanner(url=url, ignore_links=links_to_ignore)
    vuln_scan.session.post(url="http://192.168.152.129/dvwa/login.php/", data=credentials, headers=HEADERS)
    vuln_scan.crawl()
    vuln_scan.run()


if __name__ == "__main__":
    main()
