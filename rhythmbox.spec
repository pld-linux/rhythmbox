#
# Conditional build:
%bcond_without	ipod	# build without iPod support
%bcond_without	mtp	# build without MTP support
%bcond_without	track_transfer	# build without track transfer support
#
Summary:	Music Management Application
Summary(pl.UTF-8):	Aplikacja do zarządzania muzyką
Name:		rhythmbox
Version:	0.11.6
Release:	3
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/rhythmbox/0.11/%{name}-%{version}.tar.bz2
# Source0-md5:	b827e047d13954ba956c3c4ea940935e
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-gtk2.8-crash.patch
Patch2:		%{name}-pyc.patch
Patch3:		%{name}-link.patch
Patch4:		%{name}-bug499208.patch
Patch5:		%{name}-lt.patch
Patch6:		%{name}-libmtp.patch
URL:		http://www.rhythmbox.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	avahi-glib-devel >= 0.6.14
BuildRequires:	check >= 0.9.4
BuildRequires:	dbus-glib-devel >= 0.71
BuildRequires:	gnome-common
BuildRequires:	gnome-doc-utils
BuildRequires:	gnome-keyring-devel >= 0.8
%{?with_track_transfer:BuildRequires:	gnome-media-devel}
BuildRequires:	gnome-vfs2-devel >= 2.18.0.1
BuildRequires:	gstreamer-GConf >= 0.10.4
BuildRequires:	gstreamer-devel >= 0.10.10
BuildRequires:	gstreamer-plugins-base-devel >= 0.10.10
BuildRequires:	gtk+2-devel >= 2:2.10.10
BuildRequires:	gtk-doc
BuildRequires:	hal-devel >= 0.5.7
BuildRequires:	intltool
BuildRequires:	libglade2-devel >= 1:2.6.0
BuildRequires:	libgnomeui-devel >= 2.18.1
%{?with_ipod:BuildRequires:	libgpod-devel >= 0.5.2}
%{?with_mtp:BuildRequires:	libmtp-devel >= 0.3.0}
BuildRequires:	libmusicbrainz-devel >= 2.1.4
BuildRequires:	libnotify-devel >= 0.4.2
BuildRequires:	libsexy-devel >= 0.1.10
BuildRequires:	libsoup-devel >= 2.2.100
BuildRequires:	libtool
BuildRequires:	lirc-devel
BuildRequires:	nautilus-cd-burner-devel >= 2.18.0
BuildRequires:	pkgconfig
BuildRequires:	python-pygtk-devel >= 2:2.10.4
BuildRequires:	python-gstreamer-devel >= 0.10.1
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	scrollkeeper
BuildRequires:	sed >= 4.0
BuildRequires:	totem-pl-parser-devel >= 2.22.0
BuildRequires:	xulrunner-devel
BuildRequires:	zlib-devel
%pyrequires_eq	python-modules
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	scrollkeeper
Requires(post,preun):	GConf2
Requires:	dbus >= 0.93
Requires:	gstreamer-audio-effects-base >= 0.10.10
Requires:	gstreamer-audio-formats >= 0.10.4
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= 0.10.10
Requires:	gstreamer-plugins-good >= 0.10.4
Requires:	gtk+2 >= 2:2.10.10
Requires:	libgnomeui >= 2.18.1
Suggests:	gnome-vfs2
Suggests:	gstreamer-flac
Suggests:	gstreamer-mad
Suggests:	gstreamer-neon
Suggests:	gstreamer-vorbis
Suggests:	python-Louie
Suggests:	python-coherence
Suggests:	python-gnome
Suggests:	python-gnome-vfs
Suggests:	python-gstreamer
Obsoletes:	net-rhythmbox
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rhythmbox is your one-stop multimedia application, supporting a music
library, multiple "music groups", internet radio, and more.

%description -l pl.UTF-8
Rhythmbox to kompletna aplikacja multimedialna, obsługująca bibliotekę
muzyczną, wiele "grup muzyki", radio internetowe itp.

%package -n browser-plugin-%{name}
Summary:	Rhythmbox's browser plugin
Summary(pl.UTF-8):	Wtyczka Rhythmboksa do przeglądarek WWW
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})

%description -n browser-plugin-%{name}
Rhythmbox's plugin for browsers.

%description -n browser-plugin-%{name} -l pl.UTF-8
Wtyczka Rhythmboksa do przeglądarek WWW.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p0

%{__sed} -i -e 's#sr@Latn#sr@latin#' po/LINGUAS
mv po/sr@{Latn,latin}.po
# Pashto not yet supported by (our?) libc
%{__sed} -i -e 's#ps##' po/LINGUAS
rm -rf po/ps

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
	%{?with_track_transfer:--enable-track-transfer} \
	--with-x
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_browserpluginsdir}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

