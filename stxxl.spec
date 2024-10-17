%global debug_package %{nil}

%define major 1.4.1
%define libname %mklibname stxxl %{major}
%define devname %mklibname stxxl -d

Name: stxxl
Version: 1.4.1
Release: 3
Source0: https://downloads.sourceforge.net/project/stxxl/stxxl/%{version}/stxxl-%{version}.tar.gz
Patch0: stxxl-1.4.1-pthread-linkage.patch
Summary: Standard Template Library for Extra Large Data Sets
URL: https://stxxl.org/
License: Boost Software License 1.0 (MIT-like)
Group: System/Libraries
BuildRequires: cmake
BuildRequires: ninja

%description
The core of STXXL is an implementation of the C++ standard template
library STL for external memory (out-of-core) computations, i. e.,
STXXL implements containers and algorithms that can process huge
volumes of data that only fit on disks. While the closeness to the
STL supports ease of use and compatibility with existing
applications, another design priority is high performance.

The key features of STXXL are:
* Transparent support of parallel disks. The library provides
  implementations of basic parallel disk algorithms.
  STXXL is the only external memory algorithm library supporting
  parallel disks.
* The library is able to handle problems of very large size
  (tested to up to dozens of terabytes).
* Improved utilization of computer resources. STXXL implementations
  of external memory algorithms and data structures benefit from
  overlapping of I/O and computation.
* Small constant factors in I/O volume. A unique library feature
  called "pipelining" can save more than half the number of I/Os,
  by streaming data between algorithmic components, instead of
  temporarily storing them on disk. A development branch supports
  asynchronous execution of the algorithmic components, enabling
  high-level task parallelism.
* Shorter development times due to well known STL-compatible
  interfaces for external memory algorithms and data structures.
* STL algorithms can be directly applied to STXXL containers;
  moreover, the I/O complexity of the algorithms remains optimal
  in most of the cases.
* For internal computation, parallel algorithms from the MCSTL
  or the libstdc++ parallel mode are optionally utilized, making
  the algorithms inherently benefit from multi-core parallelism.
* STXXL is free, open source, and available under the Boost
  Software License 1.0.

%package -n %{libname}
Summary: Standard Template Library for Extra Large Data Sets
Group: System/Libraries

%description -n %{libname}
Standard Template Library for Extra Large Data Sets

%package -n %{devname}
Summary: Development files for %{name}
Group: Development/C
Requires: %{libname} = %{EVRD}

%description -n %{devname}
Development files (Headers etc.) for %{name}.

%prep
%setup -q
%autopatch -p1

%cmake -G Ninja \
	-DINSTALL_LIB_DIR=%{_libdir} \
	-DINSTALL_PKGCONFIG_DIR=%{_libdir}/pkgconfig \
	-DINSTALL_CMAKE_DIR=%{_libdir}/cmake/stxxl

%build
%ninja -C build

%install
%ninja_install -C build
sed -i -e '/^libdir=/d' %{buildroot}%{_libdir}/pkgconfig/*.pc

%files
%{_bindir}/stxxl_tool

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{devname}
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_libdir}/cmake/stxxl
