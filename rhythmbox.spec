#
# Conditional build:
%bcond_without	apidocs		# gi-doc based API documentation
%bcond_without	ipod		# iPod support
%bcond_without	mtp		# MTP support
%bcond_without	daap		# DAAP support

Summary:	Music Management Application
Summary(hu.UTF-8):	Zenelejátszó alkalmazás
Summary(pl.UTF-8):	Aplikacja do zarządzania muzyką
Name:		rhythmbox
Version:	3.4.8
Release:	4
License:	GPL v2+
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/rhythmbox/3.4/%{name}-%{version}.tar.xz
# Source0-md5:	6a272ee2da9b5fd57bb12d9559bb2ee9
URL:		https://wiki.gnome.org/Apps/Rhythmbox
BuildRequires:	brasero-devel >= 2.31.5
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gdk-pixbuf2-devel >= 2.18.0
BuildRequires:	gettext-tools >= 0.18
%{?with_apidocs:BuildRequires:	gi-docgen}
BuildRequires:	glib2-devel >= 1:2.66.0
BuildRequires:	gobject-introspection-devel >= 0.10.0
BuildRequires:	grilo-devel >= 0.3.16-2
BuildRequires:	gstreamer-devel >= 1.4.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.4.0
BuildRequires:	gtk+3-devel >= 3.20.0
BuildRequires:	json-glib-devel
%if %{with daap}
BuildRequires:	libdmapsharing-devel >= 3.9.11
BuildRequires:	libdmapsharing-devel < 4.9
%endif
%{?with_ipod:BuildRequires:	libgpod-devel >= 0.8}
%{?with_mtp:BuildRequires:	libmtp-devel >= 0.3.0}
BuildRequires:	libnotify-devel >= 0.7.0
BuildRequires:	libpeas-devel >= 0.7.3
BuildRequires:	libpeas-gtk-devel >= 0.7.3
BuildRequires:	libsecret-devel >= 0.18
BuildRequires:	libsoup3-devel >= 3.0.7
BuildRequires:	libxml2-devel >= 1:2.7.8
BuildRequires:	lirc-devel
BuildRequires:	meson >= 0.64.0
BuildRequires:	ninja >= 1.5
BuildRequires:	pango-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel >= 1:3.2.3
BuildRequires:	python3-pygobject3-devel >= 3.0
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(find_lang) >= 1.23
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	tdb-devel >= 2:1.2.6
BuildRequires:	totem-pl-parser-devel >= 3.2.0
BuildRequires:	udev-glib-devel >= 1:143
BuildRequires:	vala >= 0.9.4
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xz
BuildRequires:	yelp-tools
BuildRequires:	zlib-devel
Requires:	python3-modules
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires(post,postun):	glib2 >= 1:2.66.0
Requires:	brasero >= 2.31.5
Requires:	dbus >= 0.93
Requires:	glib2 >= 1:2.66.0
Requires:	grilo >= 0.3.16-2
Requires:	gstreamer-audio-effects-base >= 1.4.0
Requires:	gstreamer-audio-formats >= 1.4.0
Requires:	gstreamer-audiosink
Requires:	gstreamer-plugins-good >= 1.4.0
Requires:	gtk+3 >= 3.20.0
%{?with_daap:Requires:	libdmapsharing >= 3.9.11}
%{?with_ipod:Requires:	libgpod >= 0.8}
%{?with_mtp:Requires:	libmtp >= 0.3.0}
Requires:	libnotify >= 0.7.0
Requires:	libpeas >= 0.7.3
Requires:	libpeas-gtk >= 0.7.3
Requires:	libsecret >= 0.18
Requires:	libsoup3 >= 3.0.7
Requires:	libxml2 >= 1:2.7.8
Requires:	tdb >= 2:1.2.6
Requires:	totem-pl-parser >= 3.2.0
Requires:	udev-glib >= 1:143
Suggests:	gstreamer-flac >= 1.4.0
Suggests:	gstreamer-mad >= 1.4.0
Suggests:	gstreamer-neon >= 1.4.0
Suggests:	gstreamer-vorbis >= 1.4.0
Suggests:	libpeas-gtk >= 0.7.3
Suggests:	libpeas-loader-python3
Suggests:	python3-Mako
Suggests:	python3-zeitgeist
Obsoletes:	browser-plugin-rhythmbox < 3.4.4
Obsoletes:	net-rhythmbox < 0.5
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

%package devel
Summary:	Header files for developing Rhythmbox plugins
Summary(pl.UTF-8):	Pliki nagłówkowe do tworzenia wtyczek Rhythmboksa
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	glib2-devel >= 1:2.66.0
Requires:	gstreamer-devel >= 1.4.0
Requires:	gtk+3-devel >= 3.20.0
Requires:	libsoup3-devel >= 3.0.7
Requires:	libxml2-devel >= 1:2.7.8
Requires:	totem-pl-parser-devel >= 3.2.0

%description devel
Header files for developing Rhythmbox plugins.

%description devel -l pl.UTF-8
Pliki nagłówkowe do tworzenia wtyczek Rhythmboksa.

%package -n vala-rhythmbox
Summary:	Vala API for Rhythmbox
Summary(pl.UTF-8):	API języka Vala dla Rhythmboksa
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description -n vala-rhythmbox
Vala API for Rhythmbox.

