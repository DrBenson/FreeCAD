# This package depends on automagic byte compilation
# https://fedoraproject.org/wiki/Changes/No_more_automagic_Python_bytecompilation_phase_3
%global py_bytecompile 1

# Setup python target for shiboken so the right cmake file is imported.
%global py_suffix %(%{__python3} -c "import sysconfig; print(sysconfig.get_config_var('SOABI'))")
%global pynum %(%{python3} -c "from sysconfig import get_python_version; print(get_python_version())")

# global py_suffix cpython-313-x86_64-linux-gnu
# Maintainers:  keep this list of plugins up to date
# List plugins in %%{_libdir}/%{name}/lib, less '.so' and 'Gui.so', here libOndselSolver
# unmark TestPathApp Raytracing ReverseEngineeringGui Image ImageGui RaytracingGui
%global plugins _PartDesign _TEMPLATE_ _TEMPLATE_Gui area Assembly AssemblyApp AssemblyGui CAMSimulator Cloud CloudGui DraftUtils Fem FemGui flatmesh FreeCAD Import ImportGui Inspection InspectionGui JtReader libarea-native libDriver libDriverDAT libDriverSTL libDriverUNV libE57Format libMEFISTO2 libfmt libNETGENPlugin libOndselSolver libSMDS libSMESH libSMESHDS libStdMeshers Material Materials MatGui Measure Mesh MeshGui MeshPart MeshPartGui Part PartDesignGui PartGui Path PathGui PathApp PathSimulator Points PointsGui QtUnitGui Raytracing RaytracingGui ReverseEngineering ReverseEngineeringGui Robot RobotGui Sketcher SketcherGui Spreadsheet SpreadsheetGui Start StartGui Surface SurfaceGui TechDraw TechDrawGui TestPathApp Web
#Sandbox Cloud CloudGui

#
#rm -rf build.log; rpmbuild -bb --nodebuginfo --noclean --with=fem_vtk FreeCAD.spec 1>>build.log 2>>build.log

# Some configuration options for other environments
# rpmbuild --with=bundled_zipios:  use bundled version of zipios++
%global bundled_zipios %{?_with_bundled_zipios: 1} %{?!_with_bundled_zipios: 1}
# rpmbuild --without=bundled_pycxx:  don't use bundled version of pycxx
%global bundled_pycxx %{?_without_bundled_pycxx: 0} %{?!_without_bundled_pycxx: 1}
# rpmbuild --without=bundled_smesh:  don't use bundled version of Salome's Mesh
%global bundled_smesh %{?_without_bundled_smesh: 0} %{?!_without_bundled_smesh: 1}
# rpmbuild --without=bundled_gtest:  don't use bundled version of gtest and gmock
%bcond_with bundled_gtest
# rpmbuild --with=fem_netgen:  don't use bundled version of Salome's Mesh
%global bundled_fem_netgen %{?_with_fem_netgen: 1} %{?!_with_fem_netgen: 0}
# rpmbuild --with=fem_vtk:  don't use bundled version of Salome's Mesh
%global bundled_fem_vtk %{?_with_fem_vtk: 1} %{?!_with_fem_vtk: 0}

# rpmbuild --without=tests   exclude tests in %%check
%bcond_without tests
# rpmbuild --without=debug_info don't generate package with debug info
%bcond_without debug_info


# Prevent RPM from doing its magical 'build' directory for now
%global __cmake_in_source_build 0

# See FreeCAD-master/src/3rdParty/salomesmesh/CMakeLists.txt to find this out.
%global bundled_smesh_version 7.7.1.0
# See /src/3rdParty/PyCXX/CXX/Version.h to find this out.
%global bundled_pycxx_version 7.1.11
# See /src/3rdParty/OndselSolver/CMakeLists.txt to find this out.
%global bundled_ondsel_solver_version 1.0.1

%global exported_libs libOndselSolver

## RPMAUTOSPEC: autorelease, autochangelog
%define autorelease(e:s:pb:n) %{?-p:0.}%{lua:
    release_number = 0;
    base_release_number = tonumber(rpm.expand("%{?-b*}%{!?-b:1}"));
    print(release_number + base_release_number - 1);
}%{?-e:.%{-e*}}%{?-s:.%{-s*}}%{!?-n:%{?dist}}
## END: Set by rpmautospec
# Some plugins go in the Mod folder instead of lib. Deal with those here:
%global mod_plugins Mod/PartDesign
%define name freecad
%define github_name FreeCAD
%define branch 1.1.1
%define rpmbranch 1.1.1
%define ReleaseNum %{git rev-list --count HEAD}
%define buildroot ~/rpmbuild/BUILDROOT
Name:                   %{name}
Epoch:                  0
Version:                %{rpmbranch}
# release=$(git rev-list --count HEAD)
Release:                %autorelease
#0{?dist}
Summary:                A general purpose 3D CAD modeler
Group:                  Applications/Engineering

License:                LGPLv2+
URL:                    http://www.freecad.org/
Source0:                https://github.com/DrBenson/FreeCAD/archive/FreeCAD-%{branch}.tar.gz
#Patch0:                PartFeature.patch
#Patch1:                PartFeatureH.patch

# Patch0:               FreeCAD.patch
# Utilities
# Utilities
# dnf install \
#Coin4-devel.x86_64 boost-devel.x86_64 boost-python3-devel eigen3-devel fmt-devel.x86_64 freeimage-devel.x86_64 gcc-gfortran.x86_64 \
#gmock-devel.x86_64 gtest-devel.x86_64 libXmu-devel.x86_64 libappstream-glib.x86_64 libglvnd-devel.x86_64 libkdtree++-devel libspnav-devel.x86_64 \
#med-devel.x86_64 mesa-libEGL-devel.x86_64 mesa-libGLU-devel.x86_64 netgen-mesher-devel.x86_64 netgen-mesher-devel-private.x86_64 opencascade-devel.x86_64 \
#openmpi-devel.x86_64 pcl-devel.x86_64 pyside6-tools.x86_64 python3-pybind11.x86_64 python3-pyside6-devel.x86_64 python3-shiboken6-devel.x86_64 \
#qt6-assistant.x86_64 qt6-designer.x86_64 qt6-qtbase-devel.x86_64 qt6-qtbase-private-devel.x86_64 qt6-qtsvg-devel.x86_64 qt6-qttools-devel.x86_64 \
#qt6-qttools-static.x86_64 qt6-qtwebengine-devel.x86_64 qt6-qtwebengine-devtools.x86_64 swig.x86_64 tbb-devel.x86_64 vtk-devel.x86_64 \
#xerces-c.x86_64 xerces-c-devel.x86_64 xorg-x11-server-Xvfb.x86_64 yaml-cpp-devel.x86_64 -y

