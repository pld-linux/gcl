Summary:	GNU Common Lisp
Summary(pl):	GNU Common Lisp
Name:		gcl
Version:	2.4.3
Release:	1
License:	LGPL v2
Group:		Development/Languages
Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tgz
Patch0:		%{name}-make.patch
Patch1:		%{name}-OPT.patch
Patch2:		%{name}-info.patch
Patch3:		%{name}-libgmp.patch
URL:		http://www.ma.utexas.edu/users/wfs/gcl.html
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gmp-devel
BuildRequires:	tk-devel
BuildRequires:	xemacs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
ExclusiveArch:	%{ix86} sparc

%description
The GNU Common Lisp system, based on KCL.

%description -l pl
System GNU Common Lisp, bazuj�cy na KCL.

%package tk
Summary:	Tcl/tk bindings for GNU Common Lisp
Summary(pl):	Interfejs Tcl/tk do GNU Common Lisp
Group:		Development/Languages
Requires:	%{name} = %{version}

%description tk
Tcl/tk bindings for GNU Common Lisp.

%description tk -l pl
Intefejs Tcl/tk dla GNU Common Lisp.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
rm -f missing
%{__aclocal}
%{__autoconf}
cp -f /usr/share/automake/config.* .
GCC="%{__cc}"; export GCC
# note: full path to xemacs must be passed
EMACS=/usr/bin/xemacs; export EMACS
%configure \
	--enable-notify=no

%{__make} OPTFLAGS="%{rpmcflags}" \
	EMACS_SITE_LISP=`xemacs -q -batch 2>&1 | sed -e /Loading/d `

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/gcl/{cmpnew,unixport,lsp,gcl-tk} \
	$RPM_BUILD_ROOT{%{_infodir},%{_mandir}/man1,%{_bindir}} \
	$RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp

(cd info
rm -f *info*
makeinfo gcl-si.texi gcl-tk.texi
install gcl*info* $RPM_BUILD_ROOT%{_infodir})
install man/man1/gcl.1 $RPM_BUILD_ROOT%{_mandir}/man1

install unixport/saved_gcl $RPM_BUILD_ROOT%{_libdir}/gcl/unixport
install info/*info* $RPM_BUILD_ROOT%{_infodir}
install cmpnew/collectfn.o $RPM_BUILD_ROOT%{_libdir}/gcl/cmpnew
install lsp/{gprof.lsp,info.o,profile.lsp} $RPM_BUILD_ROOT%{_libdir}/gcl/lsp
install gcl-tk/{decode.tcl,gcl.tcl,gcltkaux,gcltksrv,tinfo.o,tkl.o} \
	$RPM_BUILD_ROOT%{_libdir}/gcl/gcl-tk

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
	-eval '(setq si::*tk-library* "%{_libdir}/tk8.3")' \
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
%{_libdir}/gcl/cmpnew
%{_libdir}/gcl/lsp
%attr(755,root,root) %{_libdir}/gcl/unixport/saved_gcl
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
