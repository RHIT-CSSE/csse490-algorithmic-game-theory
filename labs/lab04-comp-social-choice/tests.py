"""
Unit tests for ranked voting systems.

This test suite verifies the correctness of:
- Ballot class and utility functions
- Voting algorithm implementations
- Condorcet winner detection
- Tactical voting analysis
"""

import unittest
from ballot import Ballot, aggregate_ballot_types, generate_random_ballots, generate_single_peaked_ballots
import algorithms
import tactical_voting


class TestBallotFunctions(unittest.TestCase):
    """Test ballot representation and utility functions."""
    
    def setUp(self):
        """Set up common test data."""
        self.candidates = ['A', 'B', 'C']
        self.ballot1 = Ballot(['A', 'B', 'C'])
        self.ballot2 = Ballot(['B', 'C', 'A'])
        self.ballot3 = Ballot(['A', 'B', 'C'])  # Same as ballot1
    
    def test_ballot_creation(self):
        """Test basic ballot creation."""
        ballot = Ballot(['A', 'B', 'C'])
        self.assertEqual(ballot.get_ranking(), ['A', 'B', 'C'])
    
    def test_ballot_invalid_empty(self):
        """Test that empty rankings are rejected."""
        with self.assertRaises(ValueError):
            Ballot([])
    
    def test_ballot_invalid_duplicates(self):
        """Test that duplicate candidates are rejected."""
        with self.assertRaises(ValueError):
            Ballot(['A', 'B', 'A'])
    
    def test_prefers_first_over_second(self):
        """Test preference comparison: first over second."""
        self.assertTrue(self.ballot1.prefers('A', 'B'))
        self.assertTrue(self.ballot1.prefers('A', 'C'))
        self.assertTrue(self.ballot1.prefers('B', 'C'))
    
    def test_prefers_second_not_over_first(self):
        """Test preference comparison: second not over first."""
        self.assertFalse(self.ballot1.prefers('B', 'A'))
        self.assertFalse(self.ballot1.prefers('C', 'A'))
        self.assertFalse(self.ballot1.prefers('C', 'B'))
    
    def test_prefers_different_ballot(self):
        """Test preferences with different ballot ranking."""
        self.assertTrue(self.ballot2.prefers('B', 'A'))
        self.assertTrue(self.ballot2.prefers('C', 'A'))
        self.assertFalse(self.ballot2.prefers('A', 'B'))
    
    def test_prefers_invalid_candidate(self):
        """Test that comparing unknown candidates raises error."""
        with self.assertRaises(ValueError):
            self.ballot1.prefers('A', 'X')
    
    def test_ballot_equality(self):
        """Test ballot equality based on ranking."""
        self.assertEqual(self.ballot1, self.ballot3)
        self.assertNotEqual(self.ballot1, self.ballot2)
    
    def test_ballot_hash(self):
        """Test that ballots can be hashed (for use in dicts/sets)."""
        ballot_set = {self.ballot1, self.ballot2, self.ballot3}
        self.assertEqual(len(ballot_set), 2)  # ballot1 and ballot3 are equal
    
    def test_aggregate_ballot_types(self):
        """Test aggregation of identical ballots into types."""
        ballots = [self.ballot1, self.ballot2, self.ballot3, self.ballot1]
        types = aggregate_ballot_types(ballots)
        
        self.assertEqual(len(types), 2)
        self.assertEqual(types[self.ballot1], 3)  # ballot1 appears 3 times (including ballot3)
        self.assertEqual(types[self.ballot2], 1)
    
    def test_generate_random_ballots(self):
        """Test random ballot generation."""
        ballots = generate_random_ballots(10, self.candidates)
        
        self.assertEqual(len(ballots), 10)
        for ballot in ballots:
            # Each ballot should have all candidates
            self.assertEqual(set(ballot.get_ranking()), set(self.candidates))
    
    def test_generate_single_peaked_ballots(self):
        """Test single-peaked ballot generation."""
        spectrum = ['A', 'B', 'C']
        ballots = generate_single_peaked_ballots(10, self.candidates, spectrum)
        
        self.assertEqual(len(ballots), 10)
        for ballot in ballots:
            # Each ballot should have all candidates
            self.assertEqual(set(ballot.get_ranking()), set(self.candidates))
    
    def test_single_peaked_with_default_spectrum(self):
        """Test single-peaked generation with default spectrum."""
        ballots = generate_single_peaked_ballots(5, self.candidates)
        self.assertEqual(len(ballots), 5)