BuildRequires:  cmake gcc-c++ gettext dos2unix
BuildRequires:  doxygen swig graphviz
BuildRequires:  gcc-gfortran
BuildRequires:  desktop-file-utils
BuildRequires:  git

BuildRequires:  tbb-devel
%if %{with tests}
BuildRequires:  xorg-x11-server-Xvfb python3-typing-extensions
%if %{without bundled_gtest}
BuildRequires: gtest-devel gmock-devel
%endif
%endif

# Development Libraries
BuildRequires:  freeimage-devel
BuildRequires:  libXmu-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  opencascade-devel
BuildRequires:  Coin4-devel
BuildRequires:  python3-devel
BuildRequires:  python3-matplotlib
BuildRequires:  python3-pivy
BuildRequires:  boost-devel
BuildRequires:  boost-python3-devel
BuildRequires:  eigen3-devel

BuildRequires:  fmt-devel


BuildRequires:  xerces-c
BuildRequires:  xerces-c-devel
BuildRequires:  libspnav-devel
%if ("%{pynum}" == "3.13") || ("%{pynum}" == "3.14")
BuildRequires: qt6-qtbase-devel
BuildRequires: qt6-qtbase-private-devel
BuildRequires: qt6-assistant
BuildRequires: qt6-designer
BuildRequires: qt6-qttools-devel
BuildRequires:  qt6-qtwebengine-devtools
BuildRequires:  qt6-qtwebengine-devel
BuildRequires:  qt6-qtsvg-devel
BuildRequires:  qt6-qttools-static
BuildRequires:  python3-shiboken6-devel
BuildRequires:  python3-pyside6-devel
BuildRequires:  pyside6-tools
%else
# Qt5 dependencies
BuildRequires:  qt5-qtwebengine-devel
BuildRequires:  qt5-qtsvg-devel
#BuildRequires:  qt5-qttools-static
#BuildRequires:  python3-shiboken2-devel
#BuildRequires:  python3-pyside2-devel
#BuildRequires:  pyside2-tools
#BuildRequires:  qt5-qtwebkit-devel
%endif
%if ! %{bundled_smesh}
BuildRequires:  smesh-devel
%endif
BuildRequires:  netgen-mesher-devel
BuildRequires:  netgen-mesher-devel-private
%if ! %{bundled_zipios}
BuildRequires:  zipios++-devel
%endif

%if ! %{bundled_pycxx}
BuildRequires:  python3-pycxx-devel
%endif
BuildRequires:  python3-pybind11
BuildRequires:  libicu-devel
BuildRequires:  vtk-devel
BuildRequires:  openmpi-devel
BuildRequires:  med-devel
BuildRequires:  libkdtree++-devel

BuildRequires:  pcl-devel
BuildRequires:  python3
BuildRequires:  libglvnd-devel
BuildRequires:  yaml-cpp-devel
#BuildRequires:  zlib-devel

# For appdata
%if 0%{?fedora}
BuildRequires:  libappstream-glib
%endif

# Packages separated because they are noarch, but not optional so require them
# here.
Requires:               %{name}-data = %{epoch}:%{version}-%{release}
# Obsolete old doc package since it's required for functionality.
Obsoletes:              %{name}-doc < 0.22-1
Requires:               hicolor-icon-theme

#Requires:              fmt

Requires:               python3-pivy
Requires:               python3-matplotlib
Requires:               python3-collada

%if ("%{py_suffix}" == "cpython-313-x86_64-linux-gnu") || ("%{py_suffix}" == "cpython-314-x86_64-linux-gnu")
Requires:               python3-pyside6
Requires:               qt6-assistant
%else
Requires:               python3-pyside6
Requires:               qt6-assistant
%endif

%if %{bundled_smesh}
Provides:               bundled(smesh) = %{bundled_smesh_version}
%endif
%if %{bundled_pycxx}
Provides:               bundled(python-pycxx)
%endif
Recommends:             python3-pysolar



# plugins and private shared libs in %%{_libdir}/freecad/lib are private;
# prevent private capabilities being advertised in Provides/Requires
%define plugin_regexp /^\\\(libFreeCAD.*%(for i in %{plugins}; do echo -n "\\\|$i\\\|$iGui"; done)\\\)\\\(\\\|Gui\\\)\\.so/d
%{?filter_setup:
%filter_provides_in %{_libdir}/%{name}/lib64
%filter_from_requires %{plugin_regexp}
%filter_from_provides %{plugin_regexp}
%filter_provides_in %{_libdir}/%{name}/Mod
%filter_requires_in %{_libdir}/%{name}/Mod
%filter_setup
}
# prevent private capabilities being advertised in Provides/Requires
%global plugin_exclude %( for i in %{plugins}; do  echo -n "\|$i\(Gui\)\?"; done )
# prevent declaring Requires for internal FreeCAD libraries
%global lib_exclude %( for i in %{exported_libs}; do echo -n "\|$i"; done )
%global __requires_exclude_from ^%{_libdir}/%{name}/(lib|Mod)/.*
%global __provides_exclude_from ^%{_libdir}/%{name}/Mod/.*
%global __provides_exclude ^(libFreeCAD.*%{plugin_exclude})\.so.*
%global __requires_exclude ^(libFreeCAD.*%{plugin_exclude}%{lib_exclude})\.so.*

