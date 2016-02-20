#
# Conditional build:
%bcond_without	ipod		# build without iPod support
%bcond_without	mtp		# build without MTP support
%bcond_without	daap		# build without DAAP support
%bcond_without	vis		# build with Visualization support
%bcond_with	webkit		# build with gtk-webkit support

Summary:	Music Management Application
Summary(hu.UTF-8):	Zenelejátszó alkalmazás
Summary(pl.UTF-8):	Aplikacja do zarządzania muzyką
Name:		rhythmbox
Version:	3.3
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/rhythmbox/3.3/%{name}-%{version}.tar.xz
# Source0-md5:	afffb1566172e0449095f2aaad26b693
URL:		http://projects.gnome.org/rhythmbox/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	brasero-devel >= 2.31.5
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gdk-pixbuf2-devel >= 2.18.0
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel >= 1:2.34.0
BuildRequires:	gnome-common
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	grilo-devel >= 0.1.17
BuildRequires:	gstreamer-devel >= 1.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0.0
BuildRequires:	gtk+3-devel >= 3.12.0
BuildRequires:	gtk-doc
%{?with_webkit:BuildRequires:	gtk-webkit3-devel >= 1.3.9}
BuildRequires:	intltool >= 0.35.0
BuildRequires:	json-glib-devel
%{?with_daap:BuildRequires:	libdmapsharing-devel >= 2.9.19}
%{?with_ipod:BuildRequires:	libgpod-devel >= 0.6}
%{?with_mtp:BuildRequires:	libmtp-devel >= 0.3.0}
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libpeas-devel >= 0.7.3
BuildRequires:	libpeas-gtk-devel >= 0.7.3
BuildRequires:	libsecret-devel >= 0.18
BuildRequires:	libsoup-devel >= 2.34.0
BuildRequires:	libsoup-gnome-devel >= 2.34.0
BuildRequires:	libtool
BuildRequires:	libxml2-devel >= 1:2.7.8
BuildRequires:	lirc-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-pygobject3-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sed >= 4.0
BuildRequires:	tdb-devel >= 2:1.2.6
BuildRequires:	totem-pl-parser-devel >= 3.2.0
BuildRequires:	udev-glib-devel >= 143
BuildRequires:	vala >= 0.9.4
BuildRequires:	xorg-lib-libSM-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
%if %{with vis}
BuildRequires:	clutter-devel >= 1.8
BuildRequires:	clutter-gst2-devel >= 1.0
BuildRequires:	clutter-gtk-devel >= 1.0
BuildRequires:	mx-devel >= 1.0.1
%endif
Requires:	python3-modules
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	glib2 >= 1:2.34.0
Requires:	dbus >= 0.93
Requires:	glib2 >= 1:2.34.0
Requires:	gstreamer-audio-effects-base >= 1.0.0
Requires:	gstreamer-audio-formats >= 1.0.0
Requires:	gstreamer-audiosink
Requires:	gstreamer-plugins-good >= 1.0.0
Requires:	gtk+3 >= 3.12.0
Suggests:	gstreamer-flac
Suggests:	gstreamer-mad
Suggests:	gstreamer-neon
Suggests:	gstreamer-vorbis
Suggests:	gtk-webkit3
Suggests:	libpeas-gtk >= 0.7.3
Suggests:	libpeas-loader-python3
Suggests:	python3-Mako
Suggests:	python3-zeitgeist
Obsoletes:	net-rhythmbox
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rhythmbox is your one-stop multimedia application, supporting a music
library, multiple "music groups", internet radio, and more.

%description -l hu.UTF-8
Rhythmbox egy multimédia alkalmazás, amley támogatja a
zenekönyvtárakat, több "zenecsoportokat", internetes rádiót, és még
sok mindent.

%description -l pl.UTF-8
Rhythmbox to kompletna aplikacja multimedialna, obsługująca bibliotekę
muzyczną, wiele "grup muzyki", radio internetowe itp.

%package -n browser-plugin-%{name}
Summary:	Rhythmbox's browser plugin
Summary(hu.UTF-8):	Rhythmbox böngésző plugin
Summary(pl.UTF-8):	Wtyczka Rhythmboksa do przeglądarek WWW
Group:		X11/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	browser-plugins >= 2.0
Requires:	browser-plugins(%{_target_base_arch})

%description -n browser-plugin-%{name}
iTunes detection browser plugin (for podcasts).

%description -n browser-plugin-%{name} -l hu.UTF-8
Rhythmbox böngésző plugin.