mv $RPM_BUILD_ROOT%{_libdir}/mozilla/plugins/* $RPM_BUILD_ROOT%{_browserpluginsdir}

# there is no -devel subpackage, so we don't need APIdocs
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc

%find_lang %{name} --with-gnome --with-omf

rm -f  $RPM_BUILD_ROOT%{_libdir}/librhythmbox-core.{la,a}
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

%preun
%gconf_schema_uninstall rhythmbox.schemas

%postun
/sbin/ldconfig
%scrollkeeper_update_postun
%update_desktop_database_postun
%update_icon_cache hicolor

%post -n browser-plugin-%{name}
%update_browser_plugins

%postun -n browser-plugin-%{name}
if [ "$1" = 0 ]; then
	%update_browser_plugins
fi

%files -f rhythmbox.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_libdir}/rhythmbox-metadata
%attr(755,root,root) %{_libdir}/librhythmbox-core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librhythmbox-core.so.0
%dir %{_libdir}/rhythmbox
%dir %{_libdir}/rhythmbox/plugins
%dir %{_libdir}/rhythmbox/plugins/artdisplay
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/artdisplay/*.py[co]
%{_libdir}/rhythmbox/plugins/artdisplay/rhythmbox-missing-artwork.svg
%{_libdir}/rhythmbox/plugins/artdisplay/*-plugin
%dir %{_libdir}/rhythmbox/plugins/audiocd
%{_libdir}/rhythmbox/plugins/audiocd/*.xml
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/audiocd/*.so
%{_libdir}/rhythmbox/plugins/audiocd/*-plugin
%{_libdir}/rhythmbox/plugins/audiocd/*.glade
%dir %{_libdir}/rhythmbox/plugins/audioscrobbler
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/audioscrobbler/*.so
%{_libdir}/rhythmbox/plugins/audioscrobbler/*-plugin
%{_libdir}/rhythmbox/plugins/audioscrobbler/*.xml
%{_libdir}/rhythmbox/plugins/audioscrobbler/as-icon.png
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
%dir %{_libdir}/rhythmbox/plugins/fmradio
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/fmradio/*.so
%{_libdir}/rhythmbox/plugins/fmradio/*-plugin
%{_libdir}/rhythmbox/plugins/fmradio/*.xml
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
%{_libdir}/rhythmbox/plugins/lyrics/lyrics-prefs.glade
%dir %{_libdir}/rhythmbox/plugins/magnatune
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/magnatune/*.py[co]
%{_libdir}/rhythmbox/plugins/magnatune/*-plugin
%{_libdir}/rhythmbox/plugins/magnatune/*.glade
%{_libdir}/rhythmbox/plugins/magnatune/*.png
%dir %{_libdir}/rhythmbox/plugins/mmkeys
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/mmkeys/libmmkeys.so
%{_libdir}/rhythmbox/plugins/mmkeys/mmkeys.rb-plugin
%{?with_mtp:%dir %{_libdir}/rhythmbox/plugins/mtpdevice}
%{?with_mtp:%attr(755,root,root) %{_libdir}/rhythmbox/plugins/mtpdevice/libmtpdevice.so}
%{?with_mtp:%{_libdir}/rhythmbox/plugins/mtpdevice/mtpdevice.rb-plugin}
%{?with_mtp:%{_libdir}/rhythmbox/plugins/mtpdevice/mtp-ui.xml}
%dir %{_libdir}/rhythmbox/plugins/power-manager
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/power-manager/*.so
%{_libdir}/rhythmbox/plugins/power-manager/*-plugin
%dir %{_libdir}/rhythmbox/plugins/python-console
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/python-console/*.py[co]
%{_libdir}/rhythmbox/plugins/python-console/*-plugin
%dir %{_libdir}/rhythmbox/plugins/rb
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/rb/*.py[co]
%dir %{_libdir}/rhythmbox/plugins/upnp_coherence
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/upnp_coherence/*.py[co]
%{_libdir}/rhythmbox/plugins/upnp_coherence/coherence.rb-plugin
%dir %{_libdir}/rhythmbox/plugins/visualizer
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/visualizer/libvisualizer.so
%{_libdir}/rhythmbox/plugins/visualizer/rb-visualizer-glue.h
%{_libdir}/rhythmbox/plugins/visualizer/visualizer-controls.glade
%{_libdir}/rhythmbox/plugins/visualizer/visualizer-ui.xml
%{_libdir}/rhythmbox/plugins/visualizer/visualizer.rb-plugin
%dir %{_libdir}/rhythmbox/plugins/dontreallyclose
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/dontreallyclose/dontreallyclose.py[co]
%{_libdir}/rhythmbox/plugins/dontreallyclose/dontreallyclose.rb-plugin
%{_datadir}/%{name}
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/rhythmbox.png
%{_iconsdir}/hicolor/*/*/rhythmbox.svg
%{_sysconfdir}/gconf/schemas/rhythmbox.schemas

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/*.so