%description
FreeCAD is a general purpose Open Source 3D CAD/MCAD/CAx/CAE/PLM modeler, aimed
directly at mechanical engineering and product design but also fits a wider
range of uses in engineering, such as architecture or other engineering
specialities. It is a feature-based parametric modeler with a modular software
architecture which makes it easy to provide additional functionality without
modifying the core system.


%package data
Summary:                Data files for FreeCAD
BuildArch:              noarch
Requires:               %{name} = %{epoch}:%{version}-%{release}

%description data
Data files for FreeCAD

%package libondselsolver-devel
Summary:        Development file for OndselSolver
BuildArch:      noarch
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description libondselsolver-devel
Development file for OndselSolver


#path that contain main FreeCAD sources for cmake
%global tests_resultdir %{_datadir}/%{name}/tests_result/%{_arch}

%if %{without debug_info}
%global debug_package %{nil}
%global _enable_debug_packages 0
%endif

%prep 1>>/dev/null 2>>/dev/null
%autosetup -N -p1 -n FreeCAD-%{rpmbranch}
# Remove bundled pycxx if we're not using it
#rsync -altp /media/ERP/sources/FreeCAD/src ./
#rsync -altp /media/ERP/sources/PRIVACY_POLICY.md ./
#patch --binary --force -r ./pd0 -N -p0 </media/UserTemp/Sources/conda/media/1.1.0/patch/110src-app.patch
#patch -r ./pd0 -N -p1 </media/UserTemp/Sources/conda/media/1.1.0/patch/110src-app.patch
echo "patch Done..."
rm -rf src/3rdParty/GSL src/3rdParty/OndselSolver src/3rdParty/tracy tests/lib src/Mod/AddonManager
git submodule add --force https://github.com/Ondsel-Development/OndselSolver.git src/3rdParty/OndselSolver
git submodule add --force https://github.com/google/googletest tests/lib
git submodule add --force https://github.com/microsoft/GSL src/3rdParty/GSL
#git submodule add --force https://github.com/wolfpld/tracy.git src/3rdParty/tracy
git submodule add --branch 1.1.0 --force https://github.com/DrBenson/FreeCAD_AddonManager.git src/Mod/AddonManager
#rsync -avltp /media/ERP/sources/FreeCAD/src .
#rsync -altp /media/UserTemp/Sources/conda/media/patch/src/ .
rsync -altp patch/src/ ./
rsync -altp patch/PRIVACY_POLICY.md .
#rsync -altp /media/ERP/sources/FreeCAD/LICENSE.html src/Doc/
find . -name \*.orig -delete -print
%if ! %{bundled_pycxx}
#rm -rf src/CXX
%endif

%if ! %{bundled_zipios}
#rm -rf src/zipios++
#sed -i "s/zipios-config.h/zipios-config.hpp/g" \
#       src/Base/Reader.cpp src/Base/Writer.h
%endif

# Fix encodings
# dos2unix -k src/Mod/Test/unittestgui.py

# Removed bundled libraries


%build
#cd FreeCAD-%{rpmbranch}
%define Release %{git rev-list --count HEAD}
#git submodule update --init --recursive
#git restore src/Doc/CONTRIBUTORS
sed -i 's/set(PACKAGE_VERSION_SUFFIX "rc1")/set(PACKAGE_VERSION_SUFFIX " ")/g' CMakeLists.txt
sed -i 's/set(PACKAGE_VERSION_SUFFIX "rc2")/set(PACKAGE_VERSION_SUFFIX " ")/g' CMakeLists.txt
sed -i 's/set(PACKAGE_VERSION_SUFFIX " rc1")/set(PACKAGE_VERSION_SUFFIX " ")/g' CMakeLists.txt
sed -i 's/set(PACKAGE_VERSION_SUFFIX " rc2")/set(PACKAGE_VERSION_SUFFIX " ")/g' CMakeLists.txt
sed -i 's/set(PACKAGE_VERSION_SUFFIX " RC1")/set(PACKAGE_VERSION_SUFFIX " ")/g' CMakeLists.txt
sed -i 's/set(PACKAGE_VERSION_SUFFIX " dev")/set(PACKAGE_VERSION_SUFFIX " ")/g' CMakeLists.txt
sed -i 's/set(PACKAGE_VERSION_SUFFIX "_QT5-dev")/set(PACKAGE_VERSION_SUFFIX " ")/g' CMakeLists.txt
#sed -i 's/Dion Moult (Moult)/Dion Moult (Moult)\n白鴻崇 (DrBenson)/g' src/Doc/CONTRIBUTORS
# Disable Boost search on Fedora-41
#sed -i 's/(BOOST_COMPONENTS program_options regex system thread date_time)/(BOOST_COMPONENTS filesystem program_options regex system thread date_time)/g' cMake/FreeCAD_Helpers/SetupBoost.cmake
#sed -i 's/SetupBoost()/#SetupBoost()/g' CMakeLists.txt
#sed -i 's/https:\/\/github.com\/fmtlib\/fmt\/archive\/refs\/tags\/9.1.0.zip/https:\/\/github.com\/fmtlib\/fmt\/archive\/refs\/tags\/11.0.2.zip/g' cMake/FreeCAD_Helpers/SetupLibFmt.cmake
# 11.1.4
#sed -i 's/e6754011ff56bfc37631fcc90961e377/90667b07f34d91554cf8285ae234ff66/g' cMake/FreeCAD_Helpers/SetupLibFmt.cmake
# 11.0.2
#sed -i 's/e6754011ff56bfc37631fcc90961e377/6e20923e12c4b78a99e528c802f459ef/g' cMake/FreeCAD_Helpers/SetupLibFmt.cmake
#sed -i 's/#!\/usr\/bin\/python/#!\/usr\/bin\/python3/g' src/Tools/freecad-thumbnailer.in
sed -i 's/#include "RowTypeMatrix.h"/#include "RowTypeMatrix.h"\n#include <cstdint>/g' src/3rdParty/OndselSolver/OndselSolver/FullMatrix.h
sed -i 's/#include "Solver.h"/#include "Solver.h"\n#include <cstdint>/g' src/3rdParty/OndselSolver/OndselSolver/NewtonRaphson.h

