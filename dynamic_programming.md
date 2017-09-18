# Dynamic Programming

Steps for solving DP:
1. Define the allowed choices
2. Define recurrence using subproblem
3. Define the boundary conditions
4. Create recursive solution

There are three main types of recurrency:
* suffix [i:] (solving for the rest of the problem)
* prefix [:i] (solving for the first part of the problem)
* substring [i:j] (solving for a substring within the problem)

## Edit distance

Edit distance is a *suffix* problem, where given two strings $x$ and $y$, we want to know the minimum number of operations required to make the strings the same. The allowed operations are:
* nothing
* substitution
* insert into $x$
* delete from $y$

Following the steps:
1. We want to change $x_i$ or $y_j$ to make the two strings more similar. The allowed choices are:
a. insert
b. delete
c. substitute
d. do nothing
2. The boundary conditions are if either $x_i$ or $y_j$ reach the end. If they're finished, we've reached the end. If $i$ is 0, then we can delete from $y$, and if $j$ is 0, we can insert into $x$.
3. The recurrence is:

$$
DP(i, j) = \begin{cases}
0 & i < 0, j < 0 \\
DP(i, j-1)+\text{delete}(y_i) & i < 0 \\
DP(i-1, j-1)+\text{insert}(x_i) & j < 0 \\
\begin{aligned}\min(&DP(i-i, j-1)+\text{match}(x_i, y_j),\\
&DP(i-1, j)+\text{insert}(x_i)),\\
&DP(i, j-1)+\text{delete}(y_i))\end{aligned} & \text{else} \\
\end{cases}
$$

Translating our recurrence into code looks like this:

```python
def edit_distance(x, i, y, j):
  if i < 0 and j < 0: return 0
  if i < 0: return edit_distance(x, i, y, j-1) + delete(y[j])
  if j < 0: return edit_distance(x, i-1, y, j) + insert(x[i])
  match_cost = edit_distance(x, i-1, y, j-1) + match(x[i], y[j])
  insert_cost = edit_distance(x, i-1, y, j) + insert(x[i])
  delete_cost = edit_distance(x, i, y, j-1) + delete(y[j])

  return min(match_cost, insert_cost, delete_cost)
```

Without DP, the runtime of this algorithm will be exponential $O(3^n)$. However, we can use a table to store our intermediate results bringing the runtime to $O(mn)$:

```python
def edit_distance(x, y):
  cost = np.zeros((len(x)+1, len(y)+1), dtype=np.uint32)

  # set up boundary conditions
  cost[0, 0] = 0

  for i in range(1, len(x)+1):
      cost[i, 0] = cost[i-1, 0] + delete(' ')

  for j in range(1, len(y)+1):
      cost[0, j] = cost[0, j-1] + insert(' ')

  # create table
  for i in range(1, len(x)+1):
      for j in range(1, len(y)+1):
          match_cost = cost[i-1, j-1] + match(x[i-1], y[j-1])
          insert_cost = cost[i, j-1] + insert(y[i-1])
          delete_cost = cost[i-1, j] + delete(x[j-1])
          cost[i, j] = min(match_cost, insert_cost, delete_cost)

  return cost[-1, -1]
```

NB: Because we can't have indices less than $0$ in our table, we add $1$ to all the values.

### Variants on Edit Distance
1. Inexact substring matching
2. Longest common subsequence
3. Maximum monotone subsequence

## Knapsack 1-0

The Knapsack problem comes in a few different flavors. For our example, we have $S$ items that we want to place in a knapsack. Each item has a weight $w_i$, and we have a maximum weight allowed for the knapsack. We would like the maximize the total number of items we can place in the knapsack.

Following the steps:
1. The allowed choices are:
  a. add item $w_i$
  b. do not add item $w_i$
2. The boundary condition is that we've filled up the knapsack.
3. The recurrence is:

$$ DP(i, t) = \begin{cases}
0 & t \leq 0 \\
0 & i \geq |w|\\
\begin{aligned}\max(&DP(i+1, t-w_i)+1,\\
&DP(i+1, t))\end{aligned} & \text{else} \\
\end{cases}$$

