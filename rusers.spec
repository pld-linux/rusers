Summary:	Displays the users logged into machines on the local network
Summary(de):	Anzeige von Login-Infos für entfernte Computer
Summary(fr):	Affiche des informations de login pour les machines distantes
Summary(tr):	Að üzerindeki makinalardaki kullanýcýlarý sorgular
Name:		rusers
Version:	0.17
Release:	7
License:	BSD
Group:		Networking
Group(de):	Netzwerkwesen
Group(pl):	Sieciowe
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
Source1:	%{name}d.init
Source2:	rstatd.init
Source3:	rstatd.tar.gz
Patch0:		netkit-%{name}-numusers.patch
Patch1:		rstatd-jbj.patch
Buildrequires:	procps
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rusers program allows users to find out who is logged into various
machines on the local network. The rusers command produces output
similar to who, but for the specified list of hosts or for all
machines on the local network.

%description -l de
Mit Hilfe des rusers-Server und Client (beide Teil dieses Pakets) kann
man herausfinden, welche Benutzer an welchen Rechnern im lokalen
Netwerk angemeldet sind.

%description -l fr
Le client et le serveur rusers, tous deux inclus dans ce package,
permettent aux utilisateurs de trouver quels utilisateurs sont
connectés sur les différentes machines du réseau local.

%description -l tr
Bu pakette yer alan rusers sunucusu ve istemcisi ile bir kullanýcý að
üzerinde bu hizmeti sunan diðer makinalardaki kullanýcýlarý
sorgulayabilir.

%package -n rusersd
Summary:	Server for the rusers protocol
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Obsoletes:	rusers-server
Prereq:		/sbin/chkconfig
Requires:	rc-scripts

%description -n rusersd
machines on the local network. The rusersd package contains the server
for responding to rusers requests.

%package -n rup
Summary:	rstatd client
Group:		Networking
Group(de):	Netzwerkwesen
Group(pl):	Sieciowe

%description -n rup
rup displays a summary of the current system status of a particular
host or all hosts on the local network. The output shows the current
time of day, how long the system has been up, and the load averages.
The load average numbers give the number of jobs in the run queue
averaged over 1, 5 and 15 minutes.

%package -n rstatd
Summary:	kernel statistics server
Group:		Networking/Daemons
Group(de):	Netzwerkwesen/Server
Group(pl):	Sieciowe/Serwery
Prereq:		/sbin/chkconfig
Requires:	rc-scripts

%description -n rstatd
rpc.rstatd is a server which returns performance statistics obtained
from the kernel. These statistics are usually read using the rup(1)
command.

%prep
%setup -q -n netkit-rusers-%{version} -a3
%patch0 -p1
%patch1 -p1

%build
./configure

%{__make} CC="%{__cc}" \
	CFLAGS="%{!?debug:$RPM_OPT_FLAGS}%{?debig:-O -g} -DGNU_LIBC -D_GNU_SOURCE -D_NO_UT_TIME"

%{__make} CC="%{__cc}" \
	CFLAGS="%{!?debug:$RPM_OPT_FLAGS}%{?debig:-O -g}" -C rpc.rstatd

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_sbindir},%{_mandir}/man{1,8}} \
	$RPM_BUILD_ROOT/etc/rc.d/init.d

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

%clean
rm -rf $RPM_BUILD_ROOT

%post -n rusersd
/sbin/chkconfig --add rusersd
if [ -f /var/lock/subsys/rusersd ]; then
	/etc/rc.d/init.d/rusersd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rusersd start\" to start rusersd server" 1>&2
fi
	
%postun -n rusersd
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/rusersd ]; then
		/etc/rc.d/init.d/rusersd stop 1>&2
	fi
	/sbin/chkconfig --del rusersd
fi

%post -n rstatd
/sbin/chkconfig --add rstatd
if [ -f /var/lock/subsys/rstatd ]; then
	/etc/rc.d/init.d/rstatd restart 1>&2
else
	echo "Type \"/etc/rc.d/init.d/rstatd start\" to start rstatd server" 1>&2
fi
	
%postun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/rstatd ]; then
		/etc/rc.d/init.d/rstatd stop 1>&2
	fi
	/sbin/chkconfig --del rstatd
fi

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rusers
%{_mandir}/man1/rusers.1*

%files -n rusersd
%defattr(644,root,root,755)
%attr(754,root,root) %config /etc/rc.d/init.d/rusersd
%attr(755,root,root) %{_sbindir}/rpc.rusersd
%{_mandir}/man8/rpc.rusersd.8*
%{_mandir}/man8/rusersd.8*

%files -n rup
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rup
%{_mandir}/man1/rup.1*

%files -n rstatd
%defattr(644,root,root,755)
%attr(754,root,root) %config /etc/rc.d/init.d/rstatd
%attr(755,root,root) %{_sbindir}/rpc.rstatd
%{_mandir}/man8/rpc.rstatd.8*
%{_mandir}/man8/rstatd.8*
