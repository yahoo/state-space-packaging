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

#
# [[FIXTHIS]] many of these southside schemes are not yet possible in state space (testing).
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
%warning DEBUG %{?with_nonstd_leveldb} %{?nonstd_leveldb_prefix}

#
# Dissection of the Name
#
#          /---------------------------------------- this package supplies a State Space-series repo
#          |
#          |         /------------------------------ supplies testing
#          |         |
#          |         |
#          |         |
#          |         |
#          |         |
#          v         v
Name:      %{series}-testing
Version:   0.0.0
Release:   1%{?dist}

# <tutorial ref="https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch-specfile-syntax.html" />
# <tutorial ref="http://www.rpm.org/max-rpm/s1-rpm-build-creating-spec-file.html" />
# <tutorial ref="https://fedoraproject.org/wiki/Packaging:DistTag" />
Summary: Operability testing for the State Space Solutions
URL:     https://git.state-space.dev/core/testing
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

Source0: %{name}-%{version}.tgz

BuildRequires: automake, autoconf, libtool, make
# We're going to go as close to C++2a as the compiler will allow.
# So consider using gcc 9.1
BuildRequires: gcc-c++ >= 7.1.0
# But until ModulesTS is available S.C.O.L.D methodology is used.
# https://fedoraproject.org/wiki/Packaging:Guidelines#Rich.2FBoolean_dependencies
# http://rpm.org/user_doc/boolean_dependencies.html
BuildRequires: (SCOLD-DC or anguish-answer or baleful-ballad or ceremonial-contortion or demonstrable-deliciousness)

BuildRequires: temerarious-flagship >= 1.4.2

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
# the nonstd prefix will need to be mentioned in the configuration step
%bcond_with nonstd_leveldb
%if %{with southside_leveldb}
%define module_leveldb_version 2:0.2.1
BuildRequires: module-leveldb-devel >= %{module_leveldb_version}
%if %{without static_libtool_libs}
Requires:      module-leveldb >= %{module_leveldb_version}
%endif
%endif


%description
The repository configuration for %{fullname}.

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
# 
%{__mkdir_p} %{buildroot}%{pkglocalstatedir}
#
# install -D is mkdir -p $(@D)
# install -d is mkdir -p everything
%{__install} -d %{buildroot}%{pkgsysconfdir}
%{__install} -D -m 444 %{_sourcedir}/01.maximum-hammer.repo %{buildroot}%{pkgsysconfdir}/.

%check
: nothing to check

%clean
: nothing clean

%files
%defattr(444,root,root,-)
%{pkgsysconfdir}

%pre
%post
%preun
%postun

%changelog
* Fri Sep 13 2019 Wendell Baker <wbaker@verizonmedia.com> - 0.0.0-1
- first packaging