class TestVotingAlgorithms(unittest.TestCase):
    """Test voting algorithm implementations."""
    
    def setUp(self):
        """Set up common test data."""
        # Clear Condorcet winner: A beats all others
        self.ballots_condorcet = [
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'C', 'B']),
            Ballot(['B', 'A', 'C']),
            Ballot(['C', 'A', 'B']),
        ]
        self.candidates_abc = ['A', 'B', 'C']
        
        # Condorcet paradox: A>B, B>C, C>A
        self.ballots_cycle = [
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'B', 'C']),
            Ballot(['B', 'C', 'A']),
            Ballot(['B', 'C', 'A']),
            Ballot(['C', 'A', 'B']),
            Ballot(['C', 'A', 'B']),
        ]
        
        # Unanimous: everyone ranks A first
        self.ballots_unanimous = [
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'B', 'C']),
        ]
    
    def test_head_to_head_matrix(self):
        """Test head-to-head matrix computation."""
        h2h = algorithms.get_head_to_head_matrix(self.ballots_condorcet, self.candidates_abc)
        
        # A should beat B (4 votes to 1)
        self.assertEqual(h2h[('A', 'B')], 4)
        self.assertEqual(h2h[('B', 'A')], 1)
        
        # A should beat C (4 votes to 1)
        self.assertEqual(h2h[('A', 'C')], 4)
        self.assertEqual(h2h[('C', 'A')], 1)
    
    def test_head_to_head_cycle(self):
        """Test head-to-head matrix with Condorcet paradox."""
        h2h = algorithms.get_head_to_head_matrix(self.ballots_cycle, self.candidates_abc)
        
        # Should have cycle: A>B>C>A (each by 4-2)
        self.assertEqual(h2h[('A', 'B')], 4)
        self.assertEqual(h2h[('B', 'C')], 4)
        self.assertEqual(h2h[('C', 'A')], 4)
    
    def test_copeland_condorcet_winner(self):
        """Test Copeland with clear Condorcet winner."""
        winners, scores = algorithms.copeland(self.ballots_condorcet, self.candidates_abc)
        
        self.assertIn('A', winners)
        self.assertGreater(scores['A'], scores['B'])
        self.assertGreater(scores['A'], scores['C'])
    
    def test_copeland_unanimous(self):
        """Test Copeland with unanimous preferences."""
        winners, scores = algorithms.copeland(self.ballots_unanimous, self.candidates_abc)
        
        self.assertEqual(winners, ['A'])
        self.assertEqual(scores['A'], 2.0)  # Beats both B and C
    
    def test_copeland_returns_correct_format(self):
        """Test that Copeland returns (list, dict) format."""
        winners, scores = algorithms.copeland(self.ballots_condorcet, self.candidates_abc)
        
        self.assertIsInstance(winners, list)
        self.assertIsInstance(scores, dict)
        self.assertEqual(set(scores.keys()), set(self.candidates_abc))
    
    def test_borda_count_unanimous(self):
        """Test Borda count with unanimous preferences."""
        winners, scores = algorithms.borda_count(self.ballots_unanimous, self.candidates_abc)
        
        self.assertEqual(winners, ['A'])
        # Each ballot: A gets 2 points, B gets 1, C gets 0
        self.assertEqual(scores['A'], 6)  # 3 ballots * 2 points
        self.assertEqual(scores['B'], 3)  # 3 ballots * 1 point
        self.assertEqual(scores['C'], 0)  # 3 ballots * 0 points
    
    def test_borda_count_returns_correct_format(self):
        """Test that Borda count returns (list, dict) format."""
        winners, scores = algorithms.borda_count(self.ballots_condorcet, self.candidates_abc)
        
        self.assertIsInstance(winners, list)
        self.assertIsInstance(scores, dict)
        self.assertEqual(set(scores.keys()), set(self.candidates_abc))
    
    def test_schulze_condorcet_winner(self):
        """Test Schulze with clear Condorcet winner."""
        winners, scores = algorithms.schulze(self.ballots_condorcet, self.candidates_abc)
        
        # Schulze should elect the Condorcet winner
        self.assertIn('A', winners)
    
    def test_schulze_returns_correct_format(self):
        """Test that Schulze returns (list, dict) format."""
        winners, scores = algorithms.schulze(self.ballots_condorcet, self.candidates_abc)
        
        self.assertIsInstance(winners, list)
        self.assertIsInstance(scores, dict)
        self.assertEqual(set(scores.keys()), set(self.candidates_abc))


