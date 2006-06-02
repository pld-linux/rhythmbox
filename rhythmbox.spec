#
# Conditional build:
%bcond_without	ipod	# build without iPod support
#
Summary:	Music Management Application
Summary(pl):	Aplikacja do zarz±dzania muzyk±
Name:		rhythmbox
Version:	0.9.4.1
Release:	7
License:	GPL v2+
Group:		Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/rhythmbox/0.9/%{name}-%{version}.tar.bz2
# Source0-md5:	d725eb7134d1997efe28285715ebc05e
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-broken_locale.patch
Patch2:		%{name}-gtk2.8-crash.patch
Patch3:		%{name}-pyc.patch
Patch4:		%{name}-use-icon-name.patch
URL:		http://www.rhythmbox.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-glib-devel
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	gnome-vfs2-devel >= 2.14.0
BuildRequires:	gstreamer-devel >= 0.10.2
BuildRequires:	gstreamer-GConf >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	hal-devel >= 0.5.4
BuildRequires:	intltool
BuildRequires:	libbonobo-devel >= 2.14.0
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeui-devel >= 2.14.0
%{?with_ipod:BuildRequires:	libgpod-devel >= 0.3.0}
BuildRequires:	libmusicbrainz-devel >= 2.0.1
BuildRequires:	libnotify-devel >= 0.4.0
BuildRequires:	libsexy-devel >= 0.1.5
BuildRequires:	libsoup-devel
BuildRequires:	libtool
BuildRequires:	nautilus-cd-burner-devel >= 2.14.0.1-2
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2.6.0
BuildRequires:	rpmbuild(macros) >= 1.176
BuildRequires:	scrollkeeper
BuildRequires:	totem-devel >= 1.1.3
BuildRequires:	zlib-devel
%pyrequires_eq	python-modules
Requires(post,preun):	GConf2
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires:	dbus >= 0.60
Requires:	gstreamer-audio-effects-base >= 0.10
Requires:	gstreamer-plugins-good >= 0.10.3
Requires:	gstreamer-audio-formats >= 0.10.3
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= 0.10
Requires:	gtk+2 >= 2:2.6.3
Requires:	libgnomeui >= 2.14.1
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
%patch2 -p1
%patch3 -p1
%patch4 -p1

# broken
rm po/{ar,mn}.po

%build
%{__intltoolize}
%{__glib_gettextize}
%{__libtoolize}
%{__aclocal} -I macros
%{__autoheader}
%{__automake}
%{__autoconf}
%configure \
	--disable-schemas-install \
	--disable-scrollkeeper \
	--with-bonobo \
	--with-cd-burner \
	--with-dbus \
	%{!?with_ipod:--without-ipod} \
	--with-mds=avahi \
	--with-internal-libsexy=no
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

# there is no -devel subpackage, so we don't need APIdocs
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc

%find_lang %{name} --with-gnome --all-name

rm -f  $RPM_BUILD_ROOT%{_libdir}/bonobo/lib*.{la,a}
rm -f  $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins/*.{a,la,py}
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
- gstreamer-neon (for HTTP streams)

EOF

%postun 
%scrollkeeper_update_postun
%update_desktop_database_postun

%preun
%gconf_schema_uninstall rhythmbox.schemas

%files -f rhythmbox.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/bonobo/*.so
%attr(755,root,root) %{_libdir}/rhythmbox-metadata

%dir %{_libdir}/rhythmbox
%dir %{_libdir}/rhythmbox/plugins
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/*.so
%{_libdir}/rhythmbox/plugins/*-plugin
%{_libdir}/rhythmbox/plugins/*.py[co]

%{_datadir}/idl/*
%{_datadir}/%{name}
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/*
%{_libdir}/bonobo/servers/*
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/*
%{_pkgconfigdir}/*
%{_sysconfdir}/gconf/schemas/rhythmbox.schemas
