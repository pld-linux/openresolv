Summary:	A POSIX resolvconf(8) implementation, a middleman for resolv.conf(5)
Name:		openresolv
Version:	3.12.0
Release:	1
License:	BSD
Group:		Base
Source0:	https://roy.marples.name/downloads/openresolv/%{name}-%{version}.tar.xz
# Source0-md5:	595f8633c111c150b86825b027e0bbde
URL:		https://roy.marples.name/projects/openresolv/
Conflicts:	resolvconf
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
/etc/resolv.conf is a file that holds the configuration for the local
resolution of domain names. Normally this file is either static or
maintained by a local daemon, normally a DHCP daemon. But what happens
if more than one thing wants to control the file? Say you have wired
and wireless interfaces to different subnets and run a VPN or two on
top of that, how do you say which one controls the file? It’s also not
as easy as just adding and removing the nameservers each client knows
about as different clients could add the same nameservers.

Enter resolvconf, the middleman between the network configuration
services and /etc/resolv.conf. resolvconf itself is just a script that
stores, removes and lists a full resolv.conf generated for the
interface. It then calls all the helper scripts it knows about so it
can configure the real /etc/resolv.conf and optionally any local
nameservers other than libc.

%prep
%setup -q

%build
%configure \
	--libexecdir=%{_libexecdir}/%{name} \
	--sbindir=/sbin
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.md
%config(noreplace,missingok) %verify(not md5 mtime size) %{_sysconfdir}/resolvconf.conf
%attr(755,root,root) /sbin/resolvconf
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/dnsmasq
%{_libexecdir}/%{name}/libc
%dir %{_libexecdir}/%{name}/libc.d
%{_libexecdir}/%{name}/libc.d/avahi-daemon
%{_libexecdir}/%{name}/libc.d/mdnsd
%{_libexecdir}/%{name}/named
%{_libexecdir}/%{name}/pdns_recursor
%{_libexecdir}/%{name}/pdnsd
%{_libexecdir}/%{name}/unbound
%{_mandir}/man5/resolvconf.conf.5*
%{_mandir}/man8/resolvconf.8*
