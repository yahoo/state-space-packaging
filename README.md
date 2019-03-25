# State Space, Packaging
This repository contains code to perform package production for the State Space implementation of the IAB PrivacyChain Reference Design.
The <em>Maximum Hammer</em> release 

![banner](logo.png)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)

More detailed information can be found at the following locations:
* IAB [PrivacyChain](https://github.com/InteractiveAdvertisingBureau/PrivacyChain)
** Specification Documents
** Runbooks, Operation Documents
** Project Governance Documents
** Reference Design
* State Space cluster of capabilities
** [Montara](https://github.com/yahoo/tunitas-montara), a "Northside" API Service.
** [Tooling](https://github.com/yahoo/statespace-tooling), Tooling.
** [Testing](https://github.com/yahoo/statespace-testing), Testing.
** [PrivacyChain C++](https://github.com/yahoo/PrivacyChain-sdk-cxx)
** [Hyperledger Fabric C++](https://github.com/yahoo/hyperledger-fabric-sdk-cxx)
* [Hyperledger Fabric](https://github.com/hyperledger/fabric)

## Table of Contents

- [Background](#background)
- [Install](#install)
- [Configuration](#configuration)
- [Build](#build)
- [Usage](#usage)
- [Security](#security)
- [Contribute](#contribute)
- [License](#license)

## Background

The IAB PrivacyChain system and the Hyperledger Fabric upon which the v0.0- and v1.0-series of PrivacyChain Reference Design is defined are envisioned to be deployed in a <em>cloud native</em> mode.  This can be by any of a number of methods in modern cloud operating systems: Open Container Initiative, Kubernetes and Docker.  The operation of a Hyperledger Fabric peer chaincode node requires an installation of Docker to run the chaincode within a container.

Neither the State Space implementation of the PrivacyChain reference design nor Hyperledger Fabric require any particular deployment channel.  This separable repository is provided to provide options for deployment beyond "manual build it; push it to the docker hub."

### Current
This project provides
* rpm-type packaging for Red Hat-based systems.

### Future
It is an open task to provide
* deb-type packaging for Debian-based systems (e.g. Ubuntu).
* other cloud-native image formats.

## Install

Install by running the following command.

```
git clone https://github.com/yahoo/statespace-packaging.git
```
This will create a directory called `statespace-packaging` and download the contents of this repo to it.

## Configuration

There is no configuration step.

## Build

Once you have installed the repo in your development area, you can assemble the packages.
The instructions here are based upon the RPM build flow that has been developed to date.

```
make -C hyperledger/fabric &&
make -C privacychain &&
echo OK DONE
```

## Usage

The result of the build step will result in a set of installable rpm packages.  These packages should be installed or copied to your organizatoin's DNF repository system for deployment.

For example, if you built rpms in `/build/rpms` and your nearby DNF repository is `/site/repos/maximum-hammer`:
```
cd /build/rpms/RPMS/*/*.rpm /build/rpms/SRPMS/*.rpm /site/repos/maximum-hammer/.
createrepo /site/repos/maximum-hammer
```

And then, for example:
```
sudo dnf install --refresh tunitas-montara statespace-tooling
```

## Security

This project does not have any specific security concerns.  As always, the integrity of the build process is a requirement for the integrity in the deployment and operations phases.

## Contribute

Please refer to [the contributing.md file](Contributing.md) for information about how to get involved. We welcome issues, questions, and pull requests. Pull Requests are welcome.

## Maintainers
Wendell Baker <wbaker@verizonmedia.com>

## License

This project is licensed under the terms of the [Apache 2.0](LICENSE-Apache-2.0) open source license. Please refer to [LICENSE](LICENSE) for the full terms.
