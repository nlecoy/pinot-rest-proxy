<br />
<p align="center">
  <h1 align="center">Pinot REST Proxy</h3>
  <p align="center">
    <a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square"></a>
    <a href="https://github.com/nlecoy/pinot-rest-proxy/issues"><img alt="Issues" src="https://img.shields.io/github/issues/nlecoy/pinot-rest-proxy.svg?style=flat-square"></a>
    <a href="https://github.com/nlecoy/pinot-rest-proxy/blob/master/LICENSE"><img alt="License" src="https://img.shields.io/github/license/nlecoy/pinot-rest-proxy.svg?style=flat-square"></a>
  </p>
  <p align="center">
    Simple REST service providing a convenient way for applications to query any Pinot table
    <br />
    <br />
    <a href="https://github.com/nlecoy/pinot-rest-proxy/issues/new?template=BUG_REPORT.md">Report Bug</a>
    ·
    <a href="https://github.com/nlecoy/pinot-rest-proxy/issues/new?template=FEATURE_REQUEST.md">Request Feature</a>
  </p>
</p>

## Table of Contents

- [Table of Contents](#table-of-contents)
- [About The Project](#about-the-project)
- [License](#license)

## About The Project

This project is inspired by the work done at Uber and presented in [this article](https://eng.uber.com/operating-apache-pinot/).


Most of the time, a Pinot table is associated with a tenant which has a unique set of brokers. Any client application must query one of these brokers in order to reach the specified table. This adds some complexity since the client applications need to be aware of the different tenants and brokers thereof. **Pinot REST Proxy** tries to solve this issue. Using this service, the client application can reach any one of the rest proxy nodes via its favorite load balancer. Each Pinot Rest Proxy instance locally caches the Pinot routing information (obtained via [Apache Helix](https://helix.apache.org/)). It uses this information to identify the tenant, identify the broker set, and route the client request to one of them in an asynchronous manner.

**This project is under development.**

## License

Distributed under the Apache-2.0 License. See [LICENSE](LICENSE) for more information.
