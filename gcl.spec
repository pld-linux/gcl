Summary:	GNU Common Lisp system
Summary(pl):	System GNU Common Lisp
Name:		gcl
Version:	2.6.2
Release:	2
License:	LGPL v2
Group:		Development/Languages
Source0:	ftp://ftp.gnu.org/gnu/gcl/%{name}-%{version}.tar.gz
# Source0-md5:	dfb205e96b5cfa1ab1795110cf38f209
Patch0:		%{name}-make.patch
Patch1:		%{name}-info.patch
URL:		http://www.gnu.org/software/gcl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gmp-devel >= 4.0
BuildRequires:	readline-devel
%define	_tkline	8.4
BuildRequires:	tk-devel >= %{_tkline}
BuildRequires:	xemacs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The GNU Common Lisp system, based on KCL.

%description -l pl
System GNU Common Lisp, bazuj±cy na KCL.

%package tk
Summary:	Tcl/Tk bindings for GNU Common Lisp
Summary(pl):	Interfejs Tcl/Tk do GNU Common Lisp
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description tk
Tcl/Tk bindings for GNU Common Lisp.

%description tk -l pl
Intefejs Tcl/Tk dla GNU Common Lisp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

%build
%{__aclocal}
%{__autoconf}
cp -f /usr/share/automake/config.* .
GCC="%{__cc}"; export GCC
# note: full path to xemacs must be passed
EMACS=/usr/bin/xemacs; export EMACS
%configure \
	--disable-statsysbfd \
%ifnarch alpha hppa ia64 mips
	--enable-dynsysbfd \
%endif
	--enable-dynsysgmp \
	--enable-notify=no

%{__make} \
	EMACS_SITE_LISP=`xemacs -q -batch 2>&1 | sed -e /Loading/d `

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_infodir},%{_mandir}/man1}

%{__make} install1 \
	DESTDIR=$RPM_BUILD_ROOT \
	INSTALL_LIB_DIR=%{_libdir}/gcl

mv -f $RPM_BUILD_ROOT%{_libdir}/gcl/info/* $RPM_BUILD_ROOT%{_infodir}
rmdir $RPM_BUILD_ROOT%{_libdir}/gcl/info

install man/man1/gcl.1 $RPM_BUILD_ROOT%{_mandir}/man1

ln -sf %{_libdir}/gcl/unixport/saved_gcl $RPM_BUILD_ROOT%{_bindir}/gcl.exe

cat <<EOF > $RPM_BUILD_ROOT%{_bindir}/gcl
#!/bin/sh
exec %{_libdir}/gcl/unixport/saved_gcl \
	-dir {_libdir}/gcl/unixport/ \
	-libdir %{_libdir}/gcl/ \
	-eval '(setq si::*allow-gzipped-file* t)' \
	"$@"
EOF

cat <<EOF > $RPM_BUILD_ROOT%{_bindir}/gcl-tk
#!/bin/sh
exec %{_libdir}/gcl/unixport/saved_gcl \
	-dir {_libdir}/gcl/unixport/ \
	-libdir %{_libdir}/gcl/ \
	-eval '(setq si::*allow-gzipped-file* t)' \
	-eval '(setq si::*tk-library* "/usr/lib/tk%{_tkline}")' \
	"$@"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post tk
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun tk
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%files
%defattr(644,root,root,755)
%doc readme faq ChangeLog
%attr(755,root,root) %{_bindir}/gcl
%attr(755,root,root) %{_bindir}/gcl.exe
%dir %{_libdir}/gcl
%{_libdir}/gcl/clcs
%{_libdir}/gcl/cmpnew
%{_libdir}/gcl/h
%{_libdir}/gcl/lsp
%{_libdir}/gcl/pcl
%dir %{_libdir}/gcl/unixport
%attr(755,root,root) %{_libdir}/gcl/unixport/saved_gcl
%{_libdir}/gcl/unixport/*.lsp
# to -devel?
#%{_libdir}/gcl/unixport/*.a
%{_infodir}/gcl-si.info*
%{_mandir}/man1/*

%files tk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gcl-tk
%dir %{_libdir}/gcl/gcl-tk
%attr (755,root,root) %{_libdir}/gcl/gcl-tk/gcltkaux
%attr (755,root,root) %{_libdir}/gcl/gcl-tk/gcltksrv
%{_libdir}/gcl/gcl-tk/*.o
%{_libdir}/gcl/gcl-tk/*.tcl
%{_infodir}/gcl-tk.info*
