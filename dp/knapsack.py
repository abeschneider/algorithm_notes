def knapsack(w, i, t):
    if t < 0 or i < 0: return 0
    if w[i-1] > t: return knapsack(w, i-1, t)
    val = max(knapsack(w, i-1, t-w[i-1])+1, knapsack(w, i-1, t))
    print t
    return val

if __name__ == "__main__":
    weight = [10, 20, 30, 40]
    print knapsack(weight, len(weight), 60)
