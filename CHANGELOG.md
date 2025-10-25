# Changelog

All notable changes to the Balancing Services REST API will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Version bumping script (`scripts/bump-version.sh`) to automate version updates across repository files
- Automated Python client publishing workflow

## [1.1.1] - 2025-10-24

### Fixed
- Python client documentation examples now use correct types (`Area` enum and `datetime` objects) instead of strings (#1318)

### Added
- Automated tests for README code examples to prevent documentation drift

## [1.1.0] - 2025-10-22

### Added
- Official Python client library generated from OpenAPI specification
- `procuredAt` timestamp field to `BalancingCapacityPrice` and `BalancingCapacityVolume` schemas (#1)
  - Enables distinguishing between multiple procurement rounds (e.g., D-2 vs D-1 auctions)
  - Marked as EXPERIMENTAL - may change without standard deprecation period
  - Optional field, initially rolled out for markets with multiple auctions

### Changed
- Simplified Python client README by removing endpoint listing to avoid documentation drift

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

[Unreleased]: https://github.com/balancing-services/rest-api/compare/v1.1.1...HEAD
[1.1.1]: https://github.com/balancing-services/rest-api/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/balancing-services/rest-api/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/balancing-services/rest-api/releases/tag/v1.0.0
