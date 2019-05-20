# State Space, Packaging
This repository contains code to perform package production for the State Space implementation of the IAB PrivacyChain Reference Design.

The current release is the <em>Maximum Hammer</em> release.

This is the main body of documentation for State Space reference implementation of the IAB PrivacyChain Technology Specification.  These are the authoritative documentation points among all of the repositories that comprise the the project.  Where documentation in the submodule packages conflicts with this package, we view that the the statements here are authoritative and supercede the submodule when the two are in conflict.

This repo supports the State Space reference implementation of the IAB PrivacyChain Technology Specification.

![banner](logo.png)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

More detailed information can be found at the following locations:
* IAB [PrivacyChain](https://github.com/InteractiveAdvertisingBureau/PrivacyChain)
** Specification Documents
** Runbooks, Operation Documents
** Project Governance Documents
** Reference Design
* State Space reference implemetnation of the IAB PrivacyChain Technology Specification
** [Packaging](https://github.com/yahoo/state-space-packaging), the packaging, the top-level repository.
** [Apanolio](https://github.com/yahoo/tunitas-apanolio), a "Northside" API Service, as a macroservice, in [Apache HTTPd](https://httpd.apache.org/).
** [Montara](https://github.com/yahoo/tunitas-montara), a "Northside" API Service, as a microservice.
** [Tooling](https://github.com/yahoo/state-space-tooling), some operability tooling.
** [Testing](https://github.com/yahoo/state-space-testing), some testing and performance assessments.
** [PrivacyChain C++](https://github.com/yahoo/PrivacyChain-sdk-cxx), part of the "Southside" service components.
** [Hyperledger Fabric C++](https://github.com/yahoo/hyperledger-fabric-sdk-cxx), part of the "Southside" service components.
* [Hyperledger Fabric](https://github.com/hyperledger/fabric), the upstream.

## Table of Contents

- [Background](#background)
- [Dependencies](#dependencies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Build](#build)
- [Usage](#usage)
- [Security](#security)
- [Contribute](#contribute)
- [License](#license)

## Background

The [IAB PrivacyChain](https://github.com/Interactive-Advertising-Bureau/PrivacyChain) provides an API service and a distributed, blockchain platform, based on a shared, immutable, distributed ledger (a database). This ledger (database) ensures that participants in a PrivacyChain have a single, consistent, up-to-date view to a consumers consent choices.  The system consists of two components, the "Northside" or "Northbound" service interface and the "Southside" or "Southbound" service interface.  This repository provides portions of the "Southbound" interface towards the Hyperledger Fabric database.

### Service Architecture

#### The "Northside" Services

The "Northside" Services or "Northbound" API offers a REST API to create, update and revoke consent records pertaining to a data subject.  The current generation of API is specified in [PC-11 REST API](https://github.com/InteractiveAdvertisingBureau/PrivacyChain/blob/master/design/PC-11_REST-API.md).

Examples of components implementing this interface are [Apanolio](https://github.com/yahoo/tunitas-apanolio) and [Montara](https://github.com/yahoo/tunitas-montara).

#### The "Southside" Service

The "Soutside Services" or "Southbound Interface" offers database access to a number of database technology.  The expected and preferred database technology, of course, is the distributed shared ledger database of the [Hyperledger Fabric](https://www.hyperledger.org/projects/fabric).

This repo provides a client library (a.k.a. a "software development kit") which implements the soutbound interface into Hyperledger Fabric.  It requires the [Hyperledger Fabric C++ SDK](https://github.com/yahoo/hyperledger-fabric-sdk-c++).  The components in this repository provide domain-specific interfaces to the underlying database. These features include schema versioning and evolution as well as the ability to process different consent representations.  The current consent representation is the [IAB Transparency and Consent Framework](https://github.com/InteractiveAdvertisingBureau/GDPR-Transparency-and-Consent-Framework) as encoded for [Version 1.1](https://github.com/InteractiveAdvertisingBureau/GDPR-Transparency-and-Consent-Framework/blob/master/Consent%20string%20and%20vendor%20list%20formats%20v1.1%20Final.md).

### Deployment

The IAB PrivacyChain system and the Hyperledger Fabric upon which the v0.0- and v1.0-series of PrivacyChain Reference Design is defined are envisioned to be deployed in a <em>cloud native</em> mode.  This can be by any of a number of methods in modern cloud operating systems: Open Container Initiative, Kubernetes and Docker.  The operation of a Hyperledger Fabric peer chaincode node requires an installation of Docker to run the chaincode within a container.

Beyond the specific requirements for operating a Hyperledger Fabric cluster, neither the State Space implementation of the PrivacyChain reference design nor Hyperledger Fabric require any particular deployment channel.  This separable repository is provided to provide options for deployment beyond "manual build it; push it to the docker hub."

#### Current
This project provides
* rpm-type packaging for Red Hat-based systems.

#### Future
It is an open task to provide
* deb-type packaging for Debian-based systems (<em>e.g.</em> Ubuntu).
* other cloud-native image formats.

## Dependencies

The [configuration](#configuration) step will check for many but not all required packages and operating system features.  There is a list of known [package-dependencies](https://github.com/yahoo/state-space-packaging/blob/master/PACKAGES.md) which you will need to install beyond your base operating system.

Generally, the dependencies are among:
- Hyperledger Fabric and allied components.
- A modern (C++2a) development environment.
- A recent Fedora, but any recent Linux distro should suffice.

The system was developed on Fedora 27 through Fedora 30 using GCC 7 and GCC 8 with `-fconcepts` and at least `-std=c++1z`.  More details on the required development environment, the C++ language policies, the build system and the deployment choices can be found in [temerarious-flagship](https://github.com/yahoo/temerarious-flagship/blob/master/README.md).

## Installation

### Installation from Sources

Install this repo and its dependents by running the following command.

``` bash
git clone https://github.com/yahoo/state-space-packaging.git
```

This will create a directory called `state-space-packaging` and download the contents of this repo to it.

### Installation a Deployment Channel

The result of the build step will result in a set of installable rpm packages.  These packages should be installed or copied to your organization's DNF repository system for deployment.  For example, if you built rpms in `/build/rpms` and your nearby DNF repository is `/site/repos/maximum-hammer` then the following will update the repository and install the newly-built components::

```
cd /build/rpms/RPMS/*/*.rpm /build/rpms/SRPMS/*.rpm /site/repos/maximum-hammer/.
createrepo /site/repos/maximum-hammer
```

And then, for example:

``` bash
sudo dnf install --refresh tunitas-apanolio tunitas-montara state-space-tooling
```

## Configuration

Upon first clone of the repository, the git submodules system must be initialized.
The command to run is `git submodule update --init`.  If your repo clone is at `/build/state-space/packaging` then should see something approximating the following:

``` bash
$ git submodule update --init
Submodule 'hyperledger/fabric' (ssh://EXAMPLE.HOSTNAME/repos/state-space/submodule-packaging-hyperledger-fabric.git) registered for path 'hyperledger/fabric'
Cloning into '/build/state-space/packaging/hyperledger/fabric'...
Submodule path 'hyperledger/fabric': checked out 'ca9fcc740e69533807c252fb73059e19e40d728e'
```

Of course the checksums may vary.  The `01.maximum-hammer` release of State Space PrivacyChain should be fixed to the `04.bitter-vole` branch of Hyperledger Fabric.  You should check this, as follows, before proceeding:

``` bash
# cd hyperledger/fabric
$ git branch -l
* 04.bitter-vole
  master
```

There is no other configuration step.

## Build

Once you have installed the repo in your development area, you can assemble the packages.
The instructions here are based upon the RPM build flow that has been developed to date.

``` bash
make -C hyperledger/fabric &&
make -C privacychain &&
echo OK DONE
```

## Usage

Once installed, you will need to enable services.
The steps involved are roughly

1. Establish a Public Key Infrastructure (PKI) design for your Hyperledger Fabric database sites.
2. Design and deploy Hyperledger Fabric database replicas
3. Instantiate database operations stored procedures (a.k.a. "the chaincode", "the smart contracts")
4. Configure and enable the Northface-/Southfacing- API services.
5. Profit!

### Steps 1-3: Setting up Hyperledger Fabric

Steps 1-3 are covered by existing tutorials and explainers.
They are not covered here.

### Step 4: Configure API Services

You will need to choose which API service you wish to use.  Designing a _cloud native_ or _container-based_ deployment scheme is beyond the scope here.

The following instructions pertain to systemd-maintained operating systems such as Fedora and Red Hat (RHEL).

#### Apanolio API Server

``` bash
systemd enable apanolio
systemd start apanolio
```

Detailed instructions for configuring Tunitas' Apanolio including security operations and database location specification can be found in the [tunitas-apanolio](https://github.com/yahoo/tunitas-apanolio) repository.

#### Montara API Server

``` bash
systemd enable montara
systemd start montara
```
Detailed instructions for configuring Tunitas' Montara including security operations and database location specification can be found in the [tunitas-montara](https://github.com/yahoo/tunitas-montara) repository.

## Security

This project does not have any specific security concerns.  As always, the integrity of the build process is a requirement for the integrity in the deployment and operations phases.

## Contribute

Please refer to [the contributing.md file](Contributing.md) for information about how to get involved. We welcome issues, questions, and pull requests. Pull Requests are welcome.

## Maintainers
- Wendell Baker <wbaker@verizonmedia.com>
- The State Space Team at Verizon Media.
- The IAB PrivacyChain Engineering Working Group.

You may contact us at least at <state-space@verizonmedia.com>

## License

This project is licensed under the terms of the [Apache 2.0](LICENSE-Apache-2.0) open source license. Please refer to [LICENSE](LICENSE) for the full terms.
