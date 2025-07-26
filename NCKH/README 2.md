## Important Information
### Useful list
- [Integer programming](https://en.wikipedia.org/wiki/Integer_programming)
- [Computational complexity theory](https://en.wikipedia.org/wiki/Computational_complexity_theory)
- [Branch and bound](https://en.wikipedia.org/wiki/Branch_and_bound)
### Checking list
- [ ] [Convex optimization](https://en.wikipedia.org/wiki/Convex_optimization)
- [ ] [Interior-point method](https://en.wikipedia.org/wiki/Interior-point_method)
- [ ] [Cutting-plane method](https://en.wikipedia.org/wiki/Cutting-plane_method)
- [ ] [Nonlinear programming](https://en.wikipedia.org/wiki/Nonlinear_programming)
### Octave
- Checking Big-O
  - $$O(2^n)$$
```
n = 1:100;
big_o = 2 .^n;
for i = 1:rows(n)
  for j = 1:columns(n)
    disp(sprintf("2 ^ %d = %d", n(i, j), big_o(i, j)));
  end
end
```

\begin{proof}
\begin{table}[h!]
	\centering
    \begin{tabular}{| c | c | c |} 
    \hline
    Job ($j$) & $p_j$ & $w_j$ \\
    \hline
    1 & $p_1$ & $w_1$ \\
    2 & $p_2$ & $w_2$ \\
    $\vdots$ & $\vdots$ & $\vdots$ \\
    $k$ & $p_k$ & $w_k$ \\
    $\vdots$ & $\vdots$ & $\vdots$ \\
    $n$ & $p_n$ & $w_n$ \\
    \hline
    \end{tabular}
\end{table}
Giả sử $p_k = const$ với $const$ là một số vô cùng lớn $(C \simeq \infty)$.

\begin{equation} \label{bao1}
\implies \underset{1 \leq j \leq n}{p\text{-factor}} = \scalebox{1.5}{$\frac{\sum_{j=1}^{n}w_j}{\sum_{j=1}^{k-1}p_j + p_k + \sum_{j=k+1}^{n}p_j}$}. \\
\end{equation}

Từ \eqref{bao1} $\implies \underset{1 \leq j \leq n}{p\text{-factor}} \simeq 0 \quad (dpcm)$.

Vì ta tìm chuỗi có giá trị lớn nhất, vậy $p$-factor tối ưu luôn luôn là $$\underset{1 \leq j \leq l^*}{p\text{-factor}} = \underset{1 \leq l \leq k-1}{\max} \biggl(\frac{\sum_{j=1}^{l}w_j}{\sum_{j=1}^{l}p_j}\biggr).$$

Ta chứng minh trường hợp ngược lại,

\begin{equation} \label{bao2}
\underset{1 \leq j \leq n}{p\text{-factor}}
=
\scalebox{1.5}{$\frac{\sum_{j=1}^{k-1}p_j + p_k + \sum_{j=k+1}^{n}p_j}{\sum_{j=1}^{n}w_j}$}. \\
\end{equation}

Từ \eqref{bao2} $\implies \underset{1 \leq j \leq n}{p\text{-factor}} \simeq \infty \quad (dpcm)$.

Vì ta tìm chuỗi có giá trị nhỏ nhất, vậy $p$-factor tối ưu luôn luôn là $$\underset{1 \leq j \leq l^*}{p\text{-factor}} = \underset{1 \leq l \leq k-1}{\min} \biggl(\frac{\sum_{j=1}^{l}p_j}{\sum_{j=1}^{l}w_j}\biggr).$$
\end{proof}
