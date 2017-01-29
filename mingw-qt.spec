%?mingw_package_header

# Override the __debug_install_post argument as this package
# contains both native as well as cross compiled binaries
%global __debug_install_post %%{mingw_debug_install_post}; %{_rpmconfigdir}/find-debuginfo.sh %{?_missing_build_ids_terminate_build:--strict-build-id} %{?_find_debuginfo_opts} "%{_builddir}/%%{?buildsubdir}" %{nil}

#%%global pre RC

%global platform_win32 win32-g++-cross
%global platform_win64 win32-g++-cross-x64

# Helper macro to retrieve the name of the openssl library
%global openssl_soname %(rpm -ql mingw32-openssl | grep -Eo 'libssl.*$' | grep -Eo '[0-9]+')

Name:           mingw-qt
Version:        4.8.7
Release:        1%{?pre}%{?dist}
Summary:        Qt for Windows

License:        GPLv3 with exceptions or LGPLv2 with exceptions
Group:          Development/Libraries

URL:            http://www.qtsoftware.com/
Source0:        http://download.qt-project.org/official_releases/qt/4.8/%{version}/qt-everywhere-opensource-src-%{version}%{?pre:-%{pre}}.tar.gz

# Special cross-compilation qmake target.
Source1:        qmake.conf.win32
Source2:        qmake.conf.win64
Source3:        qplatformdefs.h

# When building Qt as static library some files have a different content
# when compared to the static library. Merge those changes manually.
# This patch also applies some additional changes which are required to make
# linking against the static version of Qt work without any manual fiddling
Patch0:         qt-merge-static-and-shared-library-trees.patch

# When linking against the static dbus library, the #define DBUS_EXPORT must be set
Patch1:         qt4-fix-linking-against-static-dbus.patch

# Disable WebKit tests that are failing (as of Qt 4.8.0 rc1) with
# out of source builds.
Patch10:        mingw32-qt-4.8.0-no-webkit-tests.patch

# The configure script thinks that there is no IPC/shared memory support
# for this platform, while there is support. Fix the configure script
Patch17:        qt-dont-perform-ipc-checks-for-win32.patch

# Openssl is loaded at runtime
Patch19:         qt-4.7.3-fix-loading-openssl.patch

# Fix compilation of the designer tool
Patch20:        qt-4.8.0-fix-include-windows-h.patch

# Make sure the QtUiTools are built as both a static and a shared library
# https://bugreports.qt-project.org/browse/QTBUG-20498
Patch21:        qt-4.8.0-build-qtuitools-dynamically.patch

# Javascript-JIT fails to link on mingw x86_64
Patch22:        qt-fix-javascript-jit-on-mingw-x86_64.patch

# As of qt 4.8.1 the qt build system tries to build a activeqt module for
# the designer component. However, this fails to compile:
# In file included from ../../../../../include/ActiveQt/qaxselect.h:1:0,
#                 from /home/erik/fedora/mingw-qt/qt-everywhere-opensource-src-4.8.1/tools/designer/src/plugins/activeqt/qaxwidgettaskmenu.cpp:55:
# ../../../../../include/ActiveQt/../../../qt-everywhere-opensource-src-4.8.1/src/activeqt/container/qaxselect.h:47:26: fatal error: ui_qaxselect.h: No such file or directory
# Workaround this for now until a proper fix has been found
Patch23:        qt-4.8.1-fix-activeqt-compilation.patch

# lrelease-qt4 tries to run qmake not qmake-qt4 (http://bugzilla.redhat.com/820767)
Patch24:        qt-everywhere-opensource-src-4.8.1-linguist_qmake-qt4.patch

# When building static binaries, make sure the gcc argument -DQT_DLL isn't used
Patch28:        qt-dont-set-qt-dll-define-for-static-builds.patch

# When using pkg-config to detect static libraries, the --static flag should also be used
Patch31:        qt4-use-correct-pkg-config-static-flags.patch

# Add support for gcc6 (patch taken from native Fedora package)
Patch35:        qt-everywhere-opensource-src-4.8.7-gcc6.patch

BuildRequires:  mingw32-filesystem >= 95
BuildRequires:  mingw32-gcc
BuildRequires:  mingw32-gcc-c++
BuildRequires:  mingw32-binutils
BuildRequires:  mingw32-openssl
BuildRequires:  mingw32-zlib
BuildRequires:  mingw32-win-iconv
BuildRequires:  mingw32-libjpeg-turbo
BuildRequires:  mingw32-libpng
BuildRequires:  mingw32-libtiff
BuildRequires:  mingw32-sqlite
BuildRequires:  mingw32-dbus
BuildRequires:  mingw32-pkg-config

BuildRequires:  mingw32-dbus-static
BuildRequires:  mingw32-libjpeg-turbo-static
BuildRequires:  mingw32-libtiff-static
BuildRequires:  mingw32-libpng-static
BuildRequires:  mingw32-sqlite-static
BuildRequires:  mingw32-zlib-static
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
BuildRequires:  mingw32-winpthreads-static
%endif

BuildRequires:  mingw64-filesystem >= 95
BuildRequires:  mingw64-gcc
BuildRequires:  mingw64-gcc-c++
BuildRequires:  mingw64-binutils
BuildRequires:  mingw64-openssl
BuildRequires:  mingw64-zlib
BuildRequires:  mingw64-win-iconv
BuildRequires:  mingw64-libjpeg-turbo
BuildRequires:  mingw64-libpng
BuildRequires:  mingw64-libtiff
BuildRequires:  mingw64-sqlite
BuildRequires:  mingw64-dbus
BuildRequires:  mingw64-pkg-config

BuildRequires:  mingw64-dbus-static
BuildRequires:  mingw64-libjpeg-turbo-static
BuildRequires:  mingw64-libtiff-static
BuildRequires:  mingw64-libpng-static
BuildRequires:  mingw64-sqlite-static
BuildRequires:  mingw64-zlib-static
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
BuildRequires:  mingw64-winpthreads-static
%endif

BuildRequires:  zip
BuildRequires:  dos2unix


%description
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.


# Win32
%package -n mingw32-qt
Summary:        Qt for Windows
# This package contains the cross-compiler setup for qmake
Requires:       mingw32-qt-qmake = %{version}-%{release}
BuildArch:      noarch

%description -n mingw32-qt
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.

%package -n mingw32-qt-qmake
Summary:       Qt for Windows Build Environment

%description -n mingw32-qt-qmake
This package contains the build environment for cross compiling
applications with the Fedora Windows Qt Library and cross-compiler.

%package -n mingw32-qt-tools
Summary:       Various tools belonging to the mingw32-qt library
Requires:      mingw32-qt = %{version}-%{release}
BuildArch:     noarch

%description -n mingw32-qt-tools
Various tools belonging to the mingw32-qt library.

%package -n mingw32-qt-static
Summary:       Static version of the mingw32-qt library
Requires:      mingw32-qt = %{version}-%{release}
Requires:      mingw32-dbus-static
Requires:      mingw32-libjpeg-turbo-static
Requires:      mingw32-libtiff-static
Requires:      mingw32-libpng-static
Requires:      mingw32-sqlite-static
Requires:      mingw32-zlib-static
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
Requires:      mingw32-winpthreads-static
%endif
BuildArch:     noarch

%description -n mingw32-qt-static
Static version of the mingw32-qt library.

# Win64
%package -n mingw64-qt
Summary:        Qt for Windows
# This package contains the cross-compiler setup for qmake
Requires:       mingw64-qt-qmake = %{version}-%{release}
BuildArch:      noarch

%description -n mingw64-qt
This package contains the Qt software toolkit for developing
cross-platform applications.

This is the Windows version of Qt, for use in conjunction with the
Fedora Windows cross-compiler.

%package -n mingw64-qt-qmake
Summary:       Qt for Windows Build Environment

%description -n mingw64-qt-qmake
This package contains the build environment for cross compiling
applications with the Fedora Windows Qt Library and cross-compiler.

%package -n mingw64-qt-tools
Summary:       Various tools belonging to the mingw64-qt library
Requires:      mingw64-qt = %{version}-%{release}
BuildArch:     noarch

%description -n mingw64-qt-tools
Various tools belonging to the mingw32-qt library.

%package -n mingw64-qt-static
Summary:       Static version of the mingw64-qt library
Requires:      mingw64-qt = %{version}-%{release}
Requires:      mingw64-dbus-static
Requires:      mingw64-libjpeg-turbo-static
Requires:      mingw64-libtiff-static
Requires:      mingw64-libpng-static
Requires:      mingw64-sqlite-static
Requires:      mingw64-zlib-static
%if 0%{?fedora} >= 20 || 0%{?rhel} >= 7
Requires:      mingw64-winpthreads-static
%endif
BuildArch:     noarch

