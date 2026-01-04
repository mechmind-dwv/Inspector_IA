#!/bin/bash

# Inspector IA - Documentation Deployment Script
# This script deploys the CRYPTO_HIDING pattern documentation to the repository
# Version: 1.0
# Date: December 2025

set -e  # Exit on any error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored messages
print_message() {
    local color=$1
    local message=$2
    echo -e "${color}${message}${NC}"
}

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Header
print_message "$BLUE" "=========================================="
print_message "$BLUE" "Inspector IA Documentation Deployment"
print_message "$BLUE" "=========================================="
echo ""

# Check prerequisites
print_message "$YELLOW" "Step 1: Checking prerequisites..."

if ! command_exists git; then
    print_message "$RED" "Error: git is not installed. Please install git first."
    exit 1
fi

if ! command_exists python3; then
    print_message "$RED" "Error: python3 is not installed. Please install Python 3.10+ first."
    exit 1
fi

print_message "$GREEN" "✓ Prerequisites check passed"
echo ""

# Verify we're in a git repository
print_message "$YELLOW" "Step 2: Verifying git repository..."

if [ ! -d ".git" ]; then
    print_message "$RED" "Error: Not in a git repository root directory."
    print_message "$RED" "Please navigate to the Inspector_IA repository root and run this script again."
    exit 1
fi

print_message "$GREEN" "✓ Git repository verified"
echo ""

# Create directory structure if it doesn't exist
print_message "$YELLOW" "Step 3: Creating directory structure..."

mkdir -p docs/patterns
mkdir -p docs/implementation_guides
mkdir -p src/synthetic/injectors
mkdir -p src/detection/patterns
mkdir -p src/detection/heuristics
mkdir -p config/patterns
mkdir -p tests/synthetic
mkdir -p tests/unit

print_message "$GREEN" "✓ Directory structure created"
echo ""

# Create the CRYPTO_HIDING Technical Specification
print_message "$YELLOW" "Step 4: Creating CRYPTO_HIDING Technical Specification..."

cat > docs/patterns/CRYPTO_HIDING_SPECIFICATION.md << 'SPEC_EOF'
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

SPEC_EOF

print_message "$GREEN" "✓ Technical specification created"
echo ""

# Create the Implementation Guide
print_message "$YELLOW" "Step 5: Creating Implementation Guide..."

cat > docs/implementation_guides/CRYPTO_HIDING_IMPLEMENTATION.md << 'IMPL_EOF'
# CRYPTO_HIDING Pattern: Implementation Guide

## Document Purpose

This implementation guide provides software engineers with practical instructions for developing the CRYPTO_HIDING pattern within the Inspector IA synthetic fraud ecosystem.

## Prerequisites

Developers implementing the CRYPTO_HIDING pattern require familiarity with Python 3.10+, blockchain fundamentals, graph data structures, Neo4j concepts, statistical distributions with NumPy, and the Inspector IA architecture.

## Development Environment Setup

Clone the Inspector IA repository and create a Python virtual environment. Install dependencies from requirements.txt and configure environment variables from .env.example. Verify database connectivity and execute existing tests to confirm baseline system operation.

Create a feature branch for CRYPTO_HIDING implementation following project naming conventions.

## Module Organization

Primary implementation resides in src/synthetic/injectors/crypto_hiding_injector.py containing the CryptoHidingInjector orchestration class, CryptoWallet and CryptoTransaction dataclasses, helper generator classes, and sophistication level enumerations.

Supporting components include detection/patterns/crypto_hiding.py for production detection algorithms, detection/heuristics/crypto_heuristics.py for risk calculation heuristics, comprehensive test files in tests/synthetic/ and tests/unit/, and configuration parameters in config/patterns/crypto_hiding.yml.

## Core Implementation Pattern

The implementation follows a sequential pipeline transforming clean politician profiles into complete synthetic fraud cases. The process calculates hidden amounts using log-normal distributions, generates hierarchical wallet structures across sophistication-appropriate layers, constructs connection paths through realistic intermediaries, creates transaction histories implementing specified patterns, calculates risk metrics through heuristic evaluation, and compiles comprehensive ground truth metadata.

## Testing Strategy

Comprehensive testing validates components through unit tests for individual functions, integration tests for complete pattern generation, and validation tests confirming realistic statistical distributions and detection heuristic triggering.

