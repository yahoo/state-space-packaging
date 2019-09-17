# This is an RPM specification file which is best treated as a -*- bash -*- script because the parts that matter are shell
# Copyright 2019, Oath Inc.
# Licensed under the terms of the Apache-2.0 license.
# See the LICENSE file in https://github.com/yahoo/state-space-packaging/blob/master/LICENSE for terms.

# https://wiki.tunitas.technology/page/Libtool
# https://wiki.scold-lang.org/page/Libtool
# -all-static
#    If the output-file is a library, then only create a static library. This flag cannot be used together with disable-static (see LT_INIT).
#    If the output-file is a program, then do not link it against any shared libraries at all. 
# -static
#    If the output-file is a library, then only create a static library.
#    If the output-file is a program, then do not link it against any uninstalled shared libtool libraries. 
# -static-libtool-libs
#    If the output-file is a library, then only create a static library.
#    If the output-file is a program, then do not link it against any shared libtool libraries. 
#
# i.e. the 'without' are by default enabled
#      the 'with'    are by default disabled
#
%bcond_without static_libtool_libs

%global _prefix /opt/state-space
%define modulesdir %{_prefix}/modules

%global series   state-space
%global reponame maximum-hammer
%global fullname Maximum Hammer, Release 01, of the State Space Solutions

%global pkglocalstatedir %{_localstatedir}/state-space

%global std_hyperledger_fabric_prefix /opt/hyperledger/fabric
%global std_scold_prefix              /opt/scold
%global std_state_space_prefix        /opt/state-space
%global std_tunitas_prefix            /opt/tunitas

#
# [[FIXTHIS]] many of these southside schemes are not yet possible in state space (tooling).
# All of these may be used simultaneously; they are further enabled at configure time.
# Build the service with 
# rpmbuild --with=NAME --with=NAME ...etc...
# mock --with=NAME --with=NAME ...etc...
#
#   --with=southside_fabric           The "southside" storage backend can be Hyperledger Fabric
#   --with=southside_leveldb          The southside can be  a filesystem-local LevelDB
#   --with=southside_sqlite           The southside can be  a filesystem-local SQLite
#   --with=southside_mysql            The southside can be a nearby MySQL
#   --with=southside_pgsql            The southside can be a nearby PostgreSQL (PgSQL)
#   --with=southside_ramcloud         The southside can be a nearby RAMCloud
#   --with=southside_scarpet          Tunitas has the DID Identity Systems (Hipster, Philosophical, Elemental, etc.)
#
# Recall (via /usr/lib/rpm/macros)
#
#    %%bcond_with foo       defines symbol with_foo if --with foo was specified on command line.
#    %%bcond_without foo    defines symbol with_foo if --without foo was *not* specified on command line.
#
# i.e. the 'without' are by default enabled
#      the 'with'    are by default disabled
#
%bcond_with    southside_fabric
%bcond_without southside_leveldb
%bcond_without southside_mysql
%bcond_with    southside_pgsql
%bcond_without southside_sqlite
%bcond_with    southside_ramcloud
%bcond_with    southside_scarpet

%if %{defined declare_nonstd_leveldb}
%declare_nonstd_leveldb
%else
# Whereas leveldb-1.20 sufficient and supplied since Fedora 28, we only handle exceptional ase as Fedora 27 & prior.
# 
# bcond_with    means you have to say --with=THING    to     get THING (default is without)
# bcond_without means you have to say --without=THING to NOT get THING (default is with)
#
%bcond_with nonstd_leveldb
%global nonstd_leveldb_prefix     /opt/nonstd/leveldb
%global nonstd_leveldb_includedir %{nonstd_leveldb_prefix}/include
%global nonstd_leveldb_libdir     %{nonstd_leveldb_prefix}/%{_lib}
%global leveldb_CPPFLAGS          %{?with_nonstd_leveldb:-I%{nonstd_leveldb_includedir}}
%global leveldb_CXXFLAGS          %{nil}
%global leveldb_LDFLAGS           %{?with_nonstd_leveldb:-L%{nonstd_leveldb_prefix}/%{_lib} -Wl,-rpath=%{nonstd_leveldb_prefix}/%{_lib}} -lleveldb
%global leveldb_package           %{?with_nonstd_leveldb:nonstd-leveldb}%{!?with_nonstd_leveldb:leveldb}
%global leveldb_package_devel     %{leveldb_package}-devel
%endif
%if %{without nonstd_leveldb}
# 
# testing:
#   rpmspec -q --define='%with_nonstd_leveldb 1' module-leveldb.spec 
# 
# Also, /opt/scold/libexec/vernacular-doggerel/extract-rpm-specfile-value
# will run rpmspec without any other arguments, so you cannot %%error here
#
# See below, you need at least leveldb-1.20 with the Fedora-specific API patches
%warning specifying nonstd_leveldb is required on Fedora 27 because there is no "standard" leveldb prior to Fedora 28
%endif

