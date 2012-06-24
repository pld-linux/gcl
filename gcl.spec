Summary:	GNU Common Lisp
Summary(pl):	GNU Common Lisp
Name:		gcl
Version:	2.4.0
Release:	1
License:	GPL
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/J�zyki
Source0:	ftp://ftp.gnu.org/gnu/%{name}/%{name}-%{version}.tgz
Patch0:		%{name}-make.patch
Patch1:		%{name}-OPT.patch
URL:		http://www.gnu.org/projects/gcl
BuildRequires:	tk-devel
BuildRequires:	emacs-leim
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The GNU Common Lisp system, based on KCL.

%description -l pl
System GNU Common Lisp, bazuj�cy na KCL.

%package tk
Summary:	Tcl/tk bindings for GNU Common Lisp
Summary(pl):	Interfejs Tcl/tk do GNU Common Lisp
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/J�zyki
Requires:	%{name} = %{version}

%description tk
Tcl/tk bindings for GNU Common Lisp

%description tk -l pl
Intefejs Tcl/tk dla GNU Common Lisp

%package doc-html
Summary:	HTML documntation for GNU Common Lisp
Summary(pl):	Dokumentacja dla GNU Common Lisp w formacie HTML
Group:		Development/Languages
Group(de):	Entwicklung/Sprachen
Group(pl):	Programowanie/J�zyki
Requires:	%{name} = %{version}

%description doc-html
HTML documntation for GNU Common Lisp.

%description doc-html -l pl
Dokumentacja dla GNU Common Lisp w formacie HTML.

%prep
%setup  -q
%patch0 -p1
%patch1 -p1

%build
GCC="%{__cc}"; export GCC
%configure2_13 \
	--enable-notify=no
%{__make} OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/gcl/{cmpnew,unixport,lsp,gcl-tk}
install -d $RPM_BUILD_ROOT{%{_infodir},%{_bindir}}
install -d $RPM_BUILD_ROOT%{_datadir}/emacs/site-lisp
install unixport/saved_gcl $RPM_BUILD_ROOT%{_libdir}/gcl/unixport
install info/*info*.gz $RPM_BUILD_ROOT%{_infodir}
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

gzip -9nf readme faq ChangeLog

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
%doc *.gz
%attr(755,root,root) %{_bindir}/gcl
%attr(755,root,root) %{_bindir}/gcl.exe
%{_libdir}/gcl/cmpnew
%{_libdir}/gcl/lsp
%attr(755,root,root) %{_libdir}/gcl/unixport/saved_gcl
%{_infodir}/gcl-si.info*.gz

%files doc-html
%defattr(644,root,root,755)
%doc info/*.html

%files tk
%defattr(644,root,root,755)
%dir %{_infodir}
%attr(755,root,root) %{_bindir}/gcl-tk
%{_libdir}/gcl/gcl-tk
%{_infodir}/gcl-tk.info*.gz
