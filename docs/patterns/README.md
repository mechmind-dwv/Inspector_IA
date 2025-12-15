# Inspector IA Pattern Documentation

This directory contains comprehensive technical specifications for fraud patterns implemented in the Inspector IA synthetic fraud ecosystem.

## Available Patterns

### CRYPTO_HIDING Pattern

The CRYPTO_HIDING pattern addresses cryptocurrency-based asset concealment through three sophistication levels. This pattern represents the most technically advanced detection challenge within Inspector IA.

**Documentation:**
- [Technical Specification](CRYPTO_HIDING_SPECIFICATION.md)
- [Implementation Guide](../implementation_guides/CRYPTO_HIDING_IMPLEMENTATION.md)

**Status:** Design Phase - Ready for Implementation

**Key Features:**
- Three sophistication levels (Basic, Intermediate, Advanced)
- Seven wallet type taxonomy
- Five transaction pattern taxonomy
- Five detection heuristics with weighted scoring
- Comprehensive ground truth validation

## Future Patterns

The following patterns are planned for future implementation:

- **OFFSHORE_LAUNDERING:** Shell company networks and offshore jurisdiction usage
- **TRAVEL_COINCIDENCE:** Temporal-spatial correlation analysis
- **GHOST_COMPANY:** Low-activity high-contract entity detection
- **INSIDER_TRADING:** Legislative action and asset accumulation correlation

## Pattern Development Process

Pattern development follows a structured four-phase approach:

1. **Design Phase:** Technical specification and architecture definition
2. **Implementation Phase:** Code development following implementation guides
3. **Validation Phase:** Testing against ground truth and performance benchmarks
4. **Production Phase:** Integration with detection systems and deployment

## Contributing

Developers contributing to pattern implementation should review the implementation guides carefully and follow established coding standards. All patterns require comprehensive testing and documentation before production integration.

