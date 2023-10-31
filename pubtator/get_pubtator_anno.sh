#!/bin/bash

F_DIR="annos"
F_LIST="../pubmed/abstract/pmid"

i=1
while IFS= read -r line
do
	printf "$line \n"
	curl "https://www.ncbi.nlm.nih.gov/research/pubtator-api/publications/export/pubtator?pmids=$line" | sed '/\.$/d' | sed '/|$/d'  > "$F_DIR/$line.txt"
	printf "$i processing... \n"
	i=$[i+1]
	sleep 3s
done<"$F_LIST"
