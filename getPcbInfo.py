# -*- coding: utf-8 -*-
__author__ = 'Yu Sun'

import re
from urllib.request import urlopen

from bs4 import BeautifulSoup

# To avoid problems induced by JavaScript, this html file is downloaded from http://datasets.pacb.com.s3.amazonaws.com/2014/Iso-seq_Human_Tissues/list.html.
all_the_text = open('tissues.html').read()
bs_obj = BeautifulSoup(all_the_text, 'lxml')
links = bs_obj.find_all("a", href=re.compile('.xml'))
with open("data_info", "w") as f:
    f.write("Cell ID\tTissue\tLibrary size\tBinding Kit\n")
    for link in links:
        child_link = link.attrs.get('href')
        cell_id = "_".join(child_link.split('/')[7].split("_")[:-2])
        tissue = child_link.split('/')[6]
        while True:
            try:
                html = urlopen(child_link)
                child_obj = BeautifulSoup(html, 'lxml')
                sample_name = child_obj.select("sample name")[0].get_text()
                child_name_info = re.split('_|\s+', sample_name)
                lib_size = re.search(r'(\d+-\d+)kb', "".join(child_name_info)).group(1) + ' Kbp'
                kit = child_name_info[-1]
                f.writelines('\t'.join([cell_id, tissue, lib_size, kit]) + '\n')
            except:
                print("Waiting for retry", cell_id, "...")
                continue
            print("Success: ", cell_id, "is done.")
            break
