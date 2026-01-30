"""
Experimental framework for exploring ranked voting systems.

This module provides pre-configured experiments for Activities 1-3:
- Activity 1: Implement and analyze ranked voting systems
- Activity 2: Analyze effects of single-peaked preferences
- Activity 3: Investigate tactical voting
"""
from colorama import Fore

from ballot import Ballot, generate_random_ballots, generate_single_peaked_ballots
import algorithms
import tactical_voting


def run_activity1():
    """
    Activity 1: Implement and Analyze Ranked Voting Systems
    
    Tasks:
    (a) Which voting systems are Condorcet methods?
        (A Condorcet method always elects the Condorcet winner when one exists)
    (b) Which voting systems can be implemented efficiently (polynomial time)?
    """
    # TODO: Consider toggling these flags to show/hide certain outputs
    show_head_to_head_results = True
    show_num_voter_and_candidate_list = True

    print("\n" + "="*70)
    print("ACTIVITY 1: IMPLEMENT AND ANALYZE RANKED VOTING SYSTEMS")
    print("="*70)
    
    # Example 1: Clear Condorcet winner
    print("\n" + "-"*70)
    print("Example 1: Clear Condorcet Winner")
    print("-"*70)
    
    ballots_1 = [
        Ballot(['A', 'B', 'C']),
        Ballot(['A', 'B', 'C']),
        Ballot(['A', 'C', 'B']),
        Ballot(['A', 'C', 'B']),
        Ballot(['B', 'A', 'C']),
        Ballot(['C', 'A', 'B']),
    ]
    candidates_1 = ['A', 'B', 'C']
    
    run_all_voting_systems(ballots_1, candidates_1, show_head_to_head_results, show_num_voter_and_candidate_list)
    
    # Example 2: Rock-paper-scissors
    print("\n" + "-"*70)
    print("Example 2: Rock-paper-scissors")
    print("-"*70)
    
    ballots_2 = [
        Ballot(['A', 'B', 'C']),
        Ballot(['A', 'B', 'C']),
        Ballot(['B', 'C', 'A']),
        Ballot(['B', 'C', 'A']),
        Ballot(['C', 'A', 'B']),
        Ballot(['C', 'A', 'B']),
    ]
    candidates_2 = ['A', 'B', 'C']
    
    run_all_voting_systems(ballots_2, candidates_2, show_head_to_head_results, show_num_voter_and_candidate_list)
    
    # Example 3: Narrow win, but for whom?
    print("\n" + "-"*70)
    print("Example 3: Narrow win, but for whom?")
    print("-"*70)
    
    ballots_3 = [
        Ballot(['A', 'B', 'C']),
        Ballot(['A', 'B', 'C']),
        Ballot(['A', 'B', 'C']),
        Ballot(['A', 'B', 'C']),
        Ballot(['A', 'B', 'C']),
        Ballot(['A', 'B', 'C']),
        Ballot(['B', 'C', 'A']),
        Ballot(['B', 'C', 'A']),
        Ballot(['B', 'C', 'A']),
        Ballot(['C', 'B', 'A']),
        Ballot(['C', 'B', 'A']),
    ]
    candidates_3 = ['A', 'B', 'C']
    
    run_all_voting_systems(ballots_3, candidates_3, show_head_to_head_results, show_num_voter_and_candidate_list)
    
    # Example 4: Four-candidate election with interesting properties
    print("\n" + "-"*70)
    print("Example 4: Four Candidates, Methods Disagree")
    print("-"*70)
    
    ballots_4 = [
        Ballot(['A', 'B', 'C', 'D']),
        Ballot(['A', 'B', 'C', 'D']),
        Ballot(['A', 'B', 'C', 'D']),
        Ballot(['B', 'C', 'D', 'A']),
        Ballot(['B', 'C', 'D', 'A']),
        Ballot(['C', 'D', 'A', 'B']),
        Ballot(['C', 'D', 'A', 'B']),
        Ballot(['D', 'A', 'B', 'C']),
    ]
    candidates_4 = ['A', 'B', 'C', 'D']
    
    run_all_voting_systems(ballots_4, candidates_4, show_head_to_head_results, show_num_voter_and_candidate_list)
    
    # Example 5: Effect of irrelevant candidates
    print("\n" + "-"*70)
    print("Example 5: Effect of Irrelevant Candidates")
    print("-"*70)
    
    # First election with just A and B
    print("Sub-example 5a: Two-candidate election (A vs B)")
    print("Voters at positions 0-5 prefer A, voters at positions 6-10 prefer B\n")
    ballots_5a = [
        Ballot(['A', 'B']),  # voter 0
        Ballot(['A', 'B']),  # voter 1
        Ballot(['A', 'B']),  # voter 2
        Ballot(['A', 'B']),  # voter 3
        Ballot(['A', 'B']),  # voter 4
        Ballot(['A', 'B']),  # voter 5
        Ballot(['B', 'A']),  # voter 6
        Ballot(['B', 'A']),  # voter 7
        Ballot(['B', 'A']),  # voter 8
        Ballot(['B', 'A']),  # voter 9
        Ballot(['B', 'A']),  # voter 10
    ]
    candidates_5a = ['A', 'B']
    run_all_voting_systems(ballots_5a, candidates_5a, show_head_to_head_results, show_num_voter_and_candidate_list)
    
    # Second election with A, B, C, D (irrelevant candidates C and D enter)
    print("\n" + "-"*40)
    print("Sub-example 5b: Four-candidate election (A, B, C, D)")
    print("Same voter preferences, but C and D enter to the right of A and B\n")
    print("Voters rank candidates by spatial proximity")
    ballots_5b = [
        Ballot(['A', 'B', 'C', 'D']),  # voter 0
        Ballot(['A', 'B', 'C', 'D']),  # voter 1
        Ballot(['A', 'B', 'C', 'D']),  # voter 2
        Ballot(['A', 'B', 'C', 'D']),  # voter 3
        Ballot(['A', 'B', 'C', 'D']),  # voter 4
        Ballot(['A', 'B', 'C', 'D']),  # voter 5
        Ballot(['B', 'A', 'C', 'D']),  # voter 6
        Ballot(['B', 'C', 'A', 'D']),  # voter 7
        Ballot(['C', 'B', 'D', 'A']),  # voter 8
        Ballot(['C', 'D', 'B', 'A']),  # voter 9
        Ballot(['D', 'C', 'B', 'A']),  # voter 10
    ]
    candidates_5b = ['A', 'B', 'C', 'D']
    run_all_voting_systems(ballots_5b, candidates_5b, show_head_to_head_results, show_num_voter_and_candidate_list)


