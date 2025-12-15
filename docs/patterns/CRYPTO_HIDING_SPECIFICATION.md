# CRYPTO_HIDING Pattern: Technical Specification v2.0

## Document Control

**Version:** 2.0  
**Status:** Design Phase - Ready for Implementation  
**Last Updated:** December 2024  
**Owner:** Inspector IA Core Team  
**Classification:** Internal Development Documentation

## Executive Summary

The CRYPTO_HIDING pattern represents the most technically sophisticated fraud detection challenge within the Inspector IA system. This pattern addresses the use of cryptocurrency infrastructure to conceal illicit wealth through pseudonymity, privacy-enhancing technologies, and blockchain obfuscation techniques.

## Pattern Definition

### Objective

The CRYPTO_HIDING pattern simulates advanced techniques employed by corrupt public officials to obscure asset ownership and fund flows within cryptocurrency ecosystems. The pattern exploits the pseudonymous nature of blockchain transactions, privacy-focused technologies, and the regulatory complexity of cross-jurisdictional crypto assets.

### Sophistication Levels

The pattern implements three distinct sophistication levels:

**Basic Level:** Single-layer wallet structures with direct peer-to-peer transfers through exchange-linked wallets. This level permits minimal obfuscation with one intermediary entity maximum. Detection probability remains high due to limited complexity. IRA contribution ranges from five to ten bonus points.

**Intermediate Level:** Two-layer wallet structures incorporating decentralized exchanges and initial mixer services. This level permits two intermediary entities and introduces cross-chain bridge transactions. Detection probability ranges from medium to high depending on technique combinations. IRA contribution ranges from ten to twenty bonus points.

**Advanced Level:** Three-layer wallet structures with comprehensive obfuscation including cascading mixers, privacy coin conversions, and temporal obfuscation. This level permits three intermediary entities and full utilization of available privacy technologies. Detection probability reaches medium levels representing the system's technical limit. IRA contribution ranges from twenty to thirty bonus points.

## Wallet Type Taxonomy

The implementation defines seven distinct wallet types:

**Exchange-Linked Wallets:** Custodial wallets with KYC verification providing entry and exit points for fiat conversion. Anonymity score of 0.1 reflects identity verification requirements.

**Standard Wallets:** Self-custody wallets for general transactions providing basic pseudonymity. Anonymity score of 0.3 reflects public transaction traceability.

**Mixer-Connected Wallets:** Wallets interacting with coin mixing services demonstrating clear obfuscation intent. Anonymity score of 0.8 reflects transaction obfuscation capabilities.

**Privacy Coin Wallets:** Wallets supporting enhanced privacy features including stealth addresses and ring signatures. Anonymity score of 0.95 reflects protocol-level privacy.

**Cold Storage Wallets:** Hardware or offline wallets for long-term holdings prioritizing security. Anonymity score of 0.6 reflects limited activity patterns.

**DeFi Wallets:** Wallets for decentralized finance interactions enabling complex contract operations. Anonymity score of 0.5 reflects transaction complexity.

**Burner Wallets:** Temporary wallets for single-use purposes with intentionally limited history. Anonymity score of 0.7 reflects disposal intent.

## Transaction Pattern Taxonomy

The implementation defines five transaction patterns:

**Peeling Chain Pattern:** Large transaction followed by numerous smaller transactions attempting to obscure ultimate destinations through fragmentation. Contributes ten IRA bonus points.

**Structured Transaction Pattern:** Transactions with amounts specifically chosen to fall below regulatory reporting thresholds. Contributes fourteen IRA bonus points.

**Mixer Cascade Pattern:** Sequential routing through multiple cryptocurrency mixing services to break transaction graph analysis. Contribution scales with mixing round count.

**Cross-Chain Hopping Pattern:** Rapid movement across multiple blockchain networks forcing analysts to correlate distinct systems. Contributes eleven IRA bonus points.

**Privacy Coin Conversion Pattern:** Conversion to privacy-focused cryptocurrencies providing enhanced transaction privacy. Contributes twelve IRA bonus points.

## Detection Heuristics

Five primary heuristics analyze patterns:

**Mixer Interaction Detection (Weight 25%):** Identifies wallets interacting with known mixing services through address database matching and transaction analysis. Contributes fifteen IRA bonus points.

**Privacy Coin Conversion Detection (Weight 20%):** Monitors conversions to privacy-focused cryptocurrencies and evaluates volume relative to total activity. Contributes twelve IRA bonus points.

**Peeling Chain Detection (Weight 15%):** Identifies large-to-small transaction progressions through statistical analysis and temporal clustering. Contributes ten IRA bonus points.

**Cross-Chain Suspicious Flow (Weight 18%):** Tracks rapid multi-chain movements and evaluates bridge protocol usage patterns. Contributes eleven IRA bonus points.

**Structured Transaction Detection (Weight 22%):** Identifies amounts clustering near reporting thresholds through statistical analysis. Contributes fourteen IRA bonus points.

## Ground Truth Validation

Generated patterns include comprehensive ground truth metadata documenting all techniques employed, expected detection signals, pattern characteristics, and validation criteria. Validation metrics include true positive threshold of seventy percent, false positive tolerance of ten percent, pattern completeness scoring, and obfuscation effectiveness measurement.

Performance benchmarks specify detection rate targets of eighty-five percent, false positive limits of five percent, mean detection time under forty-eight simulated hours, and explainable AI quality scores above 0.8.

## Implementation Roadmap

Implementation follows a four-week development cycle delivering complete pattern generator and detection system capabilities through progressive component development, testing, and refinement.

