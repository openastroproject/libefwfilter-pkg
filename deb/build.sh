#!/bin/bash

export DEBEMAIL=james@openastroproject.org
export DEBFULLNAME="James Fidell"

version=`cat version`

srcdir=libefwfilter-$version
debdir=debian
debsrc=$debdir/source
quiltconf=$HOME/.quiltrc-dpkg

mkdir $srcdir
cd $srcdir
tar zxf ../libefwfilter-$version.tar.gz
chmod -x demo/c/*.*
chmod -x demo/c/Makefile
YFLAG=-y
dh_make -v | fgrep -q '1998-2011'
if [ $? -eq 0 ]
then
  YFLAG=''
fi
dh_make $YFLAG -l -f ../libefwfilter-$version.tar.gz

cp ../debfiles/control $debdir
cp ../debfiles/copyright $debdir
cp ../debfiles/changelog $debdir
cp ../debfiles/docs $debdir
cp ../debfiles/watch $debdir
cp ../debfiles/libefwfilter.dirs $debdir
cp ../debfiles/libefwfilter.install $debdir
cp ../debfiles/libefwfilter.symbols $debdir
cp ../debfiles/libefwfilter.doc-base $debdir
cp ../debfiles/libefwfilter-dev.dirs $debdir
cp ../debfiles/libefwfilter-dev.install $debdir
cp ../debfiles/libefwfilter-dev.examples $debdir

echo 10 > $debdir/compat

sed -e '/^.*[ |]configure./a\
        ldconfig\
	udevadm control --reload-rules || true' < $debdir/postinst.ex > $debdir/postinst
chmod +x $debdir/postinst
sed -e '/^.*[ |]remove./a\
        ldconfig\
	udevadm control --reload-rules || true' < $debdir/postrm.ex > $debdir/postrm
chmod +x $debdir/postrm
echo "3.0 (quilt)" > $debsrc/format

sed -e "s/DEBVERSION/$version/g" < ../debfiles/rules.overrides >> $debdir/rules

rm $debdir/README.Debian
rm $debdir/README.source
rm $debdir/libefwfilter-docs.docs
rm $debdir/libefwfilter1.*
rm $debdir/*.[Ee][Xx]


export QUILT_PATCHES="debian/patches"
export QUILT_PATCH_OPTS="--reject-format=unified"
export QUILT_DIFF_ARGS="-p ab --no-timestamps --no-index --color=auto"
export QUILT_REFRESH_ARGS="-p ab --no-timestamps --no-index"
mkdir -p $QUILT_PATCHES

for p in `ls -1 ../debfiles/patches`
do
  quilt --quiltrc=$quiltconf new $p
  for f in `egrep '^\+\+\+' ../debfiles/patches/$p | awk '{ print $2; }'`
  do
    quilt --quiltrc=$quiltconf add $f
  done
pwd
  patch -p0 < ../debfiles/patches/$p
  quilt --quiltrc=$quiltconf refresh
done

dpkg-buildpackage -us -uc

echo "Now run:"
echo
echo "    lintian -i -I --show-overrides libefwfilter_$version-3_amd64.changes"