class TestCondorcetAnalysis(unittest.TestCase):
    """Test Condorcet winner detection."""
    
    def test_condorcet_winner_exists(self):
        """Test detection when Condorcet winner exists."""
        ballots = [
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'C', 'B']),
            Ballot(['B', 'A', 'C']),
            Ballot(['C', 'A', 'B']),
        ]
        candidates = ['A', 'B', 'C']
        
        winner = algorithms.find_condorcet_winner(ballots, candidates)
        self.assertEqual(winner, 'A')
    
    def test_condorcet_paradox(self):
        """Test detection when no Condorcet winner exists (cycle)."""
        ballots = [
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'B', 'C']),
            Ballot(['B', 'C', 'A']),
            Ballot(['B', 'C', 'A']),
            Ballot(['C', 'A', 'B']),
            Ballot(['C', 'A', 'B']),
        ]
        candidates = ['A', 'B', 'C']
        
        winner = algorithms.find_condorcet_winner(ballots, candidates)
        self.assertIsNone(winner)
    
    def test_condorcet_unanimous(self):
        """Test Condorcet winner with unanimous preferences."""
        ballots = [
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'B', 'C']),
        ]
        candidates = ['A', 'B', 'C']
        
        winner = algorithms.find_condorcet_winner(ballots, candidates)
        self.assertEqual(winner, 'A')


class TestTacticalVoting(unittest.TestCase):
    """Test tactical voting analysis."""
    
    def setUp(self):
        """Set up common test data."""
        self.ballots = [
            Ballot(['A', 'B', 'C']),
            Ballot(['A', 'B', 'C']),
            Ballot(['B', 'C', 'A']),
            Ballot(['B', 'C', 'A']),
            Ballot(['C', 'A', 'B']),
        ]
        self.candidates = ['A', 'B', 'C']
    
    def test_simulate_election_no_change(self):
        """Test election simulation with non-existent voter type."""
        fake_type = Ballot(['X', 'Y', 'Z'])
        
        # Should return same result as original when type doesn't exist
        winners, scores = tactical_voting.simulate_election_with_modified_ballots(
            self.ballots,
            fake_type,
            ['A', 'B', 'C'],
            algorithms.copeland,
            self.candidates
        )
        
        # Should have returned some result (exact result depends on copeland implementation)
        self.assertIsInstance(winners, list)
        self.assertIsInstance(scores, dict)
    
    def test_simulate_election_with_modification(self):
        """Test election simulation with actual ballot modification."""
        voter_type = Ballot(['A', 'B', 'C'])
        new_ranking = ['C', 'B', 'A']
        
        # Get original result
        original_winners, original_scores = algorithms.copeland(self.ballots, self.candidates)
        
        # Get modified result
        modified_winners, modified_scores = tactical_voting.simulate_election_with_modified_ballots(
            self.ballots,
            voter_type,
            new_ranking,
            algorithms.copeland,
            self.candidates
        )
        
        # Results should potentially be different (depends on specific scenario)
        self.assertIsInstance(modified_winners, list)
        self.assertIsInstance(modified_scores, dict)
    
    def test_find_tactical_opportunities_format(self):
        """Test that tactical opportunity detection returns correct format."""
        voter_type = Ballot(['A', 'B', 'C'])
        
        opportunities = tactical_voting.find_tactical_opportunities(
            voter_type,
            self.ballots,
            algorithms.copeland,
            self.candidates
        )
        
        self.assertIsInstance(opportunities, list)
        
        # Each opportunity should be a dict with required keys
        for opp in opportunities:
            self.assertIsInstance(opp, dict)
            self.assertIn('original_winners', opp)
            self.assertIn('alternative_ranking', opp)
            self.assertIn('new_winners', opp)
            self.assertIn('benefit', opp)


class TestIntegration(unittest.TestCase):
    """Integration tests across multiple components."""
    
    def test_full_election_workflow(self):
        """Test complete election workflow with all three methods."""
        candidates = ['A', 'B', 'C', 'D']
        ballots = generate_random_ballots(20, candidates)
        
        # All three methods should complete without error
        copeland_result = algorithms.copeland(ballots, candidates)
        borda_result = algorithms.borda_count(ballots, candidates)
        schulze_result = algorithms.schulze(ballots, candidates)
        
        # All should return correct format
        for result in [copeland_result, borda_result, schulze_result]:
            winners, scores = result
            self.assertIsInstance(winners, list)
            self.assertIsInstance(scores, dict)
            self.assertTrue(len(winners) > 0)
            self.assertEqual(set(scores.keys()), set(candidates))
    
    def test_single_peaked_reduces_paradoxes(self):
        """Test that single-peaked preferences often have Condorcet winners."""
        candidates = ['A', 'B', 'C', 'D', 'E']
        
        # Generate multiple single-peaked elections
        condorcet_exists_count = 0
        num_trials = 10
        
        for _ in range(num_trials):
            ballots = generate_single_peaked_ballots(30, candidates)
            winner = algorithms.find_condorcet_winner(ballots, candidates)
            if winner is not None:
                condorcet_exists_count += 1
        
        # Most single-peaked elections should have Condorcet winners
        # (Not all, but significantly more than random elections)
        self.assertGreater(condorcet_exists_count, 0)


if __name__ == '__main__':
    unittest.main()
