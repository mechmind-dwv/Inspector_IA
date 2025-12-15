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

