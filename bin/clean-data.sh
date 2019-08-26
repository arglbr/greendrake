#!/bin/bash
OLDWD=`pwd`
HOMEDIR='/Users/arglbr/src/arglbr/greendrake/'

cd $HOMEDIR
mv data/db/gd-archive-ec5e29c8/* data/db/gd-raw-be3bc2c/
rm -f data/db/gd-optimized-4bf3bb45/*
cd $OLDWD
