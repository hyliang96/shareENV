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

        # <div class="RichText-LinkCardContainer">
        #   <a target="_blank" href="https://link.zhihu.com/?target=https%3A//m.sohu.com/a/260190128_425345/%3Fpvid%3D000115_3w_a" data-draft-node="block" data-draft-type="link-card" data-text="西藏嘎措人民公社，为何70%牧民投票保护？_集体" class="LinkCard new css-1wr1m8" data-image="https://pic1.zhimg.com/v2-a7b13c820bd5bba871fa6b5750fc59e0_180x120.jpg" data-image-width="1080" data-image-height="810" data-za-detail-view-id="172">
        #     <span class="LinkCard-contents">
        #       <span class="LinkCard-title two-line">西藏嘎措人民公社，为何70%牧民投票保护？_集体</span>
        #       <span class="LinkCard-desc"><span style="display: inline-flex; align-items: center;">​<svg width="14" height="14" viewbox="0 0 24 24" data-new-api="Link24" data-old-api="InsertLink" class="Zi Zi--InsertLink" fill="currentColor"><path d="M5.327 18.883a3.005 3.005 0 010-4.25l2.608-2.607a.75.75 0 10-1.06-1.06l-2.608 2.607a4.505 4.505 0 006.37 6.37l2.608-2.607a.75.75 0 00-1.06-1.06l-2.608 2.607a3.005 3.005 0 01-4.25 0zm5.428-11.799a.75.75 0 001.06 1.06L14.48 5.48a3.005 3.005 0 014.25 4.25l-2.665 2.665a.75.75 0 001.061 1.06l2.665-2.664a4.505 4.505 0 00-6.371-6.372l-2.665 2.665zm5.323 2.117a.75.75 0 10-1.06-1.06l-7.072 7.07a.75.75 0 001.061 1.06l7.071-7.07z" fill-rule="evenodd" clip-rule="evenodd"/></svg></span>m.sohu.com/a/260190128_425345/?pvid=000115_3w_a</span>
        #     </span>
        #     <span class="LinkCard-image" style="height: 60px;">
        #       <img src="https://pic1.zhimg.com/v2-a7b13c820bd5bba871fa6b5750fc59e0_180x120.jpg" alt=""/>
        #     </span>
        #   </a>
        # </div>

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
        url = img_node.attrib['href']
        tag = img_node.attrib['data-text']
        tag_url = f'[{tag}]({url})'
        new_c = etree.XML(f'<p>{tag_url}</p>')
        c.getparent().replace(c, new_c)

    content_list = content.xpath('//figure')
    for c in content_list:
        c_ = etree.fromstring(etree.tostring(c), parser=parser)
        url = c_.xpath('//img[@src]')[0].attrib['src']
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
    print(content)



    # content = re.search(r'<div class=".+?">([\s\S]+)</div>', text).group(1)

    # <p data-pid="AcipohW1">其实， “摸着石头过河”来源于四川民间鬼怪故事：</p>