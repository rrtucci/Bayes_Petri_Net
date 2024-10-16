# Bayes Petri Net

![BPN wet grass](pics/BPN_wet_grass.png)
*This is a figure of a typical **Bayes Petri Net**
(BPN). It was rendered 
by the software in this repo using Graphviz. The solid arrows
and uncircled nodes constitute a **Bayesian Network**
whereas the dotted arrows are the **arcs**,
the circled nodes are the **places**, and the
uncircled nodes are the **transitions** of a **Petri Net**.
The red numbers are the token contents of 
the place nodes (note that
we allow them to be fractional)*

This software displays the
evolution (on a Jupyter notebook) of
* a conventional **Petri Net**
* a special
Petri Net that we call a **Bayes Petri Net** (BPN).

With every **Bayesian Network** (BN),
one can define a natural BPN that has the 
nodes of the BN as the transition nodes of the
BPN.

The firing rules for the BPN are 
given by Pearl's rules for **d-separation**.

BPN are closely related to 
**message passing** which was used 
by Pearl in his book *Probabilistic Reasoning in Intelligent Systems: 
Networks of Plausible Inference (1988)*