%description -n vala-rhythmbox -l pl.UTF-8
API języka Vala dla Rhythmboksa.

%package apidocs
Summary:	Documentation for Rhythmbox plugin API
Summary(pl.UTF-8):	Dokumentacja API wtyczek Rhythmboksa
Group:		Documentation
BuildArch:	noarch

%description apidocs
Documentation for Rhythmbox plugin API.

%description apidocs -l pl.UTF-8
Dokumentacja API wtyczek Rhythmboksa.

%prep
%setup -q

%build
%meson \
	%{?with_daap:-Ddaap=enabled} \
	%{?with_apidocs:-Dapidoc=true} \
	%{!?with_ipod:-Dipod=disabled}

%meson_build

%install
rm -rf $RPM_BUILD_ROOT

%meson_install

%py3_comp $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins
%py3_ocomp $RPM_BUILD_ROOT%{_libdir}/rhythmbox/plugins

%if %{with apidocs}
# not installed by ninja install
install -d $RPM_BUILD_ROOT%{_gidocdir}
cp -pr build/doc/apidoc $RPM_BUILD_ROOT%{_gidocdir}/rhythmbox
%endif

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{name} --with-gnome

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

%files -f rhythmbox.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README.md NEWS
%attr(755,root,root) %{_bindir}/rhythmbox
%attr(755,root,root) %{_bindir}/rhythmbox-client
%attr(755,root,root) %{_libexecdir}/rhythmbox-metadata

%attr(755,root,root) %{_libdir}/librhythmbox-core.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/librhythmbox-core.so.10
%{_libdir}/girepository-1.0/MPID-3.0.typelib
%{_libdir}/girepository-1.0/RB-3.0.typelib

%dir %{_libdir}/rhythmbox
%dir %{_libdir}/rhythmbox/plugins
%dir %{_datadir}/rhythmbox
%{_datadir}/rhythmbox/rhythmbox.gep
%dir %{_datadir}/rhythmbox/plugins
%{_datadir}/dbus-1/services/org.gnome.Rhythmbox3.service
%{_datadir}/glib-2.0/schemas/org.gnome.rhythmbox.gschema.xml
%{_datadir}/metainfo/org.gnome.Rhythmbox3.appdata.xml
%{_desktopdir}/org.gnome.Rhythmbox3.desktop
%{_desktopdir}/org.gnome.Rhythmbox3.device.desktop
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Rhythmbox3.svg
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Rhythmbox3-symbolic.svg
%{_mandir}/man1/rhythmbox.1*
%{_mandir}/man1/rhythmbox-client.1*

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
%{_datadir}/rhythmbox/plugins/audioscrobbler

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

%dir %{_libdir}/rhythmbox/plugins/listenbrainz
%{_libdir}/rhythmbox/plugins/listenbrainz/listenbrainz.plugin
%{_libdir}/rhythmbox/plugins/listenbrainz/*.py
%{_libdir}/rhythmbox/plugins/listenbrainz/__pycache__
%{_datadir}/rhythmbox/plugins/listenbrainz

%dir %{_libdir}/rhythmbox/plugins/lyrics
%{_libdir}/rhythmbox/plugins/lyrics/lyrics.plugin
%{_libdir}/rhythmbox/plugins/lyrics/*.py
%{_libdir}/rhythmbox/plugins/lyrics/__pycache__
%{_datadir}/rhythmbox/plugins/lyrics

%dir %{_libdir}/rhythmbox/plugins/magnatune
%{_libdir}/rhythmbox/plugins/magnatune/magnatune.plugin
%{_libdir}/rhythmbox/plugins/magnatune/*.py
%{_libdir}/rhythmbox/plugins/magnatune/__pycache__
%{_datadir}/rhythmbox/plugins/magnatune

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
%{_datadir}/rhythmbox/plugins/rblirc

%dir %{_libdir}/rhythmbox/plugins/rbzeitgeist
%{_libdir}/rhythmbox/plugins/rbzeitgeist/rbzeitgeist.plugin
%{_libdir}/rhythmbox/plugins/rbzeitgeist/*.py
%{_libdir}/rhythmbox/plugins/rbzeitgeist/__pycache__

%dir %{_libdir}/rhythmbox/plugins/replaygain
%{_libdir}/rhythmbox/plugins/replaygain/replaygain.plugin
%{_libdir}/rhythmbox/plugins/replaygain/*.py
%{_libdir}/rhythmbox/plugins/replaygain/__pycache__
%{_datadir}/rhythmbox/plugins/replaygain

%dir %{_libdir}/rhythmbox/plugins/webremote
%{_libdir}/rhythmbox/plugins/webremote/webremote.plugin
%{_libdir}/rhythmbox/plugins/webremote/*.py
%{_libdir}/rhythmbox/plugins/webremote/__pycache__
%{_datadir}/rhythmbox/plugins/webremote

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/librhythmbox-core.so
%{_datadir}/gir-1.0/MPID-3.0.gir
%{_datadir}/gir-1.0/RB-3.0.gir
%{_includedir}/rhythmbox
%{_pkgconfigdir}/rhythmbox.pc

%files -n vala-rhythmbox
%defattr(644,root,root,755)
%{_datadir}/vala/vapi/rb.vapi
%{_datadir}/vala/vapi/rhythmdb.vapi

%files apidocs
%defattr(644,root,root,755)
%{_gidocdir}/rhythmbox
