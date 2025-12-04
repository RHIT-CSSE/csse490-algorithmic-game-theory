# A03: Greedy Algorithm for External Regret Minimization

## Overview
This visualization demonstrates the **worst-case performance** of the deterministic greedy algorithm for external regret minimization, as described in NRTV Theorem 4.2.

## Algorithm
The greedy algorithm (Algorithm 1 in the lecture notes) picks the action with the lowest cumulative loss at each time step, breaking ties by choosing the lowest index.

## Worst-Case Bound
**Proposition (NRTV Theorem 4.2):** For any sequence of losses,
$$L^T_{\text{Greedy}} \leq N \cdot L^T_{\text{min}} + (N - 1)$$

where:
- $N$ is the number of actions
- $L^T_{\text{min}}$ is the cumulative loss of the best single action
- $L^T_{\text{Greedy}}$ is the cumulative loss of the greedy algorithm

## Visualization

The script generates two plots:

1. **Bar Chart (Left)**: Shows final cumulative losses
   - Blue bars: cumulative loss of each single action
   - Red bar: cumulative loss of the greedy algorithm
   - Green dashed line: $L^T_{\text{min}}$ (best single action)
   - Orange dotted line: theoretical upper bound

2. **Line Plot (Right)**: Shows evolution over time
   - Each line tracks the cumulative loss of an action
   - Red line: greedy algorithm's cumulative loss

## Usage

Run the script to generate visualizations:
```bash
python A03_GreedyERM.py
```

This creates two examples:
- `greedy_erm_example1_N3.png`: N=3 actions, 2 increments
- `greedy_erm_example2_N5.png`: N=5 actions, 3 increments

## Customization

To create custom visualizations, modify the main section or call:
```python
visualize_worst_case(N=4, num_increments=3)
```

Parameters:
- `N`: Number of actions
- `num_increments`: Number of times $L^T_{\text{min}}$ increases

## Key Insights

The worst case occurs when:
1. The greedy algorithm always picks the worst action from the set of actions with minimum cumulative loss
2. Between each increment of $L^T_{\text{min}}$, greedy suffers $N$ losses
3. After $L^T_{\text{min}}$ reaches its final value, greedy can suffer up to $(N-1)$ additional losses

The visualization confirms that the bound is **tight** - the greedy algorithm achieves exactly $N \cdot L^T_{\text{min}} + (N-1)$ in the worst case.
