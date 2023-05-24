Name: c2-ec2-netutils
Group: server
Summary: A set of network tools for managing and auto configuration ENIs
Version: 1.1
Release: 1%{?dist}
License: MIT
Source0: 53-c2-network-interfaces.rules.systemd
Source2: 75-persistent-net-generator.rules
Source3: ec2net-functions
Source4: c2-net.hotplug
Source5: ec2ifup
Source6: ec2ifdown
Source7: ec2ifup.8
Source8: ec2ifscan
Source9: ec2ifscan.8
Source10: elastic-network-interfaces.conf
Source11: ec2net-scan.service
Source12: c2_write_net_rules
Source13: c2_rule_generator.functions
Source14: ec2net-ifup@.service

Url: https://github.com/C2Devel/c2-ec2-netutils
BuildArch: noarch
Requires: NetworkManager
Requires: curl
Requires: sed
Requires: iproute2

Provides: c2-ec2-netutils

%description
c2-ec2-netutils contains a set of utilities for managing elastic network interfaces.

%prep
%build
%install
mkdir -p $RPM_BUILD_ROOT%_sysconfdir/udev/rules.d/
mkdir -p $RPM_BUILD_ROOT%_sysconfdir/sysconfig/c2-ec2-netutils/
mkdir -p $RPM_BUILD_ROOT%_sysconfdir/sysconfig/c2-ec2-netutils/scripts/
mkdir -p $RPM_BUILD_ROOT%_mandir/man8/

install -m644 %SOURCE2 $RPM_BUILD_ROOT%_sysconfdir/udev/rules.d/
install -m644 %SOURCE3 $RPM_BUILD_ROOT%_sysconfdir/sysconfig/c2-ec2-netutils/scripts/
install -m755 %SOURCE4 $RPM_BUILD_ROOT%_sysconfdir/sysconfig/c2-ec2-netutils/scripts/
install -d -m755 $RPM_BUILD_ROOT%_sbindir
install -m755 %SOURCE5 $RPM_BUILD_ROOT%_sbindir/
install -m755 %SOURCE6 $RPM_BUILD_ROOT%_sbindir/
install -m755 %SOURCE8 $RPM_BUILD_ROOT%_sbindir/
install -m644 %SOURCE0 $RPM_BUILD_ROOT%_sysconfdir/udev/rules.d/53-c2-network-interfaces.rules
install -d -m755 $RPM_BUILD_ROOT%_unitdir
install -m644 %SOURCE11 $RPM_BUILD_ROOT%_unitdir/ec2net-scan.service
install -m644 %SOURCE14 $RPM_BUILD_ROOT%_unitdir/ec2net-ifup@.service
install -d -m755 $RPM_BUILD_ROOT/lib/udev
install -m644 %SOURCE12 $RPM_BUILD_ROOT/lib/udev
install -m644 %SOURCE13 $RPM_BUILD_ROOT/lib/udev

%post
ln -s -f %_unitdir/ec2net-scan.service %_sysconfdir/systemd/system/multi-user.target.wants/ec2net-scan.service

%postun
%__rm -f %_sysconfdir/systemd/system/multi-user.target.wants/ec2net-scan.service

%files
%_sysconfdir/udev/rules.d/53-c2-network-interfaces.rules
%_sysconfdir/udev/rules.d/75-persistent-net-generator.rules
%_sysconfdir/sysconfig/c2-ec2-netutils/scripts/ec2net-functions
%_sysconfdir/sysconfig/c2-ec2-netutils/scripts/c2-net.hotplug
%_sbindir/ec2ifup
%_sbindir/ec2ifdown
%_sbindir/ec2ifscan
%attr(0644,root,root) %_unitdir/ec2net-scan.service
%attr(0644,root,root) %_unitdir/ec2net-ifup@.service
%attr(755, -, -) /lib/udev/c2_write_net_rules
/lib/udev/c2_rule_generator.functions

%changelog
* Wed Sep 26 2023 Georgy Melnikov <gmelnikov@croc.ru> 1.1
- create c2-ec2-netutils for ALT Linux (NM keyfile backend)

