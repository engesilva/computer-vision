mkdir -p out

n=0

while read i; do
  fn=$(echo "$i" | cut -d" " -f1)
  x=$(echo "$i" | cut -d" " -f3)
  y=$(echo "$i" | cut -d" " -f4)
  w=$(echo "$i" | cut -d" " -f5)
  h=$(echo "$i" | cut -d" " -f6)
  class=$(echo "$i" | cut -d" " -f7)
  bn=$(echo "$fn" | rev | cut -d/ -f1 | rev)
  let "n+=1"
  num=$(printf %07d $n)
  convert "$fn" -crop "${w}x${h}+${x}+${y}" "out/${num}_${class}_${bn}"

done
