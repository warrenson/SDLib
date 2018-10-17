for DIR in ml-100k-0.*/*/* ; do FILE=`find $DIR -name '*cv.txt'` ; OUT=`echo $DIR | awk -F'/' 'OFS="_" {print $1, $2, $3 ".res.txt"}'` ; cat "$FILE" > res_01/${OUT}  ; done
