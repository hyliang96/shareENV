#!/usr/bin/env python
# -*- coding: utf-8 -*-



ping_count = 10

import os
# import sys
# print (sys.version_info)

import json
from jsoncomment import JsonComment
# from pprint import pprint

import subprocess
import re
from tabulate import tabulate

# get absoltae path to the dir this is in
here = os.path.dirname(os.path.realpath(__file__))

# 从这个网站更新 aws-ips.json  http://ec2-reachability.amazonaws.com
with open(os.path.join(here, "aws-ips.json"), "r") as f:
    parser = JsonComment(json)
    city2ips = parser.load(f)


def dict_mean(dict, num):
    return { key: meter/num if num != 0 else float.nan for key, meter in dict.items() }

def dict_add(dict1, dict2):
    return { key: dict1[key] + dict2[key] for key in dict1.keys() }

city_times = {}
city_ip_num = {}

for city, ips in city2ips.items():
    print(city)
    city_times[city] = {'min':0.0, 'avg':0.0, 'max':0.0, 'stddev':0.0}
    city_ip_num[city] = 0

    for ip in ips:
        result = subprocess.run(['ping',  '-c', str(ping_count), ip], stdout=subprocess.PIPE).stdout.decode('utf-8')
        # output = result.stdout
        total = result.strip('\n').split('\n')[-1]
        re_result = re.search('[0-9.]+/[0-9.]+/[0-9.]+/[0-9.]+', total)
        if not re_result is None:
            start, end =  re_result.span()
            _min, _avg, _max, _stddev = map(float, total[start:end].split('/'))
            ip_times = {'min': _min, 'avg':_avg, 'max':_max, 'stddev':_stddev}

            city_times[city] = dict_add(city_times[city], ip_times)
            city_ip_num[city] += 1

            print('   ',ip, ip_times)

    city_times[city] = dict_mean(city_times[city], city_ip_num[city])
    print('   ', 'total:', city_ip_num[city], 'nodes', city_times[city])


print()
print(tabulate(
        [ [city, *list(times.values())] for city, times in city_times.items()],
        headers = list(next(iter(city_times.values())).keys())
    ))
# for city, times in city_times.items():
#     print(city, times)
