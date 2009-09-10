%define name xsupplicant
%define version 1.2.8
%define release %mkrel 7
%define build_qt_gremlin 0

Summary:	Implementation of IEEE 802.1X
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		0
Url:		http://open1x.sourceforge.net/
Source0:	http://download.sourceforge.net/open1x/xsupplicant-%{version}.tar.bz2
Patch0:		xsupplicant-1.2.8-wireless_inc.patch
License:	GPL
Group:		Networking/Other
BuildRoot:	%{_tmppath}/%{name}-buildroot
Requires:	pcsc-lite
BuildRequires:	byacc
BuildRequires:	docbook-utils-pdf
BuildRequires:  docbook-dtd30-sgml
BuildRequires:	flex
BuildRequires:	lynx
BuildRequires:	openjade
BuildRequires:	openssl-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:	qt3-devel
BuildRequires:  libiw-devel
BuildConflicts: docbook-dtd44-xml

%description
An open source implementation of IEEE 802.1X.

IEEE 802.1x is a port based authentication protocol. It can be used in *any*
scenario where one can abstract out the notion of a port. It requires
entitie(s) to play three roles in the authentication process: that of an
supplicant, an authenticator and an authentication server.

%package -n %{name}-devel
Group:		Development/C
Summary:	Development files from %{name}

%description -n %{name}-devel
Development files from %{name}

An open source implementation of IEEE 802.1X.

IEEE 802.1x is a port based authentication protocol. It can be used in *any*
scenario where one can abstract out the notion of a port. It requires
entitie(s) to play three roles in the authentication process: that of an
supplicant, an authenticator and an authentication server.

%package doc
Group:		Networking/Other
Summary:	Implementation of the IEEE 802.1x protocol

%description doc
An open source implementation of IEEE 802.1X.

IEEE 802.1x is a port based authentication protocol. It can be used in *any*
scenario where one can abstract out the notion of a port. It requires
entitie(s) to play three roles in the authentication process: that of an
supplicant, an authenticator and an authentication server.

%prep
%setup -q
%patch0 -p1 -b .wireless_inc

%build
autoreconf -i
touch config.h
# pcsc-lite-devel 1.2.9+ has winscard.h in %{_includedir}/PCSC instead
# of just %{_includedir}. And this header file is needed for eap-sim
# support
export CPPFLAGS="-I%{_includedir}/PCSC"
%configure # --enable-eap-sim
# (cjw) parallel make doesn't always work
make
cd doc; ./builddocs.sh
%if %{build_qt_gremlin}
cd ../gui_tools/gui/qt/qt_gremlin; qmake qt_gremlin_xsupplicant.pro; %make
%endif

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall_std
mkdir -p %{buildroot}/etc/
mkdir -p %{buildroot}/usr/share/doc/%{name}
install -m 644 etc/xsupplicant.conf %{buildroot}/etc/xsupplicant.conf
%if %{build_qt_gremlin}
install -m 755 gui_tools/gui/qt/qt_gremlin/qt_gremlin_xsupplicant %{buildroot}/%{_sbindir}/qt_gremlin_xsupplicant
install -m 644 gui_tools/gui/qt/qt_gremlin/README %{buildroot}/usr/share/doc/%{name}/README.qt_gremlin
%endif
install -m 644 etc/*-example.conf %{buildroot}/usr/share/doc/%{name}/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING INSTALL LICENSE README TODO doc/README.* doc/*.html
%doc etc/*example.conf
%doc tools/pkcs12toDERandPEM.sh tools/updatedir
%config(noreplace)/etc/xsupplicant.conf
%{_bindir}/config-parser
%{_bindir}/xsup_monitor
%{_bindir}/xsup_get_state
%{_bindir}/xsup_set_pwd
%{_bindir}/xsup_ntpwdhash
%{_sbindir}/xsupplicant
%if %{build_qt_gremlin}
%{_sbindir}/qt_gremlin_xsupplicant
%endif

%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*.a

%files doc
%defattr(-,root,root)
%doc doc/code-design/*.pdf doc/html doc/pdf doc/standards doc/txt


