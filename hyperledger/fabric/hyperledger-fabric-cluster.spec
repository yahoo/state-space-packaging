# Copyright Yahoo Inc. 2021.
# Licensed under the terms of the Apache-2.0 license.
# See the LICENSE file in https://github.com/yahoo/state-space-packaging/blob/master/LICENSE for terms.

# Verizon (VZ) Media (VZM), Release 04 Bitter Vole
%global fabricate vzmf04
%global fabricate_dist %{?fabricate:.%{fabricate}}

# but could reasonably be unassigned (defaulting to /usr)
%global _prefix /opt/hyperledger/fabric

%define pkgconfdir       %{_sysconfdir}/hyperledger/fabric
%define pkgdatadir       %{_prefix}/hyperledger/fabric
%define pkgdatarootdir   %{pkgdatadir}
%define pkglocalstatedir %{_localstatedir}/hyperledger/fabric

# If these are linked from /usr/lib/systemd/system then the following "just works"
#  systemctl enable hyperledger-fabric-peer
#  systemctl enable hyperledger-fabric-orderer
%define pkgsystemdir     %{_prefix}/lib/systemd/system
%define truesystemdir    /usr/lib/systemd/system

Version: 1.4.0
Release: 4%{?fabricate_dist}%{?dist}
Name: hyperledger-fabric-cluster
Summary: The Hyperledger Fabric Cluster
License: Apache-2.0

URL: https://www.hyperledger.org/projects/fabric
Distribution: Yahoo FABRICating (YFABRIC)
Vendor: Yahoo Inc.
#Packager: That Certain Person <that@yahooinc.com>
Group:   Applications/Hyperledger

# Following https://github.com/InteractiveAdvertisingBureau/PrivacyChain/blob/master/build.md
# Reading https://github.com/InteractiveAdvertisingBureau/PrivacyChain/blob/master/docker/downloadFabricCommandPullFabricImages.sh
#
# ARCH=$(echo "$(uname -s|tr '[:upper:]' '[:lower:]'|sed 's/mingw64_nt.*/windows/')-$(uname -m | sed 's/x86_64/amd64/g')" | awk '{print tolower($0)}')
# VERSION=%%{version}
# BASE=hyperledger-fabric
# URL=https://nexus.hyperledger.org/content/repositories/releases/org/hyperledger/fabric/${BASE}/${ARCH}-${VERSION}/${BASE}-${ARCH}-${VERSION}.tar.gz
#
%global docker_tarball_arch    linux-amd64
%global docker_tarball_base    hyperledger-fabric
%global docker_tarball_version %{version}
%define docker_tarball_file    %{docker_tarball_base}-%{docker_tarball_arch}-%{docker_tarball_version}.tar.gz

# this is expected to be placed in %%{_sourcedir} manually or with a curl (wget) call
Source0: %{docker_tarball_file} 
Source1: hyperledger-fabric-orderer.service
Source2: hyperledger-fabric-peer.service

# Based on information, belief and lived experience
# https://hyperledger-fabric.readthedocs.io/en/latest/prereqs.html

Requires: curl
# though the documentation requires 1.11
Requires: golang >= 1.9
# absolutley not nodejs 9 it says
Requires: nodejs >= 8.11.4
# absolutely not python3 (it says)
Requires: python2 >= 2.7.13

Recommends: user-fabric
%description
Runtime executable, libraries, and configurations of the Hyperledger
Fabric.  The package is decontainerized.  You are expected to put these
components into your own container (Podman, Docker, LXC, KVM, etc.)

# Disable debuginfo package building
# You get debuginfo (sub-)packages by default,
# but from time to time you have to turn that off because the implementation is brittle.
#
# Such is indicated when there is no (outline) code, so there is no library, so there is no debug package
# and the debug symbol generation script kiddies cannot tolerate zero debug, as absent obj files.
#
# Ahem, or when dwz coredumps.  Witness below
#
# 2016-06, https://superuser.com/questions/1091529/rpm-build-error-empty-files-file-debugfiles-list, when?
# 2016-02-02, https://gnu.wildebeest.org/blog/mjw/2016/02/02/where-are-your-symbols-debuginfo-and-sources/
# 2012-06-13, https://fedoraproject.org/wiki/Packaging:Debuginfo?rd=Packaging/Debuginfo, undated
#
# 2018, nowadays, Fedora 27, as experienced, via rpm-4.14.0-2.fc27.x86_64
# seems to have a rudimentary switch in %%_enable_debug_packages...
#
#    %%install %%{?_enable_debug_packages:%%{?buildsubdir:%%{debug_package}}}\
#    %%%%install\
#    %%{nil}
#
# use %%undefine turn off enablement
# http://rpm.org/user_doc/macros.html
#
%global disable_debuginfo_packages \
%{!?_enable_debug_packages:%{expand:%%global debug_package %%{nil}}} \
%{?_enable_debug_packages:%{expand:%%undefine _debugsource_packages}} \
%{?_enable_debug_packages:%{expand:%%undefine _enable_debug_packages}} \
%{nil}

#
# Witness the chaos:
#
#   ...g info from /build/rpms/BUILDROOT/hyperledger-fabric-cluster-1.4.0-1.vzmf04.fc27.x86_64/opt/hyperledger/fabricate/bin/peer
#   extracting debug info from /build/rpms/BUILDROOT/hyperledger-fabric-cluster-1.4.0-1.vzmf04.fc27.x86_64/opt/hyperledger/fabricate/bin/configtxgen
#    dwz: dwz.c:1984: checksum_die: Assertion `((!op_multifile && !rd_multifile && !fi_multifile) || cu != die_cu (ref)) && (!op_multifile || cu->cu_chunk == die_cu (ref)->cu_chunk)' failed.
#   /usr/lib/rpm/find-debuginfo.sh: line 522: 26173 Aborted                 (core dumped) dwz $dwz_opts ${dwz_files[@]}
#   /usr/lib/rpm/sepdebugcrcfix: Updated 5 CRC32s, 0 CRC32s did match.
#
%disable_debuginfo_packages

