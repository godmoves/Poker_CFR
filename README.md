## Poker_CFR

Counterfactual Regret Minimization for poker games.

### CFR Algorithm

In essence, CFR is a [regret matching](https://github.com/godmoves/Rock-Paper-Scissors) procedure applied to optimize entity called **immediate counterfactual regret**.

#### Average overall regret

Let <img src="https://latex.codecogs.com/svg.latex?\pi^\sigma(h)" /> be the probability of history <img src="https://latex.codecogs.com/svg.latex?h" /> occurring if players choose actions according to <img src="https://latex.codecogs.com/svg.latex?\sigma" />. The **overall value** to player <img src="https://latex.codecogs.com/svg.latex?i"  /> of a strategy profile is then the expected payoff of the resulting terminal node:

<div align="center">
<img src="https://latex.codecogs.com/svg.latex?u_i(\sigma)=\sum_{h&space;\in&space;Z}{\pi^\sigma(h)u_i(h)}" />
</div>

Let <img src="https://latex.codecogs.com/svg.latex?\sigma_i^t" /> be the strategy used by player <img src="https://latex.codecogs.com/svg.latex?i" /> on round <img src="https://latex.codecogs.com/svg.latex?t" />. The **average overall regret** of player <img src="https://latex.codecogs.com/svg.latex?i" /> at time <img src="https://latex.codecogs.com/svg.latex?T" /> is:

<div align="center">
<img src="https://latex.codecogs.com/svg.latex?R_i^T&space;=&space;\frac{1}{T}\max_{\sigma^*_i&space;\in&space;\Sigma_i}{\sum_{t=1}^T(u_i(\sigma^*_i,\sigma^t_{-i})-u_i(\sigma^t))}" />
</div>


Moreover, define <img src="https://latex.codecogs.com/svg.latex?\bar{\sigma}_i^t" /> to be the average strategy for player <img src="https://latex.codecogs.com/svg.latex?i" /> from time 1 to <img src="https://latex.codecogs.com/svg.latex?T" />.

<div align="center">
<img src="https://latex.codecogs.com/svg.latex?\bar{\sigma}_i^t(I)(a)=\frac{\sum_{t=1}^T\pi_{i}^{\sigma^t}(I)\sigma^t(I)(a)}{\sum_{t=1}^T\pi_{i}^{\sigma^t}(I)}" />
</div>

#### Counterfactual utility

For every opponent’s hand (game state <img src="https://latex.codecogs.com/svg.latex?h" />), we use the probability of reaching <img src="https://latex.codecogs.com/svg.latex?h" /> assuming **we wanted to get to** <img src="https://latex.codecogs.com/svg.latex?h" />. So instead of using our regular strategy from strategy profile we modify it a bit so **it always tries to reach our current game state** <img src="https://latex.codecogs.com/svg.latex?h" /> – meaning that for each information set prior to currently assumed game state we pretend we always **played pure behavioral strategy** where the whole probability mass was placed in action that was actually played and led to current assumed state <img src="https://latex.codecogs.com/svg.latex?h" /> – which is in fact **counterfactual**, in opposition to facts, because we really played according to <img src="https://latex.codecogs.com/svg.latex?\sigma" />. In practice then we just consider our opponent contribution to the probability of reaching currently assumed game state <img src="https://latex.codecogs.com/svg.latex?h" />. 

<div align="center">
<img src="https://int8.io/wp-content/uploads/2018/09/counterfactualutilities.png" width="450px" />
</div>

Formally, counterfactual utility for information set <img src="https://latex.codecogs.com/svg.latex?I" />, player <img src="https://latex.codecogs.com/svg.latex?i" /> and strategy <img src="https://latex.codecogs.com/svg.latex?\sigma" /> is given by:

<div align="center">
<img src="https://latex.codecogs.com/svg.latex?u_i(\sigma,&space;I)&space;=&space;\frac{\sum_{h&space;\in&space;I,&space;h'&space;\in&space;Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(h,h')u_i(h')}}{\pi_{-i}^{\sigma}(I)}" />
</div>

denominator is a sum of our counterfactual weights – normalizing constant.

You may find unnormalized form of the above – it is ok and let’s actually have it too, it will come in handy later:

<div align="center">
<img src="https://latex.codecogs.com/svg.latex?\hat{u}_i(\sigma,&space;I)&space;=&space;\sum_{h&space;\in&space;I,&space;h'&space;\in&space;Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(h,h')u_i(h')}" />
</div>

#### Immediate Counterfactual Regret

To introduce counterfactual regret minimization we will need to look at the poker game from a certain specific angle. First of all we will be looking at **single information set**, single decision point. We will consider **acting in this information set repeatedly over time** with the goal to act in a best possible way with respect to certain reward measure.

Assuming we are playing as player <img src="https://latex.codecogs.com/svg.latex?i" />, let’s agree that reward for playing action <img src="https://latex.codecogs.com/svg.latex?a" /> is unnormalized counterfactual utility under assumption we played action <img src="https://latex.codecogs.com/svg.latex?a" /> (let’s just assume this is how environment reward us). Entity in consideration is then defined as:

<div align="center">
<img src="https://latex.codecogs.com/svg.latex?\hat{u}_{i}(\sigma|_{I&space;\to&space;a},&space;I)&space;=&space;\sum_{h&space;\in&space;I,&space;h'&space;\in&space;Z}{\pi_{-i}^{\sigma}(h)\pi^{\sigma}(ha,&space;h')u_i(h')}" />
</div>

where <img src="https://latex.codecogs.com/svg.latex?ha" /> is game state implied by playing action <img src="https://latex.codecogs.com/svg.latex?a" /> in game state <img src="https://latex.codecogs.com/svg.latex?h" />. We can do it becaue we assume we played <img src="https://latex.codecogs.com/svg.latex?a" /> with probability 1.

We can define regret in our setting to be:

<div align="center">
<img src="https://latex.codecogs.com/svg.latex?R_{i,imm}^T(I)&space;=&space;\frac{1}{T}\max_{a&space;\in&space;A(I)}\sum_{t=1}^T(\hat{u}_{i}(\sigma^t|_{I&space;\to&space;a},I)-\hat{u}_i(\sigma^t,I))" />
</div>

which called **Immediate Counterfactual Regret**.

Similarly, Immediate Counterfactual Regret of not playing action <img src="https://latex.codecogs.com/svg.latex?a" /> is given by:

<div align="center">
<img src="https://latex.codecogs.com/svg.latex?R_{i,imm}^T(I,a)=\frac{1}{T}\sum_{t=1}^T(\hat{u}_{i}(\sigma^t|_{I&space;\to&space;a},I)-\hat{u}_i(\sigma^t,I))" />
</div>

For more information about these concepts, you can refer to the [original paper](https://poker.cs.ualberta.ca/publications/NIPS07-cfr.pdf) and [this post](https://int8.io/counterfactual-regret-minimization-for-poker-ai/).
