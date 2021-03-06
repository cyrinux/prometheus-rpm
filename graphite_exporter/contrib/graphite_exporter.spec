%define _unpackaged_files_terminate_build 0
%define debug_package %{nil}
%bcond_with sysvinit
%bcond_without systemd

Name:		graphite-exporter
Version:        %{version}
%if %{with sysvinit}
Release:        1.sysvinit%{?dist}
%endif
%if %{with systemd}
Release:        1%{?dist}
%endif
Summary:	Prometheus exporter for receiving graphite metrics.
Group:		System Environment/Daemons
License:	See the LICENSE file at github.
URL:		https://github.com/prometheus/graphite_exporter
Source0:        https://github.com/prometheus/graphite_exporter/releases/download/%{version}/graphite_exporter-%{version}.linux-amd64.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-root
Requires(pre):  /usr/sbin/useradd
%if %{with sysvinit}
Requires:       daemonize
%endif
%if %{with systemd}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif
AutoReqProv:    No

%description

Prometheus exporter for machine metrics, written in Go with pluggable metric collectors.

%prep
%setup -q -n graphite_exporter-%{version}.linux-amd64

%build
echo

%install
mkdir -vp $RPM_BUILD_ROOT/var/log/prometheus/
mkdir -vp $RPM_BUILD_ROOT/var/run/prometheus
mkdir -vp $RPM_BUILD_ROOT/var/lib/prometheus
mkdir -vp $RPM_BUILD_ROOT/usr/bin
%if %{with sysvinit}
mkdir -vp $RPM_BUILD_ROOT/etc/init.d
mkdir -vp $RPM_BUILD_ROOT/etc/sysconfig
%endif
%if %{with systemd}
mkdir -vp $RPM_BUILD_ROOT/usr/lib/systemd/system
%endif

install -m 755 graphite_exporter $RPM_BUILD_ROOT/usr/bin/graphite_exporter
%if %{with sysvinit}
install -m 755 contrib/graphite_exporter.init $RPM_BUILD_ROOT/etc/init.d/graphite_exporter
install -m 644 contrib/graphite_exporter.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/graphite_exporter
%endif
%if %{with systemd}
install -m 755 contrib/graphite_exporter.service $RPM_BUILD_ROOT/usr/lib/systemd/system/graphite_exporter.service
%endif


%clean

%pre
getent group prometheus >/dev/null || groupadd -r prometheus
getent passwd prometheus >/dev/null || \
  useradd -r -g prometheus -s /sbin/nologin \
    -d $RPM_BUILD_ROOT/var/lib/prometheus/ -c "prometheus Daemons" prometheus
exit 0

%post
chgrp prometheus /var/run/prometheus
chmod 774 /var/run/prometheus
chown prometheus:prometheus /var/log/prometheus
chmod 744 /var/log/prometheus

%files
%defattr(-,root,root,-)
/usr/bin/graphite_exporter
/var/run/prometheus
/var/log/prometheus
%if %{with sysvinit}
/etc/init.d/graphite_exporter
%config(noreplace) /etc/sysconfig/graphite_exporter
%endif
%if %{with systemd}
/usr/lib/systemd/system/graphite_exporter.service
%endif

