import re
from lxml import etree

fname = '../zhihu_backup/posts/西藏嘎措人民公社，为何70%牧民投票保护？-502340263.html'

def print_node(node):
    print(etree.tostring(node, pretty_print=True, encoding='unicode'))

def url_dezhihu(url):
    url = url.replace('https://link.zhihu.com/?target=', '')
    url = url.replace('%3A//', '://')
    return url

with open(fname, 'r') as f:
    text = f.read()

    title = re.search(r'<h1>(.+?)</h1>', text).group(1)
    print(title)

    url = re.search(r'<a href="(.+?)">原文链接</a>', text).group(1)
    print(url)

    time = re.findall(r'<div>(编辑于 .+?)</div>', text)[-1]
    print(time)

    parser = etree.XMLParser(remove_blank_text=True)
    content = etree.fromstring(text, parser=parser)
    content = content.xpath('//div[starts-with(@class, "RichText ztext Post-RichText")]')[0]

    content_list = content.xpath('//a[@class=" external"]')
    for c in content_list:
        url = url_dezhihu(c.attrib['href'])
        tag_url = f'<a>&lt;{url}&gt;</a>'
        new_c = etree.XML(tag_url)
        c.getparent().replace(c, new_c)


    content_list = content.xpath('//div[@class="RichText-LinkCardContainer"]')
    for c in content_list:
        c_ = etree.fromstring(etree.tostring(c), parser=parser)
        img_node = c_.xpath('//a[@href]')[0]
        url = url_dezhihu(img_node.attrib['href'])
        tag = img_node.attrib['data-text']
        tag_url = f'[{tag}]({url})'
        new_c = etree.XML(f'<p>{tag_url}</p>')
        c.getparent().replace(c, new_c)

    content_list = content.xpath('//figure')
    for c in content_list:
        c_ = etree.fromstring(etree.tostring(c), parser=parser)
        url = url_dezhihu(c_.xpath('//img[@src]')[0].attrib['src'])
        tag_url = f'![]({url})'
        new_c = etree.XML(f'<p>{tag_url}</p>')
        c.getparent().replace(c, new_c)
    # content = content.xpath('//div')   # ('(//div[@class="css-1yuhvjn"])')


# <a href="https://link.zhihu.com/?target=http%3A//www.cwzg.cn" class=" external" target="_blank" rel="nofollow noreferrer"><span class="invisible">http://www.</span><span class="visible">cwzg.cn</span><span class="invisible"/></a>


    # text = etree.HTML(text)
    content = etree.tostring(content, encoding='unicode')

    content = re.sub(r'\<div class="RichText ztext Post-RichText \>', '', content)
    content = re.sub(r'\</div\>', '', content)
    content = re.sub(r'\<p[^\>]*?\>', '\n', content)
    content = re.sub(r'\</p\>', '\n', content)
    content = content.replace('<br/>', '\n\n')
    content = content.replace('<b>', '**')
    content = content.replace('</b>', '**')
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    content = content.replace('<a>', '')
    content = content.replace('</a>', '')


    content = \
        f'{title}\n\n'+ \
        f'<{url}>\n\n'+ \
        f'编辑于: {time}\n\n' + \
        content

    print(content)



    # content = re.search(r'<div class=".+?">([\s\S]+)</div>', text).group(1)

    # <p data-pid="AcipohW1">其实， “摸着石头过河”来源于四川民间鬼怪故事：</p>