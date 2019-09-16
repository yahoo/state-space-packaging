# This is an RPM specification file which is best treated as a -*- bash -*- script because the parts that matter are shell
# Copyright 2019, Oath Inc.
# Licensed under the terms of the Apache-2.0 license.
# See the LICENSE file in https://github.com/yahoo/state-space-packaging/blob/master/LICENSE for terms.

# https://wiki.tunitas.technology/page/Libtool
# https://wiki.scold-lang.org/page/Libtool
# -all-static
#    If output-file is a library, then only create a static library. This flag cannot be used together with disable-static (see LT_INIT).
#    If output-file is a program, then do not link it against any shared libraries at all. 
# -static
#    If output-file is a library, then only create a static library.
#    If output-file is a program, then do not link it against any uninstalled shared libtool libraries. 
# -static-libtool-libs
#    If output-file is a library, then only create a static library.
#    If output-file is a program, then do not link it against any shared libtool libraries. 
#
# i.e. the 'without' are by default enabled
#      the 'with'    are by default disabled
#
%bcond_without static_libtool_libs

%global _prefix /opt/tunitas
%define modulesdir %{_prefix}/modules

%global series   state-space
%global reponame maximum-hammer
%global fullname Maximum Hammer, Release 01, of the State Space Solutions

%global pkglocalstatedir %{_localstatedir}/state-space

%global std_tunitas_prefix /opt/tunitas
%global std_scold_prefix   /opt/scold
%global std_hyperledger_fabric_prefix   /opt/hyperledger/fabric

#
# Dissection of the Name
#
#          /---------------------------------------- this package supplies a State Space-series repo
#          |
#          |         /------------------------------ supplies privacychain-sdk-c++
#          |         |
#          |         |
#          |         |
#          |         |
#          |         |
#          v         v
Name:      %{series}-privacychain-sdk-c++
Version:   0.0.0
Release:   1%{?dist}

# <tutorial ref="https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch-specfile-syntax.html" />
# <tutorial ref="http://www.rpm.org/max-rpm/s1-rpm-build-creating-spec-file.html" />
# <tutorial ref="https://fedoraproject.org/wiki/Packaging:DistTag" />
Summary: Hyperledger Fabric Client for the State Space Solutions
URL:     https://git.state-space.dev/core/PrivacyChain-sdk-c++
License: Apache-2.0
Distribution: State Space Solutions
Vendor: Verizon Media
#Packager: The Packager <state-space-packager@@verizonmedia.com>
Packager: Wendell Baker <wbaker@verizonmedia.com>
#
# Derivation:
# State Space Solutions is an application of Hyperledger Fabric
# Hyperledger Fabric is a database (a distributed database with a very quirky stored procedure system)
Group: Database/State Space

Source0: %{name}-%{version}.tar.gz

BuildRequires: temerarious-flagship >= 1.4.2

BuildRequires: automake, autoconf, libtool, make
# We're going to go as close to C++2a as the compiler will allow.
# So consider using gcc 9.1
BuildRequires: gcc-c++ >= 7.1.0
# But until ModulesTS is available S.C.O.L.D methodology is used.
# https://fedoraproject.org/wiki/Packaging:Guidelines#Rich.2FBoolean_dependencies
# http://rpm.org/user_doc/boolean_dependencies.html
BuildRequires: (SCOLD-DC or anguish-answer or baleful-ballad or ceremonial-contortion or demonstrable-deliciousness)

# WATCHOUT - the use of Release:6 in the NEVR = tunitas-basics-1.8.2-6 is critical
#            because it is only at Release:6 that the basics were built against nonstd-libhttpserver >= 0.9.0-7.1.ipv6+poll+regex+api
#            without that, it will build, but you will get duplicate-free on exit ... mixing is unworkable.
%define tunitas_basics_version 1.8.2-6
BuildRequires: tunitas-basics-devel >= %{tunitas_basics_version}
%if %{without static_libtool_libs}
Requires:      tunitas-basics >= %{tunitas_basics_version}
%endif

%define tunitas_butano_version 1.0.0
BuildRequires: tunitas-butano-devel >= %{tunitas_butano_version}
%if %{without static_libtool_libs}
Requires:      tunitas-butano >= %{tunitas_butano_version}
%endif

%define hyperledger_fabric_version 1.4.0
BuildRequires: hyperledger-fabric-devel >= %{hyperledger_fabric_version}
%if %{without static_libtool_libs}
Requires:      hyperledger-fabric >= %{hyperledger_fabric_version}
%endif

