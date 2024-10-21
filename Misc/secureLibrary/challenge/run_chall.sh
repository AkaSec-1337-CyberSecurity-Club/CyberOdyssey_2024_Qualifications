#!/bin/bash

TMPDIR=$(mktemp -d)

cp ./chall $TMPDIR/
cp ./flag.txt $TMPDIR/

cd $TMPDIR
./chall

rm -rf $TMPDIR
