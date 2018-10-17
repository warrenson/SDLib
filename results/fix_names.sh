find . -name '*-p*.txt' | while read -r FILE ; do NEW=`echo $FILE | sed 's/-p/_p/'` ; mv $FILE $NEW ; done 
find . -name '*-k*.txt' | while read -r FILE ; do NEW=`echo $FILE | sed 's/-k/_k/'` ; mv $FILE $NEW ; done
for FILE in *.res.txt ; do NEW=`echo $FILE | perl -pe 's/(ml-100k-|-attacks)//g'` ; mv $FILE $NEW ; done