%description -n mingw64-qt-static
Static version of the mingw64-qt library.


%?mingw_debug_package


%prep
%setup -q -n qt-everywhere-opensource-src-%{version}

%patch0 -p0
%patch1 -p0 -b .dbus_static
%patch10 -p1 -b .no_webkit_tests
%patch17 -p0
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1 -b .linguist_qtmake-qt4
%patch28 -p1 -b .qt_dll_define
%patch31 -p1 -b .pkgconfig_static
%patch35 -p1 -b .gcc6

# Patch 19 (openssl) needs an additional change
# qt loads openssl libraries (ssleay32, libeay32)  at runtime, but they are called libssl-OPENSSL_SONAME
# and libcrypto-OPENSSL_SONAME in our cross build, so qt is patched to look for them additionally
sed -i "s/OPENSSL_SONAME/%{openssl_soname}/" src/network/ssl/qsslsocket_openssl_symbols.cpp

# Cross-compilation qmake target.
mkdir mkspecs/%{platform_win32}
mkdir mkspecs/%{platform_win64}
cp %{SOURCE1} mkspecs/%{platform_win32}/qmake.conf
cp %{SOURCE2} mkspecs/%{platform_win64}/qmake.conf
cp %{SOURCE3} mkspecs/%{platform_win32}
cp %{SOURCE3} mkspecs/%{platform_win64}


%build
# Generic configure arguments
# Phonon is disabled for now because we lack the directx headers
qt_configure_args_generic="\
    -qt3support \
    -optimized-qmake \
    -verbose \
    -opensource \
    -exceptions \
    -fast \
    -confirm-license \
    -force-pkg-config \
    -little-endian \
    -xmlpatterns \
    -multimedia \
    -audio-backend \
    -webkit \
    -script \
    -scripttools \
    -declarative \
    -no-phonon \
    -javascript-jit \
    -qt-libmng \
    -system-zlib \
    -system-libtiff \
    -system-libpng \
    -system-libjpeg \
    -system-sqlite \
    -iconv \
    -openssl \
    -dbus-linked \
    -make libs \
    -make tools \
    -make translations \
    -nomake demos \
    -nomake docs \
    -nomake examples"

qt_configure_args_win32="\
    -prefix %{mingw32_prefix} \
    -bindir %{mingw32_bindir} \
    -datadir %{mingw32_datadir}/qt4 \
    -demosdir %{mingw32_datadir}/qt4/demos \
    -docdir %{mingw32_docdir}/qt4 \
    -examplesdir %{mingw32_datadir}/qt4/examples \
    -headerdir %{mingw32_includedir} \
    -libdir %{mingw32_libdir} \
    -plugindir %{mingw32_libdir}/qt4/plugins \
    -sysconfdir %{mingw32_sysconfdir} \
    -translationdir %{mingw32_datadir}/qt4/translations \
    -xplatform %{platform_win32}"

qt_configure_args_win64="\
    -prefix %{mingw64_prefix} \
    -bindir %{mingw64_bindir} \
    -datadir %{mingw64_datadir}/qt4 \
    -demosdir %{mingw64_datadir}/qt4/demos \
    -docdir %{mingw64_docdir}/qt4 \
    -examplesdir %{mingw64_datadir}/qt4/examples \
    -headerdir %{mingw64_includedir} \
    -libdir %{mingw64_libdir} \
    -plugindir %{mingw64_libdir}/qt4/plugins \
    -sysconfdir %{mingw64_sysconfdir} \
    -translationdir %{mingw64_datadir}/qt4/translations \
    -xplatform %{platform_win64}"

# RPM automatically sets the environment variable PKG_CONFIG_PATH
# to point to the native pkg-config files, but while cross compiling
# we don't want to have this environment variable set
unset PKG_CONFIG_PATH

# workaround for class std::auto_ptr' is deprecated with gcc-6
export CXXFLAGS="$CXXFLAGS -std=gnu++98 -Wno-deprecated"

###############################################################################
# Win32
#
# We have to build Qt three times, once for the static release build, once
# for the shared release build and once for the shared debug build
#
# Unfortunately Qt only supports out-of-source builds which are in ../some_folder
rm -rf ../build_release_static_win32
mkdir ../build_release_static_win32
pushd ../build_release_static_win32
../qt-everywhere-opensource-src-%{version}/configure \
    -release \
    -static \
    $qt_configure_args_generic $qt_configure_args_win32
make %{?_smp_mflags}
popd

rm -rf ../build_debug_win32
mkdir ../build_debug_win32
pushd ../build_debug_win32
../qt-everywhere-opensource-src-%{version}/configure \
    -debug \
    -shared \
    $qt_configure_args_generic $qt_configure_args_win32
make %{?_smp_mflags}
popd

rm -rf ../build_release_win32
mkdir ../build_release_win32
pushd ../build_release_win32
../qt-everywhere-opensource-src-%{version}/configure \
    -release \
    -shared \
    $qt_configure_args_generic $qt_configure_args_win32
make %{?_smp_mflags}

###############################################################################
# Win64
#
# We have to build Qt three times, once for the static release build, once
# for the shared release build and once for the shared debug build
#
# Unfortunately Qt only supports out-of-source builds which are in ../some_folder
rm -rf ../build_release_static_win64
mkdir ../build_release_static_win64
pushd ../build_release_static_win64
../qt-everywhere-opensource-src-%{version}/configure \
    -release \
    -static \
    $qt_configure_args_generic $qt_configure_args_win64
make %{?_smp_mflags}
popd

rm -rf ../build_debug_win64
mkdir ../build_debug_win64
pushd ../build_debug_win64
../qt-everywhere-opensource-src-%{version}/configure \
    -debug \
    -shared \
    $qt_configure_args_generic $qt_configure_args_win64
make %{?_smp_mflags}
popd

rm -rf ../build_release_win64
mkdir ../build_release_win64
pushd ../build_release_win64
../qt-everywhere-opensource-src-%{version}/configure \
    -release \
    -shared \
    $qt_configure_args_generic $qt_configure_args_win64
make %{?_smp_mflags}


%install
# Install the static libraries in a temporary prefix so we can merge everything together properly
mkdir $RPM_BUILD_ROOT/static
make install -C ../build_release_static_win32 INSTALL_ROOT=$RPM_BUILD_ROOT/static

# Clean up everything in the static tree which we don't need to safe disk space
rm -rf $RPM_BUILD_ROOT/static/%{mingw32_bindir}
rm -rf ../build_release_static_win32

make install -C ../build_release_static_win64 INSTALL_ROOT=$RPM_BUILD_ROOT/static
rm -rf $RPM_BUILD_ROOT/static/%{mingw64_bindir}
rm -rf ../build_release_static_win64

# Drop the qtmain static library from the static tree as
# it's already part of the main tree
rm -f $RPM_BUILD_ROOT/static/%{mingw32_libdir}/libqtmain*
rm -f $RPM_BUILD_ROOT/static/%{mingw64_libdir}/libqtmain*