%prep
# -c      create the directory
# -D      do not delete
# -T      do not to default behavior (and what is that?)
# -b $n   unpack, chdir
# -a $n   chdir, unpack
%setup -c -D -T -a 0

%build
# The components are already built, being just blobs off the net.

# Fix the paths within the published config files so it is always "hyperledger/fabric" everywhere.
# If we do this enough we will need a new Epoch to avoid stepping on "their" NVR rachet
sed -i -e 's,/var/hyperledger/production,/var/hyperledger/fabric/production,g' config/*.yaml

%check
# Nothing ot check

%install
# install -D is will make the target directory
# install -d is mkdir -p (does no installation)
for e in orderer peer configtxlator cryptogen configtxgen ; do
  install -D bin/$e %{buildroot}%{_bindir}/$e
done

# common config

install -D --mode=664 config/core.yaml %{buildroot}%{pkgconfdir}/core.yaml
install -D --mode=664 config/configtx.yaml %{buildroot}%{pkgconfdir}/configtx.yaml

# arguably, this does not belong on a peer
install -D --mode=664 config/orderer.yaml %{buildroot}%{pkgconfdir}/orderer.yaml

install -d %{buildroot}%{pkgsystemdir}
install -d %{buildroot}%{truesystemdir}

install -D --mode=664 %{_sourcedir}/hyperledger-fabric-orderer.service %{buildroot}%{pkgsystemdir}/hyperledger-fabric-orderer.service
install -D --mode=664 %{_sourcedir}/hyperledger-fabric-peer.service    %{buildroot}%{pkgsystemdir}/hyperledger-fabric-peer.service
if [ %{pkgsystemdir} != %{truesystemdir} ] ; then
    ln -s %{pkgsystemdir}/hyperledger-fabric-peer.service %{buildroot}%{truesystemdir}/hyperledger-fabric-peer.service
    ln -s %{pkgsystemdir}/hyperledger-fabric-orderer.service %{buildroot}%{truesystemdir}/hyperledger-fabric-orderer.service
fi

install -d --mode=555 %{buildroot}%{pkglocalstatedir}/peer
install -d --mode=555 %{buildroot}%{pkglocalstatedir}/orderer
install -d --mode=555 %{buildroot}%{pkglocalstatedir}/production

%files
# The install was to have defined the appropriate permissions; we want ownership by user fabric.
# and yet by default we also only want the fabric group to have access
%defattr(- fabric, fabric, 2770)

# Whereas we're shipping a de-containerized set of components
# NO ---> %%{_bindir}/get-docker-images.sh

# whereas this package owns the _bindir and all that goes in it
%{_bindir}

#
# From http://people.ds.cam.ac.uk/jw35/docs/rpm_config.html
#
# FFU = File From Update
# EF  = Edited File (already on the system)
#
# File marked as     Changed in    File on the system is
# marked as          update RPM?   untouched    edited
#
# [default]          No            FFU          FFU
#                    Yes           FFU          FFU
# %config            No            FFU          EF
#                    Yes           FFU          FFU, EF in .rpmsave
# %config(noreplace) No            FFU          EF
#                    Yes           FFU          EF, FFU in .rpmnew
#
%dir %{pkgconfdir}
%config(noreplace) %{pkgconfdir}/core.yaml
%config(noreplace) %{pkgconfdir}/orderer.yaml
%config(noreplace) %{pkgconfdir}/configtx.yaml

# by mentioning it  we ensure that it is fabric.fabric
%dir %{pkglocalstatedir}

# arguably this belongs only on the orderer
%dir %{pkglocalstatedir}/orderer

# arguably these only belong on a peer
%dir %{pkglocalstatedir}/peer
%dir %{pkglocalstatedir}/production

%{pkgsystemdir}/hyperledger-fabric-orderer.service
%{pkgsystemdir}/hyperledger-fabric-peer.service
%{truesystemdir}/hyperledger-fabric-peer.service
%{truesystemdir}/hyperledger-fabric-orderer.service

%changelog
# DO NOT use ISO-8601 dates; only use date +'%%a %%b %%d %%Y'

* Fri Mar 01 2019 - Wendell Baker <wbaker@verizonmedia.com> - 1.4.0-4.vzmf04
- package the systemd units, installed in %%{pkgsystemdir}

* Tue Jan 29 2019 - Wendell Baker <wbaker@verizonmedia.com> - 1.4.0-3.vzmf04
- use --mode to install files with the mode that is intended; *.yaml files are not executable

* Tue Jan 29 2019 - Wendell Baker <wbaker@verizonmedia.com> - 1.4.0-2.vzmf04
- ensure that pkglocalstatedir is owned fabric.fabric
- add the sgid bit on the pkglocalstate directories
- add the .../orderer directory
- _prefix was inadvertently .../fabricate not .../fabric
- Fix the paths within the published config files so it is always "hyperledger/fabric" everywhere.

* Thu Jan 17 2019 - Wendell Baker <wbaker@verizonmedia.com> - 1.4.0-1.vzmf04
- first packaging; expects user fabric.