def run_activity2():
    """
    Activity 2: Analyze Effects of Single-Peaked Preferences
    
    Task: Compare voting system behavior with random vs single-peaked preferences
    """
    # TODO: Consider toggling these flags to show/hide certain outputs
    show_head_to_head_results = True
    show_num_voter_and_candidate_list = True

    print("\n" + "="*70)
    print("ACTIVITY 2: ANALYZE EFFECTS OF SINGLE-PEAKED PREFERENCES")
    print("="*70)
    
    candidates = ['Left', 'Center-Left', 'Center', 'Center-Right', 'Right']
    num_voters = 51  # Odd number to avoid ties in head-to-head matchups
    
    # Random preferences
    print("\n" + "-"*70)
    print("Experiment A: Random Preferences")
    print("-"*70)
    print(f"Generating {num_voters} ballots with uniformly random preferences\n")
    
    random_ballots = generate_random_ballots(num_voters, candidates)
    run_all_voting_systems(random_ballots, candidates, show_head_to_head_results, show_num_voter_and_candidate_list)
    
    # Single-peaked preferences
    print("\n" + "-"*70)
    print("Experiment B: Single-Peaked Preferences")
    print("-"*70)
    print(f"Generating {num_voters} ballots with single-peaked preferences")
    print(f"Political spectrum (left to right): \n\t{' → '.join(candidates)}\n")
    
    spectrum = ['Left', 'Center-Left', 'Center', 'Center-Right', 'Right']
    single_peaked_ballots = generate_single_peaked_ballots(num_voters, candidates, spectrum, seed=8675309)
    run_all_voting_systems(single_peaked_ballots, candidates, show_head_to_head_results, show_num_voter_and_candidate_list)


def run_activity3():
    """
    Activity 3: Investigate Tactical Voting
    
    Task: Analyze whether voter groups can benefit from misreporting preferences
    """
    print("\n" + "="*70)
    print("ACTIVITY 3: INVESTIGATE TACTICAL VOTING")
    print("="*70)
    
    # Example with potential for tactical voting
    print("\nScenario: Small election\n")
    
    ballots = [
        Ballot(['A', 'B', 'C']),
        Ballot(['A', 'B', 'C']),
        Ballot(['A', 'B', 'C']),
        Ballot(['B', 'A', 'C']),
        Ballot(['B', 'A', 'C']),
        Ballot(['C', 'B', 'A']),
        Ballot(['C', 'B', 'A']),
    ]
    candidates = ['A', 'B', 'C']
    
    tactical_voting.run_tactical_voting_experiments(ballots, candidates)
    
    # Larger random example
    print("\n" + "-"*70)
    print("Additional Experiment: Larger Random Election")
    print("-"*70)
    
    larger_ballots = generate_random_ballots(30, ['A', 'B', 'C', 'D'])
    larger_candidates = ['A', 'B', 'C', 'D']
    
    tactical_voting.run_tactical_voting_experiments(larger_ballots, larger_candidates)


