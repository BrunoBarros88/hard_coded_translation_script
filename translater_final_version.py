import glob
import os

from bs4 import BeautifulSoup
from mtranslate import translate

#Pass the folder path where the HTML you want to translate are placed
folder_path = r'C:\example\example\example'
#Place the data-translate="false" attribute on the HTML elements you dont want to be translated
global_exclude = 'data-translate="false"'
# Looping over all HTML files in the folder, getting the elements to be translated, and skipping images and other global_exclude elements
for file_path in glob.glob(os.path.join(folder_path, '*.html')):
    with open(file_path, encoding='utf-8') as f:
        html_content = f.read()

    soup = BeautifulSoup(html_content, 'lxml')
    tags_to_translate = ['h2', 'p', 'title', 'button', 'h3', 'span', 'a', 'strong', 'h1']
    elements_to_translate = soup.find_all(tags_to_translate)

    for img in soup.find_all('img'):
        img['data-translate'] = 'false'

    for element in elements_to_translate:
        if global_exclude in str(element):
            continue  
        else:
            text_to_translate = element.text
            translated_text = translate(text_to_translate, 'hi')
            new_tag = soup.new_tag(element.name, attrs=element.attrs)
            new_tag.string = translated_text
            if element.parent:
                element.replace_with(new_tag)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
