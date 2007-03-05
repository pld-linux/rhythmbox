#
# Conditional build:
%bcond_without	ipod	# build without iPod support
#
Summary:	Music Management Application
Summary(pl):	Aplikacja do zarz±dzania muzyk±
Name:		rhythmbox
Version:	0.9.8
Release:	2
License:	GPL v2+
Group:		Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/rhythmbox/0.9/%{name}-%{version}.tar.bz2
# Source0-md5:	648400feb794538207b4fe95f0917d1f
Patch0:		%{name}-desktop.patch
Patch2:		%{name}-gtk2.8-crash.patch
Patch3:		%{name}-pyc.patch
Patch4:		%{name}-link.patch
URL:		http://www.rhythmbox.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-glib-devel
BuildRequires:	check >= 0.9.3
BuildRequires:	dbus-glib-devel >= 0.60
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-keyring-devel
BuildRequires:	gnome-vfs2-devel >= 2.14.0
BuildRequires:	gstreamer-devel >= 0.10.10
BuildRequires:	gstreamer-GConf >= 0.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10
BuildRequires:	gtk-doc
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	hal-devel >= 0.5.7
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnomeui-devel >= 2.14.0
%{?with_ipod:BuildRequires:	libgpod-devel >= 0.4.0}
BuildRequires:	libmusicbrainz-devel >= 2.1.4
BuildRequires:	libnotify-devel >= 0.4.0
BuildRequires:	libsexy-devel >= 0.1.5
BuildRequires:	libsoup-devel
BuildRequires:	libtool
BuildRequires:	lirc-devel
BuildRequires:	nautilus-cd-burner-devel >= 2.14.0.1-2
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2.10.1
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper
BuildRequires:	totem-devel >= 1.1.3
BuildRequires:	zlib-devel
%pyrequires_eq	python-modules
Requires(post,preun):	GConf2 >= 2.14.0
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires:	dbus >= 0.60
Requires:	gstreamer-audio-effects-base >= 0.10.10
Requires:	gstreamer-audio-formats >= 0.10.4
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= 0.10.10
Requires:	gstreamer-plugins-good >= 0.10.4
Requires:	gtk+2 >= 2:2.8.0
Requires:	libgnomeui >= 2.14.0
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
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
# for snapshots
gnome-doc-prepare --copy --force
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
	--enable-lirc \
	--with-cd-burning \
	--with-gnome-keyring \
	%{!?with_ipod:--without-ipod} \
	--with-mds=avahi \
	--with-internal-libsexy=no \
	--with-x
%{__make} -j1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

# there is no -devel subpackage, so we don't need APIdocs
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc

%find_lang %{name} --with-gnome

