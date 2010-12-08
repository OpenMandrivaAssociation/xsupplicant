%define name xsupplicant
%define version 2.2.0
%define release %mkrel 3

Summary:	Implementation of IEEE 802.1X
Name:		%{name}
Version:	%{version}
Release:	%{release}
Epoch:		0
Url:		http://open1x.sourceforge.net/
Source0:	http://download.sourceforge.net/open1x/XSupplicant-%{version}-src.tar.gz
Source1:	XSupplicantUI.desktop
Patch0:		xsupplicant-2.2.0-fix-link.patch
Patch2:		xsupplicant-2.1.8-ui-Fedora.patch
Patch3:		XSupplicant-2.1.8-ppc-fix.patch
Patch4:		xsupplicant-2.1.9-force-release.patch
Patch5:		xsupplicant-2.2.0-implicit-DSO.patch
License:	GPLv2+ or BSD with advertising
Group:		Networking/Other
BuildRoot:	%{_tmppath}/%{name}-buildroot
Requires:	pcsc-lite
BuildRequires:	openssl-devel
BuildRequires:	pcsc-lite-devel
BuildRequires:  libiw-devel
BuildRequires:	qt4-devel
BuildRequires:	zlib-devel
BuildRequires:	desktop-file-utils
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

%package ui
Summary:	Graphical User Interface for xsupplicant
Group:		Networking/Other
License:	GPLv2
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description ui
QT User Interface for XSupplicant.

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
%setup -qn XSupplicant-%{version}-src
%patch0 -p0
# Find UI files in a sane system location
%patch2 -p1 -b .Fedora
# Fix PPC (enough to get it building, not run-tested)
%patch3 -p1 -b .ppc
# Force the UI bits to be built as "release", not "debug"
%patch4 -p1 -b .release
# Fix implicit linking issues
%patch5 -p1 -b .DSO

%build
pushd %name
autoreconf -fi
%configure2_5x
%make
popd

pushd %name-ui/xsupptray
%qmake_qt4 XSupplicantUI-unix.pro
%make
popd

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall_std -C %name

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
touch $RPM_BUILD_ROOT%{_sysconfdir}/xsupplicant.conf
touch $RPM_BUILD_ROOT%{_sysconfdir}/xsupplicant.user.conf

rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_libdir}/*.a

# ui bits
pushd xsupplicant-ui
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp -a Skins $RPM_BUILD_ROOT%{_datadir}/%{name}/
install -p build-release/XSupplicantUI $RPM_BUILD_ROOT%{_bindir}
popd

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
desktop-file-install --dir $RPM_BUILD_ROOT%{_datadir}/applications %{SOURCE1}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps/
cp xsupplicant-ui/Skins/Default/icons/prod_color.png $RPM_BUILD_ROOT%{_datadir}/pixmaps/XSupplicantUI.png

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc xsupplicant/AUTHORS xsupplicant/COPYING 
%doc xsupplicant/LICENSE xsupplicant/README 
%doc xsupplicant/doc/README* 
%doc xsupplicant/doc/extending_*
%doc xsupplicant/doc/xsupplicant_eap*
%doc xsupplicant/doc/Xsupplicant-wireless-cards.html
%doc xsupplicant/etc/*.conf
%config(noreplace) %ghost %{_sysconfdir}/xsupplicant.conf
%config(noreplace) %ghost %{_sysconfdir}/xsupplicant.user.conf
%{_bindir}/*
%{_libdir}/libbirddog.so.*
%{_libdir}/libsoftsim*.so
%{_bindir}/xsup_ntpwdhash
%{_sbindir}/xsupplicant

%files -n %{name}-devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/libbirddog.so

%files ui
%defattr(-,root,root,-)
%doc xsupplicant-ui/Doc/*.odt  xsupplicant-ui/Doc/*.pdf  xsupplicant-ui/Doc/*.txt
%{_bindir}/XSupplicantUI
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/XSupplicantUI.png
%{_datadir}/%{name}/

%files doc
%defattr(-,root,root)
%doc xsupplicant/doc/standards
