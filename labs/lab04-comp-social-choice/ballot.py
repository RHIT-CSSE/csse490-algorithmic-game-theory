"""
Ballot representation and utility functions for ranked voting systems.

This module provides the Ballot class for representing voter preferences,
along with utilities for generating ballots and analyzing voter types.
"""

import random
from typing import List, Dict, Tuple, Optional


class Ballot:
    """
    Represents a single ballot with a complete ranking of candidates.
    
    A ballot contains a linear order (total order) of all candidates,
    where earlier positions indicate stronger preference.
    
    Attributes:
        ranking (tuple): Immutable tuple of candidates in preference order.
                        First element is most preferred, last is least preferred.
    """
    
    def __init__(self, ranking: List[str]):
        """
        Initialize a ballot with a ranking of candidates.
        
        Args:
            ranking: List of candidate names in preference order (first = most preferred)
        
        Raises:
            ValueError: If ranking is empty or contains duplicate candidates
        """
        if not ranking:
            raise ValueError("Ranking cannot be empty")
        if len(ranking) != len(set(ranking)):
            raise ValueError("Ranking contains duplicate candidates")
        
        self.ranking = tuple(ranking)  # Store as immutable tuple
    
    def prefers(self, cand_a: str, cand_b: str) -> bool:
        """
        Determine if this ballot prefers candidate A over candidate B.
        
        Args:
            cand_a: First candidate name
            cand_b: Second candidate name
        
        Returns:
            True if cand_a is ranked higher (earlier) than cand_b, False otherwise
        
        Raises:
            ValueError: If either candidate is not in the ranking
        
        DO NOT MODIFY THIS METHOD
        """
        if cand_a not in self.ranking:
            raise ValueError(f"Candidate '{cand_a}' not in ballot")
        if cand_b not in self.ranking:
            raise ValueError(f"Candidate '{cand_b}' not in ballot")
        
        return self.ranking.index(cand_a) < self.ranking.index(cand_b)
    
    def get_ranking(self) -> List[str]:
        """
        Get the complete ranking of candidates.
        
        Returns:
            List of candidates in preference order (first = most preferred)
        
        DO NOT MODIFY THIS METHOD
        """
        return list(self.ranking)
    
    def __eq__(self, other):
        """Check equality based on ranking."""
        if not isinstance(other, Ballot):
            return False
        return self.ranking == other.ranking
    
    def __hash__(self):
        """Allow Ballot objects to be used in sets and as dict keys."""
        return hash(self.ranking)
    
    def __repr__(self):
        """String representation of the ballot."""
        return f"Ballot({' > '.join(self.ranking)})"


def aggregate_ballot_types(ballots: List[Ballot]) -> Dict[Ballot, int]:
    """
    Aggregate identical ballots into voter types.
    
    Groups ballots with the same ranking together and counts how many
    voters have each unique ranking pattern. Useful for tactical voting
    analysis where we want to consider each voter "type" separately.
    
    Args:
        ballots: List of Ballot objects
    
    Returns:
        Dictionary mapping each unique Ballot to the count of voters with that ranking
    
    Example:
        If 3 voters rank [A, B, C] and 2 voters rank [B, A, C],
        returns {Ballot([A, B, C]): 3, Ballot([B, A, C]): 2}
    
    DO NOT MODIFY THIS FUNCTION
    """
    type_counts = {}
    for ballot in ballots:
        type_counts[ballot] = type_counts.get(ballot, 0) + 1
    return type_counts


def generate_random_ballots(num_voters: int, candidates: List[str]) -> List[Ballot]:
    """
    Generate random ballots with uniformly random preference orderings.
    
    Each ballot is an independent random permutation of all candidates.
    
    Args:
        num_voters: Number of ballots to generate
        candidates: List of candidate names
    
    Returns:
        List of Ballot objects with random rankings
    
    DO NOT MODIFY THIS FUNCTION
    """
    ballots = []
    for _ in range(num_voters):
        ranking = candidates.copy()
        random.shuffle(ranking)
        ballots.append(Ballot(ranking))
    return ballots


def generate_single_peaked_ballots(num_voters: int, 
                                   candidates: List[str], 
                                   spectrum: Optional[List[str]] = None,
                                   seed: Optional[int] = None) -> List[Ballot]:
    """
    Generate ballots with single-peaked preferences over a political spectrum.
    
    Single-peaked preferences assume candidates are positioned on a linear
    spectrum (e.g., left to right politically). Each voter has an ideal point
    on this spectrum and prefers candidates closer to their ideal point.
    
    Args:
        num_voters: Number of ballots to generate
        candidates: List of candidate names
        spectrum: Optional ordering of candidates on the political spectrum.
                 If None, uses the order of the candidates list as the spectrum.
        seed: Optional random seed for reproducibility
    
    Returns:
        List of Ballot objects with single-peaked preferences
    
    Algorithm:
        1. Position candidates on a linear spectrum
        2. For each voter, randomly choose an ideal point on the spectrum
        3. Rank candidates by distance from ideal point (closer = more preferred)
    
    DO NOT MODIFY THIS FUNCTION
    """
    if seed is not None:
        random.seed(seed)
    
    if spectrum is None:
        spectrum = candidates.copy()
    else:
        # Verify spectrum contains exactly the same candidates
        if set(spectrum) != set(candidates):
            raise ValueError("Spectrum must contain exactly the same candidates")
    
    ballots = []
    for _ in range(num_voters):
        # Choose random ideal point on spectrum (can be between candidates)
        ideal_position = random.uniform(0, len(spectrum) - 1)
        # Add small noise to avoid exact equidistance (ensures Condorcet winner exists)
        ideal_position += random.uniform(-0.001, 0.001)
        
        # Rank candidates by distance from ideal point
        candidates_with_distance = []
        for i, candidate in enumerate(spectrum):
            distance = abs(i - ideal_position)
            candidates_with_distance.append((distance, candidate))
        
        # Sort by distance (ascending) - noise ensures no ties
        candidates_with_distance.sort(key=lambda x: x[0])
        
        # Extract ranking
        ranking = [candidate for _, candidate in candidates_with_distance]
        ballots.append(Ballot(ranking))
    
    return ballots
