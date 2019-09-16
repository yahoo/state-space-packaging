# This is an RPM specification file which is best treated as a -*- bash -*- script because the parts that matter are shell
# Copyright 2019, Oath Inc.
# Licensed under the terms of the Apache-2.0 license.
# See the LICENSE file in https://github.com/yahoo/state-space-packaging/blob/master/LICENSE for terms.
#
%global series   state-space
%global reponame maximum-hammer
%global fullname Maximum Hammer, Release 01, of the State Space Solutions
#
# Dissection of the Name
#
#          /---------------------------------------- this package supplies a State Space-series repo
#          |
#          |         /------------------------------ supplies configuration elements
#          |         |
#          |         |      /----------------------- which herein is a repo (destined for yum.repos.d)
#          |         |      |
#          |         |      |    /------------------ this package supplies the repo of this name
#          |         |      |    |
#          |         |      |    |
#          v         v      v    v
#         %%{series}-config-repo-%%{reponame} <----- NO in this series the %%{reponame} does not appear in the package ENVR at all
Name:      %{series}-config-repo
Conflicts: foes-config-repo-%{series}-%{reponame}
#
# Version 1 is Release 01, which only applies because this is the repository configuration file package itself.
Version:   1.0.0
# reminder, you CANNOT put the %%{releasename} in Version or Release because it contains a '-' character
Release:   2%{?dist}

# dnf or yum?  it is /etc/dnf but /etc/yum.repos.d
%global pkglocalstatedir %{_localstatedir}/state-space
%global pkgsysconfdir %{_sysconfdir}/yum.repos.d

# <tutorial ref="https://docs.fedoraproject.org/en-US/Fedora_Draft_Documentation/0.1/html/RPM_Guide/ch-specfile-syntax.html" />
# <tutorial ref="http://www.rpm.org/max-rpm/s1-rpm-build-creating-spec-file.html" />
# <tutorial ref="https://fedoraproject.org/wiki/Packaging:DistTag" />
Summary: Configuration for DNF (YUM) for %{fullname}
URL:     https://%{reponame}.repos.state-space.dev
License: Apache-2.0
Distribution: State Space Solutions
Vendor: Verizon Media
#Packager: The Packager <state-space-packager@@verizonmedia.com>
Packager: Wendell Baker <wbaker@verizonmedia.com>
#
# State Space Solutions is an application of Hyperledger Fabric
# Hyperledger Fabric is a database (a distributed database with a very quirky stored procedure system)
Group: Database/State Space

# NOT A TARBALL ---> Source0: %%{name}-%%{version}.tgz <--- NOT A TARBALL
Source0: 01.maximum-hammer.repo

BuildArchitectures: noarch
%description
The repository configuration for %{fullname}.

%prep
# nothing to set up (no tarball) -- NO ---> %%autosetup <--- NO

%build
: nothing to build

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
* Thu Sep 12 2019 Wendell Baker <wbaker@verizonmedia.com> - 1.0.0-2
- more precise commentariat

* Thu Sep 12 2019 Wendell Baker <wbaker@verizonmedia.com> - 1.0.0-1
- first build packaging