#
# Dissection of the Name
#
#          /---------------------------------------- this package supplies a State Space-series repo
#          |
#          |         /------------------------------ supplies tooling
#          |         |
#          |         |
#          |         |
#          |         |
#          |         |
#          v         v
Name:      %{series}-tooling
Version:   0.0.1
Release:   1%{?dist}

# <tutorial ref="https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch-specfile-syntax.html" />
# <tutorial ref="http://www.rpm.org/max-rpm/s1-rpm-build-creating-spec-file.html" />
# <tutorial ref="https://fedoraproject.org/wiki/Packaging:DistTag" />
Summary: Operability tooling for the State Space Solutions
URL:     https://git.state-space.dev/core/tooling
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
BuildRequires: hypogeal-twilight, incendiary-sophist >= 0.2.2

BuildRequires: automake, autoconf, libtool, make
# We're going to go as close to C++2a as the compiler will allow.
# So consider using gcc 9.1
BuildRequires: gcc-c++ >= 7.1.0
# But until ModulesTS is available S.C.O.L.D methodology is used.
# https://fedoraproject.org/wiki/Packaging:Guidelines#Rich.2FBoolean_dependencies
# http://rpm.org/user_doc/boolean_dependencies.html
BuildRequires: (SCOLD-DC or anguish-answer or baleful-ballad or ceremonial-contortion or demonstrable-deliciousness)

%define state_space_fabric_version 0.0.1
BuildRequires: state-space-fabric-sdk-c++-devel >= %{state_space_fabric_version}
%if %{without static_libtool_libs}
Requires:      state-space-fabric-sdk-c++ >= %{state_space_fabric_version}
%endif

%define state_space_privacychain_version 0.0.1
BuildRequires: state-space-privacychain-sdk-c++-devel >= %{state_space_privacychain_version}
%if %{without static_libtool_libs}
Requires:      state-space-privacychain-sdk-c++ >= %{state_space_privacychain_version}
%endif

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

# the 'without' are by default enabled
# the 'with'    are by default disabled
# the nonstd prefix will need to be mentioned in the configuration step
%bcond_with nonstd_leveldb
%if %{with southside_leveldb}
%define module_leveldb_version 2:0.2.1
BuildRequires: module-leveldb-devel >= %{module_leveldb_version}
%if %{without static_libtool_libs}
Requires:      module-leveldb >= %{module_leveldb_version}
%endif
%endif

# requires currency beyond 04.green-copper-heron
%define module_nonstd_version 2:0.3.0
BuildRequires: module-nonstd-devel >= %{module_nonstd_version}
%if %{without static_libtool_libs}
Requires:      module-nonstd >= %{module_nonstd_version}
%endif

%define module_options_version 0.14.0
BuildRequires: module-options-devel >= %{module_options_version}
%if %{without static_libtool_libs}
Requires:      module-options >= %{module_options_version}
%endif

# requires currency beyond 04.green-copper-heron
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

%define module_uuid_version 0.3.0
BuildRequires: module-uuid-devel >= %{module_uuid_version}
%if %{without static_libtool_libs}
Requires:      module-uuid >= %{module_uuid_version}
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
Operability tooling for the State Space Solutions configuration of the Hyperledger Fabric data base.

