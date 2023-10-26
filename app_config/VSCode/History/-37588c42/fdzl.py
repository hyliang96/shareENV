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
    content = data['initialState']['entities']['answers'][answer_id]['content']
    # 提取url
    video_urls = re.findall(r'(https://www.zhihu.com/zvideo/\d+)', content)

    return video_urls
