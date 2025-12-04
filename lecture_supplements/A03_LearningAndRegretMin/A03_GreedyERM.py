# Visualization of Greedy ERM algorithm for 1D data
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt


def construct_worst_case_scenario(N, num_increments):
    """
    Construct a worst-case loss sequence for the greedy algorithm.
    
    The worst case occurs when:
    - We always pick the worst possible action from S^t (actions with min cumulative loss)
    - We pick N actions that give us a loss of 1 between increments of L_min
    
    Args:
        N: Number of actions
        num_increments: Number of times L_min increases
    
    Returns:
        losses: T x N matrix where losses[t, i] is the loss of action i at time t
        greedy_actions: List of actions chosen by greedy algorithm
    """
    T = N * num_increments + (N - 1)  # Worst case: N losses per increment + (N-1) at end
    losses = np.zeros((T, N))
    
    t = 0
    # For each increment of L_min, make greedy suffer N losses of 1
    for increment in range(num_increments):
        for action in range(N):
            # All actions except 'action' get loss 0, 'action' gets loss 1
            losses[t, action] = 1
            t += 1
    
    # After L_min reaches its final value, greedy can suffer up to N-1 more losses
    for extra in range(min(N - 1, T - t)):
        losses[t, extra] = 1
        t += 1
    
    return losses[:t]


def simulate_greedy_algorithm(losses):
    """
    Simulate the greedy algorithm on a sequence of losses.
    
    Args:
        losses: T x N matrix of losses
    
    Returns:
        greedy_actions: List of actions chosen at each time step
        cumulative_losses: T x N matrix of cumulative losses through time t
        greedy_cumulative: Array of greedy's cumulative loss at each time
    """
    T, N = losses.shape
    greedy_actions = []
    cumulative_losses = np.zeros((T, N))
    greedy_cumulative = np.zeros(T)
    
    for t in range(T):
        if t == 0:
            # Start with action 0 (index 0)
            action = 0
        else:
            # Pick action with minimum cumulative loss (break ties by choosing lowest index)
            min_loss = cumulative_losses[t-1].min()
            action = np.where(cumulative_losses[t-1] == min_loss)[0][0]
        
        greedy_actions.append(action)
        
        # Update cumulative losses
        if t == 0:
            cumulative_losses[t] = losses[t]
        else:
            cumulative_losses[t] = cumulative_losses[t-1] + losses[t]
        
        # Update greedy's cumulative loss
        if t == 0:
            greedy_cumulative[t] = losses[t, action]
        else:
            greedy_cumulative[t] = greedy_cumulative[t-1] + losses[t, action]
    
    return greedy_actions, cumulative_losses, greedy_cumulative


def visualize_worst_case(N=3, num_increments=2):
    """
    Visualize the worst-case performance of the greedy algorithm.
    
    Uses vertical bars to show:
    - Cumulative losses of each single action
    - Cumulative loss of the greedy algorithm
    """
    # Construct worst-case scenario
    losses = construct_worst_case_scenario(N, num_increments)
    T = len(losses)
    
    # Simulate greedy algorithm
    greedy_actions, cumulative_losses, greedy_cumulative = simulate_greedy_algorithm(losses)
    
    # Calculate final values
    final_losses = cumulative_losses[-1]
    min_loss = final_losses.min()
    greedy_loss = greedy_cumulative[-1]
    
    # Theoretical bound: L_Greedy <= N * L_min + (N - 1)
    theoretical_bound = N * min_loss + (N - 1)
    
    # Create visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left plot: Bar chart of cumulative losses
    positions = np.arange(N + 1)
    bar_heights = list(final_losses) + [greedy_loss]
    colors = ['steelblue'] * N + ['crimson']
    labels = [f'Action {i}' for i in range(N)] + ['Greedy']
    
    bars = ax1.bar(positions, bar_heights, color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)
    
    # Add horizontal line for best single action
    ax1.axhline(y=min_loss, color='green', linestyle='--', linewidth=2, 
                label=f'$L_{{min}}^T$ = {min_loss:.0f}')
    
    # Add horizontal line for theoretical bound
    ax1.axhline(y=theoretical_bound, color='orange', linestyle=':', linewidth=2,
                label=f'Bound: $N \\cdot L_{{min}}^T + (N-1)$ = {theoretical_bound:.0f}')
    
    # Annotations
    ax1.set_xlabel('Action / Algorithm', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Cumulative Loss', fontsize=12, fontweight='bold')
    ax1.set_title(f'Final Cumulative Losses (N={N}, T={T})', fontsize=14, fontweight='bold')
    ax1.set_xticks(positions)
    ax1.set_xticklabels(labels, fontsize=10)
    ax1.legend(fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for i, (bar, height) in enumerate(zip(bars, bar_heights)):
        ax1.text(bar.get_x() + bar.get_width()/2, height + 0.5, f'{height:.0f}',
                ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Right plot: Evolution over time
    for i in range(N):
        ax2.plot(range(T), cumulative_losses[:, i], marker='o', markersize=4,
                label=f'Action {i}', alpha=0.7)
    
    ax2.plot(range(T), greedy_cumulative, marker='s', markersize=5,
            color='crimson', linewidth=2.5, label='Greedy', alpha=0.8)
    
    ax2.set_xlabel('Time Step $t$', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Cumulative Loss $L^t$', fontsize=12, fontweight='bold')
    ax2.set_title('Evolution of Cumulative Losses Over Time', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(alpha=0.3)
    
    plt.tight_layout()
    
    # Print summary statistics
    print(f"=== Worst-Case Analysis for Greedy ERM ===")
    print(f"Number of actions (N): {N}")
    print(f"Time horizon (T): {T}")
    print(f"Number of L_min increments: {num_increments}")
    print()
    print(f"Final cumulative losses:")
    for i in range(N):
        marker = " ← Best" if final_losses[i] == min_loss else ""
        print(f"  Action {i}: {final_losses[i]:.0f}{marker}")
    print(f"  Greedy:    {greedy_loss:.0f}")
    print()
    print(f"L_min^T = {min_loss:.0f}")
    print(f"L_Greedy^T = {greedy_loss:.0f}")
    print(f"Theoretical bound: N × L_min^T + (N-1) = {N} × {min_loss:.0f} + {N-1} = {theoretical_bound:.0f}")
    print(f"Actual regret: L_Greedy^T - L_min^T = {greedy_loss - min_loss:.0f}")
    print(f"Bound satisfied: {greedy_loss <= theoretical_bound}")
    
    return fig, losses, greedy_actions, cumulative_losses, greedy_cumulative


if __name__ == "__main__":
    # Example 1: Small case (N=3, easier to understand)
    print("Example 1: N=3 actions, 2 increments of L_min")
    print("=" * 60)
    fig1, losses1, actions1, cum_losses1, greedy_cum1 = visualize_worst_case(N=3, num_increments=2)
    fig1.savefig('greedy_erm_example1_N3.png', dpi=150, bbox_inches='tight')
    print("\n→ Saved visualization to greedy_erm_example1_N3.png")
    
    print("\n" + "=" * 60)
    print("\nExample 2: N=5 actions, 3 increments of L_min")
    print("=" * 60)
    fig2, losses2, actions2, cum_losses2, greedy_cum2 = visualize_worst_case(N=5, num_increments=3)
    fig2.savefig('greedy_erm_example2_N5.png', dpi=150, bbox_inches='tight')
    print("\n→ Saved visualization to greedy_erm_example2_N5.png")
    
    print("\n" + "=" * 60)
    print("Visualizations complete!")
