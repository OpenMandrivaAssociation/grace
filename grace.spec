%global debug_package %{nil}
# NOTE: this is needed to avoid broken macro format in 
# T1lib/type1/objects.c
# T1lib/type1/type1.c (presumably others)
# since IfTrace0 macro does not include the format string
# Upstream is warned
# All other formats are fixed in the patched files (sent upstream also)

%define Werror_cflags %nil

Name:		grace
Version:	5.1.24
Release:	2
Summary:	Numerical Data Processing and Visualization Tool (Grace)
License:	GPLv2+
Url:		https://plasma-gate.weizmann.ac.il/Grace/
Source0:	ftp://plasma-gate.weizmann.ac.il/pub/grace/src/grace5/%name-%version.tar.gz
Source1:	grace-icons.tar.bz2
Patch0:		svgdrv_stringliteral.patch
Patch1:		utils_stringliteral.patch
# Fixes the mouse stuck in the window, fix for #58242
# Comes from http://plasma-gate.weizmann.ac.il/Grace/phpbb/viewtopic.php?t=1813
Patch2:		mouse_stuck_in_the_window.patch
Group:		Sciences/Other
BuildRequires:	jpeg-devel
BuildRequires:	netcdf-devel
BuildRequires:	lesstif-devel
BuildRequires:	t1lib-devel
BuildRequires:	Xbae-devel
BuildRequires:	pkgconfig(libtiff-4)
BuildRequires:	pkgconfig(xext)
BuildRequires:	pkgconfig(zlib)
Requires:	webclient
Requires:	xterm

# NOTE: This can be rebuilt with pdflib-devel installed if you want to enable pdf
# support. Keep in mind that pdflib is not free (Aladdin FPL).

%description
Grace is a Motif/Lesstif application for two-dimensional data
visualization. Grace can transform the data using free equations, FFT,
cross- and auto-correlation, differences, integrals, histograms, and
much more. The generated figures are of high quality.  Grace is a very
convenient tool for data inspection, data transformation, and for
making figures for publications.

%package devel
Group:		Development/Other
Summary:	Library and header files for Grace-linked apps development
Requires:	grace = %{version}
License:	LGPL

%description devel
This package includes header and library files needed to
develop programs which will use grace as a subprocess.
This feature is currently (%{name}-%{version}) available for
C and Fortran77 languages.

%prep

%setup -a 1 -q
%patch0 -p 1
%patch1
%patch2 -p 1

%build
%configure \
	--enable-grace-home=%{_libdir}/grace \
	--with-helpviewer="xdg-open %s" \
	--with-editor="xdg-open %s" \
	--with-x \
	--disable-xmhtml \
	--without-bundled-xbae \
	--without-bundled-t1lib \
	--x-includes=%{_libdir} \
	--x-libraries=%{_libdir}

%make

%install
%makeinstall GRACE_HOME=%{buildroot}/%{_libdir}/grace

#fixup binaries
mkdir %{buildroot}/%{_bindir}
mv %{buildroot}/%{_libdir}/grace/bin/* %{buildroot}/%{_bindir}
rm -fr %{buildroot}/%{_libdir}/grace/bin
ln -s %{_bindir}/xmgrace %{buildroot}/%{_bindir}/grace

#fixup devel files
mv %{buildroot}/%{_libdir}/grace/lib/* %{buildroot}/%{_libdir}
rm -fr %{buildroot}/%{_libdir}/grace/lib
mkdir %{buildroot}/%{_includedir}
mv %{buildroot}/%{_libdir}/grace/include/* %{buildroot}/%{_includedir}
rm -fr %{buildroot}/%{_libdir}/grace/include

#fixup documentation
mkdir -p %{buildroot}/%{_mandir}/man1
mv %{buildroot}/%{_libdir}/grace/doc/*.1 %{buildroot}/%{_mandir}/man1
rm -fr %{buildroot}/%{_libdir}/grace/doc
ln -s %{_docdir}/%{name} %{buildroot}/%{_libdir}/grace/doc

install -d %{buildroot}%{_datadir}/applications
cat <<EOF > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=Grace
Comment=Graphical visualization of scientific data
Exec=xmgrace
Icon=grace
Type=Application
Categories=Science;Education;2DGraphics;
EOF

# icons
mkdir -p %{buildroot}%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
pushd grace-icons
cp grace16.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/grace.png
cp grace32.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/grace.png
cp grace48.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/grace.png
popd

%files
%doc CHANGES COPYRIGHT DEVELOPERS LICENSE README ChangeLog doc/*.html doc/*.png
%{_mandir}/man1/*
%{_libdir}/grace
%{_bindir}/grace
%{_bindir}/gracebat
%{_bindir}/xmgrace
%{_bindir}/convcal
%{_bindir}/fdf2fit
%{_bindir}/grconvert
%{_datadir}/applications/*.desktop
%{_iconsdir}/hicolor/16x16/apps/grace.png
%{_iconsdir}/hicolor/32x32/apps/grace.png
%{_iconsdir}/hicolor/48x48/apps/grace.png

%files devel
%{_includedir}/grace_np.h
%{_libdir}/libgrace_np.a
