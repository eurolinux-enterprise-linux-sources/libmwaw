%global apiversion 0.1

Name: libmwaw
Version: 0.1.11
Release: 1%{?dist}
Summary: Import library for some old mac text documents

Group: System Environment/Libraries
# The entire source code is LGPLv2+/MPLv2.0 except
# src/lib/MWAWOLEStream.[ch]xx which are BSD. There is also
# src/tools/zip/zip.cpp which is GPLv2+, but we do not build the binary
# it is used for.
License: (LGPLv2+ or MPLv2.0) and BSD
URL: http://sourceforge.net/projects/libmwaw/
Source: http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tar.xz

BuildRequires: boost-devel
BuildRequires: doxygen
BuildRequires: libwpd-devel

%description
libmwaw contains some import filters for old mac text documents
(MacWrite, ClarisWorks, ... ) based on top of the libwpd (which is
already used in three word processors). 

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%package doc
Summary: Documentation of %{name} API
Group: Documentation
BuildArch: noarch

%description doc
The %{name}-doc package contains documentation files for %{name}.

%package tools
Summary: Tools to transform the supported formats into other formats
Group: Applications/Publishing
License: LGPLv2+
Requires: %{name}%{?_isa} = %{version}-%{release}

%description tools
Tools to transform the supported document formats into other formats.
Supported output formats are XHTML, text and raw.


%prep
%setup -q


%build
%configure --disable-static --disable-werror --disable-zip --enable-docs
sed -i \
    -e 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' \
    -e 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' \
    libtool
make %{?_smp_mflags} V=1


%install
make install DESTDIR=%{buildroot}
rm -f %{buildroot}/%{_libdir}/*.la
# it seems this tool is only useful on MacOS
rm -f %{buildroot}/%{_bindir}/mwawFile
# rhbz#1001297 we install API docs directly from build
rm -rf %{buildroot}/%{_docdir}/%{name}


%post -p /sbin/ldconfig


%postun -p /sbin/ldconfig


%files
%doc CHANGES COPYING.* README
%{_libdir}/%{name}-%{apiversion}.so.*


%files devel
%{_includedir}/%{name}-%{apiversion}
%{_libdir}/%{name}-%{apiversion}.so
%{_libdir}/pkgconfig/%{name}-%{apiversion}.pc


%files doc
%doc COPYING.*
%doc docs/doxygen/html


%files tools
%{_bindir}/mwaw2html
%{_bindir}/mwaw2raw
%{_bindir}/mwaw2text


%changelog
* Mon Sep 09 2013 David Tardon <dtardon@redhat.com> - 0.1.11-1
- new upstream release

* Fri Aug 30 2013 David Tardon <dtardon@redhat.com> - 0.1.10-3
- Resolves: rhbz#1001297 duplicate documentation files / potentially conflicting

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Jun 27 2013 David Tardon <dtardon@redhat.com> - 0.1.10-1
- new release

* Tue May 14 2013 David Tardon <dtardon@redhat.com> - 0.1.9-1
- new release

* Tue Apr 30 2013 David Tardon <dtardon@redhat.com> - 0.1.8-1
- new upstream release

* Sat Apr 27 2013 David Tardon <dtardon@redhat.com> - 0.1.7-2
- minor fixes

* Tue Mar 19 2013 David Tardon <dtardon@redhat.com> 0.1.7-1
- initial import
