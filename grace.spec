Name: grace
Version: 5.1.21
Release: %mkrel 2
Summary: Numerical Data Processing and Visualization Tool (Grace)
License: GPL
Url: http://plasma-gate.weizmann.ac.il/Grace/
Source0: ftp://plasma-gate.weizmann.ac.il/pub/grace/src/%{name}-%{version}.tar.bz2
Source1: grace-icons.tar.bz2
Group: Sciences/Other
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildRequires: zlib-devel libjpeg-devel libtiff-devel lesstif-devel 
BuildRequires: netcdf-devel libpng-devel t1lib-devel
Requires: xterm www-browser

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
%configure --enable-grace-home=%_libdir/grace 
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
cat <<EOF > $RPM_BUILD_ROOT%{_datadir}/applications/madnriva-%{name}.desktop
[Desktop Entry]
Name=Grace
Comment=Graphical visualization of scientific data
Exec=xmgrace
Icon=grace
Type=Application
Categories=Science;Education;2DGraphics;
EOF

# icons
install -d $RPM_BUILD_ROOT%{_miconsdir}
install -d $RPM_BUILD_ROOT%{_iconsdir}
install -d $RPM_BUILD_ROOT%{_liconsdir}
cd grace-icons;
cp grace16.png $RPM_BUILD_ROOT%{_miconsdir}/grace.png;
cp grace32.png $RPM_BUILD_ROOT%{_iconsdir}/grace.png;
cp grace48.png $RPM_BUILD_ROOT%{_liconsdir}/grace.png;

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}

%postun
%{clean_menus}

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
%_miconsdir/grace.png
%_iconsdir/grace.png
%_liconsdir/grace.png

%files devel
%defattr (-,root,root)
%_includedir/grace_np.h
%_libdir/libgrace_np.a
