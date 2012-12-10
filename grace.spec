%global debug_package %{nil}
# NOTE: this is needed to avoid broken macro format in 
# T1lib/type1/objects.c
# T1lib/type1/type1.c (presumably others)
# since IfTrace0 macro does not include the format string
# Upstream is warned
# All other formats are fixed in the patched files (sent upstream also)

%define Werror_cflags %nil

Name: grace
Version: 5.1.22
Release: %mkrel 6
Summary: Numerical Data Processing and Visualization Tool (Grace)
License: GPLv2+
Url: http://plasma-gate.weizmann.ac.il/Grace/
Source0: ftp://plasma-gate.weizmann.ac.il/pub/grace/src/grace5/%name-%version.tar.gz
Source1: grace-icons.tar.bz2
Patch0: svgdrv_stringliteral.patch
Patch1: utils_stringliteral.patch
# Fixes the mouse stuck in the window, fix for #58242
# Comes from http://plasma-gate.weizmann.ac.il/Grace/phpbb/viewtopic.php?t=1813
Patch2: mouse_stuck_in_the_window.patch
Group: Sciences/Other
BuildRequires: jpeg-devel
BuildRequires: netcdf-devel
BuildRequires: lesstif-devel
BuildRequires: pkgconfig(libtiff-4)
BuildRequires: pkgconfig(xext)
BuildRequires: pkgconfig(zlib)

Requires: webclient
Requires: xterm

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
%configure2_5x --enable-grace-home=%_libdir/grace \
	       --with-helpviewer="xdg-open %s"  \
	       --with-x \
	       --x-includes=%_libdir \
	       --x-libraries=%_libdir

%make

%install
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


%changelog
* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 5.1.22-6mdv2011.0
+ Revision: 610980
- rebuild

* Fri Apr 16 2010 Stéphane Téletchéa <steletch@mandriva.org> 5.1.22-5mdv2010.1
+ Revision: 535481
- Fix for the stuck mouse in the window, bug #58242

* Thu Sep 10 2009 Stéphane Téletchéa <steletch@mandriva.org> 5.1.22-4mdv2010.0
+ Revision: 436803
- Update format literal files
- Added missing BR libxext6-devel
- Removed the note about the browser name since we default to xdg-open
- Try to enforce lesstif detection
- correct BR
- Fix format strings
- Inline dependencies so they are better traced
- Really use the default browser

  + Thierry Vignaud <tv@mandriva.org>
    - BR lesstif-devel
    - rebuild
    - rebuild for new libjpeg

* Thu Aug 07 2008 Thierry Vignaud <tv@mandriva.org> 5.1.22-2mdv2009.0
+ Revision: 266947
- rebuild early 2009.0 package (before pixel changes)

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Sun Jun 01 2008 Funda Wang <fwang@mandriva.org> 5.1.22-1mdv2009.0
+ Revision: 213894
- New version 5.1.22

* Wed Jan 02 2008 Olivier Blin <oblin@mandriva.com> 5.1.21-4mdv2008.1
+ Revision: 140738
- restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Thu Jul 19 2007 Adam Williamson <awilliamson@mandriva.org> 5.1.21-4mdv2008.0
+ Revision: 53389
- rebuild against new lesstif
- fd.o icons
- fix typo in .desktop file name

* Tue Jun 26 2007 Stéphane Téletchéa <steletch@mandriva.org> 5.1.21-3mdv2008.0
+ Revision: 44465
- Real requires, www-browser is incorrect, webclient not

* Mon Jun 25 2007 Stéphane Téletchéa <steletch@mandriva.org> 5.1.21-2mdv2008.0
+ Revision: 44191
- Use www-browser requires in order to not being mandatory linked to seamonkey
  Fixes bug 30127

* Sun Jun 24 2007 Funda Wang <fwang@mandriva.org> 5.1.21-1mdv2008.0
+ Revision: 43544
- New version


* Sat Mar 19 2005 Michael Scherer <misc@mandrake.org> 5.1.18-2mdk
- Rebuild to fix #14787

* Tue Jan 04 2005 Lenny Cartier <lenny@mandrakesoft.com> 5.1.18-1mdk
- 5.1.18

* Sat Aug 14 2004 Lenny Cartier <lenny@mandrakesoft.com> 5.1.17-1mdk
- 5.1.17

* Sun Jul 04 2004 Austin Acton <austin@mandrakesoft.com> 5.1.16-1mdk
- 5.1.16

* Tue Jun 01 2004 Lenny Cartier <lenny@mandrakesoft.com> 5.1.15-1mdk
- 5.1.15

* Fri Jan 09 2004 Lenny Cartier <lenny@mandrakesoft.com> 5.1.14-1mdk
- 5.1.14

