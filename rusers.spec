Summary:	Displays the users logged into machines on the local network
Summary(de):	Anzeige von Login-Infos für entfernte Computer
Summary(es):	El cliente rusers
Summary(fr):	Affiche des informations de login pour les machines distantes
Summary(pl):	Wy¶wietla listê u¿ytkowników zalogowanych na komputerach w sieci lokalnej
Summary(pt_BR):	Mostra a informação de login para máquinas remotas
Summary(tr):	Að üzerindeki makinalardaki kullanýcýlarý sorgular
Name:		rusers
Version:	0.17
Release:	14
License:	BSD
Group:		Networking
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

%description -l pl
Program rusers pozwala u¿ytkownikom sprawdziæ kto jest zalogowany na
ró¿nych maszynach w sieci lokalnej. Wynik komendy rusers jest podobne
do komendy who, ale dla okre¶lonej listy komputerów lub wszystkich
maszyn z sieci lokalnej.

%description -l pt_BR
O programa rusers permite descobrir quem está em várias máquinas na
rede. O comando rusers fornece uma saída similar a do comando who para
a lista de máquinas especificada ou para todas as máquinas da rede
local.

%description -l tr
Bu pakette yer alan rusers sunucusu ve istemcisi ile bir kullanýcý að
üzerinde bu hizmeti sunan diðer makinalardaki kullanýcýlarý
sorgulayabilir.

%package -n rusersd
Summary:	Server for the rusers protocol
Summary(es):	El servidor rusers
Summary(pl):	Serwer protoko³u rusers
Summary(pt_BR):	Servidor para o protocolo rusers
Group:		Networking/Daemons
Obsoletes:	rusers-server
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts

%description -n rusersd
The rusersd package contains the server for responding to rusers
requests.

%description -n rusersd -l pt_BR
Servidor para o protocolo rusers.

%description -n rusersd -l pl
Pakiet rusersd zawiera serwer odpowiadaj±cy na zapytania rusers.

%description -n rusersd -l es
El servidor rusers incluido en este paquete, permiten ver cual de los
usuarios están "logados" en otras máquinas de la red.

%package -n rup
Summary:	rstatd client
Summary(pl):	Klient rstatd
Group:		Networking

%description -n rup
rup displays a summary of the current system status of a particular
host or all hosts on the local network. The output shows the current
time of day, how long the system has been up, and the load averages.
The load average numbers give the number of jobs in the run queue
averaged over 1, 5 and 15 minutes.

%description -n rup -l pl
rup wy¶wietla podsumowanie aktualnego stanu systemu dla okre¶lonego
komputera lub wszystkich z sieci lokalnej. Wyj¶cie zawiera aktualny
czas, jak d³ugo system jest w³±czony i obci±¿enie. Obci±¿enie podawane
jest jako ilo¶æ procesów w kolejce ¶rednio w 1, 5 i 15 minut.

%package -n rstatd
Summary:	kernel statistics server
Summary(pl):	Serwer rstatd
Group:		Networking/Daemons
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts

%description -n rstatd
rpc.rstatd is a server which returns performance statistics obtained
from the kernel. These statistics are usually read using the rup(1)
command.

%description -n rstatd -l pl
rpc.rstatd to serwer podaj±cy statystyki wydajno¶ci pobrane od j±dra.
Statystyki te zwykle s± czytane komend± rup(1).

%prep
%setup -q -n netkit-rusers-%{version} -a3
%patch0 -p1
%patch1 -p1

%build
./configure

%{__make} CC="%{__cc}" \
	CFLAGS="%{rpmcflags} -DGNU_LIBC -D_GNU_SOURCE -D_NO_UT_TIME"

%{__make} CC="%{__cc}" \
	CFLAGS="%{rpmcflags}" -C rpc.rstatd

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

%preun -n rusersd
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

%preun -n rstatd
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