%if ("%{py_suffix}" == "cpython-314-x86_64-linux-gnu")
sed -i 's/SET(PYTHON_MAIN_DIR "\/usr\/lib\/python3.13\/site-packages")/SET(PYTHON_MAIN_DIR "\/usr\/lib64\/python3.14\/site-packages")/g' src/Ext/freecad/CMakeLists.txt
sed -i 's/SET(PYTHON_MAIN_DIR ${python_libs})/SET(PYTHON_MAIN_DIR "\/usr\/lib64\/python3.14\/site-packages")/g' src/Ext/freecad/CMakeLists.txt
%else
%if ("%{py_suffix}" == "cpython-313-x86_64-linux-gnu")
sed -i 's/SET(PYTHON_MAIN_DIR "\/usr\/lib\/python3.13\/site-packages")/SET(PYTHON_MAIN_DIR "\/usr\/lib64\/python3.13\/site-packages")/g' src/Ext/freecad/CMakeLists.txt
sed -i 's/SET(PYTHON_MAIN_DIR ${python_libs})/SET(PYTHON_MAIN_DIR "\/usr\/lib64\/python3.13\/site-packages")/g' src/Ext/freecad/CMakeLists.txt
%endif
%endif
#rm -rf build
mkdir -p build/_deps && cd build
#cp -r /media/Ext_Temp/sources/conda/fmt-src _deps/
#rsync -altp /media/Ext_Temp/sources/conda/fmt-subbuild _deps/
#cd ..

# Deal with cmake projects that tend to link excessively.
CXXFLAGS='-Wno-error=cast-function-type'; export CXXFLAGS
LDFLAGS='-Wl,--as-needed -Wl,--no-undefined '; export LDFLAGS
_PYSURFIX=${py_suffix}; export _PYSURFIX
QTv="6"

%if 0%{?fedora} > 27
%define MEDFILE_INCLUDE_DIRS %{_includedir}/med/
%else
%define MEDFILE_INCLUDE_DIRS %{_includedir}/
%endif

#               -DFREECAD_LIBPACK_USE=ON \
# for pyside6 add this line.
#               -DFORCE_LIMITED_API=no \
#               -DBUILD_QT6=ON \
# and for pyside2 use this
#               -DFORCE_LIMITED_API=ON \

#               -DQT_MAJOR_VERSION=6 \
#               -DFREECAD_QT_MAJOR_VERSION=6 \
#               -DFREECAD_QT_VERSION=6 \
#               -DQT_DEFAULT_MAJOR_VERSION=6 \
#               -DFREECAD_USE_EXTERNAL_FMT:BOOL=OFF \
#               -DCMAKE_INSTALL_PREFIX:FILEPATH=' {_libdir}/ {name}' \
#               -DSMESH_DIR=`pwd`/../cMake \
#               -DBUILD_TRACY_FRAME_PROFILER=ON \
#               -DRESOURCEDIR=%{_datadir}/%{name} \
%if ("$QTv" == "6")
%define QTver 6
%define Force_Lapi ON
%define PySide_ver 6
%else
%define QT 5
%define Force_Lapi TRUE
%define PySide_ver 2
%endif
%define QTver 6
%define Force_Lapi ON
%define PySide_ver 6
%if ("%{py_suffix}" == "cpython-314-x86_64-linux-gnu")
%define pythonexe_file = python3.14
%else
%if ("%{py_suffix}" == "cpython-313-x86_64-linux-gnu")
%define pythonexe_file = python3.13
%endif
%endif
%cmake \
        -DCMAKE_INSTALL_PREFIX:FILEPATH='%{_libdir}/%{name}' \
        -DCMAKE_INSTALL_DATADIR=%{_datadir}/%{name} \
        -DCMAKE_INSTALL_DOCDIR=%{_docdir}/%{name} \
        -DCMAKE_INSTALL_LIBDIR:PATH='%{_libdir}/%{name}/lib64' \
        -DCMAKE_INSTALL_INCLUDEDIR=%{_includedir} \
        -DLD_LIBRARY_PATH=/usr/lib64 \
        -DDEFAULT_QT_PLUGINS_DIR:FILEPATH='/usr/lib64/qt6/plugins' \
        -DDESIGNER_PLUGIN_LOCATION:FILEPATH='/usr/lib64/qt6/plugins/designer' \
        -DRESOURCEDIR=%{_datadir}/%{name} \
        -DBLAS=ON \
        -DBoost_DIR:PATH=/usr/lib64/cmake/Boost-1.83.0 \
        -Dboost_headers_DIR:PATH=/usr/lib64/cmake/boost_headers-1.83.0 \
        -DBoost_INCLUDE_DIR:PATH=/usr/include \
        -DBoost_USE_DEBUG_RUNTIME=OFF \
        -DBoost_USE_STATIC_LIBS=OFF \
        -DBUILD_DESIGNER_PLUGIN=TRUE \
        -DBUILD_FLAT_MESH=ON \
        -DBUILD_QT5=OFF \
        -DBUILD_QT6=ON \
        -DBUILD_SHIP:BOOL=OFF \
        -DBUILD_SMESH=OFF \
        -DBUILD_WITH_CONDA:BOOL=ON \
        -DBUILD_WITH_QT6=ON \
        -DCOIN3D_DOC_FOUND:BOOL=YES \
        -DCOIN3D_DOC_PATH=/usr/share/Coin4/html \
        -DCOIN3D_INCLUDE_DIRS=/usr/include/Coin4 \
        -DFORCE_LIMITED_API=1 \
        -DFREECAD_CREATE_MAC_APP=OFF \
        -DFREECAD_QT_MAJOR_VERSION=6 \
        -DFREECAD_QT_VERSION=6 \
        -DFREECAD_USE_3DCONNEXION=ON \
        -DFREECAD_USE_CCACHE=ON \
        -DFREECAD_USE_EXTERNAL_FMT:BOOL=ON \
        -DFREECAD_USE_EXTERNAL_KDL=OFF \
        -DFREECAD_USE_EXTERNAL_ONDSELSOLVER=OFF \
        -DFREECAD_USE_EXTERNAL_PIVY=ON \
        -DFREECAD_USE_EXTERNAL_SMESH=OFF \
        -DFREECAD_USE_EXTERNAL_ZIPIOS=OFF \
        -DFREECAD_USE_OCC_VARIANT='Official Version' \
        -DFREECAD_USE_PCL=OFF \
        -DFREECAD_USE_PYBIND11:BOOL=ON  \
        -DFREETYPE_INCLUDE_DIR_freetype2:PATH=/usr/include/freetype2 \
        -DFREETYPE_INCLUDE_DIR_ft2build:PATH=/usr/include/freetype2 \
        -DFREETYPE_INCLUDE_DIRS=/usr/include/freetype2 \
        -DFREETYPE_LIBRARY_RELEASE:FILEPATH=/usr/lib64/libfreetype.so \
        -DGIT_DISCOVERY_ACROSS_FILESYSTEM=TRUE \
        -DMEDFILE_INCLUDE_DIRS=%{MEDFILE_INCLUDE_DIRS} \
        -DOCCT_CMAKE_FALLBACK:BOOL=OFF \
        -DOpenGL_GL_PREFERENCE=GLVND \
        -Dpkgcfg_lib_PKG_FONTCONFIG_freetype:FILEPATH=/usr/lib64/libfreetype.so \
        -DPYSIDE_INCLUDE_DIR=/usr/include/PySide6 \
