%define major 3
%define libname %mklibname %{name} %{major}
%define devname %mklibname %{name} -d

%define ver 3.0
%define rev 1270

Name:		assimp
Version:	%{ver}.%{rev}
Release:	1
Summary:	Library to import various 3D model formats into applications
Group:		Graphics
License:	BSD
URL:		http://assimp.sourceforge.net
Source0:	http://downloads.sourceforge.net/project/assimp/%{name}-%{ver}/%{name}--%{version}-source-only.zip

BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	pkgconfig(zlib)

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
%doc README LICENSE CREDITS CHANGES
%{_includedir}/%{name}
%{_libdir}/lib%{name}.so
%{_libdir}/cmake/%{name}-%{ver}
%{_libdir}/pkgconfig/%{name}.pc

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}--%{version}-source-only
sed -i s,"exec_prefix=.*","exec_prefix=%{_bindir}",g %{name}.pc.in
sed -i s,"libdir=.*","libdir=%{_libdir}",g %{name}.pc.in
sed -i s,"includedir=.*","includedir=%{_includedir}/%{name}",g %{name}.pc.in

%build
%cmake
%make

%install
%makeinstall_std -C build

