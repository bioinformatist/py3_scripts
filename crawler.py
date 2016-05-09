import os
import re
import sys
from urllib.request import urlopen

from bs4 import BeautifulSoup

# print(html.read().decode(encoding='utf8'))
# print(bs_obj.prettify())

family_list = {}


def get_super_families():
    global family_list
    url = 'http://rice.plantbiology.msu.edu/annotation_community_families.shtml'
    html = urlopen(url)
    bs_obj = BeautifulSoup(html, 'html.parser')
    summaries = bs_obj.find_all("table", class_="summary")
    for summary in summaries:
        superfamily_name = summary.contents[1].get_text().strip().replace('/', ' or ')
        os.mkdir(superfamily_name)
        family_table = summary.find_next("table")
        relative_family_links = family_table.find_all(href=re.compile('ca/gene_fams/'))
        for relative_family_link in relative_family_links:
            family_name = relative_family_link.get_text().strip().replace('/', ' or ')
            absolute_link = 'http://rice.plantbiology.msu.edu' + relative_family_link.attrs.get('href')
            family_list.setdefault(superfamily_name, {})
            family_list[superfamily_name][family_name] = absolute_link
            # family_list[superfamily_name].append(absolute_link)


def get_family_info(**kwargs):
    for k, v in kwargs.items():
        main_path = os.path.split(os.path.realpath(sys.argv[0]))[0]
        current_path = os.path.join(main_path, k)
        os.chdir(current_path)
        for k1, v1 in v.items():
            with open(k1 + '.txt', 'w', encoding='utf8') as f:
                f.write("ID\tGene Description\tMSU Annotation\n")
                html = urlopen(v1)
                bs_obj = BeautifulSoup(html, 'html.parser')
                # print(bs_obj.prettify())
                gene_ids = bs_obj.find_all(href=re.compile("/cgi-bin/gbrowse/rice\?name"))
                for gene_id in gene_ids:
                    if gene_id.find_next(text="Gene Description:"):
                        gene_description = gene_id.find_next(text="Gene Description:").find_next().get_text()
                    else:
                        gene_description = 'NA'
                    gene_annotation = gene_id.find_next(text="MSU Annotation:").find_next().get_text()
                    gene_info = '\t'.join([gene_id.get_text(), gene_description, gene_annotation])
                    f.writelines(gene_info + '\n')


if __name__ == '__main__':
    get_super_families()
    get_family_info(**family_list)
