Summary:	Displays the users logged into machines on the local network.
Name:		rusers
Version:	0.17
Release:	2
Copyright:	BSD
Group:		Networking/Daemons
Group(pl):	Sieciowe/Serwery
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
Source1:	rusersd.init
Source2:	rstatd.init
Source3:	rstatd.tar.gz
Patch0:		netkit-rusers-numusers.patch
Patch1:		rstatd-jbj.patch
Prereq:		/sbin/chkconfig
BuildRequires:	procps >= 2.0.7
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rusers program allows users to find out who is logged into
various machines on the local network.  The rusers command produces
output similar to who, but for the specified list of hosts or for
all machines on the local network.

Install rusers if you need to keep track of who is logged into your
local network.

%prep
%setup -q -n netkit-rusers-%{version} -a3
%patch0 -p1
%patch1 -p1

%build
./configure

%{__make} CFLAGS="$RPM_OPT_FLAGS -DGNU_LIBC -D_GNU_SOURCE -D_NO_UT_TIME"
%{__make} CFLAGS="$RPM_OPT_FLAGS" -C rpc.rstatd

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

%{__make} install \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

%{__make} install install -C rpc.rstatd \
	INSTALLROOT=$RPM_BUILD_ROOT \
	MANDIR=%{_mandir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rusersd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/rstatd

rm -f $RPM_BUILD_ROOT%{_mandir}/man8/{rstatd,rusersd}.8

echo ".so rpc.rstatd.8" > $RPM_BUILD_ROOT%{_mandir}/man8/rstatd.8
echo ".so rpc.rusersd.8" > $RPM_BUILD_ROOT%{_mandir}/man8/rusersd.8

strip --strip-unneeded $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/* || :

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,8}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rusersd
/sbin/chkconfig --add rstatd
if [ -f /var/lock/subsys/rusersd ]; then
	/etc/rc.d/init.d/rusersd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rusersd start\" to start rusersd server" 1>&2
fi
if [ -f /var/lock/subsys/rstatd ]; then
	/etc/rc.d/init.d/rstatd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rstatd start\" to start rstatd server" 1>&2
fi
	
%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/rusersd ]; then
		/etc/rc.d/init.d/rusersd stop 1>&2
	fi
	if [ -f /var/lock/subsys/rstatd ]; then
		/etc/rc.d/init.d/rstatd stop 1>&2
	fi
	/sbin/chkconfig --del rusersd
	/sbin/chkconfig --del rstatd
fi

%files
%defattr(644,root,root,755)
%attr(754,root,root) %config /etc/rc.d/init.d/rusersd
%attr(754,root,root) %config /etc/rc.d/init.d/rstatd
%attr(755,root,root) %{_bindir}/rup
%attr(755,root,root) %{_bindir}/rusers
%attr(755,root,root) %{_sbindir}/rpc.rstatd
%attr(755,root,root) %{_sbindir}/rpc.rusersd
%{_mandir}/man1/rup.1*
%{_mandir}/man1/rusers.1*
%{_mandir}/man8/rpc.rstatd.8*
%{_mandir}/man8/rpc.rusersd.8*
%{_mandir}/man8/rstatd.8*
%{_mandir}/man8/rusersd.8*
