#
# Conditional build:
%bcond_without	ipod	# build without iPod support
#
Summary:	Music Management Application
Summary(pl):	Aplikacja do zarz±dzania muzyk±
Name:		rhythmbox
Version:	0.9.6
Release:	2
License:	GPL v2+
Group:		Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/rhythmbox/0.9/%{name}-%{version}.tar.bz2
# Source0-md5:	805459eafd670b18c663ba478ad2ebd4
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-broken_locale.patch
Patch2:		%{name}-gtk2.8-crash.patch
Patch3:		%{name}-pyc.patch
Patch4:		%{name}-use-icon-name.patch
URL:		http://www.rhythmbox.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-glib-devel >= 0.6.14
BuildRequires:	check >= 0.9.3
BuildRequires:	dbus-glib-devel >= 0.71
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-keyring-devel >= 0.6.0
BuildRequires:	gnome-vfs2-devel >= 2.16.0
BuildRequires:	gstreamer-devel >= 0.10.10
BuildRequires:	gstreamer-GConf >= 0.10.4
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.10
BuildRequires:	gtk-doc
BuildRequires:	gtk+2-devel >= 2:2.10.4
BuildRequires:	hal-devel >= 0.5.7
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnomeui-devel >= 2.16.0
%{?with_ipod:BuildRequires:	libgpod-devel >= 0.3.3}
BuildRequires:	libmusicbrainz-devel >= 2.1.4
BuildRequires:	libnotify-devel >= 0.4.2
BuildRequires:	libsexy-devel >= 0.1.10
BuildRequires:	libsoup-devel >= 2.2.96
BuildRequires:	libtool
BuildRequires:	nautilus-cd-burner-devel >= 2.16.0
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2.10.1
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper
BuildRequires:	totem-devel >= 2.16.1
BuildRequires:	zlib-devel
%pyrequires_eq	python-modules
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires:	dbus >= 0.93
Requires:	gstreamer-audio-effects-base >= 0.10.10
Requires:	gstreamer-audio-formats >= 0.10.4
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= 0.10.10
Requires:	gstreamer-plugins-good >= 0.10.4
Requires:	gtk+2 >= 2:2.10.4
Requires:	libgnomeui >= 2.16.0
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
# for snapshots
gnome-doc-prepare --copy
%{__gtkdocize}
%{__gnome_doc_common}
%{__glib_gettextize}
%{__intltoolize}
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

#rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

# there is no -devel subpackage, so we don't need APIdocs
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc

%find_lang %{name} --with-gnome

rm -f  $RPM_BUILD_ROOT%{_libdir}/bonobo/lib*.{la,a}
rm -f  $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins/*.{a,la}
rm -rf $RPM_BUILD_ROOT%{_datadir}/application-registry
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime-info

find $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins -name "*.py" -exec rm -f {} \;
find $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins -name "*.a" -exec rm -f {} \;
find $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins -name "*.la" -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
%gconf_schema_install rhythmbox.schemas
%scrollkeeper_update_post
%update_desktop_database_post
%update_icon_cache hicolor
%banner %{name} -e << EOF
Remember to install appropriate GStreamer plugins for files
you want to play:
- gstreamer-flac (for FLAC)
- gstreamer-mad (for MP3s)
- gstreamer-vorbis (for Ogg Vorbis)
- gstreamer-neon (for HTTP streams)
EOF

%preun
%gconf_schema_uninstall rhythmbox.schemas

%postun 
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f rhythmbox.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/rhythmbox-metadata

%dir %{_libdir}/rhythmbox
%dir %{_libdir}/rhythmbox/plugins
%dir %{_libdir}/rhythmbox/plugins/artdisplay
%dir %{_libdir}/rhythmbox/plugins/audioscrobbler
%dir %{_libdir}/rhythmbox/plugins/cd-recorder
%dir %{_libdir}/rhythmbox/plugins/generic-player
%dir %{_libdir}/rhythmbox/plugins/ipod
%dir %{_libdir}/rhythmbox/plugins/lirc
%dir %{_libdir}/rhythmbox/plugins/lyrics
%dir %{_libdir}/rhythmbox/plugins/python-console
%dir %{_libdir}/rhythmbox/plugins/rb
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/*.so
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/audioscrobbler/*.so
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/cd-recorder/*.so
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/generic-player/*.so
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/ipod/*.so
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/lirc/*.so
%{_libdir}/rhythmbox/plugins/*-plugin
%{_libdir}/rhythmbox/plugins/artdisplay/*.py[co]
%{_libdir}/rhythmbox/plugins/artdisplay/*-plugin
%{_libdir}/rhythmbox/plugins/audioscrobbler/*-plugin
%{_libdir}/rhythmbox/plugins/cd-recorder/*-plugin
%{_libdir}/rhythmbox/plugins/generic-player/*-plugin
%{_libdir}/rhythmbox/plugins/ipod/*-plugin
%{_libdir}/rhythmbox/plugins/lirc/*-plugin
%{_libdir}/rhythmbox/plugins/lyrics/*-plugin
%{_libdir}/rhythmbox/plugins/lyrics/*.py[co]
%{_libdir}/rhythmbox/plugins/python-console/*-plugin
%{_libdir}/rhythmbox/plugins/python-console/*.py[co]
%{_libdir}/rhythmbox/plugins/rb/*.py[co]

%{_datadir}/%{name}
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/*
%{_iconsdir}/hicolor/*/*/rhythmbox.png
%{_omf_dest_dir}/%{name}
%{_sysconfdir}/gconf/schemas/rhythmbox.schemas