## Common Pitfalls

Avoid inconsistent monetary flows by tracking wallet balances carefully. Prevent unrealistic temporal patterns through appropriate random variation. Ensure comprehensive ground truth metadata for validation. Match wallet types to appropriate roles within patterns. Introduce sufficient randomization to represent real-world variance.

## Performance Optimization

Scale pattern generation through wallet generation caching, batch transaction processing, lazy evaluation of expensive operations, and parallel generation for large datasets.

## Documentation Requirements

Maintain comprehensive docstrings following NumPy style. Document configuration parameters completely. Create working usage examples. Maintain changelogs tracking system evolution.

## Deployment Preparation

Implement structured logging throughout generation pipelines. Create configuration profiles for development, staging, and production environments. Establish graceful error handling and recovery. Deploy monitoring dashboards tracking generation metrics. Define data retention policies for generated patterns.

IMPL_EOF

print_message "$GREEN" "✓ Implementation guide created"
echo ""

# Create a starter implementation file
print_message "$YELLOW" "Step 6: Creating starter implementation file..."

cat > src/synthetic/injectors/crypto_hiding_injector.py << 'PYTHON_EOF'
"""
CRYPTO_HIDING Pattern Injection Engine v2.0
Supports three sophistication levels with increasingly complex evasion techniques.

This module implements the complete CRYPTO_HIDING pattern generation system
for the Inspector IA synthetic fraud ecosystem.

Author: Inspector IA Core Team
Date: December 2024
Version: 2.0
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import random
import hashlib
import secrets

# ==================== ENUMERATIONS ====================

class CryptoEvasionLevel(Enum):
    """Sophistication levels for crypto evasion techniques."""
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class WalletType(Enum):
    """Cryptocurrency wallet types with distinct characteristics."""
    EXCHANGE_HOT = "exchange_hot"
    COLD_STORAGE = "cold_storage"
    MIXER_LINKED = "mixer_linked"
    PRIVACY_COIN = "privacy_coin"
    DEX_ONLY = "dex_only"
    BURNER = "burner"
    MULTISIG = "multisig"


class TransactionPattern(Enum):
    """Transaction patterns for obfuscation techniques."""
    PEELING_CHAIN = "peeling_chain"
    STRUCTURED = "structured"
    MIXER_CASCADE = "mixer_cascade"
    CROSS_CHAIN_HOP = "cross_chain_hop"
    PRIVACY_COIN_CONVERSION = "privacy_coin_conversion"


# ==================== DATA STRUCTURES ====================

@dataclass
class CryptoWallet:
    """Cryptocurrency wallet with forensic metadata."""
    address: str
    type: WalletType
    currency: str
    creation_date: datetime
    last_active: datetime
    estimated_balance_fiat: float
    ml_risk_score: float = 0.0
    known_mixer_interactions: int = 0
    privacy_coin_holdings: bool = False
    cross_chain_transactions: int = 0
    structured_pattern_detected: bool = False
    owner_person_id: Optional[str] = None
    linked_company_id: Optional[str] = None
    
    def to_graph_node(self) -> Dict:
        """Convert wallet to Neo4j node format."""
        return {
            "address": self.address,
            "type": self.type.value,
            "currency": self.currency,
            "creation_date": self.creation_date.isoformat(),
            "last_active": self.last_active.isoformat(),
            "estimated_balance_fiat": self.estimated_balance_fiat,
            "ml_risk_score": self.ml_risk_score,
            "risk_flags": self._generate_risk_flags()
        }
    
    def _generate_risk_flags(self) -> List[str]:
        """Generate risk flags based on wallet properties."""
        flags = []
        if self.known_mixer_interactions > 0:
            flags.append(f"MIXER_INTERACTIONS_{self.known_mixer_interactions}")
        if self.privacy_coin_holdings:
            flags.append("PRIVACY_COIN_HOLDINGS")
        if self.cross_chain_transactions > 2:
            flags.append("HIGH_CROSS_CHAIN_ACTIVITY")
        if self.structured_pattern_detected:
            flags.append("STRUCTURED_TRANSACTION_PATTERN")
        if self.ml_risk_score > 0.7:
            flags.append("HIGH_ML_RISK_SCORE")
        return flags


@dataclass
class CryptoTransaction:
    """Blockchain transaction with forensic metadata."""
    tx_hash: str
    timestamp: datetime
    from_address: str
    to_address: str
    amount_fiat: float
    amount_crypto: float
    currency: str
    mixer_used: bool = False
    mixer_service: Optional[str] = None
    privacy_coin_involved: bool = False
    cross_chain: bool = False
    cross_chain_bridge: Optional[str] = None
    structured_amount: bool = False
    peeling_chain_step: Optional[int] = None
    
    def to_graph_relationship(self) -> Dict:
        """Convert transaction to Neo4j relationship format."""
        return {
            "tx_hash": self.tx_hash,
            "timestamp": self.timestamp.isoformat(),
            "amount_fiat": self.amount_fiat,
            "amount_crypto": self.amount_crypto,
            "currency": self.currency,
            "mixer_used": self.mixer_used,
            "mixer_service": self.mixer_service,
            "privacy_coin_involved": self.privacy_coin_involved,
            "cross_chain": self.cross_chain,
            "cross_chain_bridge": self.cross_chain_bridge,
            "structured_amount": self.structured_amount,
            "peeling_chain_step": self.peeling_chain_step
        }


# ==================== MAIN INJECTOR CLASS ====================

class CryptoHidingInjector:
    """
    Main pattern injection engine for CRYPTO_HIDING fraud patterns.
    
    This class orchestrates the generation of complete cryptocurrency
    obfuscation patterns at three sophistication levels.
    """
    
    # Configuration by sophistication level
    LEVEL_CONFIGS = {
        CryptoEvasionLevel.BASIC: {
            "wallet_layers": 1,
            "max_intermediaries": 1,
            "allow_mixers": False,
            "allow_privacy_coins": False,
            "allow_cross_chain": False,
            "transaction_patterns": [TransactionPattern.PEELING_CHAIN],
            "ira_bonus_range": (5, 10)
        },
        CryptoEvasionLevel.INTERMEDIATE: {
            "wallet_layers": 2,
            "max_intermediaries": 2,
            "allow_mixers": True,
            "allow_privacy_coins": False,
            "allow_cross_chain": True,
            "transaction_patterns": [
                TransactionPattern.PEELING_CHAIN,
                TransactionPattern.STRUCTURED
            ],
            "ira_bonus_range": (10, 20)
        },
        CryptoEvasionLevel.ADVANCED: {
            "wallet_layers": 3,
            "max_intermediaries": 3,
            "allow_mixers": True,
            "allow_privacy_coins": True,
            "allow_cross_chain": True,
            "transaction_patterns": [
                TransactionPattern.PEELING_CHAIN,
                TransactionPattern.STRUCTURED,
                TransactionPattern.MIXER_CASCADE,
                TransactionPattern.CROSS_CHAIN_HOP,
                TransactionPattern.PRIVACY_COIN_CONVERSION
            ],
            "ira_bonus_range": (20, 30)
        }
    }
    
    # Known services for realistic simulation
    KNOWN_MIXERS = [
        "Tornado Cash", "Wasabi Wallet", "Samourai Whirlpool",
        "CoinJoin", "CashFusion"
    ]
    
    CROSS_CHAIN_BRIDGES = [
        "Polygon Bridge", "Arbitrum Bridge", "Optimism Gateway",
        "Wormhole", "Multichain", "Synapse"
    ]
    
    PRIVACY_COINS = ["XMR", "ZEC", "DASH", "GRIN", "BEAM"]
    
    def __init__(self):
        """Initialize the CRYPTO_HIDING pattern injector."""
        # TODO: Initialize blockchain simulator and helper generators
        pass
    
    def inject_pattern(
        self,
        politician: Dict,
        level: CryptoEvasionLevel = CryptoEvasionLevel.INTERMEDIATE,
        amount_to_hide: Optional[float] = None,
        severity: float = 0.5
    ) -> Dict:
        """
        Inject a CRYPTO_HIDING pattern into a synthetic politician profile.
        
        Args:
            politician: Clean politician profile
            level: Sophistication level for obfuscation
            amount_to_hide: Total amount to conceal (auto-calculated if None)
            severity: Pattern severity from 0.1 (mild) to 1.0 (aggressive)
        
        Returns:
            Complete pattern structure with all metadata
        """
        # TODO: Implement complete pattern injection pipeline
        return {
            "pattern_type": "CRYPTO_HIDING",
            "evasion_level": level.value,
            "severity": severity,
            "status": "implementation_required"
        }


# ==================== USAGE EXAMPLE ====================

def demonstrate_crypto_hiding():
    """Demonstrate CRYPTO_HIDING pattern generation."""
    politician = {
        "id": "POL_001",
        "name": "Example Politician",
        "annual_income": 200000,
        "declared_assets": 500000,
        "position": "Congress Member"
    }
    
    injector = CryptoHidingInjector()
    
    print("=" * 80)
    print("CRYPTO_HIDING Pattern Generation Demo")
    print("=" * 80)
    
    for level in CryptoEvasionLevel:
        print(f"\nGenerating {level.value.upper()} level pattern...")
        pattern = injector.inject_pattern(
            politician=politician,
            level=level,
            severity=0.7
        )
        print(f"Status: {pattern['status']}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    demonstrate_crypto_hiding()
PYTHON_EOF

print_message "$GREEN" "✓ Starter implementation file created"
echo ""

# Create configuration file
print_message "$YELLOW" "Step 7: Creating configuration file..."

cat > config/patterns/crypto_hiding.yml << 'CONFIG_EOF'
# CRYPTO_HIDING Pattern Configuration
# Inspector IA - Synthetic Fraud Ecosystem

pattern_name: CRYPTO_HIDING
version: 2.0
status: design_phase

# Sophistication level parameters
sophistication_levels:
  basic:
    wallet_layers: 1
    max_intermediaries: 1
    allow_mixers: false
    allow_privacy_coins: false
    allow_cross_chain: false
    ira_bonus_min: 5
    ira_bonus_max: 10
    
  intermediate:
    wallet_layers: 2
    max_intermediaries: 2
    allow_mixers: true
    allow_privacy_coins: false
    allow_cross_chain: true
    ira_bonus_min: 10
    ira_bonus_max: 20
    
  advanced:
    wallet_layers: 3
    max_intermediaries: 3
    allow_mixers: true
    allow_privacy_coins: true
    allow_cross_chain: true
    ira_bonus_min: 20
    ira_bonus_max: 30

# Detection heuristic weights
heuristics:
  mixer_interaction_detection:
    weight: 0.25
    ira_contribution: 15
    
  privacy_coin_conversion:
    weight: 0.20
    ira_contribution: 12
    
  peeling_chain_detection:
    weight: 0.15
    ira_contribution: 10
    
  cross_chain_suspicious_flow:
    weight: 0.18
    ira_contribution: 11
    
  structured_transactions:
    weight: 0.22
    ira_contribution: 14

# Validation thresholds
validation:
  true_positive_threshold: 0.70
  false_positive_tolerance: 0.10
  pattern_completeness_minimum: 0.80
  
# Performance benchmarks
benchmarks:
  detection_rate_target: 0.85
  false_positive_target: 0.05
  mean_detection_time_hours: 48
  xai_quality_minimum: 0.80

CONFIG_EOF

print_message "$GREEN" "✓ Configuration file created"
echo ""

# Create README for documentation
print_message "$YELLOW" "Step 8: Creating documentation README..."

cat > docs/patterns/README.md << 'README_EOF'
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

README_EOF

print_message "$GREEN" "✓ Documentation README created"
echo ""

# Git operations
print_message "$YELLOW" "Step 9: Git operations..."

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
print_message "$BLUE" "Current branch: $CURRENT_BRANCH"

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    print_message "$YELLOW" "Warning: You have uncommitted changes. Continuing anyway..."
fi

# Create feature branch
FEATURE_BRANCH="feature/crypto-hiding-documentation"

if git show-ref --verify --quiet "refs/heads/$FEATURE_BRANCH"; then
    print_message "$YELLOW" "Branch $FEATURE_BRANCH already exists. Switching to it..."
    git checkout "$FEATURE_BRANCH"
else
    print_message "$BLUE" "Creating new branch: $FEATURE_BRANCH"
    git checkout -b "$FEATURE_BRANCH"
fi

echo ""

# Stage files
print_message "$YELLOW" "Step 10: Staging documentation files..."

git add docs/patterns/CRYPTO_HIDING_SPECIFICATION.md
git add docs/patterns/README.md
git add docs/implementation_guides/CRYPTO_HIDING_IMPLEMENTATION.md
git add src/synthetic/injectors/crypto_hiding_injector.py
git add config/patterns/crypto_hiding.yml

print_message "$GREEN" "✓ Files staged for commit"
echo ""

# Show status
print_message "$BLUE" "Git status:"
git status --short
echo ""

# Commit
print_message "$YELLOW" "Step 11: Creating commit..."

git commit -m "📚 docs: Add CRYPTO_HIDING pattern comprehensive documentation

- Add technical specification with complete architecture definition
- Add implementation guide with practical development instructions
- Add starter implementation file with core data structures
- Add configuration file with sophistication level parameters
- Add documentation README with pattern overview

This commit establishes the foundation for CRYPTO_HIDING pattern
implementation in the Inspector IA synthetic fraud ecosystem.

Components:
- Technical Specification (CRYPTO_HIDING_SPECIFICATION.md)
- Implementation Guide (CRYPTO_HIDING_IMPLEMENTATION.md)
- Starter Code (crypto_hiding_injector.py)
- Configuration (crypto_hiding.yml)
- Documentation Index (README.md)

Status: Design Phase - Ready for Implementation
Version: 2.0"

print_message "$GREEN" "✓ Commit created successfully"
echo ""

# Push to remote
print_message "$YELLOW" "Step 12: Pushing to remote repository..."

echo ""
print_message "$BLUE" "Push command:"
print_message "$BLUE" "git push -u origin $FEATURE_BRANCH"
echo ""

read -p "$(echo -e ${YELLOW}Do you want to push to remote now? [y/N]: ${NC})" -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push -u origin "$FEATURE_BRANCH"
    print_message "$GREEN" "✓ Successfully pushed to remote repository"
    echo ""
    print_message "$BLUE" "Next steps:"
    print_message "$BLUE" "1. Go to GitHub: https://github.com/mechmind-dwv/Inspector_IA"
    print_message "$BLUE" "2. Create a Pull Request from branch: $FEATURE_BRANCH"
    print_message "$BLUE" "3. Review and merge the documentation"
else
    print_message "$YELLOW" "Skipping push. You can push manually later with:"
    print_message "$BLUE" "git push -u origin $FEATURE_BRANCH"
fi

echo ""

# Summary
print_message "$GREEN" "=========================================="
print_message "$GREEN" "Deployment Script Completed Successfully"
print_message "$GREEN" "=========================================="
echo ""

print_message "$BLUE" "Created files:"
echo "  ✓ docs/patterns/CRYPTO_HIDING_SPECIFICATION.md"
echo "  ✓ docs/patterns/README.md"
echo "  ✓ docs/implementation_guides/CRYPTO_HIDING_IMPLEMENTATION.md"
echo "  ✓ src/synthetic/injectors/crypto_hiding_injector.py"
echo "  ✓ config/patterns/crypto_hiding.yml"
echo ""

print_message "$BLUE" "Branch: $FEATURE_BRANCH"
print_message "$BLUE" "Status: Ready for review and merge"
echo ""

print_message "$YELLOW" "Documentation successfully deployed to local repository!"
print_message "$YELLOW" "Review the files and push to GitHub when ready."
PYTHON_EOF

print_message "$GREEN" "✓ Deployment script created"
echo ""

# Make script executable
chmod +x deploy_documentation.sh

print_message "$GREEN" "=========================================="
print_message "$GREEN" "Script Generation Complete"
print_message "$GREEN" "=========================================="
echo ""

print_message "$BLUE" "To deploy the documentation, run:"
print_message "$YELLOW" "./deploy_documentation.sh"
echo ""

print_message "$BLUE" "The script will:"
echo "  1. Check prerequisites (git, python3)"
echo "  2. Verify you're in the correct repository"
echo "  3. Create necessary directory structure"
echo "  4. Generate all documentation files"
echo "  5. Create starter implementation code"
echo "  6. Set up configuration files"
echo "  7. Create a feature branch"
echo "  8. Stage and commit all files"
echo "  9. Optionally push to GitHub"
echo ""

print_message "$YELLOW" "Note: You'll need to manually push to GitHub after running the script."
print_message "$YELLOW" "The script will guide you through each step."
