#!/bin/bash

cp ../patches/*.patch .
rm -f makefile.patch

rel=`cut -d' ' -f3 < /etc/redhat-release`
fedpkg --release f$rel local
