%define		_snap		20060104
%define		_modname	yp
%define		_status		stable
Summary:	%{_modname} - a NIS client for PHP
Summary(pl.UTF-8):	%{_modname} - klient NIS dla PHP
Name:		php-pecl-%{_modname}
Version:	0.%{_snap}
Release:	3
License:	PHP
Group:		Development/Languages/PHP
Source0:	%{name}-%{_snap}.tar.gz
# Source0-md5:	ea77871191b0a32c4734964f7c02bc6c
URL:		http://cvs.php.net/pecl/yp/
BuildRequires:	php-devel >= 3:5.0.0
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
Requires:	php-common >= 4:5.0.4
Provides:	php(yp)
Obsoletes:	php-yp
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is a dynamic shared object (DSO) for PHP that will add NIS
(Yellow Pages) support.

%description -l pl.UTF-8
Moduł PHP dodający wsparcie dla NIS (Yellow Pages).

%prep
%setup -q -n %{name}-%{_snap}

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}

install modules/%{_modname}.so $RPM_BUILD_ROOT%{php_extensiondir}
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{_modname}.ini
; Enable %{_modname} extension module
extension=%{_modname}.so
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
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{_modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{_modname}.so
