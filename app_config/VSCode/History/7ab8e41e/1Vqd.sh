# get absoltae path to the dir this is in, work in bash, zsh
# if you want transfer symbolic link to true path, just change `pwd` to `pwd -P`

# 请先按照依赖
# `pip3 install git+https://github.com/hyliang96/zhihubackup`



testtype='**'
testfile='*'


here=$(cd "$(dirname "${BASH_SOURCE[0]-$0}")"; pwd)
zhihu_backup_dir="$here/../zhihu_backup"
zhihu_html_dir="${zhihu_backup_dir}/html"
markdown_dir="${zhihu_backup_dir}/markdown"


python "${here}/zhihu_selenium.py"

TMPFILE=$(mktemp -p . --suffix .html)

trap 'onCtrlC' INT
function onCtrlC () {
    [ -f "${TMPFILE}"  ] && rm "${TMPFILE}"
    exit 0
}


add_to_head()
{
    local temp=$(mktemp)
    echo -n "${1}" | cat - "${2}" > "${temp}" && mv "${temp}" "${2}"
}


n_total=$(ls -1 "${zhihu_html_dir}"/${testtype}/${testfile}.html | wc -l)

n=0

for file in "${zhihu_html_dir}"/${testtype}/${testfile}.html; do

    n=$(( 1 + $n ))

    relative_file="$(realpath --relative-to="${zhihu_html_dir}" "${file}")"

    relative_dir="$(dirname "${relative_file}")"
    filename=$(basename "${file}")

    # [ "${filename}" != '1466837763412307968.html' ] && continue
    echo "$n / ${n_total} | ${relative_file}"


    file_out_dir="${markdown_dir}/${relative_dir}/${filename/.html/.textbundle}"
    mkdir -p "${file_out_dir}"
    file_out="${file_out_dir}/text.markdown"
    mkdir -p "${file_out_dir}/assets"
    ln -sfT assets "${file_out_dir}/text"
    file_out_dir="$(dirname "${file_out}")"

    id="$(echo "${filename}" | grep -oE '^[0-9]+')"
    type="$(basename "${relative_dir}")"
    # url="https://www.zhihu.com/${type}/${id}"


    mkdir -p "${file_out_dir}"

    cp "${file}" "${TMPFILE}"

    perl -i -pe 'BEGIN{undef $/;} s|(\<div class="RichText ztext PinItem-remainContentRichText"\>[\n ]*?\<div class="RichText ztext css-2ncmcq" options="\[object Object\]"\>[\n ]*?\<a data-first-child="" target="_blank" )(href=".+?").+?data-text="(.+?)"(.+?\>)|<a \2>\3</a>\n\1\4|smg' "${TMPFILE}"
    perl -i -pe 'BEGIN{undef $/;} s|\<div class="css-.+?"\>[\n ]+\<div class="Catalog.+?(\</div\>[\n ]+?){6}||smg' "${TMPFILE}"

    pandoc -s "${TMPFILE}" -o "${file_out}"



    [[ "${type}" =~ ^(article|answer)$ ]] && add_to_head '# ' "${file_out}"

    sed -i '' 's|\\$|'$'\\\n''|g' "${file_out}"

    [ ${type} == pin ] && sed -i '' -E  's/(https\:\/\/[a-zA-Z0-9]+\.zhimg\.com\/[a-zA-Z0-9\.\/\_\-]+)/'$'\\\n''\!\[\]\(\1\)/g' "${file_out}"
    perl -i -pe 'BEGIN{undef $/;} s|\{\.(origin_image\|content_image).+?\}||smg' "${file_out}"   # 跨行匹配，非贪婪

    # 通用
    perl -i -pe  's|\[(.+?)\!\[\]\(data:.+?\)\{\..+?\}\]\((.+?)\)(\{.+?\})?|[\1](\2)|g' "${file_out}" # 名词解释的超链接

    # asks
    perl -i -pe 'BEGIN{undef $/;} s|\[ \]\{\.RichText[ \n].+?itemprop="text"\}||smg' "${file_out}" # 名词解释的超链接

    # answers
    perl -i -pe 'BEGIN{undef $/;} s|\[\n*\]\{\.RichText[\n ].+?\}||smg' "${file_out}"   # 跨行匹配，非贪婪

    # posts
    perl -i -pe 'BEGIN{undef $/;} s|::: css-[0-9a-zA-Z]+\n::: \{\.RichText[\n ].+?\}\n||smg' "${file_out}"  # 跨行匹配，非贪婪

    perl -i -pe 'BEGIN{undef $/;} s|::: RichText-LinkCardContainer[ \n].+?\.LinkCard-image--default\}\]||smg' "${file_out}"   # 跨行匹配，非贪婪
    perl -i -pe 'BEGIN{undef $/;} s|::: RichText-ZVideoLinkCardContainer[ \n].+?\.LinkCard-image--default\}\]||smg' "${file_out}"   # 跨行匹配，非贪婪
    perl -i -pe 'BEGIN{undef $/;} s|\{\.LinkCard[ \n].+?\}(\n:::)+||smg' "${file_out}"   # 跨行匹配，非贪婪

    perl -i -pe 'BEGIN{undef $/;} s|::: RichText-LinkCardContainer\n\[\[[ \n]||smg' "${file_out}"
    perl -i -pe 'BEGIN{undef $/;} s|\{\.LinkCard-title[ \n].+?\}[ \n]+?\[\[.+?{\.LinkCard-contents\}\]||smg' "${file_out}"
    perl -i -pe 'BEGIN{undef $/;} s|\{\.LinkCard-title[ \n].+?\}[ \n]+?\[\[.+?{\.LinkCard-image[ \n]style="height: \d+px;"\}\]||smg' "${file_out}"

    # pins
    # 结尾
    perl -i -pe 'BEGIN{undef $/;} s|\<\/div\>\n+?(\<div\>\n+?)?::: \{\.ContentItem-actions[\n ].+?\}.+:::||smg' "${file_out}"   # 跨行匹配，非贪婪
    perl -i -pe 'BEGIN{undef $/;} s|\<\/div\>\n+?(\<div\>\n+?)?::: ContentItem-actions.+:::||smg' "${file_out}"   # 跨行匹配，非贪婪

    # # 时间
    perl -i -pe 'BEGIN{undef $/;} s|::: ContentItem-time\n\[\[|\n|smg' "${file_out}"   # 跨行匹配，非贪婪
    perl -i -pe 'BEGIN{undef $/;} s|\]\{tooltip="发布于.+?\}\]\(//www.zhihu.com/pin/[0-9]+\)\n:::||smg' "${file_out}"   # 跨行匹配，非贪婪

    # # 图片
    perl -i -pe  's|::: Image-Wrapper-Preview||g' "${file_out}"
    perl -i -pe 'BEGIN{undef $/;} s|::: \{\.Thumbnail-Wrapper .+?\[||smg' "${file_out}"   # 跨行匹配，非贪婪
    perl -i -pe 'BEGIN{undef $/;} s|\{\.Image-Preview.+?\{\.Image-PreviewVague\}.*?([\n ]?:::)+||smg' "${file_out}"   # 跨行匹配，非贪婪

    # 开头
    perl -i -pe 'BEGIN{undef $/;} s|::: RichContent-inner\n\[||smg' "${file_out}"   # 跨行匹配，非贪婪
    perl -i -pe 'BEGIN{undef $/;} s|::: RichContent-inner\n+?:::\n+||smg' "${file_out}"   # 跨行匹配，非贪婪

    # 内容
    perl -i -pe 'BEGIN{undef $/;} s|::: \{\.RichText[\n ].+?\}\n::: \{\.RichText.+?\}.+?:::\n:::||smg' "${file_out}"  # 知乎视频引用
    perl -i -pe 'BEGIN{undef $/;} s|::: \{\.RichText[\n ].+?\}([ \n]?:::)?||smg' "${file_out}"   # 跨行匹配，非贪婪
    perl -i -pe 'BEGIN{undef $/;} s|\]\{\.RichText[\n ].+?itemprop="text"\}([ \n]?:::)?||smg' "${file_out}"   # 跨行匹配，非贪婪

    perl -i -pe 'BEGIN{undef $/;} s|\[ *\]\{\.UserLink\}[ \n]*?::: css-.+?[ \n]*?(\[.+?\]\(.+?\))\{\.UserLink-link\}[ \n]?:::|\1|smg' "${file_out}"   # 艾特知乎用户
    perl -i -pe 'BEGIN{undef $/;} s|::: \{\.PinItem-RichText \.PinItem-content-originpin\}|转载想法：|smg' "${file_out}"   # 转载想法
    perl -i -pe 'BEGIN{undef $/;} s|::: RichContent||smg' "${file_out}"
    perl -i -pe 'BEGIN{undef $/;} s|::: VideoCard-mask||smg' "${file_out}"

    #