The term $DP(i+1, t-w_i)+1$ means we've added item $i$ to the knapsack, we've increment the cost by $1$ to denote that will simultaneously decreasing the total allowed remaining weight, and increment $i$ to consider the next item. The other term $DP(i + 1, t)$ means that we aren't going to add item $i$ to our knapsack, and will consider item $i+1$ next.

Our code looks like:

```python
def knapsack(w, i, t):
  if t <= 0: return 0
  if i > len(w): return 0
  return max(knapsack(i+1, t-w[i])+1, knapsack(i+1, t))
```

changing it to table form gives us:

```python
def knapsack(w, t):
  cost = np.zeros((len(w), t))
  for i in range(1, len(w)):
    for j in range(1, t):
      cost[i, j] = max(cost[i-1, t-w[i-1]]+1, cost[i-1, t])
```

## Making change

Suppose we want to count the number of ways there are to make change. This is a similar problem to the knapsack problem, except that we have an infinite number of each coin. Additionally, our goal this time is to simply count the number. Each coins $c_i$ has a specific value (e.g. we may have coins with values of $5, 10, 25$)

Following the steps:
1. The allowed choices are:
a. add coin of value $c_0$
b. add coin of value $c_1$
c. etc.
2. The boundary conditions are that we've made exact change.
3. The recurrence is:

$$ DP(t) = \begin{cases}
0 & t \lt 0\\
1 & t = 0\\
DP(t-c_0) + DP(t-c_1) + \cdots + DP(t-c_n) + 1 & else\\
\end{cases}$$

Translating our recurrence into code looks like this:

```python
def DP(C, t):
  if t < 0: return 0
  if t == 0: return 1
  return sum([DP(C, t-c[j]) for j in range(len(C))])
```

Applying DP to the problem we get:

```python
def DP(C, t):
  table = np.zeros(t+1)

  # set out boundary conditions
  table[0] = 1

  # fill in table
  for c in C:
    for i in range(c, t+1):
      table[i] += table[i-c]

  return table[t]
```

## Longest increasing sequence

In this case, we have some sequence $S$ from which we want to find the longest subsequence of increasing values.

Following the steps:
1. For every item $s_i$ we can decide whether it belongs in our subsequence ($s_i > s_{i-1}$ for some $s$ in $S$).
2. Our boundary conditions are at the end of $S$.
3. Our recurrence looks like:

$$DP(i) = \begin{cases}
0 & i > |S|\\
\max(DP(i-1) + 1, DP(i-1)) & s_{i-1} < s_i\\
DP(i-1) & \text{else}\\
\end{cases}$$

## Finding the longest palindrome

Suppose we have some sequence $s_0s_1s_2\cdots s_{n-1}$, and embedded in the sequence is at least one palindrome $s_is_{i+1}\cdots s_j$. Can we find the longest sequence of the palindrome?

Following the steps:

1. There are two cases that we can have for palindromes:
a. $\{s_{k}s_{k-1}s_is_{k-1}s_k\}$, where $k = i+\frac{j}{2}$. In this case, there is symmetry around a single element $s_i$.
b. $\{s_{k}s_{k-1}s_is_{i+1}s_{k-1}s_k\}$, where $s_i = s_{i+1}$.
2. Our boundary condition is that $s_k^{-} \neq s_k^{+}$, where the $+$ and $-$ denote either side of the center element(s).
3. Our recurrence looks like:

$$DP(i, j) = \begin{cases}
0 & i > j, j < i\\
\max(DP(i+1, 1), DP(i, j-1)) & s[i+j] \neq s[i-j] \\
2 & i = j+1 \\
DP(i+1, j-1)+2 & \text{else}\\
\end{cases}$$

## Largest contiguous subarray

Given array $A$, find a subarray ($a_ia_{i+1}\cdots a_j$), that when summed, will give the largest value.

1. We can treat this as a substring problem. Thus, we get to move either $i$ forward one or $j$ backward one.
2. The boundary conditions are that $i$ and $j$ cannot equal each other.
3. Our recurrence looks like:

$$DP(i, j, t) = \begin{cases}
0 & i \geq j\\
\begin{aligned}max(&DP(i+1, 1, t-A[i]),\\
&DP(i, j-1, t-A[j]),\\
&t)\end{aligned} & \text{else}\\
\end{cases}$$