%if ("%{py_suffix}" == "cpython-314-x86_64-linux-gnu")
        -DPYSIDE_LIBRARY=/usr/lib64/libpyside6.cpython-314-x86_64-linux-gnu.so \
        -DPySide6_LIBRARIES=/usr/lib64/libpyside6.cpython-314-x86_64-linux-gnu.so \
        -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3.14 \
        -DPYTHON_EXECUTABLE=/usr/bin/python3.14 \
        -DPYTHON_INCLUDE_DIR=/usr/include/python3.14 \
        -DPYTHON_LIBRARY_DIRS='%{_libdir}/../lib64/python3.14' \
        -DPYTHON_LIBRARY='%{_libdir}/../lib64/libpython3.14.so' \
        -DPYTHON_MAIN_DIR:FILEPATH='%{_libdir}/../lib64/python3.14/site-packages' \
        -DPYTHON_PACKAGES_PATH='%{_libdir}/../lib64/python3.14/site-packages' \
        -DPYTHON_SUFFIX=.%{py_suffix} \
        -DPYTHON_VERSION_STRING=3.14 \
        -DPython3_EXECUTABLE:FILEPATH=/usr/bin/python3.14 \
        -DPython3_EXECUTABLE=/usr/bin/python3.14 \
        -DPython3_FIND_STRATEGY='%{_libdir}/../lib64/python3.14/site-packages' \
        -DPYTHON3_INCLUDE_DIR=/usr/include/python3.14 \
        -DPythonInterp=/usr/bin/python3.14 \
        -DPYTHONINTERP=/usr/bin/python3.14 \
        -DSHIBOKEN_LIBRARY=/usr/lib64/libshiboken6.cpython-314-x86_64-linux-gnu.so \
        -DShiboken6_LIBRARIES=/usr/lib64/libshiboken6.cpython-314-x86_64-linux-gnu.so \
%else
%if ("%{py_suffix}" == "cpython-313-x86_64-linux-gnu")
        -DPYSIDE_LIBRARY=/usr/lib64/libpyside6.cpython-313-x86_64-linux-gnu.so \
        -DPySide6_LIBRARIES=/usr/lib64/libpyside6.cpython-313-x86_64-linux-gnu.so \
        -DPYTHON_EXECUTABLE:FILEPATH=/usr/bin/python3.13 \
        -DPYTHON_EXECUTABLE=/usr/bin/python3.13 \
        -DPYTHON_INCLUDE_DIR=/usr/include/python3.13 \
        -DPYTHON_LIBRARY_DIRS='%{_libdir}/../lib64/python3.13' \
        -DPYTHON_LIBRARY='%{_libdir}/../lib64/libpython3.13.so' \
        -DPYTHON_MAIN_DIR:FILEPATH='%{_libdir}/../lib64/python3.13/site-packages' \
        -DPYTHON_PACKAGES_PATH='%{_libdir}/../lib64/python3.13/site-packages' \
        -DPYTHON_SUFFIX=.%{py_suffix} \
        -DPYTHON_VERSION_STRING=3.13 \
        -DPython3_EXECUTABLE:FILEPATH=/usr/bin/python3.13 \
        -DPython3_EXECUTABLE=/usr/bin/python3.13 \
        -DPython3_FIND_STRATEGY='%{_libdir}/../lib64/python3.13/site-packages' \
        -DPYTHON3_INCLUDE_DIR=/usr/include/python3.13 \
        -DPythonInterp=/usr/bin/python3.13 \
        -DPYTHONINTERP=/usr/bin/python3.13 \
        -DSHIBOKEN_LIBRARY=/usr/lib64/libshiboken6.cpython-313-x86_64-linux-gnu.so \
        -DShiboken6_LIBRARIES=/usr/lib64/libshiboken6.cpython-313-x86_64-linux-gnu.so \
%endif
%endif
        -DQT_DEFAULT_MAJOR_VERSION=6 \
        -DSHIBOKEN_INCLUDE_DIR=/usr/include/shiboken6 \
        -Dtiff_DIR=/usr/lib64 \
        -Dtiff_DIRS=/usr/lib64 \
        -Dtiff_INCLUDE_DIRS=/usr/include \
        -DUSE_CUDA=ON \
        -DUSE_OCC=ON \
        -DUSE_OPENCV=ON \