%description -n browser-plugin-%{name} -l pl.UTF-8
Wtyczka Rhythmboksa do przeglądarek WWW.

%prep
%setup -q

%build
%{__gtkdocize}
%{__glib_gettextize}
%{__intltoolize}
%{__libtoolize}
%{__aclocal} -I macros
%{__autoheader}
%{__automake}
%{__autoconf}
MOZILLA_PLUGINDIR=%{_browserpluginsdir} \
%configure \
	--disable-static \
	--disable-silent-rules \
	--enable-browser-plugin \
	--enable-lirc \
	--enable-python \
	--enable-vala \
	%{!?with_ipod:--without-ipod} \
	%{?with_daap:--enable-daap} \
	--with-gudev \
	--with-mtp \
	--with%{!?with_webkit:out}-webkit \
	--with-x \
	--without-hal

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name} --with-gnome

%{__rm} $RPM_BUILD_ROOT%{_libdir}/browser-plugins/*.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/librhythmbox-core.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins/*/*.la

# there is no -devel subpackage
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/gir-1.0
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/rhythmbox
%{__rm} -r $RPM_BUILD_ROOT%{_libdir}/rhythmbox/sample-plugins
%{__rm} $RPM_BUILD_ROOT%{_libdir}/librhythmbox-core.so
%{__rm} $RPM_BUILD_ROOT%{_pkgconfigdir}/rhythmbox.pc

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%glib_compile_schemas
%update_desktop_database_post
%update_icon_cache hicolor

%postun
/sbin/ldconfig
%glib_compile_schemas
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
%attr(755,root,root) %ghost %{_libdir}/librhythmbox-core.so.9
%{_datadir}/%{name}
%{_datadir}/appdata/rhythmbox.appdata.xml
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/*/*/rhythmbox.png
%{_iconsdir}/hicolor/*/*/rhythmbox-missing-artwork.png
%{_iconsdir}/hicolor/scalable/apps/rhythmbox-symbolic.svg
%{_mandir}/man1/rhythmbox.1*
%{_mandir}/man1/rhythmbox-client.1*

%{_libdir}/girepository-1.0/MPID-3.0.typelib
%{_libdir}/girepository-1.0/RB-3.0.typelib
%{_datadir}/glib-2.0/schemas/org.gnome.rhythmbox.gschema.xml

%dir %{_libdir}/rhythmbox
%dir %{_libdir}/rhythmbox/plugins

