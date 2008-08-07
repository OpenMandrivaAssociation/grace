Name: grace
Version: 5.1.22
Release: %mkrel 2
Summary: Numerical Data Processing and Visualization Tool (Grace)
License: GPLv2+
Url: http://plasma-gate.weizmann.ac.il/Grace/
Source0: ftp://plasma-gate.weizmann.ac.il/pub/grace/src/grace5/%name-%version.tar.gz
Source1: grace-icons.tar.bz2
Group: Sciences/Other
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: zlib-devel libjpeg-devel libtiff-devel lesstif-devel 
BuildRequires: netcdf-devel libpng-devel t1lib-devel
Requires: xterm webclient

# NOTE: This can be rebuilt with pdflib-devel installed if you want to enable pdf
# support. Keep in mind that pdflib is not free (Aladdin FPL).

%description
Grace is a Motif/Lesstif application for two-dimensional data
visualization. Grace can transform the data using free equations, FFT,
cross- and auto-correlation, differences, integrals, histograms, and
much more. The generated figures are of high quality.  Grace is a very
convenient tool for data inspection, data transformation, and for
making figures for publications.

NOTE: The help browser requires netscape or any browser linked to that
executable name.  Otherwise, help files are in /usr/share/doc, as usual.

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

%build
%configure2_5x --enable-grace-home=%_libdir/grace 
%make

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall GRACE_HOME=$RPM_BUILD_ROOT/%_libdir/grace

#fixup binaries
mkdir $RPM_BUILD_ROOT/%_bindir
mv $RPM_BUILD_ROOT/%_libdir/grace/bin/* $RPM_BUILD_ROOT/%_bindir
rm -fr $RPM_BUILD_ROOT/%_libdir/grace/bin
ln -s %_bindir/xmgrace $RPM_BUILD_ROOT/%_bindir/grace

#fixup devel files
mv $RPM_BUILD_ROOT/%_libdir/grace/lib/* $RPM_BUILD_ROOT/%_libdir
rm -fr $RPM_BUILD_ROOT/%_libdir/grace/lib
mkdir $RPM_BUILD_ROOT/%_includedir
mv $RPM_BUILD_ROOT/%_libdir/grace/include/* $RPM_BUILD_ROOT/%_includedir
rm -fr $RPM_BUILD_ROOT/%_libdir/grace/include

#fixup documentation
mkdir -p $RPM_BUILD_ROOT/%_mandir/man1
mv $RPM_BUILD_ROOT/%_libdir/grace/doc/*.1 $RPM_BUILD_ROOT/%_mandir/man1
rm -fr $RPM_BUILD_ROOT/%_libdir/grace/doc
ln -s %_docdir/%name $RPM_BUILD_ROOT/%_libdir/grace/doc

install -d $RPM_BUILD_ROOT%{_datadir}/applications
cat <<EOF > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop
[Desktop Entry]
Name=Grace
Comment=Graphical visualization of scientific data
Exec=xmgrace
Icon=grace
Type=Application
Categories=Science;Education;2DGraphics;
EOF

# icons
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}/hicolor/{16x16,32x32,48x48}/apps
pushd grace-icons
cp grace16.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/16x16/apps/grace.png
cp grace32.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/32x32/apps/grace.png
cp grace48.png $RPM_BUILD_ROOT%{_iconsdir}/hicolor/48x48/apps/grace.png
popd

%clean
rm -rf $RPM_BUILD_ROOT

%if %mdkversion < 200900
%post
%{update_menus}
%{update_icon_cache hicolor}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%{clean_icon_cache hicolor}
%endif

%files
%defattr (-,root,root)
%doc CHANGES COPYRIGHT DEVELOPERS LICENSE README ChangeLog doc/*.html doc/*.png
%_mandir/man1/*
%_libdir/grace
%_bindir/grace
%_bindir/gracebat
%_bindir/xmgrace
%_bindir/convcal
%_bindir/fdf2fit
%_bindir/grconvert
%_datadir/applications/*.desktop
%{_iconsdir}/hicolor/16x16/apps/grace.png
%{_iconsdir}/hicolor/32x32/apps/grace.png
%{_iconsdir}/hicolor/48x48/apps/grace.png

%files devel
%defattr (-,root,root)
%_includedir/grace_np.h
%_libdir/libgrace_np.a