%if ! %{bundled_smesh}
        -DFREECAD_USE_EXTERNAL_SMESH=ON \
        -DSMESH_FOUND=TRUE \
        -DSMESH_INCLUDE_DIR=%{_includedir}/smesh \
        -DSMESH_DIR=`pwd`/../cMake \
%endif
%if ! %{bundled_zipios}
        -DFREECAD_USE_EXTERNAL_ZIPIOS=TRUE \
%endif
%if ! %{bundled_pycxx}
        -DPYCXX_INCLUDE_DIR=$(pkg-config --variable=includedir PyCXX) \
        -DPYCXX_SOURCE_DIR=$(pkg-config --variable=srcdir PyCXX) \
%endif
%if %{with tests}
        -DENABLE_DEVELOPER_TESTS=TRUE \
%if %{without bundled_gtest}
        -DFREECAD_USE_EXTERNAL_GTEST=TRUE \
%else
        -DINSTALL_GTEST=OFF \
        -DINSTALL_GMOCK=OFF \
%endif
%else
        -DENABLE_DEVELOPER_TESTS=FALSE \
%endif
        -DBUILD_ADDONMGR=ON \
        -DBUILD_ASSEMBLY=ON \
        -DBUILD_BIM=ON \
        -DBUILD_BIM_WITH_LARK=ON \
        -DBUILD_CAM=ON \
        -DBUILD_CLOUD=OFF \
        -DBUILD_DRAFT=ON \
        -DBUILD_DRAWING=OFF \
        -DBUILD_FEM=ON \
%if %{bundled_fem_netgen}
        -DNETGEN_INCLUDEDIR=/usr/include/netgen-mesher \
        -DNETGEN_INCLUDE_DIRS=/usr/include/netgen-mesher \
        -DNGLIB_INCLUDE_DIR=/usr/lib64/netgen-mesher \
        -DNGLIB_INCLUDE_DIRS=/usr/lib64/netgen-mesher \
        -DNETGEN_LIBDIR=/usr/lib64 \
        -DNGLIB_LIBRARIES=/usr/lib64/libnglib.so \
        -DBUILD_FEM_NETGEN=ON \
%endif
%if %{bundled_fem_vtk}
        -DNETGEN_INCLUDEDIR=/usr/include/netgen-mesher \
        -DNETGEN_INCLUDE_DIRS=/usr/include/netgen-mesher \
        -DNGLIB_INCLUDE_DIR=/usr/lib64/netgen-mesher \
        -DNGLIB_INCLUDE_DIRS=/usr/lib64/netgen-mesher \
        -DNETGEN_LIBDIR=/usr/lib64 \
        -DNGLIB_LIBRARIES=/usr/lib64/libnglib.so \
        -DBUILD_FEM_VTK=ON \
%endif
        -DONDSELSOLVER_BUILD_EXE=TRUE \
        -DBUILD_HELP=ON \
        -DBUILD_IDF=ON \
        -DBUILD_IMPORT=ON \
        -DBUILD_INSPECTION=ON \
        -DBUILD_JTREADER=ON \
        -DBUILD_MATERIAL=ON \
        -DBUILD_MATERIAL_EXTERNAL=ON \
        -DBUILD_MEASURE=ON \
        -DBUILD_MESH_PART=ON \
        -DBUILD_MESH=ON \
        -DBUILD_OPENSCAD=ON \
        -DBUILD_PART_DESIGN=ON \
        -DBUILD_PART=ON \
        -DBUILD_PATH=ON \
        -DBUILD_PLOT=ON \
        -DBUILD_POINTS=ON \
        -DBUILD_REVERSEENGINEERING=ON \
        -DBUILD_ROBOT=ON \
        -DBUILD_SANDBOX=OFF \
        -DBUILD_SHOW=ON \
        -DBUILD_SKETCHER=ON \
        -DBUILD_SPREADSHEET=ON \
        -DBUILD_START=ON \
        -DBUILD_SURFACE=ON \
        -DBUILD_TECHDRAW=ON \
        -DBUILD_TEMPLATE=ON \
        -DBUILD_TEMPLATEPY=OFF \
        -DBUILD_TEST=OFF \
        -DBUILD_TUX=ON \
        -DBUILD_WEB=ON \
        -DBUILD_GUI=ON \
        -DCMAKE_BUILD_TYPE=Release \
        -DENABLE_DEVELOPER_TESTS=OFF \
        -DPACKAGE_VERSION_SUFFIX=' QT6' \
        -DPACKAGE_WCREF='(Git: %{ReleaseNum})' \
        -DPACKAGE_WCURL='git://github.com/DrBenson/FreeCAD.git' \
        -DPACKAGE_VERSION_SUFFIX='_QT6 (Git:%{ReleaseNum})' \
        -Wno-dev \
        ../
#       cmake_build
#        -G Ninja \

make fc_version -k
for I in src/Build/Version.h src/Build/Version.h.out; do
        sed -i 's,FCRevision      \"Unknown\",FCRevision      \"(Git:%{ReleaseNum})\",' $I
        sed -i 's,FCRepositoryURL \"Unknown\",FCRepositoryURL \"git://github.com/DrBenson/FreeCAD.git 1.1.0\",' $I
done

%if ("%{py_suffix}" == "cpython-314-x86_64-linux-gnu")
        sed -i 's/SET(PYTHON_MAIN_DIR "\/usr\/lib\/python3.13\/site-packages")/SET(PYTHON_MAIN_DIR "\/usr\/lib64\/python3.14\/site-packages")/g' ../src/Ext/freecad/CMakeLists.txt
        sed -i 's/SET(PYTHON_MAIN_DIR ${python_libs})/SET(PYTHON_MAIN_DIR "\/usr\/lib64\/python3.14\/site-packages")/g' ../src/Ext/freecad/CMakeLists.txt
%else
        %if ("%{py_suffix}" == "cpython-313-x86_64-linux-gnu")
                sed -i 's/SET(PYTHON_MAIN_DIR "\/usr\/lib\/python3.13\/site-packages")/SET(PYTHON_MAIN_DIR "\/usr\/lib64\/python3.13\/site-packages")/g' ../src/Ext/freecad/CMakeLists.txt
                sed -i 's/SET(PYTHON_MAIN_DIR ${python_libs})/SET(PYTHON_MAIN_DIR "\/usr\/lib64\/python3.13\/site-packages")/g' ../src/Ext/freecad/CMakeLists.txt
        %endif
