%define debug_package %{nil}

Name:           libefwfilter
Version:        1.6
Release:        1
Summary:        ZWO filter wheel SDK
License:        expat
URL:            http://astronomy-imaging-camera.com/
Prefix:         %{_prefix}
Provides:       libefwfilter = %{version}-%{release}
Obsoletes:      libefwfilter < 1.6
Requires:       libusbx
Source:         libefwfilter-%{version}.tar.gz
Patch0:         pkg-config.patch
Patch1:         udev-rules.patch

%description
libefwfilter is a user-space driver for ZWO filter wheels

%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name}%{?_isa} = %{version}-%{release}
Provides:       libefwfilter-devel = %{version}-%{release}
Obsoletes:      libefwfilter-devel < 1.6

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%prep
%setup -q
%patch0 -p0
%patch1 -p0

%build

sed -e "s!@LIBDIR@!%{_libdir}!g" -e "s!@VERSION@!%{version}!g" < \
    libefwfilter.pc.in > libefwfilter.pc

%install
mkdir -p %{buildroot}%{_libdir}/pkgconfig
mkdir -p %{buildroot}%{_includedir}
mkdir -p %{buildroot}%{_docdir}/%{name}-%{version}/demo/c
mkdir -p %{buildroot}/etc/udev/rules.d

case %{_arch} in
  i386)
    cp lib/x86/libEFWFilter*.so.%{version} %{buildroot}%{_libdir}
    cp lib/x86/libEFWFilter*.a %{buildroot}%{_libdir}
    ;;
  x86_64)
    cp lib/x64/libEFWFilter*.so.%{version} %{buildroot}%{_libdir}
    cp lib/x64/libEFWFilter*.a %{buildroot}%{_libdir}
    ;;
  *)
    echo "unknown target architecture %{_arch}"
    exit 1
    ;;
esac

ln -sf %{name}.so.%{version} %{buildroot}%{_libdir}/%{name}.so.0
cp include/*.h %{buildroot}%{_includedir}
cp *.pc %{buildroot}%{_libdir}/pkgconfig
cp doc/* %{buildroot}%{_docdir}/%{name}-%{version}
cp license.txt %{buildroot}%{_docdir}/%{name}-%{version}
cp lib/README.txt %{buildroot}%{_docdir}/%{name}-%{version}
cp demo/c/Makefile %{buildroot}%{_docdir}/%{name}-%{version}/demo/c
cp demo/c/*.* %{buildroot}%{_docdir}/%{name}-%{version}/demo/c
cp 70-asi-fw.rules %{buildroot}/etc/udev/rules.d

%post
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%postun
/sbin/ldconfig
/sbin/udevadm control --reload-rules

%files
%{_libdir}/*.so.*
%{_docdir}/%{name}-%{version}/*.txt
%{_sysconfdir}/udev/rules.d/*.rules

%files devel
%{_includedir}/EFW_filter*.h
%{_libdir}/pkgconfig/%{name}*.pc
%{_libdir}/*.a
%{_docdir}/%{name}-%{version}/*.pdf
%{_docdir}/%{name}-%{version}/demo/c/Makefile
%{_docdir}/%{name}-%{version}/demo/c/*.*

%changelog
* Thu Mar 25 2021 James Fidell <james@openastroproject.org> - 1.6-1
- Initial RPM release

