#
# Conditional build:
%bcond_with	xine	# build with xine-lib instead of gstreamer
#
Summary:	Music Management Application
Summary(pl):	Aplikacja do zarz±dzania muzyk±
Name:		rhythmbox
Version:	0.8.8
Release:	3
License:	GPL v2+
Group:		Applications
Source0:	http://ftp.gnome.org/pub/gnome/sources/rhythmbox/0.8/%{name}-%{version}.tar.bz2
# Source0-md5:	46cd84b3b67f85009aa48e0e301124fe
Patch0:		%{name}-vorbis.patch
Patch1:		%{name}-desktop.patch
URL:		http://www.rhythmbox.org/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{without xine}
BuildRequires:	gstreamer-GConf-devel >= 0.8.8
BuildRequires:	gstreamer-devel >= 0.8.9
BuildRequires:	gstreamer-plugins-devel >= 0.8.8
%else
BuildRequires:	flac-devel
BuildRequires:	libid3tag-devel >= 0.15.0b
BuildRequires:	libmad-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	xine-lib-devel >= 1.0.0
%endif
BuildRequires:	gnome-vfs2-devel >= 2.10.0-2
BuildRequires:	gtk+2-devel >= 2:2.6.3
BuildRequires:	libbonobo-devel >= 2.8.0
BuildRequires:	libglade2-devel >= 1:2.5.0
BuildRequires:	libgnomeui-devel >= 2.10.0-2
BuildRequires:	libmusicbrainz-devel >= 2.0.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.176
BuildRequires:	zlib-devel
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	/usr/bin/scrollkeeper-update
Requires(post):	GConf2
%if %{without xine}
Requires:	gstreamer-audio-effects >= 0.8.8
Requires:	gstreamer-audio-formats >= 0.8.8
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= 0.8.8
%else
Requires:	xine-plugin-audio
%endif
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

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	--enable-ipod \
	--enable-nautilus-menu \
	%{?_with_xine:--with-player=xine}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

rm -r $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name} --with-gnome --all-name

rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/lib*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install
/usr/bin/scrollkeeper-update
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1 ||:
%if %{without xine}
%banner %{name} -e << EOF
Remember to install appropriate GStreamer plugins for files
you want to play:
- gstreamer-flac (for FLAC)
- gstreamer-mad (for MP3s)
- gstreamer-vorbis (for Ogg Vorbis)
EOF
%else
%banner %{name} -e << EOF
Remember to install appropriate xine-decode plugins for files
you want to play:
- xine-decode-flac (for FLAC)
- xine-decode-ogg (for Ogg Vorbis)
EOF
%endif

%postun 
/sbin/ldconfig
/usr/bin/scrollkeeper-update
[ ! -x /usr/bin/update-desktop-database ] || /usr/bin/update-desktop-database >/dev/null 2>&1

%files -f rhythmbox.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog README NEWS
%attr(755,root,root) %{_bindir}/*
%{_datadir}/application-registry/*
%{_datadir}/gnome-2.0/ui/*.xml
%{_datadir}/idl/*
%{_datadir}/mime-info/*.keys
%{_datadir}/%{name}
%{_desktopdir}/*
%{_libdir}/bonobo/servers/*
%attr(755,root,root) %{_libdir}/bonobo/*.so
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/*
%{_pkgconfigdir}/*
%{_sysconfdir}/gconf/schemas/*