* Wed Dec 17 2003 Lenny Cartier <lenny@mandrakesoft.com> 5.1.13-2mdk
- Patch0: default helpviewer changed to mdkwebadmin rather than netscape (Bug #3428)

* Thu Oct 16 2003 Lenny Cartier <lenny@mandrakesoft.com> 5.1.13-1mdk
- 5.1.13

* Sat Apr 26 2003 Austin Acton <aacton@yorku.ca> 5.1.12-2mdk
- devel does not provide name

* Mon Feb 24 2003 Austin Acton <aacton@yorku.ca> 5.1.12-1mdk
- 5.1.12

* Tue Jan 21 2003 Austin Acton <aacton@yorku.ca> 5.1.11-3mdk
- redo spec file

* Tue Jan 21 2003 Austin Acton <aacton@yorku.ca> 5.1.11-2mdk
- un-fix files lists (duh)

* Tue Jan 21 2003 Austin Acton <aacton@yorku.ca> 5.1.11-1mdk
- 5.1.11
- fixup files lists

* Sat Jan 18 2003 Lenny Cartier <lenny@mandrakesoft.com> 5.1.10-2mdk
- rebuild

* Mon Sep 16 2002 Lenny Cartier <lenny@mandrakesoft.com> 5.1.10-1mdk
- from Austin Acton <aacton@yorku.ca> :
	- 5.1.10

* Mon Sep 09 2002 Lenny Cartier <lenny@mandrakesoft.com> 5.1.9-1mdk
- from Austin Acton <aacton@yorku.ca> :
	- 5.1.9

* Mon Jun 03 2002 Olivier Thauvin <thauvin@aerov.jussieu.fr> 5.1.8-1mdk
- 5.1.8

* Wed Mar 20 2002 Lenny Cartier <lenny@mandrakesoft.com> 5.1.7-1mdk
- 5.1.7

* Wed Mar 06 2002 Lenny Cartier <lenny@mandrakesoft.com> 5.1.6-2mdk
- lower optimizations
- png icons

* Mon Nov 26 2001 Lenny Cartier <lenny@mandrakesoft.com> 5.1.6-1mdk
- 5.1.6

* Fri Oct 12 2001 Lenny Cartier <lenny@mandrakesoft.com> 5.1.4-5mdk
- rbeuild against new libpng

* Wed Aug 29 2001 Lenny Cartier <lenny@mandrakesoft.com> 5.1.4-4mdk
- fix license for grace-devel

* Tue Jul 24 2001 Lenny Cartier <lenny@mandrakesoft.com> 5.1.4-3mdk
- url

* Wed Jul 11 2001 Lenny Cartier <lenny@mandrakesoft.com> 5.1.4-2mdk
- change spec name

* Tue Jul 03 2001 Lenny Cartier <lenny@mandrakesoft.com> 5.1.4-1mdk
- updated to 5.1.4

* Fri Jun 22 2001 Lenny Cartier <lenny@mandrakesoft.com> 5.1.3-3mdk 
- fixes from Thomas Leclerc <leclerc@linux-mandrake.com> (on 3mdk & 2mdk ) :
	- add menu entry

* Wed May 23 2001 Thomas Leclerc <leclerc@linux-mandrake.com> 5.1.3-2mdk
- separate grace-devel
- use installed t1lib
- remove pdf support due to license problem

* Fri May 18 2001 Thomas Leclerc <leclerc@linux-mandrake.com> 5.1.3-1mdk
- upgrade to 5.1.3
- use installed fftw
- add pdf support with pdflib (WARNING: AFPL, not GPL)
- suppress static (useless with lesstif)
- more macros, clean spec

* Wed Jan 10 2001 Lenny Cartier <lenny@mandrakesoft.com> 5.1.2-1mdk
- updated to 5.1.2
- use installed Xbae

* Thu Sep 28 2000 Lenny Cartier <lenny@mandrakesoft.com> 5.1.1-2mdk
- bm & macros

* Sat Aug 26 2000 Giuseppe Ghibò <ghibo@mandrakesoft.com> 5.1.1-1mdk
- initial Mandrake release.
- added BuildRequires.
- added --with-bundled-xbae.

* Mon Apr 03 2000 Henrik Seidel <Henrik.Seidel@gmx.de>
- upgraded to 5.1.0

* Fri Dec 17 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- upgraded to 991217

* Fri Oct 08 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- upgraded to 5.0.5pre1
- added canvas patch

* Fri Oct 01 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- upgraded to 5.0.5pre0

* Fri Sep 17 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- fixed the string copy problem (#611)

* Tue Sep 14 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- upgraded to 5.0.4gamma

* Tue Jun 29 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- upgraded to 990629

* Fri Jun 18 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- upgraded to 990614

* Wed May 19 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- upgraded to 990519

* Mon Apr 26 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- upgraded to 990424

* Wed Apr 07 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- patched pars.yacc to enable "(cond) ? a : b"

* Sun Feb 28 1999 Henrik Seidel <Henrik.Seidel@gmx.de>
- upgraded to 5.0.2beta

* Mon Feb 01 1999 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>
- upgraded to grace-990131

* Tue Jan 12 1999 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>
- upgraded to grace-981231

* Tue Dec 15 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>
- upgraded to grace-981203

* Tue Nov 03 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>
- upgraded to grace-981102

* Thu Oct 22 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>
- upgraded to grace-981021
- added patch for using -bxy "0:1", i.e. for using column specification
  "0" for index.

* Tue Sep 08 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>
- upgraded to grace-5.0.1pre

* Thu Jul 16 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>
- added autoscale patch

* Wed Jul 15 1998 Henrik Seidel <seidel@mpimg-berlin-dahlem.mpg.de>
- initial revision of GRACE rpms

