Summary:	Music Management Application
Summary(pl):	Aplikacja do zarz±dzania muzyk±
Name:		rhythmbox
Version:	0.5.0
Release:	1
License:	GPL
Group:		Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.5/%{name}-%{version}.tar.bz2
Patch0:	rb-mmkeys3.diff
# from http://www.uni-bonn.de/~jpeterse/rb-mmkeys3.diff 
# Source0-md5:	7a0f8a9bbf964b95778889e26aa011ae
BuildRequires:	flac-devel
BuildRequires:	gnome-vfs2-devel
BuildRequires:	gstreamer-GConf-devel
BuildRequires:	gstreamer-devel >= 0.6.1
BuildRequires:	gstreamer-plugins-devel >= 0.6.1
BuildRequires:	gtk+2-devel >= 2.2.1
BuildRequires:	libbonobo-devel >= 2.3.6
BuildRequires:	libglade2-devel
BuildRequires:	libgnomecanvas-devel >= 2.3.6
BuildRequires:	libgnomeui-devel >= 2.3.6
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	lirc-devel
BuildRequires:	mad-devel
BuildRequires:	libmusicbrainz-devel >= 2.0.1
BuildRequires:	pkgconfig
BuildRequires:	xosd-devel
BuildRequires:	zlib-devel
Requires(post):	/sbin/ldconfig
Requires(post):	GConf2
Requires:	gtk+2 >= 2.2.1
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rhythmbox is your one-stop multimedia application, supporting a music
library, multiple "music groups", internet radio, and more.

%description -l pl
Rhythmbox to kompletna aplikacja multimedialna, obs³uguj±ca bibliotekê
muzyczn±, wiele "grup muzyki", radio internetowe itp.

%prep
%setup -q
%patch0 -p0

%build
%configure \
	--disable-schemas-install

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%find_lang %{name} --with-gnome --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install

%postun -p /sbin/ldconfig

%files -f rhythmbox.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS
%attr(755,root,root) %{_bindir}/*
%{_sysconfdir}/gconf/schemas/*
%{_datadir}/%{name}
%{_desktopdir}/*
%{_datadir}/application-registry/*
%{_pixmapsdir}/*
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/idl/*
%{_libdir}/bonobo/*.so
%{_libdir}/bonobo/servers/*
%{_pkgconfigdir}/*
