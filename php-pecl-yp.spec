%define		modname		yp
%define		status		beta
%define		php_name	php%{?php_suffix}
Summary:	%{modname} - YP/NIS functions
Summary(pl.UTF-8):	%{modname} - klient YP/NIS dla PHP
Name:		%{php_name}-pecl-%{modname}
Version:	1.0.1
Release:	1
License:	PHP
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	6c57bf144d1bb8c4aca5309cc4281407
URL:		http://pecl.php.net/package/yp/
BuildRequires:	%{php_name}-devel >= 4:5.3.0
BuildRequires:	libnsl-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(yp)
Obsoletes:	php-pecl-yp < 1.0.0-0.RC1.1
Obsoletes:	php-yp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
NIS (formerly called Yellow Pages) allows network management of
important administrative files (e.g. the password file).

%description -l pl.UTF-8
Moduł PHP dodający obsługę NIS (Yellow Pages).

%prep
%setup -qc
%{__mv} %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