# Give the real static libraries the correct filename to avoid future conflicts with Qt5
for FN in $RPM_BUILD_ROOT/static%{mingw32_libdir}/*.a $RPM_BUILD_ROOT/static%{mingw64_libdir}/*.a ; do
    FN_NEW=$(echo $FN | sed s/'.a$'/'4.a'/)
    mv $FN $FN_NEW
done

# Install the shared libraries
make install -C ../build_debug_win32 INSTALL_ROOT=$RPM_BUILD_ROOT
make install -C ../build_release_win32 INSTALL_ROOT=$RPM_BUILD_ROOT

make install -C ../build_debug_win64 INSTALL_ROOT=$RPM_BUILD_ROOT
make install -C ../build_release_win64 INSTALL_ROOT=$RPM_BUILD_ROOT

# Remove the ActiveQt pieces from the shared build as they aren't build as shared library so
# it's good enough to only bundle the static libraries originating from the static build
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/libQAx* $RPM_BUILD_ROOT%{mingw64_libdir}/libQAx*

# Rename the .a files to .dll.a as they're actually import libraries and not static libraries
for FN in $RPM_BUILD_ROOT%{mingw32_libdir}/*.a $RPM_BUILD_ROOT%{mingw64_libdir}/*.a ; do
    # Ignore libqtmain*.a
    echo $FN | grep -q qtmain && continue

    # Rename the file
    FN_NEW=$(echo $FN | sed s/'.a$'/'.dll.a'/)
    mv $FN $FN_NEW
done

# Move the static libraries from the static tree to the main tree
mv $RPM_BUILD_ROOT/static%{mingw32_libdir}/*.a $RPM_BUILD_ROOT%{mingw32_libdir}
mv $RPM_BUILD_ROOT/static%{mingw64_libdir}/*.a $RPM_BUILD_ROOT%{mingw64_libdir}

# Clean up the static trees as we've now merged all interesting pieces
rm -rf $RPM_BUILD_ROOT/static

# Also install the lrelease tool
make -C ../build_release_win32/tools/linguist/lrelease install INSTALL_ROOT=$RPM_BUILD_ROOT
make -C ../build_release_win64/tools/linguist/lrelease install INSTALL_ROOT=$RPM_BUILD_ROOT

# move QtUiTools4.dll from lib/ to bin/
mv $RPM_BUILD_ROOT%{mingw32_libdir}/QtUiTools4.dll $RPM_BUILD_ROOT%{mingw32_bindir}/
mv $RPM_BUILD_ROOT%{mingw64_libdir}/QtUiTools4.dll $RPM_BUILD_ROOT%{mingw64_bindir}/

# Drop the debug version of the tool qmlplugindumpd.exe
rm -f $RPM_BUILD_ROOT%{mingw32_bindir}/qmlplugindumpd.exe
rm -f $RPM_BUILD_ROOT%{mingw64_bindir}/qmlplugindumpd.exe

# The .dll's are installed in both %%{mingw32_bindir} and %%{mingw32_libdir}
# One copy of the .dll's is sufficient
rm -f $RPM_BUILD_ROOT%{mingw32_libdir}/*.dll
rm -f $RPM_BUILD_ROOT%{mingw64_libdir}/*.dll

# add links with version suffix for convenience
ln -s libqtmain.a $RPM_BUILD_ROOT%{mingw32_libdir}/libqtmain4.a
ln -s libqtmaind.a $RPM_BUILD_ROOT%{mingw32_libdir}/libqtmaind4.a

ln -s libqtmain.a $RPM_BUILD_ROOT%{mingw64_libdir}/libqtmain4.a
ln -s libqtmaind.a $RPM_BUILD_ROOT%{mingw64_libdir}/libqtmaind4.a

# Drop all the files which we don't need
rm -f  $RPM_BUILD_ROOT%{mingw32_libdir}/*.prl
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/qt4/demos
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/qt4/examples
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/qt4/q3porting.xml
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/qt4/phrasebooks/

rm -f  $RPM_BUILD_ROOT%{mingw64_libdir}/*.prl
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/qt4/demos
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/qt4/examples
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/qt4/q3porting.xml
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/qt4/phrasebooks/

# The Qt build system creates a folder called 'imports' but it isn't entirely sure
# what it's purpose is. Drop it for now
rm -rf $RPM_BUILD_ROOT%{mingw32_prefix}/imports
rm -rf $RPM_BUILD_ROOT%{mingw64_prefix}/imports

# Manually install qmake and other native tools so we don't depend anymore on
# the version of the native Fedora Qt and also fix issues as illustrated at
# http://stackoverflow.com/questions/6592931/building-for-windows-under-linux-using-qt-creator
#
# Also make sure the tools can be found by CMake
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/bin
mkdir -p $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/bin

install -m0755 ../build_release_win32/bin/qmake $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/bin/qmake-qt4
ln -s ../%{mingw32_target}/bin/qmake-qt4 $RPM_BUILD_ROOT%{_bindir}/%{mingw32_target}-qmake-qt4
ln -s %{mingw32_target}-qmake-qt4 $RPM_BUILD_ROOT%{_bindir}/mingw32-qmake-qt4
rm -f $RPM_BUILD_ROOT%{mingw32_bindir}/qmake

for tool in lrelease moc rcc uic ; do
    mv $RPM_BUILD_ROOT%{mingw32_bindir}/$tool $RPM_BUILD_ROOT%{_prefix}/%{mingw32_target}/bin/$tool
    ln -s ../%{mingw32_target}/bin/$tool $RPM_BUILD_ROOT%{_bindir}/%{mingw32_target}-$tool
done

install -m0755 ../build_release_win64/bin/qmake $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/bin/qmake-qt4
ln -s ../%{mingw64_target}/bin/qmake-qt4 $RPM_BUILD_ROOT%{_bindir}/%{mingw64_target}-qmake-qt4
ln -s %{mingw64_target}-qmake-qt4 $RPM_BUILD_ROOT%{_bindir}/mingw64-qmake-qt4
rm -f $RPM_BUILD_ROOT%{mingw64_bindir}/qmake

for tool in lrelease moc rcc uic ; do
    mv $RPM_BUILD_ROOT%{mingw64_bindir}/$tool $RPM_BUILD_ROOT%{_prefix}/%{mingw64_target}/bin/$tool
    ln -s ../%{mingw64_target}/bin/$tool $RPM_BUILD_ROOT%{_bindir}/%{mingw64_target}-$tool
done

# An argument in the mkspecs profile needs to be un-commented in order to be
# useful for developers who wish to use the Qt libraries
sed -i s@'#QT_LIBINFIX'@'QT_LIBINFIX'@ $RPM_BUILD_ROOT%{mingw32_datadir}/qt4/mkspecs/%{platform_win32}/qmake.conf
sed -i s@'#QT_LIBINFIX'@'QT_LIBINFIX'@ $RPM_BUILD_ROOT%{mingw64_datadir}/qt4/mkspecs/%{platform_win64}/qmake.conf

# Remove some duplicate mkspecs data
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/qt4/mkspecs/%{platform_win32}/default
rm -rf $RPM_BUILD_ROOT%{mingw32_datadir}/qt4/mkspecs/%{platform_win32}/%{platform_win32}

rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/qt4/mkspecs/%{platform_win64}/default
rm -rf $RPM_BUILD_ROOT%{mingw64_datadir}/qt4/mkspecs/%{platform_win64}/%{platform_win64}

# Workaround a bug where building against the debug binaries will always fail:
# https://bugreports.qt.nokia.com/browse/QTBUG-14467
sed -i s@'$${QT_LIBINFIX}d'@'d$${QT_LIBINFIX}'@ $RPM_BUILD_ROOT%{mingw32_datadir}/qt4/mkspecs/features/win32/windows.prf
sed -i s@'$${QT_LIBINFIX}d'@'d$${QT_LIBINFIX}'@ $RPM_BUILD_ROOT%{mingw32_datadir}/qt4/mkspecs/features/qt_functions.prf

sed -i s@'$${QT_LIBINFIX}d'@'d$${QT_LIBINFIX}'@ $RPM_BUILD_ROOT%{mingw64_datadir}/qt4/mkspecs/features/win32/windows.prf
sed -i s@'$${QT_LIBINFIX}d'@'d$${QT_LIBINFIX}'@ $RPM_BUILD_ROOT%{mingw64_datadir}/qt4/mkspecs/features/qt_functions.prf


# Win32
%files -n mingw32-qt
%{mingw32_bindir}/Qt3Support4.dll
%{mingw32_bindir}/Qt3Supportd4.dll
%{mingw32_bindir}/QtCLucene4.dll
%{mingw32_bindir}/QtCLucened4.dll
%{mingw32_bindir}/QtCore4.dll
%{mingw32_bindir}/QtCored4.dll
%{mingw32_bindir}/QtDBus4.dll
%{mingw32_bindir}/QtDBusd4.dll
%{mingw32_bindir}/QtDeclarative4.dll
%{mingw32_bindir}/QtDeclaratived4.dll
%{mingw32_bindir}/QtDesigner4.dll
%{mingw32_bindir}/QtDesignerd4.dll
%{mingw32_bindir}/QtDesignerComponents4.dll
%{mingw32_bindir}/QtDesignerComponentsd4.dll
%{mingw32_bindir}/QtGui4.dll
%{mingw32_bindir}/QtGuid4.dll
%{mingw32_bindir}/QtHelp4.dll
%{mingw32_bindir}/QtHelpd4.dll
%{mingw32_bindir}/QtNetwork4.dll
%{mingw32_bindir}/QtNetworkd4.dll
%{mingw32_bindir}/QtOpenGL4.dll
%{mingw32_bindir}/QtOpenGLd4.dll
%{mingw32_bindir}/QtScript4.dll
%{mingw32_bindir}/QtScriptd4.dll
%{mingw32_bindir}/QtScriptTools4.dll
%{mingw32_bindir}/QtScriptToolsd4.dll
%{mingw32_bindir}/QtSql4.dll
%{mingw32_bindir}/QtSqld4.dll
%{mingw32_bindir}/QtSvg4.dll
%{mingw32_bindir}/QtSvgd4.dll
%{mingw32_bindir}/QtUiTools4.dll
%{mingw32_bindir}/QtXml4.dll
%{mingw32_bindir}/QtXmld4.dll
%{mingw32_bindir}/QtXmlPatterns4.dll
%{mingw32_bindir}/QtXmlPatternsd4.dll
%{mingw32_bindir}/QtMultimedia4.dll
%{mingw32_bindir}/QtMultimediad4.dll
%{mingw32_bindir}/QtTest4.dll
%{mingw32_bindir}/QtTestd4.dll
%{mingw32_bindir}/QtWebKit4.dll
%{mingw32_bindir}/QtWebKitd4.dll
%{mingw32_libdir}/libQt3Support4.dll.a
%{mingw32_libdir}/libQt3Supportd4.dll.a
%{mingw32_libdir}/libQtCLucene4.dll.a
%{mingw32_libdir}/libQtCLucened4.dll.a
%{mingw32_libdir}/libQtCore4.dll.a
%{mingw32_libdir}/libQtCored4.dll.a
%{mingw32_libdir}/libQtDBus4.dll.a
%{mingw32_libdir}/libQtDBusd4.dll.a
%{mingw32_libdir}/libQtDeclarative4.dll.a
%{mingw32_libdir}/libQtDeclaratived4.dll.a
%{mingw32_libdir}/libQtDesigner4.dll.a
%{mingw32_libdir}/libQtDesignerd4.dll.a
%{mingw32_libdir}/libQtDesignerComponents4.dll.a
%{mingw32_libdir}/libQtDesignerComponentsd4.dll.a
%{mingw32_libdir}/libQtGui4.dll.a
%{mingw32_libdir}/libQtGuid4.dll.a
%{mingw32_libdir}/libQtHelp4.dll.a
%{mingw32_libdir}/libQtHelpd4.dll.a
%{mingw32_libdir}/libqtmain.a
%{mingw32_libdir}/libqtmaind.a
%{mingw32_libdir}/libqtmain4.a
%{mingw32_libdir}/libqtmaind4.a
%{mingw32_libdir}/libQtMultimedia4.dll.a
%{mingw32_libdir}/libQtMultimediad4.dll.a
%{mingw32_libdir}/libQtNetwork4.dll.a
%{mingw32_libdir}/libQtNetworkd4.dll.a
%{mingw32_libdir}/libQtOpenGL4.dll.a
%{mingw32_libdir}/libQtOpenGLd4.dll.a
%{mingw32_libdir}/libQtScript4.dll.a
%{mingw32_libdir}/libQtScriptd4.dll.a
%{mingw32_libdir}/libQtScriptTools4.dll.a
%{mingw32_libdir}/libQtScriptToolsd4.dll.a
%{mingw32_libdir}/libQtSql4.dll.a
%{mingw32_libdir}/libQtSqld4.dll.a
%{mingw32_libdir}/libQtSvg4.dll.a
%{mingw32_libdir}/libQtSvgd4.dll.a
%{mingw32_libdir}/libQtTest4.dll.a
%{mingw32_libdir}/libQtTestd4.dll.a
%{mingw32_libdir}/libQtUiTools4.dll.a
%{mingw32_libdir}/libQtUiToolsd4.dll.a
%{mingw32_libdir}/libQtWebKit4.dll.a
%{mingw32_libdir}/libQtWebKitd4.dll.a
%{mingw32_libdir}/libQtXml4.dll.a
%{mingw32_libdir}/libQtXmld4.dll.a
%{mingw32_libdir}/libQtXmlPatterns4.dll.a
%{mingw32_libdir}/libQtXmlPatternsd4.dll.a
%{mingw32_libdir}/pkgconfig/Qt3Support.pc
%{mingw32_libdir}/pkgconfig/Qt3Supportd.pc
%{mingw32_libdir}/pkgconfig/QtCLucene.pc
%{mingw32_libdir}/pkgconfig/QtCLucened.pc
%{mingw32_libdir}/pkgconfig/QtCore.pc
%{mingw32_libdir}/pkgconfig/QtCored.pc
%{mingw32_libdir}/pkgconfig/QtDBus.pc
%{mingw32_libdir}/pkgconfig/QtDBusd.pc
%{mingw32_libdir}/pkgconfig/QtDeclarative.pc
%{mingw32_libdir}/pkgconfig/QtDeclaratived.pc
%{mingw32_libdir}/pkgconfig/QtGui.pc
%{mingw32_libdir}/pkgconfig/QtGuid.pc
%{mingw32_libdir}/pkgconfig/QtHelp.pc
%{mingw32_libdir}/pkgconfig/QtHelpd.pc
%{mingw32_libdir}/pkgconfig/qtmain.pc
%{mingw32_libdir}/pkgconfig/qtmaind.pc
%{mingw32_libdir}/pkgconfig/QtMultimedia.pc
%{mingw32_libdir}/pkgconfig/QtMultimediad.pc
%{mingw32_libdir}/pkgconfig/QtNetwork.pc
%{mingw32_libdir}/pkgconfig/QtNetworkd.pc
%{mingw32_libdir}/pkgconfig/QtOpenGL.pc
%{mingw32_libdir}/pkgconfig/QtOpenGLd.pc
%{mingw32_libdir}/pkgconfig/QtScript.pc
%{mingw32_libdir}/pkgconfig/QtScriptd.pc
%{mingw32_libdir}/pkgconfig/QtScriptTools.pc
%{mingw32_libdir}/pkgconfig/QtScriptToolsd.pc
%{mingw32_libdir}/pkgconfig/QtSql.pc
%{mingw32_libdir}/pkgconfig/QtSqld.pc
%{mingw32_libdir}/pkgconfig/QtSvg.pc
%{mingw32_libdir}/pkgconfig/QtSvgd.pc
%{mingw32_libdir}/pkgconfig/QtTest.pc
%{mingw32_libdir}/pkgconfig/QtTestd.pc
%{mingw32_libdir}/pkgconfig/QtUiTools.pc
%{mingw32_libdir}/pkgconfig/QtUiToolsd.pc
%{mingw32_libdir}/pkgconfig/QtWebKit.pc
%{mingw32_libdir}/pkgconfig/QtWebKitd.pc
%{mingw32_libdir}/pkgconfig/QtXmlPatterns.pc
%{mingw32_libdir}/pkgconfig/QtXmlPatternsd.pc
%{mingw32_libdir}/pkgconfig/QtXml.pc
%{mingw32_libdir}/pkgconfig/QtXmld.pc
%dir %{mingw32_libdir}/qt4/
%dir %{mingw32_libdir}/qt4/plugins
%dir %{mingw32_libdir}/qt4/plugins/accessible
%{mingw32_libdir}/qt4/plugins/accessible/qtaccessiblecompatwidgets4.dll
%{mingw32_libdir}/qt4/plugins/accessible/qtaccessiblecompatwidgetsd4.dll
%{mingw32_libdir}/qt4/plugins/accessible/qtaccessiblewidgets4.dll
%{mingw32_libdir}/qt4/plugins/accessible/qtaccessiblewidgetsd4.dll
%dir %{mingw32_libdir}/qt4/plugins/bearer
%{mingw32_libdir}/qt4/plugins/bearer/qgenericbearer4.dll
%{mingw32_libdir}/qt4/plugins/bearer/qgenericbearerd4.dll
%{mingw32_libdir}/qt4/plugins/bearer/qnativewifibearer4.dll
%{mingw32_libdir}/qt4/plugins/bearer/qnativewifibearerd4.dll
%dir %{mingw32_libdir}/qt4/plugins/codecs
%{mingw32_libdir}/qt4/plugins/codecs/qcncodecs4.dll
%{mingw32_libdir}/qt4/plugins/codecs/qcncodecsd4.dll
%{mingw32_libdir}/qt4/plugins/codecs/qjpcodecs4.dll
%{mingw32_libdir}/qt4/plugins/codecs/qjpcodecsd4.dll
%{mingw32_libdir}/qt4/plugins/codecs/qkrcodecs4.dll
%{mingw32_libdir}/qt4/plugins/codecs/qkrcodecsd4.dll
%{mingw32_libdir}/qt4/plugins/codecs/qtwcodecs4.dll
%{mingw32_libdir}/qt4/plugins/codecs/qtwcodecsd4.dll
%dir %{mingw32_libdir}/qt4/plugins/graphicssystems
%{mingw32_libdir}/qt4/plugins/graphicssystems/qglgraphicssystem4.dll
%{mingw32_libdir}/qt4/plugins/graphicssystems/qglgraphicssystemd4.dll
%{mingw32_libdir}/qt4/plugins/graphicssystems/qtracegraphicssystem4.dll
%{mingw32_libdir}/qt4/plugins/graphicssystems/qtracegraphicssystemd4.dll
%dir %{mingw32_libdir}/qt4/plugins/iconengines
%{mingw32_libdir}/qt4/plugins/iconengines/qsvgicon4.dll
%{mingw32_libdir}/qt4/plugins/iconengines/qsvgicond4.dll
%dir %{mingw32_libdir}/qt4/plugins/imageformats
%{mingw32_libdir}/qt4/plugins/imageformats/qgif4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qgifd4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qico4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qicod4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qjpeg4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qjpegd4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qmng4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qmngd4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qsvg4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qsvgd4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qtiff4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qtiffd4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qtga4.dll
%{mingw32_libdir}/qt4/plugins/imageformats/qtgad4.dll
%dir %{mingw32_libdir}/qt4/plugins/qmltooling
%{mingw32_libdir}/qt4/plugins/qmltooling/qmldbg_inspector4.dll
%{mingw32_libdir}/qt4/plugins/qmltooling/qmldbg_inspectord4.dll
%{mingw32_libdir}/qt4/plugins/qmltooling/qmldbg_tcp4.dll
%{mingw32_libdir}/qt4/plugins/qmltooling/qmldbg_tcpd4.dll
%dir %{mingw32_libdir}/qt4/plugins/script
%{mingw32_libdir}/qt4/plugins/script/qtscriptdbus4.dll
%{mingw32_libdir}/qt4/plugins/script/qtscriptdbusd4.dll
%dir %{mingw32_libdir}/qt4/plugins/sqldrivers
%{mingw32_libdir}/qt4/plugins/sqldrivers/qsqlite4.dll
%{mingw32_libdir}/qt4/plugins/sqldrivers/qsqlited4.dll
%{mingw32_libdir}/qt4/plugins/sqldrivers/qsqlodbc4.dll
%{mingw32_libdir}/qt4/plugins/sqldrivers/qsqlodbcd4.dll
%{mingw32_includedir}/ActiveQt
%{mingw32_includedir}/Qt/
%{mingw32_includedir}/Qt3Support/
%{mingw32_includedir}/QtCore/
%{mingw32_includedir}/QtDBus/
%{mingw32_includedir}/QtDeclarative/
%{mingw32_includedir}/QtDesigner/
%{mingw32_includedir}/QtGui/
%{mingw32_includedir}/QtHelp/
%{mingw32_includedir}/QtMultimedia/
%{mingw32_includedir}/QtNetwork/
%{mingw32_includedir}/QtOpenGL/
%{mingw32_includedir}/QtScript/
%{mingw32_includedir}/QtScriptTools/
%{mingw32_includedir}/QtSql/
%{mingw32_includedir}/QtSvg/
%{mingw32_includedir}/QtTest/
%{mingw32_includedir}/QtUiTools/
%{mingw32_includedir}/QtWebKit/
%{mingw32_includedir}/QtXml/
%{mingw32_includedir}/QtXmlPatterns/
%{mingw32_datadir}/qt4/

%files -n mingw32-qt-qmake
%doc LICENSE.GPL3 LICENSE.LGPL LGPL_EXCEPTION.txt README
%{_bindir}/%{mingw32_target}-lrelease
%{_bindir}/%{mingw32_target}-moc
%{_bindir}/%{mingw32_target}-qmake-qt4
%{_bindir}/%{mingw32_target}-rcc
%{_bindir}/%{mingw32_target}-uic
%{_bindir}/mingw32-qmake-qt4
%{_prefix}/%{mingw32_target}/bin/lrelease
%{_prefix}/%{mingw32_target}/bin/moc
%{_prefix}/%{mingw32_target}/bin/qmake-qt4
%{_prefix}/%{mingw32_target}/bin/rcc
%{_prefix}/%{mingw32_target}/bin/uic
%{mingw32_datadir}/qt4/mkspecs/%{platform_win32}

%files -n mingw32-qt-tools
%{mingw32_bindir}/assistant.exe
%{mingw32_bindir}/designer.exe
%{mingw32_bindir}/lconvert.exe
%{mingw32_bindir}/linguist.exe
%{mingw32_bindir}/lupdate.exe
%{mingw32_bindir}/pixeltool.exe
%{mingw32_bindir}/qcollectiongenerator.exe
%{mingw32_bindir}/qdbus.exe
%{mingw32_bindir}/qdbuscpp2xml.exe
%{mingw32_bindir}/qdbusviewer.exe
%{mingw32_bindir}/qdbusxml2cpp.exe
%{mingw32_bindir}/qhelpconverter.exe
%{mingw32_bindir}/qhelpgenerator.exe
%{mingw32_bindir}/qmlplugindump.exe
%{mingw32_bindir}/qmlviewer.exe
%{mingw32_bindir}/qt3to4.exe
%{mingw32_bindir}/qttracereplay.exe
%{mingw32_bindir}/xmlpatterns.exe
%{mingw32_bindir}/xmlpatternsvalidator.exe
%dir %{mingw32_libdir}/qt4/plugins/designer/
%{mingw32_libdir}/qt4/plugins/designer/qaxwidget.dll
%{mingw32_libdir}/qt4/plugins/designer/qdeclarativeview.dll
%{mingw32_libdir}/qt4/plugins/designer/qdeclarativeviewd.dll
%{mingw32_libdir}/qt4/plugins/designer/qt3supportwidgets.dll
%{mingw32_libdir}/qt4/plugins/designer/qt3supportwidgetsd.dll
%{mingw32_libdir}/qt4/plugins/designer/qwebview.dll
%{mingw32_libdir}/qt4/plugins/designer/qwebviewd.dll

%files -n mingw32-qt-static
%{mingw32_libdir}/libQAxContainer4.a
%{mingw32_libdir}/libQAxServer4.a
%{mingw32_libdir}/libQt3Support4.a
%{mingw32_libdir}/libQtCLucene4.a
%{mingw32_libdir}/libQtCore4.a
%{mingw32_libdir}/libQtDBus4.a
%{mingw32_libdir}/libQtDeclarative4.a
%{mingw32_libdir}/libQtDesigner4.a
%{mingw32_libdir}/libQtDesignerComponents4.a
%{mingw32_libdir}/libQtGui4.a
%{mingw32_libdir}/libQtHelp4.a
%{mingw32_libdir}/libQtMultimedia4.a
%{mingw32_libdir}/libQtNetwork4.a
%{mingw32_libdir}/libQtOpenGL4.a
%{mingw32_libdir}/libQtScript4.a
%{mingw32_libdir}/libQtScriptTools4.a
%{mingw32_libdir}/libQtSql4.a
%{mingw32_libdir}/libQtSvg4.a
%{mingw32_libdir}/libQtTest4.a
%{mingw32_libdir}/libQtUiTools4.a
%{mingw32_libdir}/libQtXml4.a
%{mingw32_libdir}/libQtXmlPatterns4.a

# Win64
%files -n mingw64-qt
%{mingw64_bindir}/Qt3Support4.dll
%{mingw64_bindir}/Qt3Supportd4.dll
%{mingw64_bindir}/QtCLucene4.dll
%{mingw64_bindir}/QtCLucened4.dll
%{mingw64_bindir}/QtCore4.dll
%{mingw64_bindir}/QtCored4.dll
%{mingw64_bindir}/QtDBus4.dll
%{mingw64_bindir}/QtDBusd4.dll
%{mingw64_bindir}/QtDeclarative4.dll
%{mingw64_bindir}/QtDeclaratived4.dll
%{mingw64_bindir}/QtDesigner4.dll
%{mingw64_bindir}/QtDesignerd4.dll
%{mingw64_bindir}/QtDesignerComponents4.dll
%{mingw64_bindir}/QtDesignerComponentsd4.dll
%{mingw64_bindir}/QtGui4.dll
%{mingw64_bindir}/QtGuid4.dll
%{mingw64_bindir}/QtHelp4.dll
%{mingw64_bindir}/QtHelpd4.dll
%{mingw64_bindir}/QtNetwork4.dll
%{mingw64_bindir}/QtNetworkd4.dll
%{mingw64_bindir}/QtOpenGL4.dll
%{mingw64_bindir}/QtOpenGLd4.dll
%{mingw64_bindir}/QtScript4.dll
%{mingw64_bindir}/QtScriptd4.dll
%{mingw64_bindir}/QtScriptTools4.dll
%{mingw64_bindir}/QtScriptToolsd4.dll
%{mingw64_bindir}/QtSql4.dll
%{mingw64_bindir}/QtSqld4.dll
%{mingw64_bindir}/QtSvg4.dll
%{mingw64_bindir}/QtSvgd4.dll
%{mingw64_bindir}/QtUiTools4.dll
%{mingw64_bindir}/QtXml4.dll
%{mingw64_bindir}/QtXmld4.dll
%{mingw64_bindir}/QtXmlPatterns4.dll
%{mingw64_bindir}/QtXmlPatternsd4.dll
%{mingw64_bindir}/QtMultimedia4.dll
%{mingw64_bindir}/QtMultimediad4.dll
%{mingw64_bindir}/QtTest4.dll
%{mingw64_bindir}/QtTestd4.dll
%{mingw64_bindir}/QtWebKit4.dll
%{mingw64_bindir}/QtWebKitd4.dll
%{mingw64_libdir}/libQt3Support4.dll.a
%{mingw64_libdir}/libQt3Supportd4.dll.a
%{mingw64_libdir}/libQtCLucene4.dll.a
%{mingw64_libdir}/libQtCLucened4.dll.a
%{mingw64_libdir}/libQtCore4.dll.a
%{mingw64_libdir}/libQtCored4.dll.a
%{mingw64_libdir}/libQtDBus4.dll.a
%{mingw64_libdir}/libQtDBusd4.dll.a
%{mingw64_libdir}/libQtDeclarative4.dll.a
%{mingw64_libdir}/libQtDeclaratived4.dll.a
%{mingw64_libdir}/libQtDesigner4.dll.a
%{mingw64_libdir}/libQtDesignerd4.dll.a
%{mingw64_libdir}/libQtDesignerComponents4.dll.a
%{mingw64_libdir}/libQtDesignerComponentsd4.dll.a
%{mingw64_libdir}/libQtGui4.dll.a
%{mingw64_libdir}/libQtGuid4.dll.a
%{mingw64_libdir}/libQtHelp4.dll.a
%{mingw64_libdir}/libQtHelpd4.dll.a
%{mingw64_libdir}/libqtmain.a
%{mingw64_libdir}/libqtmaind.a
%{mingw64_libdir}/libqtmain4.a
%{mingw64_libdir}/libqtmaind4.a
%{mingw64_libdir}/libQtMultimedia4.dll.a
%{mingw64_libdir}/libQtMultimediad4.dll.a
%{mingw64_libdir}/libQtNetwork4.dll.a
%{mingw64_libdir}/libQtNetworkd4.dll.a
%{mingw64_libdir}/libQtOpenGL4.dll.a
%{mingw64_libdir}/libQtOpenGLd4.dll.a
%{mingw64_libdir}/libQtScript4.dll.a
%{mingw64_libdir}/libQtScriptd4.dll.a
%{mingw64_libdir}/libQtScriptTools4.dll.a
%{mingw64_libdir}/libQtScriptToolsd4.dll.a
%{mingw64_libdir}/libQtSql4.dll.a
%{mingw64_libdir}/libQtSqld4.dll.a
%{mingw64_libdir}/libQtSvg4.dll.a
%{mingw64_libdir}/libQtSvgd4.dll.a
%{mingw64_libdir}/libQtTest4.dll.a
%{mingw64_libdir}/libQtTestd4.dll.a
%{mingw64_libdir}/libQtUiTools4.dll.a
%{mingw64_libdir}/libQtUiToolsd4.dll.a
%{mingw64_libdir}/libQtWebKit4.dll.a
%{mingw64_libdir}/libQtWebKitd4.dll.a
%{mingw64_libdir}/libQtXml4.dll.a
%{mingw64_libdir}/libQtXmld4.dll.a
%{mingw64_libdir}/libQtXmlPatterns4.dll.a
%{mingw64_libdir}/libQtXmlPatternsd4.dll.a
%{mingw64_libdir}/pkgconfig/Qt3Support.pc
%{mingw64_libdir}/pkgconfig/Qt3Supportd.pc
%{mingw64_libdir}/pkgconfig/QtCLucene.pc
%{mingw64_libdir}/pkgconfig/QtCLucened.pc
%{mingw64_libdir}/pkgconfig/QtCore.pc
%{mingw64_libdir}/pkgconfig/QtCored.pc
%{mingw64_libdir}/pkgconfig/QtDBus.pc
%{mingw64_libdir}/pkgconfig/QtDBusd.pc
%{mingw64_libdir}/pkgconfig/QtDeclarative.pc
%{mingw64_libdir}/pkgconfig/QtDeclaratived.pc
%{mingw64_libdir}/pkgconfig/QtGui.pc
%{mingw64_libdir}/pkgconfig/QtGuid.pc
%{mingw64_libdir}/pkgconfig/QtHelp.pc
%{mingw64_libdir}/pkgconfig/QtHelpd.pc
%{mingw64_libdir}/pkgconfig/qtmain.pc
%{mingw64_libdir}/pkgconfig/qtmaind.pc
%{mingw64_libdir}/pkgconfig/QtMultimedia.pc
%{mingw64_libdir}/pkgconfig/QtMultimediad.pc
%{mingw64_libdir}/pkgconfig/QtNetwork.pc
%{mingw64_libdir}/pkgconfig/QtNetworkd.pc
%{mingw64_libdir}/pkgconfig/QtOpenGL.pc
%{mingw64_libdir}/pkgconfig/QtOpenGLd.pc
%{mingw64_libdir}/pkgconfig/QtScript.pc
%{mingw64_libdir}/pkgconfig/QtScriptd.pc
%{mingw64_libdir}/pkgconfig/QtScriptTools.pc
%{mingw64_libdir}/pkgconfig/QtScriptToolsd.pc
%{mingw64_libdir}/pkgconfig/QtSql.pc
%{mingw64_libdir}/pkgconfig/QtSqld.pc
%{mingw64_libdir}/pkgconfig/QtSvg.pc
%{mingw64_libdir}/pkgconfig/QtSvgd.pc
%{mingw64_libdir}/pkgconfig/QtTest.pc
%{mingw64_libdir}/pkgconfig/QtTestd.pc
%{mingw64_libdir}/pkgconfig/QtUiTools.pc
%{mingw64_libdir}/pkgconfig/QtUiToolsd.pc
%{mingw64_libdir}/pkgconfig/QtWebKit.pc
%{mingw64_libdir}/pkgconfig/QtWebKitd.pc
%{mingw64_libdir}/pkgconfig/QtXmlPatterns.pc
%{mingw64_libdir}/pkgconfig/QtXmlPatternsd.pc
%{mingw64_libdir}/pkgconfig/QtXml.pc
%{mingw64_libdir}/pkgconfig/QtXmld.pc
%dir %{mingw64_libdir}/qt4/
%dir %{mingw64_libdir}/qt4/plugins
%dir %{mingw64_libdir}/qt4/plugins/accessible
%{mingw64_libdir}/qt4/plugins/accessible/qtaccessiblecompatwidgets4.dll
%{mingw64_libdir}/qt4/plugins/accessible/qtaccessiblecompatwidgetsd4.dll
%{mingw64_libdir}/qt4/plugins/accessible/qtaccessiblewidgets4.dll
%{mingw64_libdir}/qt4/plugins/accessible/qtaccessiblewidgetsd4.dll
%dir %{mingw64_libdir}/qt4/plugins/bearer
%{mingw64_libdir}/qt4/plugins/bearer/qgenericbearer4.dll
%{mingw64_libdir}/qt4/plugins/bearer/qgenericbearerd4.dll
%{mingw64_libdir}/qt4/plugins/bearer/qnativewifibearer4.dll
%{mingw64_libdir}/qt4/plugins/bearer/qnativewifibearerd4.dll
%dir %{mingw64_libdir}/qt4/plugins/codecs
%{mingw64_libdir}/qt4/plugins/codecs/qcncodecs4.dll
%{mingw64_libdir}/qt4/plugins/codecs/qcncodecsd4.dll
%{mingw64_libdir}/qt4/plugins/codecs/qjpcodecs4.dll
%{mingw64_libdir}/qt4/plugins/codecs/qjpcodecsd4.dll
%{mingw64_libdir}/qt4/plugins/codecs/qkrcodecs4.dll
%{mingw64_libdir}/qt4/plugins/codecs/qkrcodecsd4.dll
%{mingw64_libdir}/qt4/plugins/codecs/qtwcodecs4.dll
%{mingw64_libdir}/qt4/plugins/codecs/qtwcodecsd4.dll
%dir %{mingw64_libdir}/qt4/plugins/graphicssystems
%{mingw64_libdir}/qt4/plugins/graphicssystems/qglgraphicssystem4.dll
%{mingw64_libdir}/qt4/plugins/graphicssystems/qglgraphicssystemd4.dll
%{mingw64_libdir}/qt4/plugins/graphicssystems/qtracegraphicssystem4.dll
%{mingw64_libdir}/qt4/plugins/graphicssystems/qtracegraphicssystemd4.dll
%dir %{mingw64_libdir}/qt4/plugins/iconengines
%{mingw64_libdir}/qt4/plugins/iconengines/qsvgicon4.dll
%{mingw64_libdir}/qt4/plugins/iconengines/qsvgicond4.dll
%dir %{mingw64_libdir}/qt4/plugins/imageformats
%{mingw64_libdir}/qt4/plugins/imageformats/qgif4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qgifd4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qico4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qicod4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qjpeg4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qjpegd4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qmng4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qmngd4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qsvg4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qsvgd4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qtiff4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qtiffd4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qtga4.dll
%{mingw64_libdir}/qt4/plugins/imageformats/qtgad4.dll
%dir %{mingw64_libdir}/qt4/plugins/qmltooling
%{mingw64_libdir}/qt4/plugins/qmltooling/qmldbg_inspector4.dll
%{mingw64_libdir}/qt4/plugins/qmltooling/qmldbg_inspectord4.dll
%{mingw64_libdir}/qt4/plugins/qmltooling/qmldbg_tcp4.dll
%{mingw64_libdir}/qt4/plugins/qmltooling/qmldbg_tcpd4.dll
%dir %{mingw64_libdir}/qt4/plugins/script
%{mingw64_libdir}/qt4/plugins/script/qtscriptdbus4.dll
%{mingw64_libdir}/qt4/plugins/script/qtscriptdbusd4.dll
%dir %{mingw64_libdir}/qt4/plugins/sqldrivers
%{mingw64_libdir}/qt4/plugins/sqldrivers/qsqlite4.dll
%{mingw64_libdir}/qt4/plugins/sqldrivers/qsqlited4.dll
%{mingw64_libdir}/qt4/plugins/sqldrivers/qsqlodbc4.dll
%{mingw64_libdir}/qt4/plugins/sqldrivers/qsqlodbcd4.dll
%{mingw64_includedir}/ActiveQt
%{mingw64_includedir}/Qt/
%{mingw64_includedir}/Qt3Support/
%{mingw64_includedir}/QtCore/
%{mingw64_includedir}/QtDBus
%{mingw64_includedir}/QtDeclarative/
%{mingw64_includedir}/QtDesigner/
%{mingw64_includedir}/QtGui/
%{mingw64_includedir}/QtHelp/
%{mingw64_includedir}/QtMultimedia/
%{mingw64_includedir}/QtNetwork/
%{mingw64_includedir}/QtOpenGL/
%{mingw64_includedir}/QtScript/
%{mingw64_includedir}/QtScriptTools/
%{mingw64_includedir}/QtSql/
%{mingw64_includedir}/QtSvg/
%{mingw64_includedir}/QtTest/
%{mingw64_includedir}/QtUiTools/
%{mingw64_includedir}/QtWebKit/
%{mingw64_includedir}/QtXml/
%{mingw64_includedir}/QtXmlPatterns/
%{mingw64_datadir}/qt4/

%files -n mingw64-qt-qmake
%doc LICENSE.GPL3 LICENSE.LGPL LGPL_EXCEPTION.txt README
%{_bindir}/%{mingw64_target}-lrelease
%{_bindir}/%{mingw64_target}-moc
%{_bindir}/%{mingw64_target}-qmake-qt4
%{_bindir}/%{mingw64_target}-rcc
%{_bindir}/%{mingw64_target}-uic
%{_bindir}/mingw64-qmake-qt4
%{_prefix}/%{mingw64_target}/bin/lrelease
%{_prefix}/%{mingw64_target}/bin/moc
%{_prefix}/%{mingw64_target}/bin/qmake-qt4
%{_prefix}/%{mingw64_target}/bin/rcc
%{_prefix}/%{mingw64_target}/bin/uic
%{mingw64_datadir}/qt4/mkspecs/%{platform_win64}

%files -n mingw64-qt-tools
%{mingw64_bindir}/assistant.exe
%{mingw64_bindir}/designer.exe
%{mingw64_bindir}/lconvert.exe
%{mingw64_bindir}/linguist.exe
%{mingw64_bindir}/lupdate.exe
%{mingw64_bindir}/pixeltool.exe
%{mingw64_bindir}/qcollectiongenerator.exe
%{mingw64_bindir}/qdbus.exe
%{mingw64_bindir}/qdbuscpp2xml.exe
%{mingw64_bindir}/qdbusviewer.exe
%{mingw64_bindir}/qdbusxml2cpp.exe
%{mingw64_bindir}/qhelpconverter.exe
%{mingw64_bindir}/qhelpgenerator.exe
%{mingw64_bindir}/qmlplugindump.exe
%{mingw64_bindir}/qmlviewer.exe
%{mingw64_bindir}/qt3to4.exe
%{mingw64_bindir}/qttracereplay.exe
%{mingw64_bindir}/xmlpatterns.exe
%{mingw64_bindir}/xmlpatternsvalidator.exe
%dir %{mingw64_libdir}/qt4/plugins/designer/
%{mingw64_libdir}/qt4/plugins/designer/qaxwidget.dll
%{mingw64_libdir}/qt4/plugins/designer/qdeclarativeview.dll
%{mingw64_libdir}/qt4/plugins/designer/qdeclarativeviewd.dll
%{mingw64_libdir}/qt4/plugins/designer/qt3supportwidgets.dll
%{mingw64_libdir}/qt4/plugins/designer/qt3supportwidgetsd.dll
%{mingw64_libdir}/qt4/plugins/designer/qwebview.dll
%{mingw64_libdir}/qt4/plugins/designer/qwebviewd.dll

%files -n mingw64-qt-static
%{mingw64_libdir}/libQAxContainer4.a
%{mingw64_libdir}/libQAxServer4.a
%{mingw64_libdir}/libQt3Support4.a
%{mingw64_libdir}/libQtCore4.a
%{mingw64_libdir}/libQtCLucene4.a
%{mingw64_libdir}/libQtDBus4.a
%{mingw64_libdir}/libQtDeclarative4.a
%{mingw64_libdir}/libQtDesigner4.a
%{mingw64_libdir}/libQtDesignerComponents4.a
%{mingw64_libdir}/libQtGui4.a
%{mingw64_libdir}/libQtHelp4.a
%{mingw64_libdir}/libQtMultimedia4.a
%{mingw64_libdir}/libQtNetwork4.a
%{mingw64_libdir}/libQtOpenGL4.a
%{mingw64_libdir}/libQtScript4.a
%{mingw64_libdir}/libQtScriptTools4.a
%{mingw64_libdir}/libQtSql4.a
%{mingw64_libdir}/libQtSvg4.a
%{mingw64_libdir}/libQtTest4.a
%{mingw64_libdir}/libQtUiTools4.a
%{mingw64_libdir}/libQtXml4.a
%{mingw64_libdir}/libQtXmlPatterns4.a


%changelog
* Sat May  7 2016 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.7-1
- Update to 4.8.7
- Fix FTBFS against GCC 6

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 4.8.6-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.6-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Apr 24 2015 Erik van Pienbroek <epienbro@fedorproject.org> - 4.8.6-8
- Fix CVE-2015-0295, CVE-2015-1860, CVE-2015-1859 and CVE-2015-1858

* Sat Mar 21 2015 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.6-7
- Fix FTBFS against latest mingw-dbus
- Fix FTBFS against gcc5

* Sun Nov 30 2014 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.8.6-6
- Ship translations

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.6-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Aug 02 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.6-4
- Rewritten the merge-static-and-shared patch
  Fixed FTBFS on environments where std::thread support is available

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.6-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Mon Jun  2 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.6-2
- Fix FTBFS against win-iconv 0.0.6

* Tue Apr 29 2014 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.6-1
- Update to 4.8.6
- Fix DoS vulnerability in the GIF image handler (QTBUG-38367)

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Sat Jul 13 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.5-3
- Rebuild against libpng 1.6

* Thu Jul  4 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.5-2
- When building static binaries, make sure the gcc argument -DQT_DLL isn't used

* Wed Jul  3 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.5-1
- Update to 4.8.5

* Sun Jun 16 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.4-6
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Sat Jun 15 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.4-5
- Rebuild to resolve InterlockedCompareExchange regression in mingw32 libraries

* Wed May 22 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.4-4
- When qmake .pro files contain 'TEMPLATE=lib' then the 'CONFIG+=shared'
  flag should be set automatically

* Sun Apr 14 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.4-3
- QSslSocket may report incorrect errors when certificate verification fails

* Sun Jan 27 2013 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.4-2
- Rebuild against mingw-gcc 4.8 (win64 uses SEH exceptions now)

* Thu Nov 29 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.4-1
- Update to 4.8.4

* Sun Nov  4 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.3-3
- Don't automatically strip debugging symbols from binaries created using qmake
  as we've got RPM wrapper strips to automatically split off debugging symbols
  to a separate debuginfo subpackage
- Make sure linking against the static QtUiTools library works out-of-the-box

* Sat Oct 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.3-2
- Added static libraries for QtCLucene, QtDesigner, QtHelp and QtUiTools
- Added various Requires tags to the -static subpackages as automatic
  dependency resolving doesn't work on static libraries
- Make sure the function qt_sendSpontaneousEvent is exported in the
  QtGui libraries as the ActiveQt component depends on it

* Fri Sep 14 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.3-1
- Update to 4.8.3

* Sat Aug 25 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.2-3
- Rebuild against latest libtiff

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May 23 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.2-1
- Update to 4.8.2
- Dropped upstreamed gcc 4.7 patch

* Sat May 19 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-5
- Add QMAKE_DLLTOOL to the mkspecs profiles

* Thu May 17 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-4
- Really fix the lrelease issue this time

* Thu May 17 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-3
- lrelease-qt4 tries to run qmake not qmake-qt4 (#820767)
  commit copied over from the native qt package

* Thu Apr 19 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-2
- Make linking against the static version of Qt work without any manual fiddling
- Remove -mms-bitfields from the win64 qmake.conf as it's unneeded with gcc 4.7

* Wed Mar 28 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.1-1
- Update to 4.8.1
- Removed a patch which fixed a compile failure in kdelibs as
  upstream has resolved the issue properly in commit 71e88dd
- Dropped upstreamed pkgconfig patches
- Workaround compile failure of the activeqt pieces (which are now enabled by
  default as of Qt 4.8.1). Thanks to the openSuSE mingw project for the patch

* Sat Mar 10 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-8
- Added win64 support

* Fri Mar 09 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-7
- Provide an arch-specific mingw32-qt-qmake package which contains
  tools like qmake and moc which are required for compiling binaries
  against Qt with the correct environment automatically set
- Bundle QtUiTools (required by kdelibs)
- Fix a compilation issue with kdelibs
- Make sure that Qt is built with IPC/shared memory support (required by kdelibs)
- Added -static subpackages
- Workaround a qmake issue which causes building against the debug binaries to fail:
  https://bugreports.qt.nokia.com/browse/QTBUG-14467
- Make sure the various tools belonging to the Qt library are built
  and added them to the new tools subpackage. Thanks to Dominik Schmidt
  of the openSuSE mingw project
- Make QSSL work (patch from Dominik Schmidt)
- Added pkg-config files (patches from Hib Eris)
- Enable javascript-jit
- Add QMAKE_STREAM_EDITOR to the mkspecs files
- Also install the Qt tools (qmake, moc, ...) to %%{_prefix}/$target/bin
  so that CMake can find Qt more easily

* Tue Mar 06 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-6
- Renamed the source package to mingw-qt (RHBZ #800447)
- Use mingw macros without leading underscore

* Tue Feb 28 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-5
- Rebuild against the mingw-w64 toolchain
- Made the qmake.conf compatible with mingw-w64

* Tue Jan 31 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-4
- Replaced the pkg-config environment hacks with a proper fix
  in the qmake.conf mkspecs file
- Rebuild against libpng 1.5

* Fri Jan 27 2012 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-3
- Fix compilation against gcc 4.7

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Dec 21 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.8.0-1
- Update to 4.8.0

* Wed Oct 26 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.8.0-0.2.rc1
- Rebuilt for glibc bug#747377

* Sat Oct 22 2011 Kalev Lember <kalevlember@gmail.com> - 4.8.0-0.1.rc1
- Update to 4.8.0 rc1

* Sat Sep  3 2011 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.4-1
- Update to 4.7.4

* Mon Aug 29 2011 Kalev Lember <kalevlember@gmail.com> - 4.7.3-2
- List individual dlls explicitly to avoid including .dll.debug files
  in the main package

* Sun Aug 28 2011 Kalev Lember <kalevlember@gmail.com> - 4.7.3-1
- Update to 4.7.3
- Dropped upstreamed / unneeded patches
- Enable the float.h using code again, needs new mingw32-runtime and
  mingw32-gcc builds

* Fri Jun 03 2011 Kalev Lember <kalev@smartlink.ee> - 4.7.1-6
- Rebuilt with mingw32-libjpeg-turbo, dropped jpeg_boolean patch (#604702)

* Fri Apr 22 2011 Kalev Lember <kalev@smartlink.ee> - 4.7.1-5
- Rebuilt for pseudo-reloc version mismatch (#698827)

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.7.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Dec 23 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.1-3
- Use the configure argument '-dbus-linked' instead of '-dbus' as the
  latter generates a non-working QtDBus library

* Mon Nov 15 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.1-2
- Add support for QtDBus

* Fri Nov 12 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.1-1
- Update to 4.7.1
- Use the name 'win32-g++-cross' instead of 'win32-g++-fedora-cross' as
  mkspecs platform name as was decided on the mailing list. The previous
  rename was invalid

* Mon Oct 11 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-2
- Use a more proper build method than the old hacky one
- Link against the mingw32 packages mingw32-zlib, mingw32-iconv, 
  mingw32-libjpeg, mingw32-libpng, mingw32-libtiff and mingw32-sqlite
  instead of using the bundled libraries
- Use the name 'win32-g++-fedora-cross' instead of 'win32-fedora-cross' as
  mkspecs platform name. People compiling Qt applications using the
  Fedora MinGW toolchain have to use this new name when invoking qmake
- Added the QtDeclarative library
- Bundle the translations
- Dropped the old obsoletes: mingw32-qt-win
- Dropped some duplicate declarations from the qmake.conf file
- Use the correct strip command in the qmake.conf file

* Sat Sep 25 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.7.0-1
- Update to 4.7.0
- Fixed a small rpmlint warning
- Added QtWebKit support
- Added SSL support

* Sun Jun 27 2010 Erik van Pienbroek <epienbro@fedoraproject.org> - 4.6.2-2
- Enable the 'windowsxp' and 'windowsvista' styles
- Fixed the %%defattr

* Fri Feb 26 2010 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.6.2-1
- update to 4.6.2

* Sun Jan 31 2010 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.6.1-1
- update to 4.6.1

* Tue Dec  1 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.6.0-1
- update to 4.6.0

* Sun Nov 22 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.6.0-0.1.rc1
- update to 4.6.0-rc1

* Mon Nov 16 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.6.0-0.1.beta1
- update to 4.6.0-beta1

* Tue Nov  3 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.3-3
- add links with version suffix for libqtmain{,d}.a

* Tue Nov  3 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.3-2
- fix R: qt-devel

* Sun Nov  1 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.3-1
- update to 4.5.3

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.5.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Jun 26 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.2-1
- update to 4.5.2

* Thu Jun 25 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.1-7
- hopefully finally solve the 32 vs 64 bit builder issues

* Mon Jun 22 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.1-6
- add debuginfo packages

* Tue Jun 16 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.1-5
- fix building on 64bit builders

* Fri Jun 12 2009 Richard W.M. Jones <rjones@redhat.com> - 4.5.1-4
- Update to Qt 4.5.1.
- Location of *.dll files moved again.
- No longer necessary to remove libdir/qt4/bin.
- Installs more *.dll files in /usr/lib [sic].

* Thu Apr 16 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.0-5
- replace %%define with %%global

* Tue Mar 31 2009 Kalev Lember <kalev@smartlink.ee> - 4.5.0-4
- Enable QtOpenGL, QtScript, QtScriptTools, and QtXmlPatterns.
- Sort files section for readability.

* Sun Mar 15 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.0-3
- moved cross compiler qmake setup files into separate package
  to keep this package noarch
- update BR, Provides, Obsoletes with reviewer suggestions

* Thu Mar 12 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.0-2
- enable debug libraries
- rename to mingw32-qt

* Thu Mar 12 2009 Thomas Sailer <t.sailer@alumni.ethz.ch> - 4.5.0-1
- update to Qt 4.5.0 (release)
- also build QtSvg, QtSql, Qt3Support

* Sat Feb 21 2009 Richard W.M. Jones <rjones@redhat.com> - 4.5.0-0.2.rc1
- Update to Qt 4.5.0-rc1.

* Fri Feb 20 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.3-4
- Rebuild for mingw32-gcc 4.4

* Fri Feb  6 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.3-3
- Fix required for older W32API in Fedora 10.

* Sun Feb  1 2009 Richard W.M. Jones <rjones@redhat.com> - 4.4.3-2
- Initial RPM release.