rm -f  $RPM_BUILD_ROOT%{_libdir}/bonobo/lib*.{la,a}
rm -f  $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins/*/*.{a,la}
rm -rf $RPM_BUILD_ROOT%{_datadir}/application-registry
rm -rf $RPM_BUILD_ROOT%{_datadir}/mime-info

find $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins -name "*.py" -exec rm -f {} \;
find $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins -name "*.a" -exec rm -f {} \;
find $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins -name "*.la" -exec rm -f {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
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
/sbin/ldconfig
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor

%files -f rhythmbox.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/rhythmbox-metadata
%attr(755,root,root) %{_libdir}/librhythmbox-core.so.*.*.*

%dir %{_libdir}/rhythmbox
%dir %{_libdir}/rhythmbox/plugins
%dir %{_libdir}/rhythmbox/plugins/artdisplay
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/artdisplay/*.py[co]
%{_libdir}/rhythmbox/plugins/artdisplay/rhythmbox-missing-artwork.svg
%{_libdir}/rhythmbox/plugins/artdisplay/*-plugin
%dir %{_libdir}/rhythmbox/plugins/audiocd
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/audiocd/*.so
%{_libdir}/rhythmbox/plugins/audiocd/*-plugin
%{_libdir}/rhythmbox/plugins/audiocd/*.glade
%dir %{_libdir}/rhythmbox/plugins/audioscrobbler
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/audioscrobbler/*.so
%{_libdir}/rhythmbox/plugins/audioscrobbler/*-plugin
%{_libdir}/rhythmbox/plugins/audioscrobbler/*.xml
%{_libdir}/rhythmbox/plugins/audioscrobbler/audioscrobbler-prefs.glade
%dir %{_libdir}/rhythmbox/plugins/cd-recorder
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/cd-recorder/*.so
%{_libdir}/rhythmbox/plugins/cd-recorder/*-plugin
%{_libdir}/rhythmbox/plugins/cd-recorder/recorder.glade
%dir %{_libdir}/rhythmbox/plugins/daap
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/daap/*.so
%{_libdir}/rhythmbox/plugins/daap/*-plugin
%{_libdir}/rhythmbox/plugins/daap/*.glade
%{_libdir}/rhythmbox/plugins/daap/*.xml
%dir %{_libdir}/rhythmbox/plugins/generic-player
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/generic-player/*.so
%{_libdir}/rhythmbox/plugins/generic-player/*-plugin
%{_libdir}/rhythmbox/plugins/generic-player/generic-player-ui.xml
%{?with_ipod:%dir %{_libdir}/rhythmbox/plugins/ipod}
%{?with_ipod:%attr(755,root,root) %{_libdir}/rhythmbox/plugins/ipod/*.so}
%{?with_ipod:%{_libdir}/rhythmbox/plugins/ipod/*-plugin}
%{?with_ipod:%{_libdir}/rhythmbox/plugins/ipod/ipod-ui.xml}
%dir %{_libdir}/rhythmbox/plugins/iradio
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/iradio/*.so
%{_libdir}/rhythmbox/plugins/iradio/*-plugin
%{_libdir}/rhythmbox/plugins/iradio/*.xml
%{_libdir}/rhythmbox/plugins/iradio/iradio-initial.pls
%{_libdir}/rhythmbox/plugins/iradio/station-properties.glade
%dir %{_libdir}/rhythmbox/plugins/jamendo
%{_libdir}/rhythmbox/plugins/jamendo/*.py[co]
%{_libdir}/rhythmbox/plugins/jamendo/*.glade
%{_libdir}/rhythmbox/plugins/jamendo/jamendo.rb-plugin
%{_libdir}/rhythmbox/plugins/jamendo/*.png
%dir %{_libdir}/rhythmbox/plugins/lirc
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/lirc/*.so
%{_libdir}/rhythmbox/plugins/lirc/*-plugin
%dir %{_libdir}/rhythmbox/plugins/lyrics
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/lyrics/*.py[co]
%{_libdir}/rhythmbox/plugins/lyrics/*-plugin
%dir %{_libdir}/rhythmbox/plugins/magnatune
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/magnatune/*.py[co]
%{_libdir}/rhythmbox/plugins/magnatune/*-plugin
%{_libdir}/rhythmbox/plugins/magnatune/*.glade
%{_libdir}/rhythmbox/plugins/magnatune/*.png
%dir %{_libdir}/rhythmbox/plugins/mmkeys
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/mmkeys/libmmkeys.so
%{_libdir}/rhythmbox/plugins/mmkeys/mmkeys.rb-plugin
%dir %{_libdir}/rhythmbox/plugins/power-manager
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/power-manager/*.so
%{_libdir}/rhythmbox/plugins/power-manager/*-plugin
%dir %{_libdir}/rhythmbox/plugins/python-console
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/python-console/*.py[co]
%{_libdir}/rhythmbox/plugins/python-console/*-plugin
%dir %{_libdir}/rhythmbox/plugins/rb
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/rb/*.py[co]
%dir %{_libdir}/rhythmbox/plugins/visualizer
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/visualizer/libvisualizer.so
%{_libdir}/rhythmbox/plugins/visualizer/visualizer-controls.glade
%{_libdir}/rhythmbox/plugins/visualizer/visualizer-ui.xml
%{_libdir}/rhythmbox/plugins/visualizer/visualizer.rb-plugin

%{_datadir}/%{name}
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/rhythmbox.png
%{_omf_dest_dir}/%{name}
%{_sysconfdir}/gconf/schemas/rhythmbox.schemas
