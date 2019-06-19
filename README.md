## Poker_CFR

Counterfactual Regret Minimization for poker games.

### Algorithm

In essence, CFR is a regret matching procedure applied to optimize entity called **immediate counterfactual regret**.

#### Counterfactual utility

For every opponent’s hand (game state <a href="https://www.codecogs.com/eqnedit.php?latex=h" target="_blank"><img src="https://latex.codecogs.com/svg.latex?h" title="h" /></a>), we use the probability of reaching <a href="https://www.codecogs.com/eqnedit.php?latex=h" target="_blank"><img src="https://latex.codecogs.com/svg.latex?h" title="h" /></a> assuming **we wanted to get to** <a href="https://www.codecogs.com/eqnedit.php?latex=h" target="_blank"><img src="https://latex.codecogs.com/svg.latex?h" title="h" /></a>. So instead of using our regular strategy from strategy profile we modify it a bit so **it always tries to reach our current game state** <a href="https://www.codecogs.com/eqnedit.php?latex=h" target="_blank"><img src="https://latex.codecogs.com/svg.latex?h" title="h" /></a> – meaning that for each information set prior to currently assumed game state we pretend we always **played pure behavioral strategy** where the whole probability mass was placed in action that was actually played and led to current assumed state <a href="https://www.codecogs.com/eqnedit.php?latex=h" target="_blank"><img src="https://latex.codecogs.com/svg.latex?h" title="h" /></a> – which is in fact **counterfactual**, in opposition to facts, because we really played according to <a href="https://www.codecogs.com/eqnedit.php?latex=\sigma" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\sigma" title="\sigma" /></a>. In practice then we just consider our opponent contribution to the probability of reaching currently assumed game state <a href="https://www.codecogs.com/eqnedit.php?latex=h" target="_blank"><img src="https://latex.codecogs.com/svg.latex?h" title="h" /></a>. 

<div align="center">
<img src="https://int8.io/wp-content/uploads/2018/09/counterfactualutilities.png" width="450px" />
</div>

Formally, counterfactual utility for information set <a href="https://www.codecogs.com/eqnedit.php?latex=I" target="_blank"><img src="https://latex.codecogs.com/svg.latex?I" title="I" /></a>, player <a href="https://www.codecogs.com/eqnedit.php?latex=i" target="_blank"><img src="https://latex.codecogs.com/svg.latex?i" title="i" /></a> and strategy <a href="https://www.codecogs.com/eqnedit.php?latex=\sigma" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\sigma" title="\sigma" /></a> is given by:

