#Sujet 2 : Empilement de polyèdres dans un polyèdre

##Formalisation
Étant donné un conteneur $P \subset \mathbb{R}^3$ et un ensemble d’objets $P_1, \ldots, P_n$, trouver une configuration $(S, {T_i}_{i \in S})$ telle que :

1. $T_i(P_i) \subseteq P$ pour tout $i \in S$ (chaque objet est placé dans le conteneur),
2. $T_i(P_i) \cap T_j(P_j) = \emptyset$ pour tout $i \neq j$,
3. la somme des volumes $\sum_{i \in S} \mathrm{Vol}(P_i)$ soit maximale.

où $T_i$ est une transformation rigide (translation + rotation).

##Vérification d'une solution
###Propos liminaire
Une solution (sans être la maximale) est considée comme acceptable s'il respecte les deux conditions suivantes :
1. Chaque objet est à l'intérieur du conteneur.
2. Aucune objet n'entre entre collision avec un autre objet, ou le conteneur.
3. La solution doit inclure la somme du volume de tous les objets de la solution.
###Décomposition du point n°1
Un objet est un polyèdre représenté par des sommets et des faces. On peut vérifier facilement si un sommet est dans le conteneur (aussi un polyèdre) ou non.
Si et seulement tous les sommets d'un polyèdre sont vérifiés, alors on considère que l'objet est dans le conteneur. Sinon, l'objet n'est pas vérifié et la solution est invalide. 
On a implémenté la méthode du lancer de rayon dans la fonction `point_inside_polyhedron`.
Un point $P$ est à l’intérieur d’un polyèdre fermé si un rayon issu de $P$ traverse une frontière (c’est-à-dire une face du polyèdre) un nombre impair de fois.

Pour chaque triangle $T_i = (A,B,C)$, on cherche si le rayon $r(t)$ le coupe.

Équation du plan du triangle :
$$
A + \alpha (B-A) + \beta (C-A) = P + t,\mathbf{d}, \quad \alpha,\beta,t\in\mathbb{R}.
$$
On cherche des solutions avec :
$$
\alpha \ge 0,\quad \beta \ge 0,\quad \alpha + \beta \le 1,\quad t>0.
$$

On réécrit :
$$
P - A = -t,\mathbf{d} + \alpha (B-A) + \beta (C-A)
$$
et on forme le système vectoriel :
$$
[-\mathbf{d},\ B-A,\ C-A]
\begin{bmatrix}
t \ \alpha \ \beta
\end{bmatrix}
= P - A.
$$
###Décomposition du point n°2
Un objet est représenté par des sommets et des faces. Si et seulement si toutes les faces d'un objet ne rentrent pas en collision avec les faces des autres objets (dont le conteneur), alors celui-ci est vérifié. Sinon, l'objet n'est pas vérifié et la solution est invalide.
Notre algorithme va donc tester si deux triangles dans un plan ${R}^3$ se croisent.
Deux triangles $T_1$ et $T_2$ sont **coplanaires** si tous les sommets de $T_2$ sont dans le plan de $T_1$, c’est-à-dire :
$$
|{n}_1 \cdot P_i + d_1| \le \varepsilon, \quad \forall P_i \in {A'_1, B'_1, C'_1}.
$$

C’est le test effectué dans `are_coplanar`.
Dans ce cas, on passe à un traitement 2D (trivial).
Sinon, un triangle $T$ coupe un plan $\Pi$ si et seulement si ses trois sommets ne sont pas tous strictement du même côté du plan.

Mathématiquement :
$$
\exists P_i, P_j \in T \quad \text{tels que } \delta(P_i,\Pi)\cdot \delta(P_j,\Pi) \le 0.
$$

C’est le test de `triangle_intersects_plane`.
Quand $T$ coupe $\Pi$, l’intersection est un segment de droite $[Q_1, Q_2]$.
Pour chaque arête $[P_i, P_j]$ du triangle :

1. On calcule les distances signées $d_i = \delta(P_i,\Pi)$, $d_j = \delta(P_j,\Pi)$.
2. Si $d_i$ et $d_j$ ont des signes opposés (ou un nul), l’arête traverse le plan.
3. Le point d’intersection est obtenu par interpolation linéaire :
   $$
   Q = P_i + t,(P_j - P_i), \quad t = \frac{d_i}{d_i - d_j}, \quad t\in[0,1].
   $$
4. On conserve les deux points distincts $Q_1,Q_2$.

C’est ce que fait `triangle_plane_intersection_segment`.
Résultat : un segment $S = [Q_1,Q_2]$ (ou `None` si dégénéré).

Si $T_1$ et $T_2$ ne sont pas coplanaires, leurs plans se coupent suivant une **droite unique** $\mathcal{D}$.

* L’intersection $\mathcal{D}\cap T_1$ est un segment $S_1 = [Q_1, Q_2]$.
* L’intersection $\mathcal{D}\cap T_2$ est un segment $S_2 = [R_1, R_2]$.

Les deux triangles se coupent si et seulement si :
$$
S_1 \cap S_2 \neq \varnothing.
$$
C’est la condition géométrique de `segments_overlap_3d`.
###Décomposition du point n°3
L’idée du calcul est de convertir le volume du polyèdre en une somme de volumes signés de tétraèdres ayant pour origine un point de référence $O$.


L’idée du calcul est de convertir le volume du polyèdre en une somme de volumes signés de tétraèdres ayant pour origine un point de référence $O$.

Chaque face triangulaire $(A,B,C)$ définit un tétraèdre $(O,A,B,C)$, dont le volume signé est donné par le produit mixte :
$$
V_\text{tétra}(O,A,B,C)
= \frac{1}{6}, (A - O) \cdot \big[ (B - O) \times (C - O) \big].
$$

Le volume total signé du polyèdre est alors la somme de ces contributions :
$$
V_\text{signé} = \sum_{j} \frac{1}{6}, (A_j - O) \cdot \big[ (B_j - O) \times (C_j - O) \big].
$$

Voir la fonction `volume_polyhedron_triangles`.
