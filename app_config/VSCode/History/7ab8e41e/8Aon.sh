# get absoltae path to the dir this is in, work in bash, zsh
# if you want transfer symbolic link to true path, just change `pwd` to `pwd -P`

# 请先按照依赖
# `pip3 install git+https://github.com/hyliang96/zhihubackup`

# bash ./back_image.sh

# user_id='lao-liang-83-95'

here=$(cd "$(dirname "${BASH_SOURCE[0]-$0}")"; pwd)
zhihu_backup_dir="$here/../zhihu_backup"
zhihu_html_dir="${zhihu_backup_dir}/html"
markdown_dir="${zhihu_backup_dir}/markdown"
ls $zhihu_backup_dir

# # rm "${zhihu_html_dir}/record"

# mv "${zhihu_html_dir}" "${zhihu_html_dir}-$(date '+%Y-%m-%d-%H-%M-%S')"
# mkdir -p "${zhihu_backup_dir}"
# mkdir "${zhihu_html_dir}"
# cd "${zhihu_html_dir}"; https_proxy='' http_proxy='' python -c "from zhihubackup import backup_zhihu; backup_zhihu('${user_id}')"



add_to_head()
{
    local temp=$(mktemp)
    echo -n "${1}" | cat - "${2}" > "${temp}" && mv "${temp}" "${2}"
}

n_total=$(ls -1 "${zhihu_html_dir}"/**/*.html | wc -l)

n=0

for file in "${zhihu_html_dir}"/**/*.html; do

    n=$(( 1 + $n ))

    relative_file="$(realpath --relative-to="${zhihu_html_dir}" "${file}")"
    echo "$n / ${n_total} | ${relative_file}"

    relative_dir="$(dirname "${relative_file}")"
    filename=$(basename "${file}")
    file_out_dir="${markdown_dir}/${relative_dir}/${filename/.html/.textbundle}"
    mkdir -p "${file_out_dir}"
    file_out="${file_out_dir}/text.markdown"
    mkdir "${file_out_dir}/assets"
    ln -s assets "${file_out_dir}/text"
    file_out_dir="$(dirname "${file_out}")"

    id="$(echo "${filename}" | grep -oE '^[0-9]+')"
    type="$(basename "${relative_dir}")"
    url="https://www.zhihu.com/${type}/${id}"


    mkdir -p "${file_out_dir}"
    pandoc -s "${file}" -o "${file_out}"

    [[ "${type}" =~ ^(article|answer)$ ]] && add_to_head '# ' "${file_out}"

    add_to_head "来源：${url}"$'\n'$'\n' "${file_out}"

    sed -i '' 's|\\$|'$'\\\n''|g' "${file_out}"

    [ ${type} == pin ] && sed -i '' -E  's/(https\:\/\/[a-zA-Z0-9]+\.zhimg\.com\/[a-zA-Z0-9\.\/\_\-]+)/'$'\\\n''\!\[\]\(\1\)/g' "${file_out}"
    perl -i -pe 'BEGIN{undef $/;} s|\{\.(origin_image\|content_image).+?\}||smg' "${file_out}"   # 跨行匹配，非贪婪
    perl -i -pe 'BEGIN{undef $/;} s|\{\.(origin_image\|content_image).+?\}||smg' "${file_out}"   # 跨行匹配，非贪婪
    sed -i '' -E  's|http\:\/\/link\.zhihu\.com\/\?target\=([a-z]+)%3A\/\/|\1://|g' "${file_out}"
    perl -i -pe 's/\[(\[[-A-Za-z0-9+&@#\/%?=~_|!:,.;]*\]\{\.(visible|invisible|ellipsis)\})+\]\(((https?|ftp|file):\/\/[-A-Za-z0-9+&@#\/%?=~_|!:,.;]+[-A-Za-z0-9+&@#\/%=~_|])\)(\{\.external\})?/\n\3/g' "${file_out}"
    sed -i '' -E 's|\?source=[0-9a-z]+||g' "${file_out}"
    perl -i -pe 'BEGIN{undef $/;} s|\{(\.internal\|\.wrap[> \n]+\.external\|\.hash_tag\|\.member_mention\|eeimg="[0-9]+")\}||smg' "${file_out}"
    python "${here}/replace_equation.py" "${file_out}"

done


for file_out_dir in "${markdown_dir}"/**/*.textbundle; do
    echo $file_out_dir
    file_out="${file_out_dir}/text.markdown"
    for i in $(cat "${file_out}" | grep -E '\!\[\]\(https\:\/\/.+?\.zhimg\.com\/(.+?)\)' | perl -pe 's|\!\[\]\((https\:\/\/.+?\.zhimg\.com\/.+?)\)|\1|g'); do
        filename="${i##*/}"
        filename="${filename%%\?*}"
        wget --no-check-certificate -c -t 0 "$i" -O "${file_out_dir}/assets/$filename"
    done
    perl -i -pe 's|\!\[\]\(https\:\/\/.+?\.zhimg\.com\/.+?/(.+?)\)|![](assets/\1)|g' "${file_out}"
done