# ::: {.RichText-video za-detail-view-path-module="VideoItem" za-extra-module="{\"card\":{\"content\":{\"type\":\"Video\",\"sub_type\":\"SelfHosted\",\"video_id\":\"1506121028279791616\",\"is_playable\":true}}}"}
# ::: {.VideoCard .VideoCard--interactive}
# ::: VideoCard-layout
# ::: VideoCard-video
# ::: VideoCard-video-content
# ::: VideoCard-player


    perl -i -pe 's|\<div\>||smg' "${file_out}"
    perl -i -pe 's|\<\/div\>||smg' "${file_out}"

    sed -i '' -E 's|\\@|@|g' "${file_out}"
    sed -i '' -E 's| | |g' "${file_out}"

    perl -i -pe 's|(?<!\])\((https?\:\/\/.+?)\)|<\1>|g' "${file_out}"

    perl -i -pe 'BEGIN{undef $/;} s|:::\n|\n|smg' "${file_out}"   # 跨行匹配，非贪婪

    perl -i -pe 'BEGIN{undef $/;} s|(?<!\n)\n------\n(?!\n)|——|smg' "${file_out}"

    perl -i -pe 's|(https\:\/\/vdn\d*\.vzuu\d*\.com\/[A-Za-z0-9.?_=&\/\-]+)|<video width="100%" height="600" controls><source src="\1" type="video/mp4"></video>|g' "${file_out}"

    sed -i '' -E  's|https?\:\/\/link\.zhihu\.com\/\?target\=([a-z]+)%3A\/\/|\1://|g' "${file_out}"
    perl -i -pe 's/\[(\[[-A-Za-z0-9+&@#\/%?=~_|!:,.;]*\]\{\.(visible|invisible|ellipsis)\})+\]\(((https?|ftp|file):\/\/[-A-Za-z0-9+&@#\/%?=~_|!:,.;]+[-A-Za-z0-9+&@#\/%=~_|])\)(\{\.external\})?/\n\3/g' "${file_out}"
    sed -i '' -E 's|\?source=[0-9a-z]+||g' "${file_out}"
    perl -i -pe 'BEGIN{undef $/;} s|\{(\.internal\|\.wrap[> \n]+\.external\|\.hash_tag\|\.member_mention\|eeimg="[0-9]+")\}||smg' "${file_out}"
    python "${here}/replace_equation.py" "${file_out}"

    perl -i -pe 'BEGIN{undef $/;} s|\n{3,}|\n\n|smg' "${file_out}"
