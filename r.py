import requests as rqs
from bs4 import BeautifulSoup as bsp
blocks = {  # texts // str
    'title': '',
    'content': '', #0
    'input': '', #1
    'output': '', #2
    'sample_input': '', #3
    'sample_output': '', #4
    'hint': '', #5
}
def process_textp(content, pkeys: list, name: str): # 題目敘述/輸入說明/說出說明/提示
    pkeys_id = 0
    for id in [0, 1, 2, 5]:
        i = content[id]
        ok = False
        data = i.find_all(name=name)
        if len(data) != 0:
            for j in data:
                img = j.find(name='img')
                if not (img is None):
                    blocks[pkeys[pkeys_id]] +=(({img.get('src')})+'\n\n')
                else :
                    blocks[pkeys[pkeys_id]] += (j.text.strip('#')+'\n\n')
                ok = True
        else:
            blocks[pkeys[pkeys_id]] += i.text.strip('#') + '\n\n'
            ok=True
        if ok:
            pkeys_id += 1
def process_textpre(content, pkeys: list, name: str):
    pkeys_id = 0
    for i in content:
        ok = False
        text = '```\n'
        for j in i.find_all(name=name):
            text_list = j.text.strip().split('\n')
            for t in text_list:
                text += t.strip() + '\n'
            ok = True

        if ok:
            blocks[pkeys[pkeys_id]] += text + '```\n'
            pkeys_id += 1
def process_title(content): #題目名稱
    material = content.find_all(name='div', attrs={'class', 'h1'})
    blocks['title'] = material[0].text[0:5] + ' ' + material[0].find(name='span').text
def main():
    pid = 'a520'
    url = 'http://203.64.191.163/ShowProblem?problemid={}'
    response = rqs.get(url.format(pid))
    html = bsp(response.text, 'html.parser')
    content = html.find_all(name='div', attrs={'class', 'problembox'})
    process_textp(content, ['content', 'input', 'output', 'hint'], 'p')
    process_textpre(content, ['sample_input', 'sample_output'], 'pre')
    process_title(html)
    print(blocks)
   
if __name__ == '__main__':
    main()