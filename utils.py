
import re
from collections import defaultdict
import csv
from bs4 import BeautifulSoup, Tag

def extract_and_remove(content, pattern, extract=False):
    """

    Args:
        content (str): text to apply pattern 
        pattern (str): regex pattern to extract or remove
        extract (bool, optional): extract the text based on the pattern

    Returns:
        str: extracted or removed text
    """
    if extract:
        match = re.search(pattern, str(content), re.IGNORECASE | re.DOTALL)
        return match.group() 
    # r'\1' replace  the entire match capture by  (.*?)
    content= re.sub(pattern, r'\1', str(content), flags=re.IGNORECASE | re.DOTALL)
    return  content

def extract_all_between(content, pattern):
    """

    Args:
        content (str): text to apply pattern 
        pattern (str): regex pattern to extract all the matches text  

    Returns:
        list: all extracted content in list
    """
    # Using re.findall to get all matches
    return re.findall(pattern, str(content), re.IGNORECASE | re.DOTALL)

def extract_before_language(text):
    
    pattern = re.compile(r'(.*?)(?=\s*(?:<span dir="ltr">|<span class="desc-text">))', re.UNICODE)
    match = pattern.search(text)
    if match:
        return match.group(1).strip()
    return text

def nested_defaultdict():
    """
      Allows to create Nested dictionary  
    """
    return defaultdict(nested_defaultdict)

def extract_health_info(info_content, health_info_dicn):
    """

    Args:
        info_content (list): list of html content return by soup.find_all()
        health_info_dicn (dict): nested dictionary

    Returns:
        dict: nested dictionary updated with content
    """
    h3_between_pattern = r'<h3[^>]*>(.*?)</h3>(.*?)(?=<h3[^>]*>.*?</h3>|$)'
    
    head_pattern = r'<h\d+.*?>(.*?)</h\d+>'
    
    anchor_pattern = r'<a.*?>(.*?)</a>'
    
    link_pattern = r'https://[^\s"\'<>]*(?:\.pdf|/download)'
    
    
    for sec in info_content:
            if isinstance(sec, Tag):
                
                head= sec.find('h2')
                head = extract_and_remove(head, head_pattern)
                
                if head :
                    h3_groups = extract_all_between(sec, h3_between_pattern)

                    for  h3_content in  h3_groups:
                        main_dises = h3_content[0]

                        sub_dises = extract_all_between(h3_content[1], anchor_pattern)
                        links = extract_all_between(h3_content[1], link_pattern)

                        for sub_dis, link in zip(sub_dises,links):
                            sub_dis = extract_before_language(sub_dis)
                            health_info_dicn[head][main_dises][sub_dis] = link
            else:
                print("Please provide a list with bs4.element.Tag item type or returned by soup.find_all()")
                return
               
    return health_info_dicn
  
        
def flatten_dict(d, parent_key='', sep='|'):
    """

    Args:
        d (dict): nested dictionary
        parent_key (str, optional): _description_. Defaults to ''.
        sep (str, optional):  Defaults to '|'.

    Returns:
        dict: flattened dictionary
    """
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            fl_dict = flatten_dict(v, new_key, sep=sep).items()
            items.extend(fl_dict)
        else:
            items.append((new_key, v))
    return dict(items)




def convert_to_csv(dictionary,csv_file, compress=False):
    """_summary_

    Args:
        dictionary (dict): dictionary to convert to csv file
        csv_file (str): csv file name
        compress (bool, optional):  Defaults to False.

    Returns:
        file: csv file
    """
    csv_data = []
    
    if isinstance(dictionary, dict):
        if compress:
            with open(csv_file, mode='wt', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=['Disease heading', 'pdf_link'])
                writer.writeheader()
                for k, v in dictionary.items():
                       writer.writerow({'Disease heading': k, 'pdf_link': v})
            print(f"converted to csv, file : {csv_file}")
            return csv_file

        for key, value in dictionary.items():
                keys = key.split('|')
                row =  {'Alphabet': keys[0], 'Main disease heading': keys[1] if len(keys) > 1 else '', 'sub disease heading': keys[2] if len(keys) > 2 else '', 'pdf_link': value}
                csv_data.append(row)
        
        with open(csv_file, mode ='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=['Alphabet', 'Main disease heading', 'sub disease heading', 'pdf_link'] )
            writer.writeheader()
            for row in csv_data:
                writer.writerow(row)
        print(f"converted to csv, file : {csv_file}")
        return csv_file
    
    else:
        print("The given input is not dictionary , please provide dict")
        
    