done


for file_out_dir in "${markdown_dir}"/${testtype}/${testfile}.textbundle; do
    echo $file_out_dir
    file_out="${file_out_dir}/text.markdown"
    for i in $(cat "${file_out}" | grep -E '\!\[\]\(https\:\/\/.+?\.zhimg\.com\/(.+?)\)' | perl -pe 's|\!\[\]\((https\:\/\/.+?\.zhimg\.com\/.+?)\)|\1|g'); do
        filename="${i##*/}"
        filename="${filename%%\?*}"
        wget --no-check-certificate -c -t 0 "$i" -O "${file_out_dir}/assets/$filename"
    done
    perl -i -pe 's|\!\[\]\(https\:\/\/.+?\.zhimg\.com\/.+?/(.+?)\)|![](assets/\1)|g' "${file_out}"
    for i in $(cat "${file_out}" | grep --only-matching -E '\<source src="https\:\/\/vdn\d*\.vzuu\d*\.com\/[A-Za-z0-9.?_=&\/\-]+"' | grep --only-matching -E 'https\:\/\/vdn\d*\.vzuu\d*\.com\/[A-Za-z0-9.?_=&\/\-]+'); do
        filename="${i##*/}"
        filename="${filename%%\?*}"
        wget --no-check-certificate -c -t 0 "$i" -O "${file_out_dir}/assets/$filename"
    done
    perl -i -pe 's|\<source src="https\:\/\/vdn\d*\.vzuu\d*\.com\/[A-Za-z0-9]+\/([0-9a-z\-]+\.mp4)[A-Za-z0-9\/\-.?_=&]+"|<source src="assets/\1"|g' "${file_out}"
done

[ -f "${TMPFILE}"  ] && rm "${TMPFILE}"
