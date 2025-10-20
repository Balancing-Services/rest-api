# Changelog

All notable changes to the Balancing Services REST API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Official Python client library generated from OpenAPI specification

## [1.0.0] - 2025-10-20

### Added
- Initial public release of Balancing Services REST API specification
- Imbalance prices endpoint (`/imbalance/prices`)
- Imbalance total volumes endpoint (`/imbalance/total-volumes`)
- Balancing energy activated volumes endpoint (`/balancing/energy/activated-volumes`)
- Balancing energy prices endpoint (`/balancing/energy/prices`)
- Balancing energy bids endpoint (`/balancing/energy/bids`)
- Balancing capacity bids endpoint (`/balancing/capacity/bids`)
- Balancing capacity prices endpoint (`/balancing/capacity/prices`)
- Balancing capacity procured volumes endpoint (`/balancing/capacity/procured-volumes`)
- Support for 40+ European areas (AT, BE, BG, CH, CZ, DE, DK, EE, ES, FI, FR, GR, HR, HU, IT, LT, LV, NL, NO, PL, PT, RO, RS, SE, SI, SK)
- Cursor-based pagination for large result sets (bids endpoints)
- Bearer token authentication
- RFC 7807 Problem Details error handling
- Support for multiple reserve types (FCR, aFRR, mFRR, RR)
- UTC timestamp-based period filtering
- OpenAPI 3.0.3 specification

[Unreleased]: https://github.com/balancing-services/rest-api/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/balancing-services/rest-api/releases/tag/v1.0.0
