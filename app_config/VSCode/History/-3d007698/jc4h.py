from subprocess import Popen, PIPE

import re

# cmd='''curl http://ec2-reachability.amazonaws.com | grep -E '("panel-title"|"region-heading"|<tr> <td>)' | sed -E 's| +<h3 class="panel-title">(.+)</h3>|\1|g' | sed -E 's| +<th class="region-heading" colspan="4">(.+)</th>|  \1|g' | sed -E 's| +<tr> <td>(.+)</td> <td>.+</td> <td>(.+)</td> <td id="test">.+</tr>|    \1 \2|g' '''

cmd='''curl http://ec2-reachability.amazonaws.com'''

pro = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
out, err = [i.decode('utf-8') for i in pro.communicate()]
# print(out)
# print(err)

pattern = r' +<h3 class="panel-title">(.+)</h3>| +<th class="region-heading" colspan="4">(.+)</th>| +<tr> <td>(.+)</td> <td>.+</td> <td>(.+)</td> <td id="test">.+</tr>'
searched = re.findall(pattern, out)

ips = {}
for item in searched:
    if item[0] != '':
        continent = item[0]
    elif item[1] != '':
        nation = item[1]
    else:
        region_code = item[2]
        ip = item[3]
    ips[continent+' '+nation+' '+region_code]= ip

print(ips)