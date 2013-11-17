# TODO:
# - package tk-demos?
# - package emacs-lisp files (if building with xemacs)
#
# Conditional build:
%bcond_without	xemacs	# don't build/package emacs-lisp parts
#
%define	tk_ver	8.5
Summary:	GNU Common Lisp system
Summary(pl.UTF-8):	System GNU Common Lisp
Name:		gcl
Version:	2.6.10
Release:	1
License:	LGPL v2
Group:		Development/Languages
Source0:	http://ftp.gnu.org/gnu/gcl/%{name}-%{version}.tar.gz
# Source0-md5:	7cb9c388e9e77696f4e27e7a1d118524
Patch0:		%{name}-make.patch
Patch1:		%{name}-info.patch
Patch2:		%{name}-format.patch
URL:		http://www.gnu.org/software/gcl/
BuildRequires:	autoconf >= 2.61
BuildRequires:	automake
BuildRequires:	gmp-devel >= 4.0
BuildRequires:	readline-devel
BuildRequires:	texinfo
BuildRequires:	tk-devel >= %{tk_ver}
%{?with_xemacs:BuildRequires:	xemacs}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The GNU Common Lisp system, based on KCL.

%description -l pl.UTF-8
System GNU Common Lisp, bazujący na KCL.

%package tk
Summary:	Tcl/Tk bindings for GNU Common Lisp
Summary(pl.UTF-8):	Interfejs Tcl/Tk do GNU Common Lisp
Group:		Development/Languages
Requires:	%{name} = %{version}-%{release}

%description tk
Tcl/Tk bindings for GNU Common Lisp.

%description tk -l pl.UTF-8
Interfejs Tcl/Tk dla GNU Common Lisp.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
%{__aclocal}
%{__autoconf}
cp -f /usr/share/automake/config.* .
GCC="%{__cc}"; export GCC
%configure \
	%{?with_xemacs:EMACS=/usr/bin/xemacs} \
	--enable-dynsysgmp \
	--enable-notify=no

%{__make}

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
	-dir %{_libdir}/gcl/unixport/ \
	-libdir %{_libdir}/gcl/ \
	-eval '(setq si::*allow-gzipped-file* t)' \
	"$@"
EOF

cat <<EOF > $RPM_BUILD_ROOT%{_bindir}/gcl-tk
#!/bin/sh
exec %{_libdir}/gcl/unixport/saved_gcl \
	-dir %{_libdir}/gcl/unixport/ \
	-libdir %{_libdir}/gcl/ \
	-eval '(setq si::*allow-gzipped-file* t)' \
	-eval '(setq si::*tk-library* "/usr/lib/tk%{tk_ver}")' \
	"$@"
EOF

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/{dwdoc*,gcl-si*,gcl-tk*}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	tk -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	tk -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

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
%{_libdir}/gcl/xgcl-2
%dir %{_libdir}/gcl/unixport
%attr(755,root,root) %{_libdir}/gcl/unixport/saved_gcl
%{_libdir}/gcl/unixport/*.lsp
%{_libdir}/gcl/unixport/gcl.script
# to -devel?
%{_libdir}/gcl/unixport/libgcl.a
%{_libdir}/gcl/unixport/libgclp.a
%{_infodir}/gcl-si.info*
%{_mandir}/man1/gcl.1*

%files tk
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gcl-tk
%dir %{_libdir}/gcl/gcl-tk
%attr(755,root,root) %{_libdir}/gcl/gcl-tk/gcltkaux
%attr(755,root,root) %{_libdir}/gcl/gcl-tk/gcltksrv
%{_libdir}/gcl/gcl-tk/*.o
%{_libdir}/gcl/gcl-tk/*.tcl
%{_libdir}/gcl/gcl-tk/tk-package.lsp
%{_infodir}/gcl-tk.info*