%dir %{_libdir}/rhythmbox/plugins/artsearch
%{_libdir}/rhythmbox/plugins/artsearch/artsearch.plugin
%{_libdir}/rhythmbox/plugins/artsearch/*.py
%{_libdir}/rhythmbox/plugins/artsearch/__pycache__

%dir %{_libdir}/rhythmbox/plugins/android
%{_libdir}/rhythmbox/plugins/android/android.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/android/libandroid.so

%dir %{_libdir}/rhythmbox/plugins/audiocd
%{_libdir}/rhythmbox/plugins/audiocd/audiocd.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/audiocd/*.so

%dir %{_libdir}/rhythmbox/plugins/audioscrobbler
%{_libdir}/rhythmbox/plugins/audioscrobbler/audioscrobbler.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/audioscrobbler/*.so

%dir %{_libdir}/rhythmbox/plugins/cd-recorder
%{_libdir}/rhythmbox/plugins/cd-recorder/cd-recorder.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/cd-recorder/*.so

%if %{with daap}
%dir %{_libdir}/rhythmbox/plugins/daap
%{_libdir}/rhythmbox/plugins/daap/daap.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/daap/*.so
%endif

%dir %{_libdir}/rhythmbox/plugins/dbus-media-server
%{_libdir}/rhythmbox/plugins/dbus-media-server/dbus-media-server.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/dbus-media-server/libdbus-media-server.so

%dir %{_libdir}/rhythmbox/plugins/fmradio
%{_libdir}/rhythmbox/plugins/fmradio/fmradio.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/fmradio/*.so

%dir %{_libdir}/rhythmbox/plugins/generic-player
%{_libdir}/rhythmbox/plugins/generic-player/generic-player.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/generic-player/*.so

%dir %{_libdir}/rhythmbox/plugins/grilo
%{_libdir}/rhythmbox/plugins/grilo/grilo.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/grilo/libgrilo.so

%dir %{_libdir}/rhythmbox/plugins/im-status
%{_libdir}/rhythmbox/plugins/im-status/im-status.plugin
%{_libdir}/rhythmbox/plugins/im-status/*.py
%{_libdir}/rhythmbox/plugins/im-status/__pycache__

%if %{with ipod}
%dir %{_libdir}/rhythmbox/plugins/ipod
%{_libdir}/rhythmbox/plugins/ipod/ipod.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/ipod/*.so
%endif

%dir %{_libdir}/rhythmbox/plugins/iradio
%{_libdir}/rhythmbox/plugins/iradio/iradio.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/iradio/*.so

%dir %{_libdir}/rhythmbox/plugins/lyrics
%{_libdir}/rhythmbox/plugins/lyrics/lyrics.plugin
%{_libdir}/rhythmbox/plugins/lyrics/*.py
%{_libdir}/rhythmbox/plugins/lyrics/__pycache__

%dir %{_libdir}/rhythmbox/plugins/magnatune
%{_libdir}/rhythmbox/plugins/magnatune/magnatune.plugin
%{_libdir}/rhythmbox/plugins/magnatune/*.py
%{_libdir}/rhythmbox/plugins/magnatune/__pycache__

%dir %{_libdir}/rhythmbox/plugins/mmkeys
%{_libdir}/rhythmbox/plugins/mmkeys/mmkeys.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/mmkeys/libmmkeys.so

%dir %{_libdir}/rhythmbox/plugins/mpris
%{_libdir}/rhythmbox/plugins/mpris/mpris.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/mpris/libmpris.so

%if %{with mtp}
%dir %{_libdir}/rhythmbox/plugins/mtpdevice
%{_libdir}/rhythmbox/plugins/mtpdevice/mtpdevice.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/mtpdevice/libmtpdevice.so
%endif

%dir %{_libdir}/rhythmbox/plugins/notification
%{_libdir}/rhythmbox/plugins/notification/notification.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/notification/libnotification.so

%dir %{_libdir}/rhythmbox/plugins/power-manager
%{_libdir}/rhythmbox/plugins/power-manager/power-manager.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/power-manager/*.so

%dir %{_libdir}/rhythmbox/plugins/python-console
%{_libdir}/rhythmbox/plugins/python-console/pythonconsole.plugin
%{_libdir}/rhythmbox/plugins/python-console/*.py
%{_libdir}/rhythmbox/plugins/python-console/__pycache__

%dir %{_libdir}/rhythmbox/plugins/rb
%{_libdir}/rhythmbox/plugins/rb/rb.plugin
%{_libdir}/rhythmbox/plugins/rb/*.py
%{_libdir}/rhythmbox/plugins/rb/__pycache__

%dir %{_libdir}/rhythmbox/plugins/rblirc
%{_libdir}/rhythmbox/plugins/rblirc/rblirc.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/rblirc/*.so

%dir %{_libdir}/rhythmbox/plugins/rbzeitgeist
%{_libdir}/rhythmbox/plugins/rbzeitgeist/rbzeitgeist.plugin
%{_libdir}/rhythmbox/plugins/rbzeitgeist/*.py
%{_libdir}/rhythmbox/plugins/rbzeitgeist/__pycache__

%dir %{_libdir}/rhythmbox/plugins/replaygain
%{_libdir}/rhythmbox/plugins/replaygain/replaygain.plugin
%{_libdir}/rhythmbox/plugins/replaygain/*.py
%{_libdir}/rhythmbox/plugins/replaygain/__pycache__

%dir %{_libdir}/rhythmbox/plugins/sendto
%{_libdir}/rhythmbox/plugins/sendto/sendto.plugin
%{_libdir}/rhythmbox/plugins/sendto/*.py
%{_libdir}/rhythmbox/plugins/sendto/__pycache__

%dir %{_libdir}/rhythmbox/plugins/soundcloud
%{_libdir}/rhythmbox/plugins/soundcloud/soundcloud.plugin
%{_libdir}/rhythmbox/plugins/soundcloud/soundcloud.py
%{_libdir}/rhythmbox/plugins/soundcloud/__pycache__

%if %{with vis}
%dir %{_libdir}/rhythmbox/plugins/visualizer
%{_libdir}/rhythmbox/plugins/visualizer/visualizer.plugin
%attr(755,root,root) %{_libdir}/rhythmbox/plugins/visualizer/libvisualizer.so
%endif

%files -n browser-plugin-%{name}
%defattr(644,root,root,755)
%attr(755,root,root) %{_browserpluginsdir}/librhythmbox-itms-detection-plugin.so
