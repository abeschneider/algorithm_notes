## Machine Learning Notes


### Probability overview
#### Combinatorials

## Combinations and permutations

|                    | ordered (permutation)  | unordered (combination)              |
|--------------------|------------------------|--------------------------------------|
| repeated values    | $n^k$                  | ${n+k-1}\choose{k}$                  |
| no repeated values | $\frac{n!}{(n-k)!}$    | ${n\choose{k}} = \frac{n!}{k!(n-k)!}$|


### Permutations
#### Repeated values
The **ordered** case with repeated items is the most straight forward to understand. Given $k$ items pulled from $n$ possibilities ($\{x_0, x_1, \cdots, x_k \}$ where $x_i \in \{ \alpha_0, \alpha_1, \cdots, \alpha_N \}$), we can construct a tree per choice made:

(tree where each node is $\alpha_i$ and each edge is $x_j$)

To create a new permutation, for each ply we select a single $x_j$ given $n$ choices. We repeat this for $k$ plies. Because at each ply we have $n$ choices, the total number of permutations that can occur are $\prod_{i=0}^n n = n^K$.

#### No repeated values
If repeated elements are not allowed, then each time we go down a ply, we have one less choice to make. If $n$ and $k$ are equal, this is just: $\prod_{i=0}^n (n - i) = n!$. However, when $k$ is less than $n$, we instead get: $\prod_{i=0}^k (n - i)$. While this cannot be expressed as a single factorial, we can eliminate the additional terms through division:

$$\frac{n(n-1)(n-2)\cdots (n-k)(n-k-1)\cdots *1}{(n-k)(n-k-1)\cdots *1}$$
$$= \frac{n!}{(n-k)!}$$

