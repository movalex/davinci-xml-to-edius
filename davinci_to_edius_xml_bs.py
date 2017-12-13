from urllib.request import urlparse, url2pathname
from urllib.parse import unquote
from bs4 import BeautifulSoup
import re

def parse_path(fpath):
    parsed = urlparse(fpath)
    i = parsed.path.index("/", 1)
    fix_path = parsed.path[:i].replace('/','')
    parsed = parsed._replace(netloc=fix_path)
    return parsed.geturl()

orig_prettify = BeautifulSoup.prettify
r = re.compile(r'^(\s*)', re.MULTILINE)
def prettify(self, encoding=None, formatter="minimal", indent_width=4):
    return r.sub(r'\1' * indent_width, orig_prettify(self, encoding, formatter))
BeautifulSoup.prettify = prettify

with open('riccipovery8_v1 (Resolve).xml', 'r', encoding='utf-8') as xml_file:
    soup = BeautifulSoup(xml_file, "html.parser")
    usr_list = soup.find_all('pathurl')
    for tag in usr_list:
        newtag = parse_path(tag.text)
        tag.string = newtag
    bs_output = soup.prettify(indent_width=4)

with open('bs_output.xml' , 'w', encoding='utf-8') as out:
    print(bs_output, file=out)
