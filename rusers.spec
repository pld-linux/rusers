Summary: Displays the users logged into machines on the local network.
Name: rusers
Version: 0.10
Release: 23
Copyright: BSD
Group: System Environment/Daemons
Source: ftp://sunsite.unc.edu/pub/Linux/system/network/daemons/netkit-rusers-0.10.tar.gz
Source1: rusersd.init
Source2: rstatd.tar.gz
Patch0: netkit-rusers-0.10-misc.patch
Patch1: rusers-0.10-maint.patch
Prereq: /sbin/chkconfig
Buildroot: /var/tmp/%{name}-root

%description
The rusers program allows users to find out who is logged into
various machines on the local network.  The rusers command produces
output similar to who, but for the specified list of hosts or for
all machines on the local network.

Install rusers if you need to keep track of who is logged into your
local network.

%prep
%setup -q -n netkit-rusers-0.10 -a 2
%patch0 -p1
%patch1 -p1

%build
make
make -C rpc.rstatd

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/bin
mkdir -p $RPM_BUILD_ROOT/usr/sbin
mkdir -p $RPM_BUILD_ROOT/usr/man/man1
mkdir -p $RPM_BUILD_ROOT/usr/man/man8
mkdir -p $RPM_BUILD_ROOT/etc/rc.d/init.d

make INSTALLROOT=$RPM_BUILD_ROOT install
make INSTALLROOT=$RPM_BUILD_ROOT install -C rpc.rstatd

install -m 755 $RPM_SOURCE_DIR/rusersd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/rusersd
install -m 755 rstatd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/rstatd

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
%defattr(-,root,root)
/usr/bin/rup
/usr/bin/rusers
/usr/man/man1/rup.1
/usr/man/man1/rusers.1
/usr/man/man8/rpc.rstatd.8
/usr/man/man8/rpc.rusersd.8
/usr/man/man8/rusersd.8
/usr/sbin/rpc.rstatd
/usr/sbin/rpc.rusersd
%config /etc/rc.d/init.d/rusersd
%config /etc/rc.d/init.d/rstatd
