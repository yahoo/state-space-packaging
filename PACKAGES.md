Active work occurs on the branches corresponding to the "great release" events.
See branch [series/01.maximum-hammer](https://github.com/yahoo/state-space-packaging/tree/series/01.maximum-hammer)

# Required Packages

This document contains an estimate of the tools, components their versions which you will need to build the State Space repositories. This document describes the overall needs of the repositories in the projects. These are general instructions but are expected to be applicable to all of the repositories put together.

As this is the _packaging_ repository, it does not contain code directly, rather it contains configurations for building the deployable images.  These deployable images are, for this release, limited to RPM packages, which are expected to be delivered from a package manager such as DNF.

## State Space

The [hyperledger-fabric-sdk-c++](https://github.com/yahoo/hyperledger-fabric-sdk-c++) package is the earliest package in the dependency ordering among the State Space packages.  It depends directly upon Hyperledger Fabric, the compiler toolchain and the base operating system.

The lead repository for the State Space suite of services is [state-space-packaging](https://github.com/yahoo/state-space-packaging).

## Hyperledger Fabric

Hyperledger Fabric is published separately by the Hyperledger Foundation.  Its support system provides copious documentation and tutorials.  As such the presentation here is necessarily simplistic.

To set up the developmente environment for Hyperledger Fabric, you should refer to the [development environment instructions](https://hyperledger-fabric.readthedocs.io/en/release-1.4/dev-setup/devenv.html).

The dependencies documented therein are at least:
* Git
* Go  (Language)
* Docker
* Docker Compose
* LevelDB or CouchDB

You will need to acquire Hyperledger Fabric from among
* Pull the Docker images from the public repositories using the published instructions, such as [these](https://hyperledger-fabric.readthedocs.io/en/release-1.4/getting_started.html) or [these](https://openblockchain.readthedocs.io/en/latest/Setup/Network-setup).
* Install Hyperledger Fabric from pre-packaged repositories; see the [Availabilities](#availabilities) section below.
* Build from source so you control your software supply chain.

## Tunitas

* [tunitas-basics](https://github.com/yahoo/tunitas-basics) >= 2.0.0, common components of the Tunitas projects.
* [temerarious-flagship](https://github.com/yahoo/temerarious-flagship) >= 1.0.0, some build system components.

The lead repository for the Tunitas suite of services is [tunitas-packaging](https://github.com/yahoo/tunitas-packaging).

## Development Tooling

This is a C++ project.  The project approaches the upcoming C++20 standard, where available.

### C++ 20 (C++2b or C++23) Compiler
* `gcc-c++` >= 12, is preferred.
* `gcc-c++` >= 11.2, current.
* `gcc-c++` >= 10.2, feasible.
* `gcc-c++` >= 9.3, possible.
* gcc-c++ with [C++ Modules TS](https://gcc.gnu.org/wiki/cxx-modules).

### Build Support
* The [GNU Autotools](https://www.gnu.org/software/automake/manual/html_node/index.html#Top)
    * `automake` >= 1.16
    * `autoconf` >= 2.69
    * `libtool` >= 2.4
    * `make` >= 4.2
* The Tunitas Build System
    * [temerarious-flagship](https://github.com/yahoo/temerarious-flagship) >= 2.0.0, some build system components
* The [S.C.O.L.D.](https://www.scold-lang.org) [toolchain](https://git.scold-lang.org/core) and modules
    * [hypogeal-twilight](https://git.scold-lang.org/core/hypogeal-twilight) >= 0.45, fundamental build system components.
    * [incendiary-sophist](https://git.scold-lang.org/core/incendiary-sophist) >= 0.3, the test harness, is optional.
    * Any of the S.C.O.L.D. preprocessors towards a [unitary build](https://mesonbuild.com/Unity-builds.html).
        * Either [anguish-answer](https://git.scold-lang.org/core/anguish-answer) >= 2.0,
        * or equivalently [baleful-ballad](https://git.scold-lang.org/core/baleful-ballad) >= 1.0.
* `perl` prefer `perl` >= 5.28
    * and various perl modules, surely.

##  Components

This section enumerates is a best-estimate abstraction of the component dependencies for [Hyperledger Fabric SDK C++](https://github.com/yahoo/hyperledger-fabric-sdk-c++).  A master list of dependencies for the State Space reference implementation of the IAB PrivacyChain Technology Specification is with the [packaging](https://github.com/yahoo/state-space-packaging/blob/master/PACKAGES.md).

These packages are available via `dnf` or `yum`, if your machine is configured appropriately.

* `gcc-c++` >= 11.2
* `cppunit-devel` >= 1.14.0
* `jsoncpp-devel` >= 1.8.4

Modules: [json](https://git.scold-lang.org/modules/json), [nonstd](https://git.scold-lang.org/modules/nonstd), [posix](https://git.scold-lang.org/modules/posix), [std](https://git.scold-lang.org/modules/std), [string](https://git.scold-lang.org/modules/string), [sys](https://git.scold-lang.org/modules/sys); [cppunit](https://git.scold-lang.org/modules/cppunit), [rigging](https://git.scold-lang.org/modules/rigging).

See the `addenda` area of [tunitas-basics](https://github.com/yahoo/tunitas-basics) >= 2.0.

## Operating System

Development commenced on Fedora 27 and has continues on Fedora 35.

A recent Ubuntu should be fine.

## Availabilities

* [Fedora](https://getfedora.com)
    * Fedora 35, preferred.
    * Fedora 34, current.
    * Fedora 33, current.
    * ...backwards...
    * Fedora 27, possible.
* Hyperledger Fabric
    * <em>Release 04 (Bitter Vole)</em> contains <em>e.g.</em> `hyperledger-fabric-cluster-1.4.0-4.vzmf04.fc27.src.rpm`
    * <em>Release 03 (Furious Eagle)</em> unavailable (Hyperledger Fabric v1.3)
    * <em>Release 02 (Giddy Llama)</em> unavailable (Hyperledger Fabric v1.2)
    * <em>Release 01 (Heavy Fish)</em> use Docker (Hyperledger Fabric v1.1) supported Privacy Chain v1.0 <em>Release 01 (Worthy Cupboard)</em>
* [Tunitas](https://github.com/yahoo/tunitas-packaging/blob/master/README.md)
    * <em>Release 03 (Gnarled Manzanita)</em>, forthcoming, 2022ish.
    * <em>Release 02 (Towering Redwood)</em>, across 2020 & 2021.
    * <em>Release 01 (Famous Oak)</em>, original, 2019.
* [S.C.O.L.D. C++](https://www.scold-lang.org) (Scalable Object Location Disaggregation)
    * <em>Release 05, (Purple Tin Partridge)</em>, preferred.
    * <em>Release 04, (Green Copper Heron)</em>, current.
    * <em>Release 03, (Red Mercury Goose)</em>, possible.
    * <em>Release 02, (Maroon Iron Crow)</em>, maybe.
