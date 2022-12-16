This project contains the packaging for the IAB PrivacyChain system and the Hyperledger Fabric upon which the v0.0- and v1.0-series of PrivacyChain is built.

# Introduction

A filesystem hierarchy standard defines components installed.  This allows both persons and computers to understand what to expect both from the underlying platform, describing the current system, but also where to place platform or application elements _in the future_.

The tenets outlined below follow the themes and concepts which are outlined in the [Linux Filesystem Hierarchy Standard 3.0](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0/index.html).  We have also tried to be faithful to the application layout decisions made by the underlying platforms (_e.g._ by [Hyperledger Fabric](https://gerrit.hyperledger.org/r/#/admin/projects/fabric).

# Naming Conventions

The naming convention outlined here pertains substantially to the packaging of PrivacyChain and Hyperledger Fabric.  Where other aspects of naming are described, they are incidental and provided for color & context.

## Available Conventions

| Convention | Applicable Where | Examples |
| --- | --- | --- |
| lower case | special-case of kebab-case | |
| [kebab-case](https://en.wikipedia.org/wiki/Letter_case#Special_case_styles)  | application artifacts | _files & directories |
| [snake_case](https://en.wikipedia.org/wiki/Snake_case) | is reserved to intra-application artifacts |  functions & namespaces |
| [CamelCase](https://en.wikipedia.org/wiki/Camel_case)  | same | Class and type objects |
| UPPER CASE | rare, for constants and WARNINGs |


## The Two Systems

There are two systems being delivered by the packaging herein.

### The _Hyperledger_ Honorific

The Hyperledger umbrella project of The Linux Foundation tends to keep the honorific _Hyperledger_ in front of all of the different sorts of hyperledger projects that they sponsor.  Indeed, all of the hyperledger projects share the same undifferentiated publication arena at [GitHub](https://github.com/hyperledger).  One could envision trading off one hyperledger technology for another depending upon the maturity, capability or feature-function affordances offered.  Today, PrivacyChain uses Hyperledger Fabric.  The filesystem hierarchy standard is faithful to the Hyperledger Project's use of the honorific _hyperledger_, thus preferring the term _Hyperledger Fabric_ over pure name _Fabric_ from the sponsors, IBM.   This is preference is reflected in filesystem naming conventions as well.

Examples of this in material form are the directories: <code>/etc/hyperledger/fabric</code>, or  <code>/opt/hyperledger/fabric</code>.

### The PrivacyChain Brand as Application Name

In contrast, the PrivacyChain, project does not have such a branded honorific.  The brand name is atomic.  Semanticists in the audience will note that the *privacy chain* is not about developing privacy, but rather about the recordation and publication of documentary artifacts in service of regulatory compliance globally.  The brands _PrivacyChain_ and _AudienceChain_ are used instead of these other more ponderous terms.

However, the convention in the Unix-type (_e.g._ Linux) systems upon which the PrivacyChain system will be deployed is to use lower case or [kebab-case](https://en.wikipedia.org/wiki/Letter_case#Special_case_styles) for application artifacts (_e.g._ files & directories).  The use of [snake case](https://en.wikipedia.org/wiki/Snake_case) or [CamelCase](https://en.wikipedia.org/wiki/Camel_case) is reserved to intra-application artifacts (_e.g._ programming language objects, configuration objects, _etc._).

Examples of this in material form are the directories: <code>/etc/privacychain</code>, or  <code>/opt/privacychain</code>.

# Containerization

The packaging and the filesystem hierarchy standard facilitates containerization by separating the system-independent and read-only filesystem elements, <em>e.g.</em> <code>&hellip;/bin</code></em>, <code>&hellip;/lib</code></em> and allies, from the system-dependent and instance-unique elements, <em>e.g.</em> <code>/etc</code>. Also segregated are the variable-sized storage areas which contain the data of the application, <em>e.g.</em> <code>/var</code>.  The [FHS](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0/index.html) elaborates these design decisions and the reasoning behind them.  They are recited here in limited form to provide context and where the usage here differs extends the standard.

# Nomenclature

The nomenclature from the GNU project is used where appropriate.
The nomenclature follows the underlying [FHS](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0/index.html), thus indicating a preferred variable name for each denoted filesystem element.
It is summarized here.

<!-- Says this is a table https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet -->

| Directory | Value | Scope & Purpose |
| --- | --- | --- |
| <code><b>prefix</b></code> | <code>/</code> | always (root), except for devel, test & in-situ installation  |
| <code><b>bindir</b></code> | <code>$(prefix)/bin</code> | contains executables |
| <code><b>sbindir</b></code> | <code>$(prefix)/sbin | not used |
| <code><b>libexecdir</b></code> | <code>$(prefix)/libexec</code> | not used, but prefer <code>$(pkglibexecdir)</code> |
| <code><b>_lib</b></code> | <code>lib</lib> or <code>lib64</code> as used by the operating sy stem |
| <code><b>libdir</b></code> | <code>$(prefix)/$(_lib)</lib>  | shared libraries & development components |
| <code><b>libarchdir</b></code> | <code>$(libdir)</code> | with the architecture honorific, if applicable |
| <code><b>libpuredir</b></code> | <code>$(prefix)/lib</code>s | without the architecture honorific |
| <code><b>sysconfdir</b></code> | <code>/etc</code> | the configuration area, system-dependent,  |
| <code><b>localstatedir</b></code> | <code>/var</code> | the variable-sized area, is read-write |
| --- | --- |
| <code><b>pkgsysconfdir</b></code> | <code>$(sysconfdir)/$(name)</code> | the application-specific configuration area, this is small and readonly |
| <code><b>pkglocalstatedir</b></code> | <code>$(localstatedir)/$(name)</code> | the applications's state, this can be written and may be large |
| <code><b>pkglibexecdir</b><code> | <code>$(libpuredir)/$(name)</code> | is preferred over the <code>libexec</code> particle, one level up |

# The Filesystem Hierarchy Standard

## Configuration ##

The configuration area contains 

| Path | Scope | Contains |
| --- | --- | --- |
| <code>/etc/hyperledger/fabric</code> | Hyperledger Fabric | directories <code>msp</code> and <code>tls</code> |
| <code>/etc/privacychain</code> | PrivacyChain | same |

## Installation Area ##

The application installation area is <code>/opt</code>.

| Path | Scope | Contains |
| --- | --- | --- |
| <code>/opt/hyperledger/fabric</code> | Hyperledger Fabric | configurations & certificates |
| <code>/opt/privacychain</code> | PrivacyChain | same |

## Data Storage ##

| Path | Scope | Contains |
| --- | --- | --- |
| <code>/var/hyperledger/fabric</code> | Hyperledger Fabric | blocks, and production |
| <code>/var/privacychain</code> | PrivacyChain | consent & data transfer records |

This is somewhat at variance with the [FHS](https://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0/index.html) which guides that application state should be in directories within <code>/var/lib</code>.  Our expectation, being as these are blockchain-based projects with potentially <em>unlimited</em> storage needs, that the application data directories will need to be served from storage systems that are strong enough to scale towards that infinite future.  Obviously that's a core problem in the blockchain concept itself; but until such time as this is resolved by technology, policy or fiat, the filesystem hierarchy will have to facilitate _very very large storage_  within the application design plan, <em>e.g.</em> [IPFS](https://ipfs.io/) or [Ceph](https://ceph.com/).

# The Great Packagers

## RPM Systems

This would be Fedora- and Red Hat- based systems.

## APT Systems

This would be distros like Ubuntu, Debian. As time and availability permit.
Perhaps _you_ would contribute here.?

## Other

This would likely be support for those who wish to develop & test on <em>other</em> gear.
Perhaps _you_ would contribute here.?

## None

Some installations wish to have their source code hooked up directly to production through a CI/CD process without an intervening packaging step.  This configuration is not uspported (yet, at this time).
Perhaps _you_ would contribute here.?

# References

* [Linux Filesystem Hierarchy Standard](http://refspecs.linuxfoundation.org/FHS_3.0/index.html), Version 3.0, Linux Foundation, since 2015-06-03 (think "is stable," not "is too old"); [pdf](http://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.pdf), [txt](http://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.txt), [html](http://refspecs.linuxfoundation.org/FHS_3.0/fhs-3.0.html).
* [IAB PrivacyChain Code Base](https://github.com/Interactive-Advertising-Bureau/PrivacyChain), a.k.a. "the code."

* [Variables for Installation Directories](https://www.gnu.org/prep/standards/html_node/Directory-Variables.html), In <em>GNU Coding Standard</em>, GNU Project, 2018-08-16.
* [Installation Directory Variables](https://www.gnu.org/software/autoconf/manual/autoconf-2.63/html_node/Installation-Directory-Variables.html), <em>Autoconf Manual</em>, GNU Project.
* [Where are files installed](https://www.sourceware.org/autobook/autobook/autobook_76.html), In <em>That Certain Autotools Book</em> (sic).
* [GNUInstallDirs](https://cmake.org/cmake/help/v3.9/module/GNUInstallDirs.html), Documentation for Cmake (here cited as) Version v3.9.

## Security

This repo offers packaging capabilities in support of the State Space reference implementation of the IAB PrivacyChain Technology Specification. As such, this project does not have any direct security concerns.

However, good source code supply chain management practices should be used when building and deploying this software.  This includes at least the use of a verified chain-of-custody build system from the git-managed sources through the use of signed packages and repositories in deployment.  The description of such methods are beyond the scope of this overview presentation.  The point is that as code is deployed, you should know what you have built and where you got the components that you are deploying.

# Contribute

Please refer to [contribution instructions](Contributing.md) for information about how to get involved. We welcome issues, questions, and pull requests. Pull Requests are welcome.

Current work with modern-generation tooling, <em>e.g.</em> circa Fedora 36+ and GCC 12+, is occurring around the <em>thematic</em> themed branches; <em>e.g.</em> 01.worthy-cupboard, 02.maximum-hammer and so forth.
# Maintainers
- Wendell Baker <wbaker@yahooinc.com>
- The State Space Team at Yahoo <state-space@yahooinc.com>
- <strike>The [IAB PrivacyChain Engineering Working Group](https://iabtechlab.com/working-groups/blockchain-working-group/)</strike> is no longer active.

You may contact us at least at <state-space@yahooinc.com>

# License

This project is licensed under the terms of the [Apache 2.0](LICENSE-Apache-2.0) open source license. Please refer to [LICENSE](LICENSE) for the full terms.