%package devel
Summary: The development components of the State Space Solutions operability tool suite
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: gcc-c++
%if %{with hyperleder_fabric}
Requires: hyperledger-fabric-devel
%endif
Requires: state-space-privacychain-sdk-c++-devel
Requires: state-space-fabric-sdk-c++-devel
Requires: tunitas-butano-devel
Requires: tunitas-basics-devel
Requires: module-json-devel
%if %{with southside_leveldb}
Requires: module-leveldb-devel
%endif
Requires: module-nonstd-devel
Requires: module-options-devel
Requires: module-posix-devel
Requires: module-rabinpoly-devel
Requires: module-std-devel
Requires: (module-c-string-devel or module-string-devel)
Requires: module-string-devel
Requires: module-sys-devel
Requires: module-uuid-devel
%if %{with nonstd_jsoncpp}
Requires: nonstd-jsoncpp-devel
%endif
%if %{with southside_leveldb}
%if %{with nonstd_leveldb}
Requires: nonstd-leveldb-devel
%endif
%endif

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
    --enable-FIXTHIS-when-it-exists-add-back__with-std-hyperledger-fabric=%{std_hyperledger_fabric_prefix} \
    --with-std-scold=%{std_scold_prefix} \
    --with-std-state-space=%{std_state_space_prefix} \
    --with-std-tunitas=%{std_tunitas_prefix} \
    --with-temerarious-flagship=%{std_tunitas_prefix} --with-FIXTHIS=this_should_not_be_needed_the_std_tunitas_should_be_sufficient \
    ${end}
# Build ID
#
# Folklore:
#   c2008 https://fedoraproject.org/wiki/Releases/FeatureBuildId
#   c2007 <broken>http://people.redhat.com/roland/build-id/</broken>
#   c200? <discursive>http://pkgbuild.sourceforge.net/spec-files.txt</discursive>, helpful but specific to Sun Microsystems.
#
# WATCHOUT - must pass --builtin directly to the linker
#            else g++: error: unrecognized command line option '--build-id'; did you mean '--builtin'?
# and --build-id gives sha1 of the build, --build-id=uuid merely generates an identifer
%global __build_id_LDFLAGS -Wl,--build-id
%make_build \
    LDFLAGS='%{__build_id_LDFLAGS} %{?with_static_libtool_libs: -static-libtool-libs}' \
    ${end}

%install
%make_install \
    LDFLAGS='%{__build_id_LDFLAGS} %{?with_static_libtool_libs: -static-libtool-libs}' \
    ${end}

%check
%make_build check

%clean
%make_build clean

%files
%defattr(444,root,root,-)
%license LICENSE
%{_bindir}/*
%if %{without static_libtool_libs}
%{_libdir}/*.so.*
%endif

%files devel
%doc README.md
%{modulesdir}/*
# even if the executable is statically linked, the libraries are available for development (they will be static libraries)
# reminder: the sst libraries are used in state-space-testing so you will need them even if the executables are linked -static-libtool-libs
%{_libdir}/*
%if %{without static_libtool_libs}
%exclude %{_libdir}/*.so.*
%endif
%exclude %{modulesdir}/want
%exclude %{modulesdir}/fpp/want
%exclude %{modulesdir}/hpp/want
%exclude %{modulesdir}/ipp/want

%pre
%post
# show that they function (enough DSO are installed)
%{_prefix}/bin/pcd --version
%{_prefix}/bin/pck --version
%{_prefix}/bin/pct --version

%preun
%postun

%changelog
* Tue Sep 17 2019 Wendell Baker <wbaker@verizonmedia.com> - 0.0.1-1
- package the executables
- build install with the deprecated BB_SOURCE_SET because that is the one that works
- align the --with-std-{hyperledger-fabric,scold,state-space,tunitas}=DIRECTORY options and the relevant rpm variables
- avoid --with-std-hyperledger-fabric because Release 01 (Maximum Hammer) is not ready for it yet

* Fri Sep 13 2019 Wendell Baker <wbaker@verizonmedia.com> - 0.0.0-1
- first packaging, a skeleton, does not package the project
