import subprocess
import re

# cmd='''curl http://ec2-reachability.amazonaws.com | grep -E '("panel-title"|"region-heading"|<tr> <td>)' | sed -E 's| +<h3 class="panel-title">(.+)</h3>|\1|g' | sed -E 's| +<th class="region-heading" colspan="4">(.+)</th>|  \1|g' | sed -E 's| +<tr> <td>(.+)</td> <td>.+</td> <td>(.+)</td> <td id="test">.+</tr>|    \1 \2|g' '''

cmd='''curl http://ec2-reachability.amazonaws.com'''
result=subprocess.call(cmd, shell=True)
searchObj = re.search(r'\<h3 class\="panel-title"\>(.+)\<\/h3\>', result)
print(searchObj.group(1))