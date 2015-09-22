file=$1
scale=$2
randomNumber=$3

cd tmp/$randomNumber

perl bin/profiler.pl $file $scale

Rscript bin/plotter.r outputs/profile.txt $scale

awk -F'\t' 'BEGIN{printf "<tbody>\n"}{printf "\t<tr>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n\t\t<td>%s</td>\n",$1, $2, $3, $4, $5}END{printf "</tbody>\n"}' ./outputs/table.txt > ./outputs/table.html

cd ../..