%define major 5
%define libname %mklibname %{name}
%define devname %mklibname %{name} -d

%global optflags %{optflags} -isystem %{_includedir}/minizip -Wno-error=unknown-warning-option -Wno-error=unused-but-set-variable

Name:		assimp
Version:	5.4.2
Release:	1
Summary:	Library to import various 3D model formats into applications
Group:		Graphics
License:	BSD
URL:		https://github.com/assimp/assimp
Source0:	https://github.com/assimp/assimp/archive/refs/tags/v%{version}.tar.gz

BuildRequires:	boost-devel
BuildRequires:	cmake ninja
BuildRequires:	pkgconfig(zlib)
BuildRequires:	pkgconfig(minizip)

%description
Assimp, the Open Asset Import Library, is a free library to import various
well-known 3D model formats into applications. Assimp aims to provide a full
asset conversion pipeline for use in game engines and real-time rendering
systems, but is not limited to these applications.

This package contains assimp binary, a tool to work with various formats.

%files
%{_bindir}/assimp
#----------------------------------------------------------------------------

%package -n %{libname}
Summary:	Library to import various 3D model formats into applications
Group:		System/Libraries

%description -n %{libname}
Assimp, the Open Asset Import Library, is a free library to import various
well-known 3D model formats into applications. Assimp aims to provide a full
asset conversion pipeline for use in game engines and real-time rendering
systems, but is not limited to these applications.

%files -n %{libname}
%{_libdir}/lib%{name}.so.%{major}*

#----------------------------------------------------------------------------

%package -n %{devname}
Summary:	Header files and libraries for assimp
Group:		Development/C++
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}

%description -n %{devname}
This package contains the header files and libraries for assimp.
You need to install it if you want to develop programs using assimp.

%files -n %{devname}
%doc LICENSE CREDITS CHANGES
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}-%(echo %{version}|cut -d. -f1-2)
%{_libdir}/pkgconfig/%{name}.pc

#----------------------------------------------------------------------------

%prep
%autosetup -p1

# Port to current minizip/zlib-ng
sed -i -e 's,uLong,unsigned long,g;s,voidpf,void*,g' code/Common/ZipArchiveIOSystem.cpp

sed -i s,"exec_prefix=.*","exec_prefix=%{_bindir}",g %{name}.pc.in
sed -i s,"libdir=.*","libdir=%{_libdir}",g %{name}.pc.in
sed -i s,"includedir=.*","includedir=%{_includedir}/%{name}",g %{name}.pc.in

%cmake \
	-DASSIMP_BUILD_ASSIMP_TOOLS:BOOL=ON \
	-DASSIMP_BUILD_ZLIB:BOOL=OFF \
	-G Ninja

%build
%ninja_build -C build

%install
%ninja_install -C build
