Summary:	Displays the users logged into machines on the local network.
Name:		rusers
Version:	0.10
Release:	24
Copyright:	BSD
Group:		System Environment/Daemons
Source0:	ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-%{name}-%{version}.tar.gz
Source1:	rusersd.init
Source2:	rstatd.init
Source3:	rstatd.tar.gz
Patch0:		netkit-rusers-0.10-misc.patch
Patch1:		rusers-0.10-maint.patch
Patch2:		netkit-rusers-install.patch
Prereq:		/sbin/chkconfig
Requires:	rc-scripts
Buildroot:	/tmp/%{name}-%{version}-root

%description
The rusers program allows users to find out who is logged into
various machines on the local network.  The rusers command produces
output similar to who, but for the specified list of hosts or for
all machines on the local network.

Install rusers if you need to keep track of who is logged into your
local network.

%prep
%setup -q -n netkit-rusers-0.10 -a3
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
make
make -C rpc.rstatd

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}}
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

make install \
	INSTALLROOT=$RPM_BUILD_ROOT
make install install -C rpc.rstatd \
	INSTALLROOT=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/rusersd
install %{SOURCE2} $RPM_BUILD_ROOT/etc/rc.d/init.d/rstatd

strip --strip-unneeded $RPM_BUILD_ROOT{%{_bindir},%{_sbindir}}/* || :

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man{1,8}/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add rusersd
/sbin/chkconfig --add rstatd

%postun
if [ $1 = 0 ]; then
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
%{_mandir}/man8/rusersd.8*