def run_all_voting_systems(ballots, candidates, show_head_to_head_results=True, show_num_voter_and_candidate_list=True):
    """
    Helper function: Run all three voting systems on given ballots.
    
    Args:
        ballots: List of Ballot objects
        candidates: List of candidate names
        show_head_to_head_results: Whether to display head-to-head comparison matrix
        show_num_voter_and_candidate_list: Whether to display voter count and candidate list
    """
    if show_num_voter_and_candidate_list:
        print(f"\nNumber of voters: {len(ballots)}")
        print(f"Candidates: {', '.join(candidates)}\n")
    
    # Check for Condorcet winner
    print("Condorcet Analysis:")
    try:
        condorcet = algorithms.find_condorcet_winner(ballots, candidates)
        if condorcet:
            print(f"  {Fore.GREEN}✓{Fore.RESET} Condorcet winner exists: {condorcet}")
        else:
            print(f"  {Fore.RED}✗{Fore.RESET} No Condorcet winner (Condorcet paradox)")
    except NotImplementedError:
        print("  Not yet implemented")
    
    # Head-to-head matrix for reference
    if show_head_to_head_results:
        print("\nHead-to-Head Results:")
        h2h = algorithms.get_head_to_head_matrix(ballots, candidates)
        for cand_a in candidates:
            for cand_b in candidates:
                if cand_a < cand_b:  # Only show each pair once
                    a_over_b = h2h.get((cand_a, cand_b), 0)
                    b_over_a = h2h.get((cand_b, cand_a), 0)
                    print(f"  {cand_a} vs {cand_b}: {a_over_b} - {b_over_a}", end="")
                    if a_over_b > b_over_a:
                        print(f" ({cand_a} wins)")
                    elif b_over_a > a_over_b:
                        print(f" ({cand_b} wins)")
                    else:
                        print(" (tie)")
    
    methods = {"Copeland's Method": algorithms.copeland,
               "Borda Count":       algorithms.borda_count,
               "Schulze Method":    algorithms.schulze}

    for method_name, method_func in methods.items():
        print(f"\n{method_name}:")
        try:
            winners, scores = method_func(ballots, candidates)
            print(f"  Winners: {{{', '.join(winners)}}}")
            
            # Print scores with 70-character line wrapping
            print_line_wrap(f"  Scores:  {scores}", indent=11, max_length=70)
            
        except NotImplementedError:
            print(f"  {Fore.RED}Not yet implemented{Fore.RESET}")


def print_line_wrap(text, indent=0, max_length=70):
    """
    Helper function to print long text with line wrapping. 
    Attempts to line wrap at space characters for readability. 
    
    Args:
        text: The text to print
        indent: Number of spaces to indent each line
        max_length: Maximum length of each line
    """
    if len(text) <= max_length:
        print(text)
        return
    
    # Print first line
    if len(text) <= max_length:
        print(text)
        return
    
    # Find last space before max_length
    break_point = text[:max_length].rfind(' ')
    if break_point == -1:  # No space found, break at max_length
        break_point = max_length
    
    print(text[:break_point])
    remaining = text[break_point:].lstrip()
    
    # Print remaining lines with indentation
    while remaining:
        if len(remaining) <= max_length - indent:
            print(f"{' ' * indent}{remaining}")
            break
        
        # Find last space before max_length - indent
        break_point = remaining[:max_length - indent].rfind(' ')
        if break_point == -1:  # No space found, break at max_length - indent
            break_point = max_length - indent
        
        print(f"{' ' * indent}{remaining[:break_point]}")
        remaining = remaining[break_point:].lstrip()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("LAB 4: COMPUTATIONAL SOCIAL CHOICE - RANKED VOTING SYSTEMS")
    print("="*70)
    
    run_activity1()
    # run_activity2() # TODO: Uncomment to run Activity 2
    # run_activity3() # TODO: Uncomment to run Activity 3
