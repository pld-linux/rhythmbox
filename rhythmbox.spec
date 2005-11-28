Summary:	Music Management Application
Summary(pl):	Aplikacja do zarz±dzania muzyk±
Name:		rhythmbox
Version:	0.9.2
Release:	1
License:	GPL v2+
Group:		Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/rhythmbox/0.9/%{name}-%{version}.tar.bz2
# Source0-md5:	533223578c9c37bd72634755b33beab7
Patch0:		%{name}-desktop.patch
Patch1:		%{name}-broken_locale.patch
Patch2:		%{name}-gtk2.8-crash.patch
URL:		http://www.rhythmbox.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	dbus-glib-devel >= 0.35
BuildRequires:	gstreamer-GConf-devel >= 0.8.8
BuildRequires:	gstreamer-devel >= 0.8.9
BuildRequires:	gstreamer-plugins-devel >= 0.8.8
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	gtk+2-devel >= 2:2.8.0
BuildRequires:	hal-devel >= 0.5.4
BuildRequires:	howl-devel
BuildRequires:	intltool
BuildRequires:	libbonobo-devel >= 2.8.0
BuildRequires:	libglade2-devel >= 1:2.5.1
BuildRequires:	libgnomeui-devel >= 2.10.0-2
BuildRequires:	libgpod-devel
BuildRequires:	libmusicbrainz-devel >= 2.0.1
BuildRequires:	libtool
BuildRequires:	nautilus-cd-burner-devel >= 2.9.0
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.176
BuildRequires:	scrollkeeper
BuildRequires:	totem-devel >= 1.1.3
BuildRequires:	zlib-devel
Requires(post,preun):	GConf2
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	scrollkeeper
Requires:	dbus >= 0.35
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
%patch2 -p1

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
	--with-bonobo \
	--with-cd-burner \
	--with-dbus \
	--with-ipod \
	--with-mds=howl
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
%{_datadir}/idl/*
%{_datadir}/%{name}
%{_datadir}/dbus-1/services/*.service
%{_desktopdir}/*
%{_libdir}/bonobo/servers/*
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/*
%{_pkgconfigdir}/*
%{_sysconfdir}/gconf/schemas/rhythmbox.schemas
