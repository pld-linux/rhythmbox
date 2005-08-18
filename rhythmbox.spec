Summary:	Music Management Application
Summary(pl):	Aplikacja do zarz±dzania muzyk±
Name:		rhythmbox
Version:	0.9.0
Release:	2
License:	GPL v2+
Group:		Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/rhythmbox/0.9/%{name}-%{version}.tar.bz2
# Source0-md5:	3e01834c5085af7fc11d0b98b76b9354
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-broken_locale.patch
URL:		http://www.rhythmbox.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gstreamer-GConf-devel >= 0.8.8
BuildRequires:	gstreamer-devel >= 0.8.9
BuildRequires:	gstreamer-plugins-devel >= 0.8.8
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	intltool
BuildRequires:	libbonobo-devel >= 2.8.0
BuildRequires:	libglade2-devel >= 1:2.5.0
BuildRequires:	libgnomeui-devel >= 2.10.0-2
BuildRequires:	libmusicbrainz-devel >= 2.0.1
BuildRequires:	libtool
BuildRequires:	nautilus-cd-burner-devel >= 2.9.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.176
BuildRequires:	scrollkeeper
BuildRequires:	totem-devel >= 1.1.3
BuildRequires:	zlib-devel
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	/usr/bin/scrollkeeper-update
Requires(post,preun):	GConf2
Requires:	gstreamer-audio-effects >= 0.8.8
Requires:	gstreamer-audio-formats >= 0.8.8
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= 0.8.8
Requires:	gtk+2 >= 2:2.6.3
Obsoletes:	net-rhythmbox
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rhythmbox is your one-stop multimedia application, supporting a music
library, multiple "music groups", internet radio, and more.

%description -l pl
Rhythmbox to kompletna aplikacja multimedialna, obs³uguj±ca bibliotekê
muzyczn±, wiele "grup muzyki", radio internetowe itp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

# broken
rm po/{ar,mn}.po

%build
%{__intltoolize}
%{__glib_gettextize}
%{__libtoolize}
%{__aclocal}
%{__autoheader}
%{__automake}
%{__autoconf}
# NOTE: ipod needs dbus < 0.30, not ported yet
%configure \
	--disable-schemas-install \
	--with-bonobo \
	--with-cd-burner
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --with-gnome --all-name

rm -f  $RPM_BUILD_ROOT%{_libdir}/bonobo/lib*.{la,a}
rm -rf $RPM_BUILD_ROOT%{_datadir}/application-registry
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime-info

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install rhythmbox.schemas
%scrollkeeper_update_post
%update_desktop_database_post
%banner %{name} -e << EOF
Remember to install appropriate GStreamer plugins for files
you want to play:
- gstreamer-flac (for FLAC)
- gstreamer-mad (for MP3s)
- gstreamer-vorbis (for Ogg Vorbis)
EOF

%preun
%gconf_schema_uninstall rhythmbox.schemas

%postun
%scrollkeeper_update_postun
%update_desktop_database_postun

%files -f rhythmbox.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/bonobo/*.so
%{_datadir}/idl/*
%{_datadir}/%{name}
%{_desktopdir}/*
%{_libdir}/bonobo/servers/*
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/*
%{_pkgconfigdir}/*
%{_sysconfdir}/gconf/schemas/rhythmbox.schemas
