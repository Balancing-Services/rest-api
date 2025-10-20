# Balancing Services REST API

OpenAPI specification for the Balancing Services REST API - providing comprehensive access to European electricity balancing market data.

## Overview

The Balancing Services REST API provides access to real-time and historical electricity balancing market data across 40+ European areas. Access imbalance prices, balancing energy bids and prices, balancing capacity information, and more through a modern RESTful interface.

**Key features:**
- Comprehensive balancing market data for European electricity markets
- RESTful design with JSON responses
- Cursor-based pagination for large datasets
- Bearer token authentication
- Standardized error handling (RFC 7807 Problem Details)

## Getting Started

### API Server

**Production API:** https://api.balancing.services/v1

**Interactive Documentation:** https://api.balancing.services/v1/documentation

The interactive documentation provides a Swagger UI interface where you can explore all endpoints, view request/response schemas, and test API calls directly in your browser.

### Authentication

API access requires authentication using a Bearer token. Include your API token in the `Authorization` header of each request:

```bash
Authorization: Bearer YOUR_API_TOKEN
```

To obtain an API token, please contact us:
- **Email:** info@balancing.services
- **Website:** https://balancing.services
- **LinkedIn:** https://linkedin.com/company/balancing-services

### Quick Start Example

Fetch imbalance prices for Estonia on January 1st, 2025:

```bash
curl -X GET "https://api.balancing.services/v1/imbalance/prices?area=EE&period-start-at=2025-01-01T00:00:00Z&period-end-at=2025-01-02T00:00:00Z" \
  -H "Authorization: Bearer YOUR_API_TOKEN"
```

## Available Endpoints

The API provides 8 endpoints across three categories:
- **Imbalance Data:** Prices and total volumes
- **Balancing Energy:** Activated volumes, prices, and bids
- **Balancing Capacity:** Bids, prices, and procured volumes

The API covers 40+ European areas and supports multiple reserve types (FCR, aFRR, mFRR, RR). For complete endpoint details, parameters, and response schemas, see the [OpenAPI specification](./openapi.yaml) or the [interactive documentation](https://api.balancing.services/v1/documentation).

## API Specification

The complete OpenAPI 3.0 specification is available in [`openapi.yaml`](./openapi.yaml). You can use this specification to:
- Generate client SDKs in your preferred programming language
- Import into API development tools (Postman, Insomnia, etc.)
- Understand detailed request/response schemas
- View all available parameters and error responses

## Versioning

This project follows [Semantic Versioning](https://semver.org/):
- **Major version** (X.0.0): Breaking changes to the API
- **Minor version** (0.X.0): New features, backward compatible
- **Patch version** (0.0.X): Bug fixes and minor improvements

Version history and changelog are available in [`CHANGELOG.md`](./CHANGELOG.md).

## Error Handling

The API uses standard HTTP status codes and returns errors in RFC 7807 Problem Details format:

```json
{
  "type": "invalid-parameter",
  "title": "Invalid Parameter",
  "status": 400,
  "detail": "The area parameter value is not valid"
}
```

Common status codes:
- **200** - Success
- **400** - Bad request (invalid parameters)
- **401** - Unauthorized (missing or invalid token)
- **403** - Forbidden (insufficient permissions)
- **404** - Not found
- **429** - Too many requests (rate limited)
- **500** - Internal server error
- **501** - Not implemented (feature unavailable)

## Contributing

We welcome contributions and feedback from the community:

- **Issues:** Found a bug or have a feature request? [Open an issue](https://github.com/balancing-services/rest-api/issues)
- **Discussions:** Questions or suggestions? [Start a discussion](https://github.com/balancing-services/rest-api/discussions)
- **Pull Requests:** Improvements to documentation or specification are welcome

When reporting issues, please include:
- The endpoint and parameters you're using
- Expected vs actual behavior
- Any relevant error messages

## Contact

- **Website:** https://balancing.services
- **Email:** info@balancing.services
- **LinkedIn:** https://linkedin.com/company/balancing-services

## License

This OpenAPI specification is licensed under the MIT License. See [`LICENSE`](./LICENSE) for details.

---

**Note:** This repository contains the API specification only. For implementation details, server infrastructure, and private components, please refer to the private repository or contact us directly.
