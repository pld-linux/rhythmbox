
%bcond_with xine		# build with xine-lib instead of gstreamer

%define 	min_ver 0.6.3

Summary:	Music Management Application
Summary(pl):	Aplikacja do zarządzania muzyką
Name:		rhythmbox
Version:	0.6.1
Release:	1
License:	GPL
Group:		Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.6/%{name}-%{version}.tar.bz2
# Source0-md5:	5791f9fb69c9a855d84e1e666b2e86a9
BuildRequires:	flac-devel
BuildRequires:	gnome-vfs2-devel >= 2.4.0
%if %{without xine}
BuildRequires:	gstreamer-GConf-devel >= %{min_ver}
BuildRequires:	gstreamer-devel >= %{min_ver}
BuildRequires:	gstreamer-plugins-devel >= %{min_ver}
%else
BuildRequires:	xine-lib-devel
%endif
BuildRequires:	gtk+2-devel >= 2.2.2
BuildRequires:	libbonobo-devel >= 2.4.0
BuildRequires:	libglade2-devel >= 2.0.1
BuildRequires:	libgnomecanvas-devel >= 2.4.0
BuildRequires:	libgnomeui-devel >= 2.4.0
BuildRequires:	libid3tag-devel
BuildRequires:	libmad-devel
BuildRequires:	libmusicbrainz-devel >= 2.0.1
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	/usr/bin/scrollkeeper-update
Requires(post):	GConf2
Requires:	gtk+2 >= 2.2.2
%if %{without xine}
Requires:	gstreamer-audio-effects >= %{min_ver}
Requires:	gstreamer-audio-formats >= %{min_ver}
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= %{min_ver}
%endif
Obsoletes:	net-rhythmbox
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Rhythmbox is your one-stop multimedia application, supporting a music
library, multiple "music groups", internet radio, and more.

%description -l pl
Rhythmbox to kompletna aplikacja multimedialna, obsługująca bibliotekę
muzyczną, wiele "grup muzyki", radio internetowe itp.

%prep
%setup -q

%build
%configure \
	--disable-schemas-install \
	%{?_with_xine:--enable-xine}
	
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1

%find_lang %{name} --with-gnome --all-name

rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/lib*.{la,a}

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%gconf_schema_install
/usr/bin/scrollkeeper-update
%if %{without xine}
echo "Remember to install appropriate gstreamer plugins for files"
echo "you want to play:"
echo "- gstreamer-mad (for mp3s)"
echo "- gstreamer-vorbis (for Ogg Vorbis)"
echo "- gstreamer-flac (for FLAC)"
%endif

%postun 
/sbin/ldconfig
/usr/bin/scrollkeeper-update

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
%{_libdir}/bonobo/*.so
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/*
%{_pkgconfigdir}/*
%{_sysconfdir}/gconf/schemas/*
