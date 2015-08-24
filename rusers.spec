Summary:	Displays the users logged into machines on the local network
Summary(de.UTF-8):	Anzeige von Login-Infos für entfernte Computer
Summary(es.UTF-8):	El cliente rusers
Summary(fr.UTF-8):	Affiche des informations de login pour les machines distantes
Summary(pl.UTF-8):	Wyświetla listę użytkowników zalogowanych na komputerach w sieci lokalnej
Summary(pt_BR.UTF-8):	Mostra a informação de login para máquinas remotas
Summary(tr.UTF-8):	Ağ üzerindeki makinalardaki kullanıcıları sorgular
Name:		rusers
Version:	0.17
Release:	28
License:	BSD
Group:		Networking
Source0:	ftp://ftp.linux.org.uk/pub/linux/Networking/netkit/netkit-%{name}-%{version}.tar.gz
# Source0-md5:	dc99a80b9fde2ab427c874f88f1c1602
Source1:	%{name}d.init
Source2:	rstatd.init
Source3:	rstatd.tar.gz
# Source3-md5:	75c1f4b3df318cf509593af1ee1d52e5
Patch0:		netkit-%{name}-numusers.patch
Patch1:		rstatd-jbj.patch
Patch2:		netkit-%{name}-droppriv-later.patch
Patch3:		netkit-%{name}-includes.patch
BuildRequires:	procps-devel >= 1:3.2.5-3
BuildRequires:	rpmbuild(macros) >= 1.268
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The rusers program allows users to find out who is logged into various
machines on the local network. The rusers command produces output
similar to who, but for the specified list of hosts or for all
machines on the local network.

%description -l de.UTF-8
Mit Hilfe des rusers-Server und Client (beide Teil dieses Pakets) kann
man herausfinden, welche Benutzer an welchen Rechnern im lokalen
Netwerk angemeldet sind.

%description -l fr.UTF-8
Le client et le serveur rusers, tous deux inclus dans ce package,
permettent aux utilisateurs de trouver quels utilisateurs sont
connectés sur les différentes machines du réseau local.

%description -l pl.UTF-8
Program rusers pozwala użytkownikom sprawdzić kto jest zalogowany na
różnych maszynach w sieci lokalnej. Wynik komendy rusers jest podobne
do komendy who, ale dla określonej listy komputerów lub wszystkich
maszyn z sieci lokalnej.

%description -l pt_BR.UTF-8
O programa rusers permite descobrir quem está em várias máquinas na
rede. O comando rusers fornece uma saída similar a do comando who para
a lista de máquinas especificada ou para todas as máquinas da rede
local.

%description -l tr.UTF-8
Bu pakette yer alan rusers sunucusu ve istemcisi ile bir kullanıcı ağ
üzerinde bu hizmeti sunan diğer makinalardaki kullanıcıları
sorgulayabilir.

%package -n rusersd
Summary:	Server for the rusers protocol
Summary(es.UTF-8):	El servidor rusers
Summary(pl.UTF-8):	Serwer protokołu rusers
Summary(pt_BR.UTF-8):	Servidor para o protocolo rusers
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Obsoletes:	rusers-server

%description -n rusersd
The rusersd package contains the server for responding to rusers
requests.

%description -n rusersd -l es.UTF-8
El servidor rusers incluido en este paquete, permiten ver cual de los
usuarios están "logados" en otras máquinas de la red.

%description -n rusersd -l pl.UTF-8
Pakiet rusersd zawiera serwer odpowiadający na zapytania rusers.

%description -n rusersd -l pt_BR.UTF-8
Servidor para o protocolo rusers.

%package -n rup
Summary:	rstatd client
Summary(pl.UTF-8):	Klient rstatd
Group:		Networking

%description -n rup
rup displays a summary of the current system status of a particular
host or all hosts on the local network. The output shows the current
time of day, how long the system has been up, and the load averages.
The load average numbers give the number of jobs in the run queue
averaged over 1, 5 and 15 minutes.

%description -n rup -l pl.UTF-8
rup wyświetla podsumowanie aktualnego stanu systemu dla określonego
komputera lub wszystkich z sieci lokalnej. Wyjście zawiera aktualny
czas, jak długo system jest włączony i obciążenie. Obciążenie podawane
jest jako ilość procesów w kolejce średnio w 1, 5 i 15 minut.

%package -n rstatd
Summary:	kernel statistics server
Summary(pl.UTF-8):	Serwer rstatd
Group:		Networking/Daemons
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts

%description -n rstatd
rpc.rstatd is a server which returns performance statistics obtained
from the kernel. These statistics are usually read using the rup(1)
command.

%description -n rstatd -l pl.UTF-8
rpc.rstatd to serwer podający statystyki wydajności pobrane od jądra.
Statystyki te zwykle są czytane komendą rup(1).

%prep
%setup -q -n netkit-%{name}-%{version} -a3
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
./configure

%{__make} \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -DGNU_LIBC -D_GNU_SOURCE -D_NO_UT_TIME"

%{__make} -C rpc.rstatd \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" \
	LIBS="-lprocps"

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
%service rusersd restart "rusersd server"

%preun -n rusersd
if [ "$1" = "0" ]; then
	%service rusersd stop
	/sbin/chkconfig --del rusersd
fi

%post -n rstatd
/sbin/chkconfig --add rstatd
%service rstatd restart "rstatd server"

%preun -n rstatd
if [ "$1" = "0" ]; then
	%service rstatd stop
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
