#
# Conditional build:
%bcond_with	xine	# build with xine-lib instead of gstreamer
#
%define 	min_ver 0.8.1

Summary:	Music Management Application
Summary(pl):	Aplikacja do zarz±dzania muzyk±
Name:		rhythmbox
Version:	0.8.5
Release:	2
License:	GPL
Group:		Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.8/%{name}-%{version}.tar.bz2
# Source0-md5:	50d2ebb835f89e01c6fb0531d65c1341
Patch0:		%{name}-locale-names.patch
Patch1:		%{name}-vorbis.patch
Patch2:		%{name}-desktop.patch
URL:		http://www.rhythmbox.org/
BuildRequires:	autoconf
BuildRequires:	automake
%if %{without xine}
BuildRequires:	gstreamer-GConf-devel >= %{min_ver}
BuildRequires:	gstreamer-devel >= %{min_ver}
BuildRequires:	gstreamer-plugins-devel >= %{min_ver}
%else
BuildRequires:	flac-devel
BuildRequires:	libid3tag-devel >= 0.15.0b
BuildRequires:	libmad-devel
BuildRequires:	libogg-devel
BuildRequires:	libvorbis-devel
BuildRequires:	xine-lib-devel >= 1.0.0
%endif
BuildRequires:	gnome-vfs2-devel >= 2.4.0
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	libbonobo-devel >= 2.4.0
BuildRequires:	libglade2-devel >= 2.0.1
BuildRequires:	libgnomeui-devel >= 2.4.0
BuildRequires:	libmusicbrainz-devel >= 2.0.1
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	zlib-devel
Requires(post,postun):	/sbin/ldconfig
Requires(post,postun):	/usr/bin/scrollkeeper-update
Requires(post):	GConf2
%if %{without xine}
Requires:	gstreamer-audio-effects >= %{min_ver}
Requires:	gstreamer-audio-formats >= %{min_ver}
Requires:	gstreamer-audiosink
Requires:	gstreamer-gnomevfs >= %{min_ver}
%endif
Requires:	gtk+2 >= 2:2.4.0
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

mv po/{no,nb}.po

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--disable-schemas-install \
	--enable-ipod \
	%{?_with_xine:--with-player=xine}
	
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
echo
echo "Remember to install appropriate gstreamer plugins for files"
echo "you want to play:"
echo "- gstreamer-flac (for FLAC)"
echo "- gstreamer-mad (for mp3s)"
echo "- gstreamer-vorbis (for Ogg Vorbis)"
echo
%else
echo
echo "Remember to install appropriate xine-decode plugins for files"
echo "you want to play:"
echo "- xine-decode-flac (for FLAC)"
echo "- xine-decode-ogg (for Ogg Vorbis)"
echo
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
%attr(755,root,root) %{_libdir}/bonobo/*.so
%{_omf_dest_dir}/%{name}
%{_pixmapsdir}/*
%{_pkgconfigdir}/*
%{_sysconfdir}/gconf/schemas/*
