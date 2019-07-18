# This is a GNU -*- Makefile -*- and you will need at least GNU make-4, and maybe make-4.2.1
# Copyright 2019, Oath Inc.
# Licensed under the terms of the Apache-2.0 license.
# See the LICENSE file in https://github.com/yahoo/state-space-packaging/blob/master/LICENSE for terms.
default:
PACKAGES = \
  privacychain-montara \
  $(end)
include ../../mk/rpmbuild/Makefrag
PACKAGES.deferred = \
  privacychain-mariadb \
  privacychain-api-javelin \
  privacychain-notification \
  $(end)