<div align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=u_i(\sigma,&space;I)&space;=&space;\frac{\sum_{h&space;\in&space;I,&space;h'&space;\in&space;Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(h,h')u(h')}}{\pi_{-i}^{\sigma}(I)}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?u_i(\sigma,&space;I)&space;=&space;\frac{\sum_{h&space;\in&space;I,&space;h'&space;\in&space;Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(h,h')u(h')}}{\pi_{-i}^{\sigma}(I)}" title="u_i(\sigma, I) = \frac{\sum_{h \in I, h' \in Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(h,h')u(h')}}{\pi_{-i}^{\sigma}(I)}" /></a>
</div>

denominator is a sum of our counterfactual weights – normalizing constant.

You may find unnormalized form of the above – it is ok and let’s actually have it too, it will come in handy later:

<div align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=\hat{u}_i(\sigma,&space;I)&space;=&space;\sum_{h&space;\in&space;I,&space;h'&space;\in&space;Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(h,h')u(h')}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\hat{u}_i(\sigma,&space;I)&space;=&space;\sum_{h&space;\in&space;I,&space;h'&space;\in&space;Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(h,h')u(h')}" title="\hat{u}_i(\sigma, I) = \sum_{h \in I, h' \in Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(h,h')u(h')}" /></a>
</div>

#### Immediate Counterfactual Regret

To introduce counterfactual regret minimization we will need to look at the poker game from a certain specific angle. First of all we will be looking at **single information set**, single decision point. We will consider **acting in this information set repeatedly over time** with the goal to act in a best possible way with respect to certain reward measure.

Assuming we are playing as player <a href="https://www.codecogs.com/eqnedit.php?latex=i" target="_blank"><img src="https://latex.codecogs.com/svg.latex?i" title="i" /></a>, let’s agree that reward for playing action <a href="https://www.codecogs.com/eqnedit.php?latex=a" target="_blank"><img src="https://latex.codecogs.com/svg.latex?a" title="a" /></a> is unnormalized counterfactual utility under assumption we played action <a href="https://www.codecogs.com/eqnedit.php?latex=a" target="_blank"><img src="https://latex.codecogs.com/svg.latex?a" title="a" /></a> (let’s just assume this is how environment reward us). Entity in consideration is then defined as:

<div align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=\hat{u}_{i|I&space;\to&space;a}(\sigma,&space;I)&space;=&space;\sum_{h&space;\in&space;I,&space;h'&space;\in&space;Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(ha,&space;h')u(h')}" target="_blank"><img src="https://latex.codecogs.com/svg.latex?\hat{u}_{i|I&space;\to&space;a}(\sigma,&space;I)&space;=&space;\sum_{h&space;\in&space;I,&space;h'&space;\in&space;Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(ha,&space;h')u(h')}" title="\hat{u}_{i|I \to a}(\sigma, I) = \sum_{h \in I, h' \in Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(ha, h')u(h')}" /></a>
</div>

where <a href="https://www.codecogs.com/eqnedit.php?latex=ha" target="_blank"><img src="https://latex.codecogs.com/svg.latex?ha" title="ha" /></a> is game state implied by playing action <a href="https://www.codecogs.com/eqnedit.php?latex=a" target="_blank"><img src="https://latex.codecogs.com/svg.latex?a" title="a" /></a> in game state <a href="https://www.codecogs.com/eqnedit.php?latex=h" target="_blank"><img src="https://latex.codecogs.com/svg.latex?h" title="h" /></a>. We can do it becaue we assume we played <a href="https://www.codecogs.com/eqnedit.php?latex=a" target="_blank"><img src="https://latex.codecogs.com/svg.latex?a" title="a" /></a> with probability 1.

We can define regret in our setting to be:

<div align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=R_{i,imm}^T(I)&space;=&space;\frac{1}{T}\max_{a&space;\in&space;A(I)}\sum_{t=1}^T(\hat{u}_{i|I&space;\to&space;a}(\sigma_H^t,I)-\hat{u}_i(\sigma_H^t,I))" target="_blank"><img src="https://latex.codecogs.com/svg.latex?R_{i,imm}^T(I)&space;=&space;\frac{1}{T}\max_{a&space;\in&space;A(I)}\sum_{t=1}^T(\hat{u}_{i|I&space;\to&space;a}(\sigma_H^t,I)-\hat{u}_i(\sigma_H^t,I))" title="R_{i,imm}^T(I) = \frac{1}{T}\max_{a \in A(I)}\sum_{t=1}^T(\hat{u}_{i|I \to a}(\sigma_H^t,I)-\hat{u}_i(\sigma_H^t,I))" /></a>
</div>

which called **Immediate Counterfactual Regret**.

Similarly, Immediate Counterfactual Regret of not playing action <a href="https://www.codecogs.com/eqnedit.php?latex=a" target="_blank"><img src="https://latex.codecogs.com/svg.latex?a" title="a" /></a> is given by:

<div align="center">
<a href="https://www.codecogs.com/eqnedit.php?latex=R_{i,imm}^T(I,a)&space;=&space;\frac{1}{T}\sum_{t=1}^T(\hat{u}_{i|I&space;\to&space;a}(\sigma_H^t,I)-\hat{u}_i(\sigma_H^t,I))" target="_blank"><img src="https://latex.codecogs.com/svg.latex?R_{i,imm}^T(I,a)&space;=&space;\frac{1}{T}\sum_{t=1}^T(\hat{u}_{i|I&space;\to&space;a}(\sigma_H^t,I)-\hat{u}_i(\sigma_H^t,I))" title="R_{i,imm}^T(I,a) = \frac{1}{T}\sum_{t=1}^T(\hat{u}_{i|I \to a}(\sigma_H^t,I)-\hat{u}_i(\sigma_H^t,I))" /></a>
</div>

For more information about these concepts, you can refer to the [original paper](https://poker.cs.ualberta.ca/publications/NIPS07-cfr.pdf) and [this post](https://int8.io/counterfactual-regret-minimization-for-poker-ai/).
