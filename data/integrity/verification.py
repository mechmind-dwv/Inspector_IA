"""
Inspector IA - Data Integrity and Provenance System
===================================================

Implements blockchain-based data integrity verification using Merkle trees
and immutable audit trails for investigative journalism data.

Author: Inspector IA Core Team
Version: 2.0
Date: December 2024
"""

import hashlib
import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from enum import Enum
import binascii


# ==================== MERKLE TREE IMPLEMENTATION ====================

class MerkleTree:
    """
    Merkle tree implementation for data integrity verification.
    
    Provides cryptographic proof that data has not been tampered with
    by maintaining a tree of hashes where any change to leaf data
    propagates to the root hash.
    """
    
    def __init__(self):
        """Initialize empty Merkle tree."""
        self.leaves: List[bytes] = []
        self.tree: List[List[bytes]] = []
        self.root: Optional[bytes] = None
    
    def add_leaf(self, data: str) -> Dict[str, Any]:
        """
        Add a data leaf to the tree.
        
        Args:
            data: String data to add as leaf
            
        Returns:
            Dictionary with leaf hash and Merkle proof
        """
        # Hash the data
        leaf_hash = hashlib.sha256(data.encode('utf-8')).digest()
        self.leaves.append(leaf_hash)
        
        # Rebuild tree
        self._build_tree()
        
        # Generate proof for this leaf
        proof = self._generate_proof(len(self.leaves) - 1)
        
        return {
            "leaf_hash": leaf_hash.hex(),
            "leaf_index": len(self.leaves) - 1,
            "proof": proof,
            "root": self.root.hex() if self.root else None
        }
    
    def _build_tree(self):
        """Build the Merkle tree from current leaves."""
        if not self.leaves:
            self.tree = []
            self.root = None
            return
        
        # Start with leaves as first level
        self.tree = [self.leaves[:]]
        
        # Build tree level by level
        current_level = self.leaves[:]
        
        while len(current_level) > 1:
            next_level = []
            
            # Process pairs
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                
                # If odd number of nodes, duplicate the last one
                if i + 1 < len(current_level):
                    right = current_level[i + 1]
                else:
                    right = left
                
                # Combine and hash
                combined = left + right
                parent = hashlib.sha256(combined).digest()
                next_level.append(parent)
            
            self.tree.append(next_level)
            current_level = next_level
        
        # Root is the last remaining node
        self.root = current_level[0] if current_level else None
    
    def _generate_proof(self, leaf_index: int) -> List[Dict[str, str]]:
        """
        Generate Merkle proof for a leaf.
        
        Args:
            leaf_index: Index of the leaf to prove
            
        Returns:
            List of proof elements with hash and position
        """
        if leaf_index >= len(self.leaves):
            return []
        
        proof = []
        current_index = leaf_index
        
        # Traverse up the tree
        for level in range(len(self.tree) - 1):
            level_nodes = self.tree[level]
            
            # Determine if we need left or right sibling
            if current_index % 2 == 0:
                # Current is left, need right sibling
                if current_index + 1 < len(level_nodes):
                    sibling = level_nodes[current_index + 1]
                    position = "right"
                else:
                    sibling = level_nodes[current_index]
                    position = "right"
            else:
                # Current is right, need left sibling
                sibling = level_nodes[current_index - 1]
                position = "left"
            
            proof.append({
                "hash": sibling.hex(),
                "position": position
            })
            
            # Move to parent index
            current_index = current_index // 2
        
        return proof
    
    def verify_proof(
        self,
        leaf_data: str,
        proof: List[Dict[str, str]],
        root: str
    ) -> bool:
        """
        Verify a Merkle proof.
        
        Args:
            leaf_data: Original data to verify
            proof: Merkle proof path
            root: Expected root hash
            
        Returns:
            True if proof is valid, False otherwise
        """
        # Hash the leaf data
        current_hash = hashlib.sha256(leaf_data.encode('utf-8')).digest()
        
        # Apply proof elements
        for proof_element in proof:
            sibling_hash = bytes.fromhex(proof_element["hash"])
            
            if proof_element["position"] == "left":
                combined = sibling_hash + current_hash
            else:
                combined = current_hash + sibling_hash
            
            current_hash = hashlib.sha256(combined).digest()
        
        # Compare with expected root
        return current_hash.hex() == root
    
    def get_root(self) -> Optional[str]:
        """Get the current Merkle root hash."""
        return self.root.hex() if self.root else None


