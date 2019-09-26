# This is a GNU -*- Makefile -*- and you will need at least GNU make-4, and maybe make-4.2.1
# Copyright 2019, Oath Inc.
# Licensed under the terms of the Apache-2.0 license. See LICENSE file in https://github.com/yahoo/state-space-packaging/blob/master/LICENSE for terms.
#
# Usage:
#
#   make [all]
#
#   make hyperledger-fabric-cluster
#
default:
notready = \
  hyperledger-fabric-ca \
  hyperledger-fabric-peer \
  hyperledger-fabric-orderer \
  $(end)
PACKAGES = \
  hyperledger-fabric-cluster \
  $(end)
# must match the definition within hyperledger-fabric-cluster.spec
hyperledger-fabric-cluster.nv.tarz = hyperledger-fabric-linux-amd64-1.1.0.tar.gz
DIRECTORY.hyperledger-fabric-cluster = ignore
include ../../mk/rpmbuild/Makefrag

HFC.lhs = $(specdir)/$(hyperledger-fabric-cluster.nv.spec)
HFC.rhs = $(sourcedir)/hyperledger-fabric-peer.service $(sourcedir)/hyperledger-fabric-orderer.service
$(HFC.lhs) : $(HFC.rhs)
$(HFC.rhs) : $(sourcedir)/% : systemd/%
	install -m 444 $< $@

