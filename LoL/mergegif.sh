#!/bin/bash

mkdir top1
convert $1/$1-top1.gif top1/x%04d.gif
mkdir top2
convert $1/$1-top2.gif top2/x%04d.gif
mkdir top4
convert $1/$1-top4.gif top4/x%04d.gif
mkdir top6
convert $1/$1-top6.gif top6/x%04d.gif

mkdir recap
k=-1
for filename in top1/*
do
  filename=`basename $filename`
  montage -tile 2x2 -geometry 614x360 top1/$filename top2/$filename top4/$filename top6/$filename recap/$filename
  k=$[k+1]
done
printf -v src "%04d" $k
for i in {1..50}
do
	printf -v trg "%04d" $((k+i))
	cp top1/x$src.gif top1/x$trg.gif
done
for i in {1..50}
do
	printf -v trg "%04d" $((k+i))
	cp top2/x$src.gif top2/x$trg.gif
done
for i in {1..50}
do
	printf -v trg "%04d" $((k+i))
	cp top4/x$src.gif top4/x$trg.gif
done
for i in {1..50}
do
	printf -v trg "%04d" $((k+i))
	cp top6/x$src.gif top6/x$trg.gif
done
for i in {1..50}
do
	printf -v trg "%04d" $((k+i))
	cp recap/x$src.gif recap/x$trg.gif
done

convert top1/* $1/$1-top1-final.gif
convert top2/* $1/$1-top2-final.gif
convert top4/* $1/$1-top4-final.gif
convert top6/* $1/$1-top6-final.gif
convert recap/* $1/$1-recap-final.gif

rm -rf top1
rm -rf top2
rm -rf top4
rm -rf top6
rm -rf recap