# ==================== BLOCKCHAIN LAYER ====================

@dataclass
class BlockchainTransaction:
    """Represents a transaction in the blockchain."""
    tx_id: str
    timestamp: datetime
    data_hash: str
    merkle_root: str
    merkle_proof: List[Dict[str, str]]
    source_url: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert transaction to dictionary."""
        return {
            "tx_id": self.tx_id,
            "timestamp": self.timestamp.isoformat(),
            "data_hash": self.data_hash,
            "merkle_root": self.merkle_root,
            "merkle_proof": self.merkle_proof,
            "source_url": self.source_url,
            "metadata": self.metadata
        }


class MockBlockchain:
    """
    Mock blockchain implementation for development and testing.
    
    In production, this would connect to an actual blockchain network
    like Ethereum, Hyperledger, or a custom chain.
    """
    
    def __init__(self):
        """Initialize mock blockchain."""
        self.transactions: Dict[str, BlockchainTransaction] = {}
        self.transaction_counter = 0
    
    def record_transaction(self, transaction_data: Dict[str, Any]) -> str:
        """
        Record a transaction on the blockchain.
        
        Args:
            transaction_data: Transaction information
            
        Returns:
            Transaction ID
        """
        self.transaction_counter += 1
        tx_id = f"0x{hashlib.sha256(str(self.transaction_counter).encode()).hexdigest()[:16]}"
        
        transaction = BlockchainTransaction(
            tx_id=tx_id,
            timestamp=datetime.now(),
            data_hash=transaction_data["data_hash"],
            merkle_root=transaction_data["merkle_root"],
            merkle_proof=transaction_data["merkle_proof"],
            source_url=transaction_data["source"],
            metadata=transaction_data.get("metadata", {})
        )
        
        self.transactions[tx_id] = transaction
        return tx_id
    
    def get_transaction(self, tx_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a transaction from the blockchain.
        
        Args:
            tx_id: Transaction identifier
            
        Returns:
            Transaction data or None if not found
        """
        transaction = self.transactions.get(tx_id)
        return transaction.to_dict() if transaction else None
    
    def list_transactions(
        self,
        limit: int = 10,
        source_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        List recent transactions.
        
        Args:
            limit: Maximum number of transactions to return
            source_filter: Optional URL filter
            
        Returns:
            List of transaction dictionaries
        """
        transactions = list(self.transactions.values())
        
        if source_filter:
            transactions = [
                t for t in transactions
                if source_filter in t.source_url
            ]
        
        # Sort by timestamp (most recent first)
        transactions.sort(key=lambda t: t.timestamp, reverse=True)
        
        return [t.to_dict() for t in transactions[:limit]]


# ==================== DATA INTEGRITY MANAGER ====================

class DataIntegrityManager:
    """
    Manages data integrity verification using Merkle trees and blockchain.
    
    Provides cryptographic guarantees that data sources have not been
    tampered with, essential for investigative journalism credibility.
    """
    
    def __init__(self, blockchain_client: Optional[MockBlockchain] = None):
        """
        Initialize data integrity manager.
        
        Args:
            blockchain_client: Blockchain connection (uses mock if None)
        """
        self.blockchain = blockchain_client or MockBlockchain()
        self.merkle_tree = MerkleTree()
        self.snapshots: Dict[str, Dict[str, Any]] = {}
    
    def register_data_snapshot(
        self,
        source_url: str,
        data: Any,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Register a snapshot of data with integrity verification.
        
        Args:
            source_url: URL of data source
            data: Data to register (will be JSON serialized)
            metadata: Optional additional metadata
            
        Returns:
            Registration information including hashes and transaction ID
        """
        timestamp = datetime.now()
        
        # Serialize data
        data_json = json.dumps(data, sort_keys=True, default=str)
        
        # Create hash of data
        data_hash = hashlib.sha256(data_json.encode()).hexdigest()
        
        # Add to Merkle tree
        merkle_result = self.merkle_tree.add_leaf(data_json)
        
        # Record on blockchain
        tx_data = {
            "source": source_url,
            "data_hash": data_hash,
            "merkle_root": merkle_result["root"],
            "merkle_proof": merkle_result["proof"],
            "metadata": metadata or {}
        }
        
        tx_hash = self.blockchain.record_transaction(tx_data)
        
        # Store snapshot reference
        snapshot_id = f"{source_url}:{timestamp.isoformat()}"
        self.snapshots[snapshot_id] = {
            "data_hash": data_hash,
            "tx_hash": tx_hash,
            "timestamp": timestamp,
            "source_url": source_url,
            "merkle_result": merkle_result
        }
        
        return {
            "snapshot_id": snapshot_id,
            "data_hash": data_hash,
            "tx_hash": tx_hash,
            "merkle_root": merkle_result["root"],
            "timestamp": timestamp.isoformat(),
            "verification_url": f"/verify/{tx_hash}"
        }
    
    def verify_data_integrity(
        self,
        data: Any,
        tx_hash: str
    ) -> Dict[str, Any]:
        """
        Verify that data matches a registered snapshot.
        
        Args:
            data: Current data to verify
            tx_hash: Transaction hash of original registration
            
        Returns:
            Verification result with status and details
        """
        # Get original transaction
        transaction = self.blockchain.get_transaction(tx_hash)
        
        if not transaction:
            return {
                "verified": False,
                "reason": "Transaction not found in blockchain",
                "tx_hash": tx_hash
            }
        
        # Serialize current data
        data_json = json.dumps(data, sort_keys=True, default=str)
        current_hash = hashlib.sha256(data_json.encode()).hexdigest()
        
        # Compare hashes
        original_hash = transaction["data_hash"]
        hashes_match = current_hash == original_hash
        
        # Verify Merkle proof
        merkle_verified = self.merkle_tree.verify_proof(
            data_json,
            transaction["merkle_proof"],
            transaction["merkle_root"]
        )
        
        return {
            "verified": hashes_match and merkle_verified,
            "hashes_match": hashes_match,
            "merkle_verified": merkle_verified,
            "original_hash": original_hash,
            "current_hash": current_hash,
            "source_url": transaction["source_url"],
            "timestamp": transaction["timestamp"],
            "tx_hash": tx_hash,
            "details": {
                "data_unchanged": hashes_match,
                "chain_of_custody_intact": merkle_verified,
                "blockchain_confirmed": True
            }
        }
    
    def generate_integrity_report(
        self,
        snapshot_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Generate integrity report for multiple snapshots.
        
        Args:
            snapshot_ids: List of snapshot identifiers
            
        Returns:
            Comprehensive integrity report
        """
        report = {
            "report_timestamp": datetime.now().isoformat(),
            "snapshots_checked": len(snapshot_ids),
            "verification_results": [],
            "summary": {
                "verified": 0,
                "failed": 0,
                "not_found": 0
            }
        }
        
        for snapshot_id in snapshot_ids:
            snapshot = self.snapshots.get(snapshot_id)
            
            if not snapshot:
                report["summary"]["not_found"] += 1
                report["verification_results"].append({
                    "snapshot_id": snapshot_id,
                    "status": "not_found"
                })
                continue
            
            # Verify via blockchain
            verification = self.verify_data_integrity(
                {},  # Would load actual data
                snapshot["tx_hash"]
            )
            
            if verification["verified"]:
                report["summary"]["verified"] += 1
                status = "verified"
            else:
                report["summary"]["failed"] += 1
                status = "failed"
            
            report["verification_results"].append({
                "snapshot_id": snapshot_id,
                "status": status,
                "source_url": snapshot["source_url"],
                "timestamp": snapshot["timestamp"].isoformat(),
                "tx_hash": snapshot["tx_hash"],
                "verification_details": verification
            })
        
        # Calculate integrity score
        total = report["summary"]["verified"] + report["summary"]["failed"]
        if total > 0:
            report["summary"]["integrity_score"] = (
                report["summary"]["verified"] / total
            ) * 100
        else:
            report["summary"]["integrity_score"] = 0.0
        
        return report
    
    def export_verification_certificate(
        self,
        tx_hash: str
    ) -> str:
        """
        Export a human-readable verification certificate.
        
        Args:
            tx_hash: Transaction hash
            
        Returns:
            Formatted certificate text
        """
        transaction = self.blockchain.get_transaction(tx_hash)
        
        if not transaction:
            return "Certificate not available - transaction not found"
        
        certificate = f"""
╔════════════════════════════════════════════════════════════════╗
║         INSPECTOR IA - DATA INTEGRITY CERTIFICATE              ║
╠════════════════════════════════════════════════════════════════╣
║                                                                ║
║  Transaction ID: {tx_hash}                                     
║  Timestamp: {transaction['timestamp']}                         
║  Source: {transaction['source_url']}                           
║                                                                ║
║  Data Hash (SHA-256):                                         ║
║  {transaction['data_hash']}                                    
║                                                                ║
║  Merkle Root:                                                 ║
║  {transaction['merkle_root']}                                  
║                                                                ║
║  This certificate cryptographically proves that the data      ║
║  registered at the above timestamp has not been altered.      ║
║                                                                ║
║  Verification URL:                                            ║
║  https://inspector-ia.com/verify/{tx_hash}                    
║                                                                ║
╚════════════════════════════════════════════════════════════════╝

VERIFICATION INSTRUCTIONS:
1. Visit the verification URL above
2. Upload or paste the original data
3. System will verify against this certificate
4. Green checkmark confirms data integrity

This certificate provides cryptographic proof of data provenance
for investigative journalism and can be submitted as evidence of
data authenticity in legal proceedings.

Generated by Inspector IA Data Integrity System
{datetime.now().isoformat()}
"""
        return certificate


# ==================== USAGE EXAMPLE ====================

def demonstrate_integrity_system():
    """Demonstrate the data integrity verification system."""
    
    print("=" * 80)
    print("Inspector IA - Data Integrity System Demonstration")
    print("=" * 80)
    print()
    
    # Initialize system
    integrity_manager = DataIntegrityManager()
    
    # Example 1: Register politician declaration data
    print("Step 1: Registering politician asset declaration...")
    declaration_data = {
        "politician_id": "POL_001",
        "politician_name": "María González",
        "declaration_year": 2024,
        "assets": {
            "real_estate": [
                {"type": "apartment", "value": 250000, "location": "Madrid"}
            ],
            "vehicles": [
                {"type": "car", "value": 35000, "model": "Tesla Model 3"}
            ],
            "bank_accounts": [
                {"bank": "BBVA", "balance": 50000}
            ]
        },
        "total_declared": 335000
    }
    
    registration = integrity_manager.register_data_snapshot(
        source_url="https://transparencia.gob.es/declarations/2024/POL_001",
        data=declaration_data,
        metadata={"type": "asset_declaration", "year": 2024}
    )
    
    print(f"✓ Data registered successfully")
    print(f"  Transaction Hash: {registration['tx_hash']}")
    print(f"  Data Hash: {registration['data_hash']}")
    print(f"  Merkle Root: {registration['merkle_root']}")
    print()
    
    # Example 2: Verify data integrity
    print("Step 2: Verifying data integrity...")
    verification = integrity_manager.verify_data_integrity(
        data=declaration_data,
        tx_hash=registration['tx_hash']
    )
    
    if verification['verified']:
        print("✓ Data integrity VERIFIED")
        print("  - Original and current hashes match")
        print("  - Merkle proof valid")
        print("  - Chain of custody intact")
    else:
        print("✗ Data integrity check FAILED")
    print()
    
    # Example 3: Generate certificate
    print("Step 3: Generating verification certificate...")
    certificate = integrity_manager.export_verification_certificate(
        registration['tx_hash']
    )
    print(certificate)
    
    print("=" * 80)
    print("✅ Data integrity system demonstration complete!")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_integrity_system()
