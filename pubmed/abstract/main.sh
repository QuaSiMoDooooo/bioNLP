#!/bin/bash

folder="/home/wtian/bioNLP/pubmed/abstract/pmid_sid"
file_paths=()

# 使用 find 命令查找文件夹下的所有文件，并将结果保存到 file_paths 数组中
while IFS= read -r -d '' file; do
    file_paths+=("$file")
done < <(find "$folder" -type f -print0)

# 使用 for 循环遍历 file_paths 数组，并在循环中使用这些文件路径
for path in "${file_paths[@]}"; do
    echo "文件路径: $path"
    # 在这里可以使用文件路径进行一些操作，例如拷贝、重命名等
    python get_abstract.py --sid_path $path
done