# the 'without' are by default enabled
# the 'with'    are by default disabled
%bcond_with nonstd_jsoncpp
%if %{with nonstd_jsoncpp}
# Generally this is not warranted after jsoncpp-devel-1.7 era
%define nonstd_jsoncpp_version 1.7
%define nonstd_jsoncpp_prefix /opt/nonstd/jsoncpp
BuildRequires: nonstd-jsoncpp-devel >= %{nonstd_jsoncpp_version}
%if %{without static_libtool_libs}
Requires:      nonstd-jsoncpp >= %{nonstd_jsoncpp_version}
%endif
%endif
# requires currency beyond 04.green-copper-heron
%define module_json_version 2:0.8.0
BuildRequires: module-json-devel >= %{module_json_version}
%if %{without static_libtool_libs}
Requires:      module-json >= %{module_json_version}
%endif

# requires currency beyond 04.green-copper-heron
%define module_nonstd_version 2:0.3.0
BuildRequires: module-nonstd-devel >= %{module_nonstd_version}
%if %{without static_libtool_libs}
Requires:      module-nonstd >= %{module_nonstd_version}
%endif

%define module_posix_version 2:0.27.0
BuildRequires: module-posix-devel >= %{module_posix_version}
%if %{without static_libtool_libs}
Requires:      module-posix >= %{module_posix_version}
%endif

# requires currency beyond 04.green-copper-heron
%define module_rabinpoly_version 2:0.2.0
BuildRequires: module-rabinpoly-devel >= %{module_rabinpoly_version}
%if %{without static_libtool_libs}
Requires:      module-rabinpoly >= %{module_rabinpoly_version}
%endif

%define module_std_version 2:0.27.0
BuildRequires: module-std-devel >= %{module_std_version}
%if %{without static_libtool_libs}
Requires:      module-std >= %{module_std_version}
%endif

%define module_c_string_version 0.12.0
%define module_string_version   0.13.1
BuildRequires: (module-c-string-devel >= %{module_string_version} or module-string-devel >= %{module_string_version})
%if %{without static_libtool_libs}
Requires:      (module-c-string >= %{module_string_version} or module-string >= %{module_string_version})
%endif

%define module_sys_version 2:0.27.0
BuildRequires: module-sys-devel >= %{module_sys_version}
%if %{without static_libtool_libs}
Requires:      module-sys >= %{module_sys_version}
%endif

# the 'without' are by default enabled
# the 'with'    are by default disabled
%bcond_without make_check
%if %{with make_check}
%define module_rigging_unit_version 0.8.1
%define module_rigging_version      2:0.10.0
BuildRequires: (module-unit-rigging-devel >= %{module_rigging_unit_version} or module-rigging-devel >= %{module_rigging_version})
%endif

%description
A C++ API for use with Hyperledger Fabric.  The implementation herein is optimized to perform with Hyperledger Fabric v1.4.

%package devel
Summary: The development components of the Tunitas Tarwater Identity Management System
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gcc-c++
Requires: module-nonstd-devel
Requires: module-posix-devel
Requires: module-std-devel
Requires: (module-c-string-devel >= %{module_string_version} or module-string-devel >= %{module_string_version})
Requires: module-sys-devel

%description devel
A C++ API for use with Hyperledger Fabric.

The S.C.O.L.D.-style modules of 'namespace hyperledger::PrivacyChain' are supplied.
These are "header files" and static & shared libraries.

%prep
%autosetup
make -i distclean >& /dev/null || : in case a devel tarball was used

%build
eval \
    prefix=%{_prefix} \
    with_temerarious_flagship=%{std_tunitas_prefix} \
    with_hypogeal_twilight=%{std_scold_prefix} \
    ./buildconf
%configure \
    --prefix=%{_prefix} \
    --with-std-scold=%{std_scold_prefix} \
    --with-std-tunitas=%{std_tunitas_prefix} \
    --with-temerarious-flagship=%{std_tunitas_prefix} --with-FIXTHIS=this_should_not_be_needed_the_std_tunitas_should_be_sufficient \
    ${end}
%make_build \
    %{?with_static_libtool_libs:LDFLAGS=-static-libtool-libs} \
    ${end}

%install
%make_install

%check
: nothing to check

%clean
: nothing clean

%files
%license LICENSE
%if %{without static_libtool_libs}
%{_libdir}/*.so.*
%endif

%files devel
%doc README.md
%{modulesdir}/*
# even if the executable is statically linked, the libraries are available for development (they will be static libraries)
%{_libdir}/*
%if %{with static_libtool_libs}
%exclude %{_libdir}/*.so.*
%endif
%exclude %{modulesdir}/want
%exclude %{modulesdir}/fpp/want
%exclude %{modulesdir}/hpp/want
%exclude %{modulesdir}/ipp/want

%pre
%post
%preun
%postun

%changelog
* Fri Sep 13 2019 Wendell Baker <wbaker@verizonmedia.com> - 0.0.0-1
- first packaging
