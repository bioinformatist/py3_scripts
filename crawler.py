import re
from urllib.request import urlopen

from bs4 import BeautifulSoup

url = 'http://rice.plantbiology.msu.edu/annotation_community_families.shtml'
html = urlopen(url)
# print(html.read().decode(encoding='utf8'))
bs_obj = BeautifulSoup(html, 'html.parser')
# print(bs_obj.prettify())
# print(bs_obj.title)
# print(bs_obj.h1.get_text())

for link in bs_obj.find_all(href=re.compile('ca/gene_fams/')):
    print(link)