%endif

%{make_build}

%install
cd build
#export buildroot='~/rpmbuild/BUILDROOT/FreeCAD-1.0.0'
#echo buildroot='%{buildroot}'
#make install DESTDIR="~/rpmbuild/BUILDROOT" 'INSTALL=/usr/bin/install -p'
#cd FreeCAD-1.1.0/build
%make_install

# Symlink binaries to /usr/bin
mkdir -p %{buildroot}%{_bindir}
ln -s ../%{_lib}/%{name}/bin/FreeCAD %{buildroot}%{_bindir}/FreeCAD
ln -s ../%{_lib}/%{name}/bin/FreeCADCmd %{buildroot}%{_bindir}/FreeCADCmd
ln -s ../%{_lib}/%{name}/bin/FreeCAD %{buildroot}%{_bindir}/freecad
ln -s ../%{_lib}/%{name}/bin/FreeCADCmd %{buildroot}%{_bindir}/freecadcmd

mkdir -p %{buildroot}%{_metainfodir}/
mv %{buildroot}%{_libdir}/%{name}/share/metainfo/* %{buildroot}%{_metainfodir}/

mkdir -p %{buildroot}%{_datadir}/applications/
mv %{buildroot}%{_libdir}/%{name}/share/applications/* %{buildroot}%{_datadir}/applications/

mkdir -p %{buildroot}%{_datadir}/thumbnailers/
mv %{buildroot}%{_libdir}/%{name}/share/thumbnailers/* %{buildroot}%{_datadir}/thumbnailers/

mkdir -p %{buildroot}%{_datadir}/icons/hicolor/scalable/apps
#rsync -avltp /media/Ext_Temp/sources/conda/Image-Qt6/icons %{buildroot}%{_datadir}/
#mv --force %{buildroot}%{_libdir}/%{name}/share/icons/hicolor  %{buildroot}%{_datadir}/icons/

rsync -avltp %{buildroot}%{_libdir}/%{name}/share/* %{buildroot}%{_datadir}/
#rm -rf

#cp -R /home/Benson/rpmbuild/BUILD/freecad-1.1.0-build/FreeCAD-1.1.0/src/Mod/Material/Gui/Resources/ui %{buildroot}/usr/share/freecad/Mod/Material/Resources/
#rm -rf /home/Benson/rpmbuild/BUILD/freecad-1.0.0-build/BUILDROOT/home

mkdir -p %{buildroot}%{_datadir}/pixmaps/
mv %{buildroot}%{_libdir}/%{name}/share/pixmaps/* %{buildroot}%{_datadir}/pixmaps/

mkdir -p %{buildroot}%{_datadir}/mime/packages/
mv %{buildroot}%{_libdir}/%{name}/share/mime/packages/* %{buildroot}%{_datadir}/mime/packages/

#mkdir -p %{buildroot}%{_libdir}/../lib64/freecad/lib64
#mv  %{buildroot}%{_datadir}/%{name}/lib64 %{buildroot}%{_libdir}/%{name}/
#mv /home/Benson/rpmbuild/BUILD/freecad-1.0.0-build/BUILDROOT/usr/share/freecad/lib64 %{buildroot}%{_libdir}/%{name}/
#mv %{buildroot}%{_libdir}/%{name}/lib64 %{buildroot}%{_datadir}/%{name}/
cp -r %{buildroot}%{_libdir}/%{name}/Mod/Material/Resources/ui %{buildroot}%{_datadir}/%{name}/Mod/Material/Resources/
#mv %{buildroot}%{_libdir}/%{name}/Mod/_TEMPLATEPY_/Resources %{buildroot}%{_datadir}/%{name}/Mod/_TEMPLATEPY_/
%if ("%{py_suffix}" == "cpython-314-x86_64-linux-gnu")
mkdir -p %{buildroot}%{_libdir}/../lib64/python3.14/site-packages
%else
%if ("%{py_suffix}" == "cpython-313-x86_64-linux-gnu")
mkdir -p %{buildroot}%{_libdir}/../lib64/python3.13/site-packages
%endif
%endif
mv %{buildroot}%{_libdir}/../lib/python%{pynum}/site-packages/%{name} %{buildroot}%{_libdir}/../lib64/python%{pynum}/site-packages
# %{buildroot}%{_libdir}/../lib/python3.13 %{buildroot}%{_libdir}/%{name}/share
#rm -rf %{buildroot}%{_libdir}/../lib %{buildroot}%{_libdir}/../lib64/freecad/lib64 /home/Benson/rpmbuild/BUILD/freecad-1.0.0-build/BUILDROOT/usr/lib64/freecad
#rsync -altp /media/ERP/sources/FreeCAD/LICENSE.html %{buildroot}%{_docdir}/%{name}/LICENSE.html
rm -rf %{buildroot}%{_libdir}/../lib

pushd %{buildroot}%{_libdir}/%{name}/share/
rmdir metainfo/
rmdir applications/
rm -rf mime
rm -rf icons
popd

echo buildroot='%{buildroot}'

# Remove obsolete Start_Page.html
rm -f %{buildroot}%{_docdir}/%{name}/Start_Page.html
# Belongs in %%license not %%doc
#rm -f %{buildroot}%{_docdir}/freecad/ThirdPartyLibraries.html

# Remove header from external library that's erroneously installed
rm -f %{buildroot}%{_libdir}/%{name}/include/E57Format/E57Export.h
#rm -rf %{buildroot}%{_includedir}/OndselSolver/*
#rm -f %{buildroot}%{_libdir}/%{name}/share/pkgconfig/OndselSolver.pc
#rm -f %{buildroot}%{_datadir}/pkgconfig/OndselSolver.pc

#rsync -avltpu %{buildroot} ~/rpmbuild
# Bug maintainers to keep %%{plugins} macro up to date.
#
# Make sure there are no plugins that need to be added to plugins macro
new_plugins=`ls %{buildroot}%{_libdir}/../lib64/%{name}/lib64 | sed -e  '%{plugin_regexp}'`
if [ -n "$new_plugins" ]; then
        echo -e "\n\n\n**** ERROR:\n" \
                "\nPlugins not caught by regexp:  " $new_plugins \
                "\n\nPlugins in %{_libdir} do not exist in" \
                "\nspecfile %%{plugins} macro.  Please add these to" \
                "\n%%{plugins} macro at top of specfile and rebuild.\n****\n" 1>&2
#       exit 1
fi
# Make sure there are no entries in the plugins macro that don't match plugins
for p in %{plugins}; do
        if [ -z "`ls %{buildroot}%{_libdir}/%{name}/lib64/$p*.so`" ]; then
                set +x
                echo -e "\n\n\n**** ERROR:\n" \
                "\nExtra entry in %%{plugins} macro with no matching plugin:" \
                "'$p'.\n\nPlease remove from %%{plugins} macro at top of" \
                "\nspecfile and rebuild.\n****\n" 1>&2
#               exit 1
        fi
done

# Bytecompile Python modules
%if ("%{py_suffix}" == "cpython-314-x86_64-linux-gnu")
%py_byte_compile %{__python3} %{buildroot}%{_libdir}/python3.14/site-packages/%{name}
%else
%if ("%{py_suffix}" == "cpython-313-x86_64-linux-gnu")
%py_byte_compile %{__python3} %{buildroot}%{_libdir}/python3.13/site-packages/%{name}
%endif
%endif
# check
%if %{with tests}
    mkdir -p %{buildroot}%tests_resultdir
    if %ctest -E '^QuantitySpinBox_Tests_run$' &> %{buildroot}%tests_resultdir/ctest.result ; then
        echo "ctest OK"
    else
        echo "**** Failed ctest ****"
        touch %{buildroot}%tests_resultdir/ctest.failed
    fi

    if xvfb-run \%ctest -R '^QuantitySpinBox_Tests_run$' &>> %{buildroot}%tests_resultdir/ctest_gui.result ; then
        echo "ctest gui OK"
    else
        echo "**** Failed ctest gui ****"
        touch %{buildroot}%tests_resultdir/ctest_gui.failed
    fi
%endif

desktop-file-validate --no-hints \
    %{buildroot}%{_datadir}/applications/org.freecad.FreeCAD.desktop
appstream-util validate-relax --nonet \
    %{buildroot}%{_metainfodir}/*.metainfo.xml


%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%postun
if [ $1 -eq 0 ] ; then
        /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
        /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &> /dev/null || :
/usr/bin/update-mime-database %{_datadir}/mime &> /dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor/scalable/apps &>/dev/null || :

%files
%{_bindir}/*
%{_metainfodir}/*
%{_includedir}/*
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/bin/
%{_libdir}/%{name}/%{_lib}/
%{_libdir}/%{name}/Ext/
%{_libdir}/%{name}/Mod/
%{_libdir}/%{name}/share/
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*
%{_datadir}/pixmaps/*
%{_datadir}/mime/packages/*
%{_datadir}/thumbnailers/*
%{_libdir}/qt6/plugins/designer/*
%if %{with tests}
    %tests_resultdir/*
%endif
%if ("%{py_suffix}" == "cpython-314-x86_64-linux-gnu")
%{_libdir}/../lib64/python3.14/site-packages/%{name}
%else
%if ("%{py_suffix}" == "cpython-313-x86_64-linux-gnu")
%{_libdir}/../lib64/python3.13/site-packages/%{name}
%endif
%endif

%files data
%{_datadir}/%{name}/
%{_docdir}/%{name}/LICENSE.html
%{_docdir}/%{name}/ThirdPartyLibraries.html

%files libondselsolver-devel
    %{_datadir}/pkgconfig/OndselSolver.pc
    %{_includedir}/OndselSolver/*

%autochangelog
* Tue Apr 28 2026 DrBenson <Benson.Dr@GMail.com> - 0:1.1.1-0
- First Release 1.1.1
- Update Tranditional Chinese translation.

* Wed Apr 15 2026 DrBenson <Benson.Dr@GMail.com> - 1:1.1.0-5
- Release
- Update Tranditional Chinese translation.

* Tue Mar 24 2026 DrBenson <Benson.Dr@GMail.com> - 1:1.1.0-3
- Release RC3
- Update Tranditional Chinese translation.

* Mon Feb 02 2026 DrBenson <Benson.Dr@GMail.com> - 1:1.1.0-2
- Building with Qt6 and PySide6 on Fedora
- Update Tranditional Chinese translation.

* Sat Mar 22 2025 DrBenson <Benson.Dr@GMail.com> - 1:1.1.0-1
- Update Tranditional Chinese translation.

* Thu May 30 2024 DrBenson <Benson.Dr@GMail.com> - 1:0.22.0_pre
- Update Tranditional Chinese translation.

* Mon May 20 2024 DrBenson <Benson.Dr@GMail.com> - 1:0.22.0_pre
- Update Tranditional Chinese translation.

* Tue May 14 2024 DrBenson <Benson.Dr@GMail.com> - 1:0.22.0_pre
- Update Tranditional Chinese translation.

* Fri May 10 2024 DrBenson <Benson.Dr@GMail.com> - 1:0.22.0_pre
- Update Tranditional Chinese translation.

* Wed May 01 2024 DrBenson <Benson.Dr@GMail.com> - 1:0.22.0_pre
- Update Tranditional Chinese translation.

* Sun Nov 05 2023 DrBenson <Benson.Dr@GMail.com> - 1:0.22.0_dev
- Update Tranditional Chinese to latest translations development.

* Fri Oct 20 2023 DrBenson <Benson.Dr@GMail.com> - 1:0.22.0_dev
- Update Tranditional Chinese to latest translations development.
- Assembly: Fix locale log message for translation.