### Combinations
#### No repeated values
The **unordered** case with no repeat items falls out directly from this equation. By not enforcing ordering means that $\{ x_i, x_j, x_k\}$ is equal to $\{ x_j, x_i, x_k \}$. The total number of unique orderings is $k$ possibilities for the first element, $k-1$ for the next elements (since we can't re-use whatever element was used in the first position), etc: $\prod_{i=1}^k i = k!$. By dividing the value we derived for permutations without repeated values by $k!$, we count all these possible permutations of the set as one:

$$\frac{n!}{k!(n-k)!}$$

#### Repeated values
$$\frac{n^k}{k!}$$

$$\frac{(n-k-1)!}{k!(n-2k-1)!}$$


#### Basic probability
Probability chain rule:

$$ p(A,B) = p(A|B)p(B) $$

from which we get:

$$ p(A|B)p(B) = p(B|A)p(A) $$

which can be transformed into Bayes' Theorem:
$$ p(A|B) = \frac{p(B|A)p(A)}{p(B)}$$

where $p(A|B)$ is the posterior, $p(B|A)$ is the likelihood, $p(A)$ is the prior, and $p(B)$ is the marginal.

### Gaussian
$$ p(x) = \frac{1}{\sigma\sqrt{2\pi}}e^{-(x-\mu)^2/2\sigma^2}$$

### Entropy
$$ H(P) = -\sum_i p(x_i)\log p(x_i) $$

### Cross entropy
$$ H(P, Q) = -\sum_i p(x_i)\log q(x_i)  $$

### KL Divergence
The KL divergence between distributions $P$ and $Q$ is defined as:

$$ D_{KL}(P||Q) = \sum_i p(x_i)\log\frac{p(x_i)}{q(x_i)}$$

which can also be written as:

$$ \underbrace{-\sum_i p(i)\log q(i)}_{H(P,Q)} + \underbrace{\sum_i p(i)\log p(i)}_{H(P)}$$

where $H(P, Q)$ is the cross entropy of $P$ and $Q$ and $H(P)$ is the entropy of $P$. Thus, KL Divergence can be thought of as the cross-entropy of $P$ and $Q$ with a baseline entropy of $P$ subtracted out.

### Bayesian

### Naive Bayes

Naive Bayes calculates the conditional probability of a class $c$ given the input $x_i$:

$$ p(c | x_0, x_1, \cdots, x_{n-1}) = \frac{p(x_0, x_1, \cdots, x_{n-1} | c)p(c)}{p(x_0, x_1, \cdots, x_{n-1})}$$

If $x_i$ is independent of $x_j$, then $p(x_i, x_j) = p(x_i)p(x_j)$, thus we get:

$$ p(c | x_0, x_1, \cdots, x_{n-1}) = \frac{\left[\prod p(x_i|c)\right] p(c)}{p(x_0, x_1, \cdots, x_{n-1})}$$

The denominator is a constant, so we can simplify this as:
$$ p(c | x_0, x_1, \cdots, x_{n-1}) \propto \left[\prod p(x_i|c)\right] p(c)$$



### Maximum Likelihood
The maximum likelihood is given as:

$$C_{ML} = \arg\max_{C} p(x_0, x_1, \cdots, x_{n-1} | C)$$

One method to find the value of $C$ which maximizes the value is to take the derivative and set it to $0$. Taking the log makes the problem easier to solve:

$$\frac{\partial \sum \log p(x_0|C)}{\partial C} = 0$$

### MAP
MLE with a prior

### GMM

### K-Means
#### Definition

K-Means is a method of clustering where data is clustered on $K$ centroids. It is a form of EM, where alternating steps are taken to:

1. assign data points to centroids based on distance of $||x_i - c_j||^2$.
2. update centroids based on their assignment: $c_j = \frac{1}{|x\in c_j|}\sum_{x\in c_j} x$

```python
def euclidean_distances(data, centroids):
    return np.array([np.sum((d - centroids)**2, 1)
        for d in data])

def cluster(data, centroids):
  for iterations in range(max_iterations):
      distances = euclidean_distances(data, centroids)

      # distances is: [SxK], per S_i find min K
      labels = np.argmin(distances, 1)

      for c in range(centroids.shape[0]):
          assigned = data[np.where(labels == c)]
          if assigned.shape[0] > 0:
              centroids[c] = np.mean(assigned)
```

### kNN
k Nearest Neighbors is a non-parametric classification and regression method. Given an unlabeled data point, kNN will assign a label based on the k nearest neighbors. A majority function may be used, in which case the label is determined by whatever label has the highest count. Other decision functions can also be used.

### TFIDF

#### MLPs
#### Definition
For a given DAG $G$ that consists of transforms $T_{0..n-1}$:
* $\vec{x}_i$ is input to the leaf nodes of the graph
* each edge $(i, j)$ between two transforms $T_i$ and $T_j$ defines $T_i$ as input to $T_j$ (i.e. $T_j(T_i(\vec{x}_i))$)
* Any node $T_i$ can be a loss function $\mathcal{L}$ (though traditionally there is just one at the root node).

#### Optimization
We with to optimize $\theta$ given $\mathcal{L}$ in $G$. For the smallest possible graph, this looks like:

$$ \arg\min_{\theta} \mathcal{L}(T_0(\vec{x}; \theta_0))$$

For our small graph $G$, we want to optimize $\theta_0$. To optimize $G$, can set our desired error to be zero:

$$ \mathcal{L} (T_0(\vec{x}_i, \theta_0)) = 0 $$

Because we're trying to minimize $\mathcal{L}$ over $\theta$, we can write this as the optimization:

$$ \frac{\partial L}{\partial \theta_0} = 0$$

While we don't know this value, we can employ the calculus chain rule:

$$ \frac{\partial L}{\partial \theta_0} = \frac{\partial L}{\partial T_0}\frac{\partial T_0}{\partial\theta_0}
$$

The first term is the derivative of $\mathcal{L}$ to its input. The second term is dependent on how the transform uses $\theta_0$.

### Backpropagation

Suppose we make $G$ larger and add a second transform such that:

$$
\mathcal{C} = \mathcal{L}(T_1(T_0(\vec{x}_i; \theta_0); \theta_1))
$$


We now need to propagate the error from $T_1$ to $T_0$. To do so, we can look at how $\mathcal{L}$ changes with $\vec{x}$, and once again employ the chain rule:

$$
\frac{\partial \mathcal{L}}{\partial \vec{x}} = \frac{\partial \mathcal{L}}{\partial T_1}\frac{\partial T_1}{\partial T_0}\frac{\partial T_0}{\partial \vec{x}_i}
$$

Note that $\frac{\partial \mathcal{L}}{\partial T_1}$ is the derivative of $\mathcal{L}$ to its input, $\frac{\partial T_1}{\partial T_0}$ is the derivative of $T_1$ to its input, and $\frac{\partial T_0}{\vec{x}_i}$ is the derivative of $T_0$ to its input. Thus, we can take the derivative of our total error, and multiply it by the derivative of each transform  with respect to its input in order to propagate the error.

Therefore, any transform $T_i$ can be optimized over using BP if we have a well defined derivative given its input and given its parameter $\theta$.

TODO: discuss relationship to automatic backwards differentiation

### Linear Transform

Given:

$$ T_i(\vec{x}; \theta_i) = W\vec{x}$$

where $\theta_i$ is a matrix, we can define its derivative with respect to its input as:

$$
\frac{\partial T_i}{\partial \vec{x}} = W^T\vec{x}
$$

and its derivative with respect to $\theta$ as:

$$
\frac{\partial T_i(\vec{x})}{\partial \theta_i} = \frac{\partial T_j(T_i(\vec{x}))}{\partial T_i(\vec{x})}x^T
$$

#### Intuition

To understand how we got the derivative with respect to the input, we need to look at the definition of $W\vec{x}$:

$$
W\vec{x} = \sum_j W_{i,j}x_j
$$

taking the derivative of:

$$
\frac{\partial \sum_j W_{i,j}x_j}{\partial x_j}
$$

we can see any term that isn't $x_j$ is a constant, and therefore goes to $0$:

$$
\left[\begin{array}{c}
W_{0,0}x_0 + W_{1, 0}x_0 + \cdots + W_{n-1, 0}x_0\\
W_{0,1}x_1 + W_{1, 0}x_1 + \cdots + W_{n-1, 1}x_1\\
W_{0,2}x_2 + W_{1, 2}x_2 + \cdots + W_{n-1, 2}x_2\\
\vdots\\
W_{0,m-1}x_{m-1} + W_{1, m-1}x_{m-1} + \cdots + W_{n-1, m-1}x_{m-1}\\
\end{array}\right]
$$

which happens to be $W^T\vec{x}$.

(include a graphical representation with nodes as well)

To get the derivative of $T_i$ with respect to $\theta_i$, we can look at it in the form of:

$$
\frac{\partial W_{i,j}x_j}{\partial W_{i, j}}
$$

We can rewrite this as:

$$
\left[\begin{array}{c}
\frac{\partial \sum_j W_{0, j}x_j}{\partial W_{0, k}}\\
\frac{\partial \sum_j W_{1, j}x_j}{\partial W_{1, k}}\\
\vdots\\
\frac{\partial \sum_j W_{n-1, j}x_j}{\partial W_{n-1, k}}
\end{array}\right]
$$

The value of $\frac{\partial \sum_j W_{k, j}x_j}{\partial W_{k, l}}$ is zero when $l \neq j$ and $W_{k, j}$ divided by $W_{k, l}$ equals $1$ when $l = j$, we are left with:

$$
\left[\begin{array}{c}
x_0\\
x_1\\
\vdots\\
x_{n-1}
\end{array}\right]
$$

or more simply: $x^T$.

### Sigmoid

The sigmoid function $\sigma(\vec{x})$ squashes its input to $0 \leq \sigma(\vec{x}) \leq 1$ using the *logit* function. If the sigmoid function is paired with a *binary cross entropy* loss, that turns the problem into a logistic regression problem.

### Softmax

The softmax function can be viewed as a generalization of the *sigmoid* function for a multi-class problem. If paired with a *negative log likelihood* loss, that gives a *cross entropy* loss.

### Negative Log Likelihood Loss
This is actually just the cross entropy:

$$\mathcal{L} = \sum_i^{|C|} p(x_i)\log q(x_i)$$

where $p(x_i)$ is the actual probability of $x_i$ belonging to a specific class, $q(x_i)$ is the predict probability, and $|C|$ is the total number of classes.

Thus, minimizing with cross entropy forces our $Q$ distribution to go towards our $P$ distributions.

In the case where there are two classes ($|C| = 2$), we get:

$\mathcal{L} = p(x_i)\log(x_i) + (1 - p(x_i))\log (1-x_i)$

### ConvNets
(include Toplitz transform)

### RNNs
