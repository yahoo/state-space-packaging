# This is a GNU -*- Makefile -*- and you will need at least GNU make-4, and maybe make-4.2.1
# Copyright 2019, Oath Inc.
# Licensed under the terms of the Apache-2.0 license. See LICENSE file in https://github.com/yahoo/state-space-packaging/blob/master/LICENSE for terms.
default:
UNREADY = \
  state-space-fabric-sdk-c++ \
  state-space-PrivacyChain-sdk-c++ \
  state-space-tooling \
  state-space-testing \
  $(end)
PACKAGES = \
  state-space-config-repo \
  $(end)
DIRECTORY.state-space-tooling              = $(nearby)/tooling
DIRECTORY.state-space-testing              = $(nearby)/testing
DIRECTORY.state-space-privacychain-sdk-c++ = $(nearby)/PrivacyChain-sdk-c++
DIRECTORY.state-space-fabric-sdk-c++       = $(nearby)/fabric-sdk-c++
DIRECTORY.state-space-config-repo          = ignore
include ../mk/rpmbuild/Makefrag

$(rpmdir)/$(state-space-config-repo.nvr.arch)/$(state-space-config-repo.nvr.arch.rpm) : $(sourcedir)/01.maximum-hammer.repo
$(sourcedir)/01.maximum-hammer.repo : $(sourcedir)/% : $(cwd/..)/repos/%
	install -c -m 444 $< $@
