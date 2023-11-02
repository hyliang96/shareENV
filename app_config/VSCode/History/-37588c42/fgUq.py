# https://github.com/jinl1874/spider/tree/master/zhihu_video

import requests
import re
import json


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:83.0) Gecko/20100101 Firefox/83.0'
}


def get_video_urls(url):
    res = requests.get(url, headers=headers)
    # 获取答案url上的id
    answer_id = re.findall(r'answer/(\d+)', url)[0]

    # 获取json文本
    text = res.text
    json_text = re.findall(
        r'<script id="js-initialData" type="text/json">(.*?)</script>', text)[0]

    # 提取答案的content文件。
    data = json.loads(json_text)
    # print(data['initialState']['entities']['answers'][answer_id]['content'])
    content = data['initialState']['entities']['answers'][answer_id]['content']
    print(content)
    # 提取url
    video_urls = re.findall(r'(https://www.zhihu.com/video/\d+)', content)
    return video_urls

def get_name_url(url):
    res = requests.get(url, headers=headers)
    data = json.loads(res.text)
    video_url = data["SD"]
    # LD（标清）, SD（高清）, HD（超清）

# def get_name_url(url):
#     get_video_url = 'https://lens.zhihu.com/api/v4/videos/{}'
#     # 找到 json_url 的id
#     res = requests.get(url, headers=headers)
#     print(res.text)
#     url = re.findall(
#         '<iframe class="ZVideo-player" src=\"(.*?)\"', res.text)[0]
#     video_id = re.findall(r'/video/(\d+)', url)[0]
#     # 合并
#     json_url = get_video_url.format(video_id)

#     # 获取真实的视频url
#     res = requests.get(json_url, headers=headers)
#     data = json.loads(res.text)
#     # 可选 LD 和 SD，不过一般选最清晰的 HD
#     HD_url = data['playlist']['HD']['play_url']

#     title = data['title']
#     video_name = title + '.mp4'
#     return video_name, HD_url


def save(name, url):
    res = requests.get(url, headers=headers)
    with open(name, 'wb') as fp:
        fp.write(res.content)


def main():
    url = 'https://www.zhihu.com/question/391948709/answer/1205530203'
    urls = get_video_urls(url)
    print('urls', urls)
    for i in urls:
        name, HD_url = get_name_url(i)
        save(name, HD_url)


if __name__ == "__main__":
    main()


# ————————————————
# 版权声明：本文为CSDN博主「polyhedronx」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
# 原文链接：https://blog.csdn.net/polyhedronx/article/details/81610734

# import os
# import re
# import json
# import requests
# from requests import RequestException
# from pyquery import PyQuery as pq


# def get_page(url):
#     try:
#         headers = {
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
#         }
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code == 200:
#             return response.text
#         return None
#     except RequestException:
#         return None


# def parse_page(html):
#     doc = pq(html)
#     items = doc('.url').items()
#     for item in items:
#         yield item.text()


# def get_real_url(url, try_count=1):
#     if try_count > 3:
#         return None
#     try:
#         headers = {
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
#         }
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code >= 400:
#             return get_real_url(url, try_count+1)
#         return response.url
#     except RequestException:
#             return get_real_url(url, try_count+1)


# def get_m3u8_url(url):
#     try:
#         path_pattern = re.compile('(\d+)', re.S).search(url).group(1)
#         get_play_url = 'https://lens.zhihu.com/api/videos/' + path_pattern
#         headers = {
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
#         }
#         content = requests.get(get_play_url, headers=headers).text
#         data = json.loads(content)  # 将json格式的字符串转化为字典
#         if data and 'playlist' in data.keys():
#             m3u8_url = data.get('playlist').get('sd').get('play_url')
#             return m3u8_url
#     except Exception:
#         return None


# def get_m3u8_content(url, try_count=1):
#     if try_count > 3:
#         print('Get M3U8 Content Failed', url)
#         return None
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
#     }
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code == 200:
#             return response.text
#         return get_m3u8_content(url, try_count+1)
#     except RequestException:
#         return get_m3u8_content(url, try_count+1)


# def get_ts(url, try_count=1):
#     if try_count > 3:
#         print('Get TS Failed', url)
#         return None
#     headers = {
#         'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.75 Safari/537.36'
#     }
#     try:
#         response = requests.get(url, headers=headers, timeout=10)
#         if response.status_code == 200:
#             return response
#         return get_ts(url, try_count+1)
#     except RequestException:
#         return get_ts(url, try_count+1)


# def download_ts(m3u8_url, video_url, video_count):
#     print('准备下载', video_url)
#     download_path = 'E:/PycharmProjects/zhihu_vedio/'
#     try:
#         all_content = get_m3u8_content(m3u8_url)
#         file_line = all_content.split('\n')  # 读取文件里的每一行
#         # 通过判断文件头来确定是否是M3U8文件
#         if file_line[0] != '#EXTM3U':
#             raise BaseException('非M3U8链接')
#         else:
#             unknow = True  # 用来判断是否找到了下载的地址
#             for index, line in enumerate(file_line):
#                 if "EXTINF" in line:
#                     unknow = False
#                     # 拼出ts片段的URL
#                     pd_url = m3u8_url.rsplit('/', 1)[0] + '/' + file_line[index + 1]  # rsplit从字符串最后面开始分割
#                     response = get_ts(pd_url)
#                     c_fule_name = str(file_line[index + 1]).split('?', 1)[0]
#                     source_path = c_fule_name.split('-', 1)[0]  # 区分不同源的视频流
#                     print('正在下载', c_fule_name)
#                     with open(download_path + c_fule_name, 'wb') as f:
#                         f.write(response.content)
#                         f.close()
#             if unknow:
#                 raise BaseException('未找到对应的下载链接')
#             else:
#                 print('下载完成，准备合并视频流...')
#                 merge_file(download_path, source_path, video_count)
#     except Exception:
#         return None


# def merge_file(download_path, source_path, video_count):
#     os.chdir(download_path)  # 修改当前工作目录
#     merge_cmd = 'copy /b ' + source_path + '*.ts video' + str(video_count) + '_' + source_path + '.mp4'
#     split_cmd = 'del /Q ' + source_path + '*.ts'
#     os.system(merge_cmd)
#     os.system(split_cmd)


# def main():
#     url = 'https://www.zhihu.com/question/279405182/answer/410204397'  # 含有知乎小视频的链接
#     html = get_page(url)
#     video_count = 0
#     if html:
#         video_urls = parse_page(html)
#         for video_url in video_urls:
#             if video_url:
#                 real_url = get_real_url(video_url)
#                 if real_url:
#                     m3u8_url = get_m3u8_url(real_url)
#                     if m3u8_url:
#                         video_count += 1
#                         download_ts(m3u8_url, video_url, video_count)


# if __name__ == '__main__':
#     main()
