## **Exponential quantum advantage in processing massive classical data** 

Haimeng Zhao,[1, 2,] _[ âˆ—]_ Alexander Zlokapa,[3] Hartmut Neven,[2] Ryan Babbush,[2] John Preskill,[1, 4] Jarrod R. McClean,[2] and Hsin-Yuan Huang[4, 1,] _[ â€ ]_ 

> _1California Institute of Technology, Pasadena, California 91125, USA_ 

> _2Google Quantum AI, Venice, California 90291, USA_ 

> _3Massachusetts Institute of Technology, Cambridge, Massachusetts 02139, USA_ 

> _4Oratomic, Pasadena, California 91125, USA_ 

Broadly applicable quantum advantage, particularly in classical data processing and machine learning, has been a fundamental open problem. In this work, we prove that a small quantum computer of polylogarithmic size can perform large-scale classification and dimension reduction on massive classical data by processing samples on the fly, whereas any classical machine achieving the same prediction performance requires exponentially larger size. Furthermore, classical machines that are exponentially larger yet below the required size need superpolynomially more samples and time. We validate these quantum advantages in real-world applications, including single-cell RNA sequencing and movie review sentiment analysis, demonstrating four to six orders of magnitude reduction in size with fewer than 60 logical qubits. These quantum advantages are enabled by quantum oracle sketching, an algorithm for accessing the classical world in quantum superposition using only random classical data samples. Combined with classical shadows, our algorithm circumvents the data loading and readout bottleneck to construct succinct classical models from massive classical data, a task provably impossible for any classical machine that is not exponentially larger than the quantum machine. These quantum advantages persist even when classical machines are granted unlimited time or if BPP = BQP, and rely only on the correctness of quantum mechanics. Together, our results establish machine learning on classical data as a broad and natural domain of quantum advantage and a fundamental test of quantum mechanics at the complexity frontier. 

## **I. INTRODUCTION** 

The search for useful quantum advantage has been a formidable challenge. Despite decades of effort since early foundational advances [1, 2], compelling end-to-end advantages with real-world impact have been established only for a few specialized tasks, most notably cryptanalysis and quantum simulation [3, 4]. These advantages rely on particular structures [5â€“7] exploitable by quantum machines which rarely arise in broader applications. Consequently, quantum computers are often seen as powerful but specialized devices, and whether their advantages extend beyond these narrow domains remains a central open question. 

Classical data processing and machine learning represent perhaps the most compelling test of this question, for we are macroscopic creatures in an effectively classical world. The scale of data generated across science, industry, and everyday computation has grown at an extraordinary pace, and the need to distill useful information from it has driven the overwhelming success of modern machine learning. Numerous quantum algorithms have been developed under the banner of quantum machine learning and quantum linear algebra [8â€“11] with the hope of bringing significant speedup to this domain, but their end-to-end advantage remains largely unclear [12]. 

The central challenge is that these algorithms require access to classical data in superposition, modeled as _quantum oracle queries_ , which is fundamentally in tension with the classical access the world provides. Existing attempts to resolve this tension proceed by storing the entire dataset in a quantum random access memory (QRAM) [13â€“15], but maintaining such coherent access incurs significant overhead in fault-tolerance and control [16], to the point where the classical co-processors required to sustain a QRAM could often be repurposed to solve the tasks directly. Skepticism about the practical impact of quantum processing on machine learning [17â€“19] has been reinforced by several factors: proposed quantum speedups often rely on highly contrived problems [20â€“28], numerous proposed algorithms have been dequantized [29â€“31], and training of quantum variational models can be difficult in practice [32â€“41]. We provide a review of related works in Section B. 

This challenge points to a more fundamental tension between machine size and data scale. Even for classical machines, processing massive data has become a critical bottleneck across science and technology, from machine learning [42â€“45] and single-cell RNA sequencing [46â€“48] to particle colliders [49â€“51] and astronomical sky surveys [52]. Classical streaming, sketching, and online learning algorithms [53â€“62] offer partial relief by processing 

> _âˆ—_ Corresponding author: haimeng@caltech.edu 

> _â€ _ Corresponding author: hhuang@oratomic.com; hsinyuan@caltech.edu 

2 

## **(a) Classical data** 

**==> picture [474 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
Classical data (b) Data collection<br>Small quantum chip<br>Science Day 1 Day 2 Day 3<br>machine<br>size<br>Engineering 1 S is e o<br>Ã©s Quantum  ofs y * r<br>sketch<br>Internet A I (c) Quantum advantage : _<br>1 0 0 1 0 1 1 0<br>Classical  machine size<br>Market ?<br>L~ Lal storage J<br>Task superpoly( N )<br>1 â€” O ( N [0] [.] [99] )<br>O Ëœ( N )<br>problem size  N classical data centerMassive   poly(log  N ) time<br>1<br>0<br>1<br>0<br>1<br>0<br>1<br>1<br>0<br>1<br>**----- End of picture text -----**<br>


FIG. 1: **Overview of quantum advantage in processing massive classical data. (a)** We prove that a quantum computer can outperform exponentially larger classical machines in a wide range of classical data processing tasks, including solving linear systems, classification, and dimension reduction. **(b)** Our quantum algorithm enables coherent quantum queries to the noisy and evolving classical world. **(c)** For various classical data processing tasks with problem size _N_ , a poly(log _N_ )-size quantum machine can succeed in _O_[Ëœ] ( _N_ ) time using quantum oracle sketching. In contrast, we prove that any classical machine, even with exponentially larger size _O_ ( _N_[0] _[.]_[99] ), cannot solve the same task unless given time super-polynomial in _N_ . This exponential quantum advantage relies only on the principle of quantum superposition, independent of any computational complexity conjectures. 

data samples on the fly, using incrementally updated models without storing the entire dataset. However, in reducing machine size these techniques also sacrifice prediction accuracy. This raises a foundational question: 

_Can small quantum machines leverage the exponential dimensionality of quantum Hilbert spaces to learn and predict better than exponentially larger classical machines?_ 

At first glance, such a space advantage may appear to be unlikely. Holevoâ€™s bound shows that only _n_ classical bits can be stored in an _n_ -qubit state [63], and prior results imply that a large space advantage is not possible when the entire dataset is stored [64, 65]. Existing demonstrations of exponential space advantage are restricted to streaming tasks specifically designed to be classically hard [66â€“73], many of which become classically easy under random sampling and ordering, and none of which correspond to natural machine learning tasks. In this work, we resolve this question by proving exponential space advantages in a variety of classical processing tasks. We prove that a small quantum computer of poly(log _N_ ) size can perform large-scale classification, dimension reduction, and linear system solving on massive classical data by processing classical data samples on the fly, whereas any classical machine achieving the same performance requires exponentially larger size or superpolynomially more samples and time, as summarized in Figure 1. We illustrate the practical relevance of this approach through numerical experiments on real-world datasets; for movie review sentiment analysis and single-cell RNA sequencing we demonstrate reductions in size by six orders of magnitude compared to classical sparse-matrix and QRAM-based algorithms, and by four orders of magnitude compared to classical streaming algorithms, all while using fewer than 60 logical qubits. 

Our results are enabled by a new framework, _quantum oracle sketching_ , which resolves the tension between quantum query access and classical data. Rather than storing the full dataset, this algorithm constructs coherent quantum queries from streaming classical data samples. Each sample is processed once and then immediately discarded, as a sequence of carefully designed quantum operations incrementally builds an approximate oracle that can be used within quantum algorithms. The required number of classical data samples scales quadratically with the number of quantum queries used. We prove the optimality of this quadratic scaling, which arises from the quadratic relationship between quantum amplitudes and probabilities governed by the Born rule. 

Quantum oracle sketching natively handles noisy and correlated data with generic distributions and data structures. We use it to construct state preparation unitaries of vectors and block encodings of matrices. Combined with classical shadow tomography [74] for efficient readout, our quantum algorithms enable the construction of compact and accurate classical models from massive classical data, a task provably impossible for any classical machine that is not exponentially larger. We provide a code implementation in JAX and benchmark its performance via numerical simulation. 

We prove classical hardness by establishing a fundamental relation between machine size and query complexity. For any oracle problem with exponential classical query complexity, if it can be solved in polynomial quantum 

3 

**==> picture [413 x 14] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a) Movie review sentiment analysis (b) Single cell RNA sequencing<br>**----- End of picture text -----**<br>


**==> picture [428 x 49] intentionally omitted <==**

**----- Start of picture text -----**<br>
â€œOne of the best movies.â€<br>T cell<br>movie<br>â€œStory makes no sense.â€<br>B cell<br>**----- End of picture text -----**<br>


FIG. 2: **Numerical experiments demonstrating exponential quantum advantage in real-world datasets.** We perform binary classification and dimension reduction for **(a)** sentiment analysis of movie reviews from the Internet Movie Database (IMDb) [79] and **(b)** single-cell RNA sequencing analysis of peripheral blood mononuclear cells (PBMC) [80]. We compare four general-purpose algorithms: quantum oracle sketching (orange), quantum algorithms using QRAM (gray), classical sparse-matrix algorithms (gray), and classical streaming algorithms (blue). For each algorithm, we truncate the dimension to filter out a varying number of rare features to plot the trade-off between machine size and performance, with standard error indicated by the shaded region. Machine size is defined as the total consumption of fundamental memory units: logical qubits for quantum and floating-point numbers for classical. Performance is quantified by the 5-fold cross validation accuracy averaged over random category pairs and explained variance relative to the untruncated baseline. 

space with slightly better than quadratic quantum query advantage, then there is a corresponding learning task using random classical data samples for which any classical machine requires exponentially larger size than the quantum machine to perform the task successfully. This quantum advantage is information-theoretic and unconditional, relying only on the validity of quantum mechanics; it persists even if classical machines are granted unlimited time or if BPP = BQP. Consequently, experimental confirmation or disproof of our results would provide a fundamental test of quantum mechanics at the complexity frontier [73, 75], analogous to how Bell inequalities [76] test quantum nonlocality [77, 78]. 

## **II. MAIN RESULTS** 

We begin by modeling how a machine processes massive amounts of classical data generated in the real world, which are typically random and noisy. The machine observes one classical data sample _z_ at a time, processes the sample, updates its memory, and moves on to the next. Each data sample may represent, for example, a point of a function _z_ = ( _x, f_ ( _x_ )) obtained from experimental observations, an entry _z_ = ( _i, j, Aij_ ) of a matrix describing a dynamical system, or a feature vector and label _z_ = ( _i, âƒ—xi, yi_ ) from user activity on the internet. After _M_ time steps, the machine has processed samples _z_ 1 _, . . . , zM_ . The goal is to use these samples to learn properties of the underlying _data generation process D_ , ranging from basic statistics to complex models such as classifying cells based on RNA sequences or predicting the next word in a sentence or the next frame of a video. 

In realistic settings, the data generation process may evolve over time, introducing time-varying features and correlations across multiple time scales, such as the ubiquitous 1 _/f_ noise in electronic devices or weatherdependent fluctuations in astronomical observations (Figure 1(b)). In such a dynamic process, each data point _z_ is sampled from a distribution depending on the current _situation_ , which evolves as time progresses. We formalize this setting as a hierarchical model in Section C 1. 

To quantify this correlation structure, we introduce two parameters. The _refreshing time Ï„_ is the time scale beyond which samples become effectively uncorrelated, and the _repetition number R_ is the maximum expected number of times a sample is repeated within a window of _Ï„_ time steps. A larger _R_ implies greater redundancy in that the same information is repeated multiple times, requiring proportionally more samples to gather sufficient 

4 

information to solve a task. For simplicity, we assume _R_ = _O_ (1) in the main text. All of our results extend to general _R_ , where sample complexity scales linearly with _R_ . 

One of the most fundamental tasks in science and engineering is solving linear systems, a key subroutine in regression, optimization, and differential equations. As dataset sizes, sampling rates, or precision requirements increase, the dimension _N_ of these systems can become extremely large. Consider, for example, a power grid in an integrated circuit or civil infrastructure network, modeled as a graph with a massive number of nodes and edges. According to Ohmâ€™s law and Kirchhoffâ€™s laws, measurements of resistances and voltages yield a sparse and well-conditioned _N_ -dimensional linear system _Aâƒ—x_ = _[âƒ—] b_ , where _A âˆˆ_ R _[N][Ã—][N]_ encodes the resistances, _[âƒ—] b âˆˆ_ R _[N]_ the voltage values, and _âƒ—x_ the unknown currents. The accessible data are of the form _z_ = ( _i, j, Aij, k, bk_ ), where _Aij_ is a resistance measurement and _bk_ a voltage measurement. To avoid overheating in critical components, we want to estimate the heat dissipation in the network. By Jouleâ€™s law, this is given by a quadratic form _âƒ—x[T] Mâƒ—x_ , where _M âˆˆ_ R _[N][Ã—][N]_ specifies the components of interest. 

In Section F 1, we formally define this task as estimating the normalized value of an efficiently measurable quadratic form to some error, given access to sampled data _z_ = ( _i, j, Aij, k, bk_ ) from a sparse and well-conditioned linear system _Aâƒ—x_ = _[âƒ—] b_ . Here _i, j_ specifies a uniformly random non-zero entry of _A_ and _k_ specifies a uniformly random component of _[âƒ—] b_ . For this linear system task, we prove the following, where the exponent 0 _._ 99 for the classical machine size can be replaced by any constant less than one. 

**Theorem 1** (Solving linear systems; formalized in Theorem F.3) **.** _Using O_[Ëœ] ( _N_ ) _samples, a quantum computer with_ poly(log _N_ ) _size can solve the linear system task with dimension N , whereas any classical machine with O_ ( _N_[0] _[.]_[99] ) _size cannot._ 

In many realistic scenarios, the linear system evolves over time while the property we wish to estimate remains approximately fixed, due to fluctuating noise or changing environmental conditions. We formalize this as the _dynamic_ linear system task in Section F 1, in which the linear system changes every _Ï„_ samples but has approximately the same target property. For such a task, we can further establish the following super-polynomial quantum advantage in sample efficiency. 

**Theorem 2** (Solving dynamic linear systems; formalized in Theorem F.4) **.** _A quantum computer of_ poly(log _N_ ) _size can use O_[Ëœ] ( _N_ ) _samples to solve the dynamic linear system task with dimension N and Ï„_ = _O_[Ëœ] ( _N_ ) _, whereas any classical machine with O_ ( _N_[0] _[.]_[99] ) _size requires_ superpoly( _N_ ) _samples._ 

The applications of computation extend far beyond traditional science and engineering, encompassing a vast array of problems in pattern recognition and artificial intelligence, where machines autonomously learn from data to perform desired tasks. A canonical example is _classification_ . Consider a dataset of _N_ items, each represented by a sparse _D_ -dimensional feature vector _âƒ—xi âˆˆ_ R _[D]_ and a binary label _yi âˆˆ{_ +1 _, âˆ’_ 1 _}_ . Together, these form a training dataset with feature matrix _X âˆˆ_ R _[N][Ã—][D]_ and label vector _âƒ—y âˆˆ_ R _[N]_ . The accessible data consist of samples _z_ = ( _i, âƒ—xi, yi_ ), where _âƒ—xi_ is a uniformly random row of _X_ and _yi_ is the corresponding label. 

This framework captures many real-world tasks. In _sentiment analysis_ , for instance, millions of users on e-commerce or video streaming platforms write reviews of products or movies; each vector _âƒ—xi_ encodes a review, and each label _yi âˆˆ{_ +1 _, âˆ’_ 1 _}_ indicates whether the review is positive or negative. Accurately classifying such reviews helps businesses make informed commercial decisions. A standard approach to classification is the _leastsquares support vector machine_ (LS-SVM), also known as the ridge classifier. It identifies a hyperplane decision boundary with normal vector _âƒ—w âˆˆ_ R _[D]_ by minimizing the regularized loss _L_ ( _âƒ—w_ ) = _âˆ¥X âƒ—w âˆ’ âƒ—yâˆ¥_ 2[2][+] _[ Î»][âˆ¥][âƒ—w][âˆ¥]_[2] 2 _[,]_[where] _Î» >_ 0 is the _â„“_ 2 regularization parameter. The predicted label of a test sample _âƒ—x[â€²]_ is then given by sgn( _âƒ—x[â€²] Â· âƒ—w_ ). A test sample is said to be _classifiable_ if its margin from the decision boundary, _[|] âˆ¥[âƒ—x] âƒ—w[â€²][Â·] âˆ¥[âƒ—w]_ 2 _[|][,]_[ is bounded away from zero.] 

In Section F 2, we formalize this as the following learning task: given sample access to data _z_ = ( _i, âƒ—xi, yi_ ) drawn from a sparse training set ( _X, âƒ—y_ ) that is well-conditioned after regularization, predict the label of any sparse and classifiable test vector _âƒ—x[â€²]_ according to the LS-SVM decision rule. For a binary classification task of dimension _N Ã— D_ , we establish the following quantum advantage. 

**Theorem 3** (Classification; formalized in Theorem F.11) **.** _Using O_[Ëœ] ( _N_ ) _samples, a quantum computer with_ poly(log _D_ ) _size can solve the binary classification task with N items and D-dimensional features, whereas any classical machine with O_ ( _D_[0] _[.]_[99] ) _size cannot._ 

In many realistic scenarios, the accessible training data evolves over time while the classification rule we wish to model remains approximately fixed. This time dependence may arise from changing user behaviors or language habits. We formalize this more challenging setting as the _dynamic_ binary classification task in Section F 2, in which the dataset is refreshed every _Ï„_ samples while the underlying classification rule stays the same. For this task, we prove the following super-polynomial quantum advantage in sample efficiency. 

**Theorem 4** (Dynamic classification; formalized in Theorem F.12) **.** _A quantum computer with_ poly(log _D_ ) _size can use O_[Ëœ] ( _N_ ) _samples to solve the dynamic binary classification task with N items, D features, and Ï„_ = _O_[Ëœ] ( _N_ ) _, whereas any classical machine with O_ ( _D_[0] _[.]_[99] ) _size requires_ superpoly( _N_ ) _samples._ 

5 

Supervised tasks such as classification require labels to guide the learning process, which may be inaccessible or prohibitively expensive to obtain, particularly when the goal is to discover unknown patterns latent in the data. Such scenarios call for _unsupervised_ learning approaches. A canonical example is _dimension reduction_ , which aims to distill high-dimensional data into a small number of explanatory variables so that hidden structure may be revealed. 

Consider _N_ items, each associated with a sparse _D_ -dimensional feature vector _âƒ—xi âˆˆ_ R _[D]_ . A prominent use case arises in modern biology, where experimental advances enable the generation of large volumes of unlabeled data. In _single-cell RNA sequencing_ (scRNA-seq), for instance, each item is a cell encoded as a sparse vector _âƒ—xi âˆˆ_ R _[D]_ representing its gene expression profile. The accessible data are of the form _z_ = ( _i, âƒ—xi_ ), forming a dataset _X âˆˆ_ R _[N][Ã—][D]_ . To discover unknown cell types or developmental trajectories hidden within this high-dimensional gene expression space, one applies _principal component analysis_ (PCA), which identifies the direction _âƒ—w âˆˆ_ R _[D]_ , _âˆ¥âƒ—wâˆ¥_ = 1, of maximum variance _âƒ—w[âŠ¤] X[âŠ¤] X âƒ—w_ , yielding low-dimensional representations _Î¾_ ( _âƒ—xi_ ) = _âƒ—xi Â· âƒ—w_ of the cells that distinguish, for example, T cells from B cells while filtering out noise. In many cases, a good initial estimate of the principal component is available by choosing an important feature with non-vanishing overlap with the true principal component; we refer to this initial estimate as a _guiding vector âƒ—g_ . Furthermore, the principal component is typically prominent enough that the spectral gap âˆ†between the largest and secondlargest eigenvalues of _X[âŠ¤] X_ does not vanish [81]. 

In Section F 3, we formalize dimension reduction as the task of estimating the low-dimensional representation _Î¾_ ( _âƒ—x[â€²]_ ) of any sparse test vector _âƒ—x[â€²]_ , given a guiding vector _âƒ—g_ and sample access to data _z_ = ( _i, âƒ—xi_ ) drawn from a sparse, spectrally gapped dataset _X_ , where _âƒ—xi_ is a uniformly random row of _X_ . For a dimension reduction task of dimension _N Ã— D_ , we prove the following quantum advantage. 

**Theorem 5** (Dimension reduction; formalized in Theorem F.21) **.** _Using O_[Ëœ] ( _N_ ) _samples, a quantum computer with_ poly(log _D_ ) _size can solve the dimension reduction task with N items and D features, whereas any classical machine with O_ ( _D_[0] _[.]_[99] ) _size cannot._ 

Analogously to the previous applications, we consider the more challenging dynamic variant in which the accessible data evolves over time while the principal component remains approximately fixed. This time dependence may arise from changing experimental conditions or donors. For a dynamic dimension reduction task with refreshing time _Ï„_ = _O_[Ëœ] ( _N_ ), we prove the following super-polynomial advantage in sample efficiency. 

**Theorem 6** (Dynamic dimension reduction; formalized in Theorem F.22) **.** _A quantum computer with_ poly(log _D_ ) _size can use O_[Ëœ] ( _N_ ) _samples to solve the dynamic dimension reduction task with N items, D features, and Ï„_ = _O_[Ëœ] ( _N_ ) _, whereas any classical machine with O_ ( _D_[0] _[.]_[99] ) _size requires_ superpoly( _N_ ) _samples._ We conduct numerical experiments to demonstrate these quantum advantages in real-world applications, including sentiment analysis of movie reviews from the Internet Movie Database (IMDb) [79] and single-cell RNA sequencing (scRNA-seq) analysis of peripheral blood mononuclear cells (PBMCs) [80]. To handle limited memory in realistic scenarios, we truncate the feature dimension of each sample by discarding rare features (e.g., infrequent words in text or rare genes in RNA sequences). Varying this truncation threshold traces the trade-off between machine size and task performance. 

In Figure 2, we plot on a log scale the relationship between machine size and prediction performance for binary classification and dimension reduction across four algorithmic approaches: our quantum oracle sketching algorithm (orange), classical streaming algorithms (blue), classical sparse-matrix algorithms (gray), and QRAMbased quantum algorithms (gray). Performance is quantified by the 5-fold cross-validation accuracy (averaged over random category pairs) for classification, and the explained variance of the first principal component relative to the untruncated baseline for dimension reduction. Machine size is defined as the total number of fundamental memory units: logical qubits for quantum processors and floating-point numbers for classical machines. To isolate size scaling, we assume access to sufficient samples and computation time. As a conservative lower bound, we use the feature dimension as the memory consumption for classical streaming algorithms [60, 61], and the number of nonzero elements for classical sparse-matrix and QRAM-based quantum algorithms. We note that these classical baselines are general-purpose algorithms with provable guarantees; comparisons with dataset-specific heuristics are left to future work, as their performance requires extensive empirical study. 

The results demonstrate that to achieve high performance, the memory required by quantum oracle sketching remains nearly constant, whereas that of classical and QRAM-based approaches grows exponentially. This yields quantum advantages of four to six orders of magnitude using fewer than 60 logical qubits. In Section A, we provide further details and additional experiments demonstrating the broad applicability of this advantage on datasets spanning social media topic analysis and pharmaceutical drug discovery. 

6 

~~N=125 N=125~~ **(a) Quantum sketching (b)** 10 ~~-2 @& N=250N=500~~ 10 ~~_~~ 4 ~~E@ N=250N=500~~ **20 6 17 3 5** _x_ ~~& N=1000 % N=1000~~ Â© 10 ~~73~~ 10 ~~-5~~ **1 0 1 1 0** _f_ ( _x_ ) e wi 10 ~~-4~~ 10 ~~-6~~ **oracle** ~~**Boolean function Vector** â€” Fit: M=4.8N1/e100 â€” Fit: M=0.9N1l/e1.00~~ _â†’_ ~~_O_~~ 10 ~~-> RMS rel. err.: 0.3%~~ 10 ~~-7 RMS rel. err.: 0.3%~~ 10Â° 10Â° 10â€ 108 10â€™ 108 10Â° **# samples** ~~-1~~ _M_ = !( _N/Ï‰_ ) 10 ~~5 Nanz= 250~~ 10 ~~N=50 & None =500 Â¢@ N=100 |S Nz =1000 |~~ 10 ~~72 |e N=200 -3 @ Nowe =2000 @ N=400~~ Â» 10 ~~_O_~~ ui 10 ~~-4~~ ~~_O[â€ ]_~~ ~~**Matrix element**~~ 10 ~~-4~~ ~~**Matrix index**~~ 1075 ~~& â€” Fit: M=1.1N e100 â€” Fit: M=2.2(NlogyNy! !/e100 RMS rel. err.: 1.2%~~ 10 ~~-5 RMS rel. err.: 2.9%~~ **any quantum query algorithm** 10Â° 106 107 108 10Â° 10Â° 107 108 Number of samples4â€œ Number of samplesM@ FIG. 3: **Access the classical world in superposition with quantum oracle sketching. (a)** An example of making quantum coherent query to a Boolean function using its classical data ( _x, f_ ( _x_ )) with quantum oracle sketching. Upon receiving each classical sample ( _x, f_ ( _x_ )), we apply a multi-controlled phase gate exp( _iÎ¸ |xâŸ©âŸ¨x|_ ) _, Î¸ âˆ f_ ( _x_ ). With _M_ = Î˜( _N/Ïµ_ ) samples, the resulting random unitary channel approximates the phase oracle _O_ : _|xâŸ©â†’_ ( _âˆ’_ 1) _[f]_[(] _[x]_[)] _|xâŸ©_ of _f_ to _Ïµ_ error in diamond distance. This allows us to instantiate oracle queries in any quantum query algorithm that extracts the desired property of _f_ . **(b)** Numerical experiments benchmarking the number of samples _M_ needed to approximate various oracle queries to _Ïµ_ operator norm error of the expected unitary, which upper bounds the diamond distance error, as a proxy. We consider oracles of Boolean functions, state preparation unitaries of any vectors, and the sparse matrix element and index oracles of any sparse matrices. We use _N_ to denote the domain size of Boolean functions, the dimension of vectors, and the dimension of square matrices. _N_ nnz represents the number of non-zero elements in a sparse matrix. The solid lines represent the fitted sample complexity scaling, with fitted parameters and root-mean-squared relative errors (RMS rel. err.) listed. **III. ORIGIN OF ADVANTAGE A. Quantum Oracle Sketching** We prove the main results by introducing _quantum oracle sketching_ , a quantum data-loading algorithm that resolves the fundamental tension between the quantum coherent queries we need and the classical data access the world provides. It allows us to access the classical world in quantum superposition using only classical data samples, without the overhead of storing the entire dataset. We achieve this by applying a sequence of incremental quantum rotations using fresh data samples on the fly. Each data sample is processed once and then immediately discarded without being stored. With the oracles instantiated by quantum oracle sketching, we can execute any quantum query algorithm, including various quantum linear algebra algorithms [82â€“84], to prepare small quantum states that encode the solutions to the application tasks. Finally, we apply a variant of classical shadow tomography [74] to efficiently extract classical outputs, thereby solving the application tasks in an end-to-end fashion. The idea of applying incremental quantum rotations based on data samples is reminiscent of classical streaming algorithms, which also update a model on the fly without storing the full dataset. However, the coherence requirement of quantum computation may seem at first to rule out this approach; wonâ€™t the randomness and entropy in the data, continuously pumped into the quantum machine, cause it to decohere quickly? To be more precise, suppose we have _M_ data samples _z_ 1 _, . . . , zM_ uniformly drawn from _N_ possibilities. For each sample _zt_ we apply a small rotation exp( _ihzt/M_ ) driven by some Hamiltonian _hzt_ with constant operator norm. One might hope that the resulting evolution approximates evolution governed by the expected Hamiltonian exp( _i_ E[ _hz_ ]) _â‰ˆ_ exp( _i t[h][z][t][/M]_[).][Unfortunately,][results][from][studies][of][randomized][Hamiltonian] simulation show that the error compounds to _Ïµ âˆ¼ N_[2] _/M_ in general [85â€“87]. Hence the randomness in the data destroys the coherence of the quantum machine, incurring a large error, unless the number of samples is at least _M âˆ¼ N_[2] . However, as we discuss in Section D 2, consuming _N_[2] samples to generate just a single quantum query eliminates any potential quantum advantage. 

7 

To overcome decoherence while retaining advantage, we design the incremental rotations so that their contributions accumulate coherently. The general mechanism can be illustrated by sketching the phase oracle of a Boolean function _f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ , summarized in Figure 3(a). Consider a sequence of _M_ independent samples _zt_ = ( _xt, f_ ( _xt_ )) _, t_ = 1 _, . . . , M_ , where _xt_ is sampled uniformly from [ _N_ ] = _{_ 1 _, . . . , N }_ with distribution _p_ ( _x_ ) = 1 _/N_ . Our goal is to implement the phase oracle 

**==> picture [292 x 13] intentionally omitted <==**

To achieve this goal, upon receiving each sample ( _xt, f_ ( _xt_ )), we apply a multi-controlled phase gate 

**==> picture [306 x 11] intentionally omitted <==**

for some _Ï„_ to be chosen later, which applies a small phase rotation to the basis state _|xtâŸ©_ and leaves all other basis states unchanged. After processing all _M_ samples, the resulting unitary is 

**==> picture [399 x 31] intentionally omitted <==**

where _mx_ =[ï¿½] _t_[1[] _[x][t]_[=] _[ x]_[]] _[/M]_[is][the][empirical][frequency][of] _[x]_[.] As the sample size _M_ grows, the frequency _mx_ concentrates around the probability _p_ ( _x_ ) = 1 _/N_ . Therefore, choosing the evolution time to be _Ï„_ = _Ï€N_ so that _Ï„mx â‰ˆ Ï„p_ ( _x_ ) = _Ï„/N_ = _Ï€_ , the random gate sequence _V_ approaches the phase oracle as desired: 

**==> picture [408 x 30] intentionally omitted <==**

In Section D, we rigorously prove that the error of this procedure scales as _Ïµ âˆ¼ N/M_ , substantially better than the _Ïµ âˆ¼ N_[2] _/M_ scaling for generic Hamiltonians. The key point is that Hamiltonians associated with distinct values of _x_ act on mutually orthogonal subspaces, which prevents errors from accumulating across different basis states. Consequently, _M_ = Î˜( _N/Ïµ_ ) samples suffice to construct an _Ïµ_ -error approximation in diamond distance (Theorem D.12). The inverse and controlled oracles can be constructed similarly by negating _Ï„_ or adding control to each gate. 

The above procedure allows us to execute any quantum query algorithm by sketching each oracle query with classical data samples. To run an algorithm making _Q_ queries with total error _Ïµ_ , we set the error of each oracle sketch to be _Ïµ/Q_ . Since each query consumes Î˜( _N/_ ( _Ïµ/Q_ )) samples, we need 

**==> picture [319 x 13] intentionally omitted <==**

samples in total. In Section D 3, we prove that this sample complexity is optimal. The quadratic dependence on _Q_ is the necessary price to pay for converting classical samples into coherent quantum queries, mirroring the relationship between quantum amplitudes and probabilities in the Born rule. 

To generalize quantum oracle sketching beyond simple data distributions and orthogonal Hamiltonians, we develop a suite of algorithmic and theoretical tools in Section D 4 that enable applications to a wide range of data distributions and data structures. Contrary to its apparent susceptibility to decoherence, we prove that quantum oracle sketching naturally handles noisy and correlated data with time-varying features, only at the cost of its sample complexity being multiplied by the repetition number _R_ of the data generation process. This factor is intuitive, as we need _R_ times more samples if each sample is repeated _R_ times. 

We further generalize the method to handle unknown or non-uniform data distributions via the quantum singular value transformation (QSVT). For applications related to linear algebra, we extend quantum oracle sketching to construct the state preparation unitaries of arbitrary vectors, which we call _quantum state sketching_ , as well as sparse oracles and block encodings of matrices. These extensions are enabled by combining a suite of algorithmic techniques including QSVT, in-place binary search, oblivious amplitude amplification, and a randomized Hadamard transform. These extensions involve non-orthogonal quantum rotations and hence their performance guarantees require significantly more sophisticated variance analysis that we detail in Section D 5. 

In Figure 3(b), we benchmark the empirical sample complexity of quantum oracle sketching on various data structures. We generate random Boolean functions, unit vectors, and sparse matrices, use quantum oracle sketching to approximate their oracle queries, and calculate the average error, for a wide range of dimensions and sample sizes. We report the operator norm error of the expected unitary, which upper bounds the diamond distance, as a proxy. To isolate the performance of quantum oracle sketching without the overhead of QSVT, we report results for vectors without amplitude amplification and assume random row access to construct matrix row index oracles as in the binary classification and dimension reduction tasks. The results show accurate agreement with theoretical predictions, highlighted by the favorable constants and exponents in the sample complexity extracted by least-squares fit, with root-mean-squared relative errors all below 3%. Further details are provided in Section A. 

8 

## **B. Interferometric Classical Shadows** 

With the data successfully loaded into the quantum computer, the remaining challenge is to efficiently read out classical results. In particular, we need to retain the sign structures that are necessary in applications such as SVM, where the sign of the inner product between the weight vector and the data vector determines the predicted label. To this end, we develop the _interferometric classical shadow_ algorithm in Theorem F.16, which combines the idea of the Hadamard test with the efficient offline prediction capability of classical shadow tomography. This method allows us to construct a completely classical model that can compute predictions for an arbitrary number of sparse test inputs. 

Remarkably, this shows that quantum technology can compress relevant information in classical data into a very compact classical representation without sacrificing accuracy, which would be impossible with classical machines alone unless provided with exponentially larger memory. This achievement does not violate the Holevo bound; rather it exploits the structure of a task to enable highly efficient extraction of useful outputs. 

## **C. Classical Hardness** 

Having shown that quantum machines excel at these tasks, it remains to prove classical hardness to rigorously establish quantum advantage. We do so by connecting advantage in machine size to separation in query complexity. In particular, we consider the task of estimating a property of some Boolean function _f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ using noisy query data, which we formalize as Noisy Oracle Property Estimation (NOPE) in Section E 1. Its complexity is characterized by the classical query complexity _QC_ of the target property, which captures the amount of information about _f_ that a classical machine has to extract to estimate the property. 

To obtain a lower bound on the space required by a classical machine, we consider a NOPE task such that each piece of useful information is scattered across blocks of _N_ noisy samples. To extract it, the machine must store the noisy information from one block in its memory of size _S_ and combine it with the next. Consequently, after _M_ samples, the machine can carry at most _S_ bits across the _O_ ( _M/N_ ) block boundaries, retrieving at most _S Â· O_ ( _M/N_ ) bits of information. To solve the task, this must be at least _QC_ , yielding a tradeoff between space and sample size for any classical machine: 

**==> picture [279 x 11] intentionally omitted <==**

We formally prove this lower bound in Section E 3 using communication complexity tools [88â€“94]. Combining this bound with the sample complexity _M_ = Î˜( _NQ_[2] ) of quantum oracle sketching yields the following fundamental relation between space advantage and oracle query separation. 

**Theorem 7** (Space advantage from oracle separation; formalized in Theorem E.2) **.** _To solve a NOPE task with quantum query complexity Q and classical query complexity QC using the same number of samples needed by quantum machines, any classical machine must be of size at least_ â„¦( _QC/Q_[2] ) _._ 

When the NOPE task has exponentially large classical query complexity and can be solved in poly(log _N_ ) quantum space with a super-quadratic quantum query advantage, Theorem 7 unconditionally implies a corresponding exponential quantum space advantage. For example, if _QC_ = Î˜( _N_ ) and _Q_ = _O_ ( _N_[0] _[.]_[49] ), then any classical algorithm using the same number of samples must have memory size at least _S â‰¥_ â„¦( _N_[0] _[.]_[02] ). As a concrete instance, consider the NOPE task of estimating the Forrelation property [95, 96], which exhibits the maximal average-case query separation: _Q_ = _O_ (1) and _QC_ = â„¦( _N_[1] _[âˆ’][Î¶]_ ) for any constant _Î¶ >_ 0. This immediately yields a large space separation between quantum and classical algorithms. 

From this space advantage result, we can derive a superpolynomial advantage in sample complexity. By developing a learning version of the XOR lemma [97â€“99] in Section E 4, we prove that classical machines without sufficient space are fundamentally unable to track dynamically evolving data distributions and therefore require superpolynomially more samples. Via reductions, we also prove that the classical hardness of NOPE implies classical hardness for our target applications. Specifically, we prove in Section E 5 that tasks such as predicting labels or obtaining low-dimensional representations of test data are BQP-hard. Thus any algorithm that solves these tasks can be used to simulate the quantum circuit that solves NOPE. Because we have already established that NOPE is classically hard, the classical hardness of these other applications follows. 

## **IV. DISCUSSION** 

In this work, we establish classical data processing and machine learning as a broad domain of exponential quantum advantage, extending the reach of quantum computation beyond specialized tasks. We demonstrate this 

9 

advantage across fundamental applications including solving linear systems, binary classification, and dimension reduction. Notably, our exponential separation reaches the ultimate limit allowed by quantum mechanics, since a classical machine with _O_[Ëœ] ( _N_ ) size can always store the full dataset and simulate a poly(log _N_ )-qubit quantum computation with only poly(log _N_ ) space overhead [64, 65]. 

Our results are enabled by introducing quantum oracle sketching and interferometric classical shadows, which together circumvent the data loading and readout bottlenecks. These techniques allow the construction of exponentially compact classical models of massive classical data which could not be achieved efficiently without the use of quantum technology. The existence of such compact classical models demonstrates that, in useful tasks such as classification and dimension reduction, the relevant information has sufficient structure to permit its efficient extraction without violating the generic Holevo bound. 

Our numerical experiments support the practical relevance of these methods, showing orders-of-magnitude memory savings with fewer than 60 logical qubits. Extrapolating this scaling, while ignoring the exponential runtime overhead, suggests that relatively small quantum devices with hundreds of logical qubits could outperform even extremely large classical systems, barring unforeseen limitations to quantum mechanics. 

Beyond space advantages, we also establish super-polynomial advantage in sample complexity for dynamic tasks, where classical algorithms are fundamentally unable to track evolving data distributions. The runtime of quantum oracle sketching is dominated by the _O_[Ëœ] ( _N_ ) data loading time, which is unavoidable if each gate has only a constant number of degrees of freedom, but subsequent processing of each sample requires only poly(log _N_ ) time. Notably, the quantum oracle sketching algorithm is largely composed of commuting operations, suggesting significant opportunities for parallelization which might dramatically reduce the wall-clock runtime. Exploring such parallel implementations, potentially through hardware-software co-design and optimized quantum error correction architectures, is an important direction for future work [100]. 

We have presented quantum oracle sketching as a general classical-to-quantum converter that enables quantum queries to the classical world with provable guarantees even in the worst-case. There are substantial opportunities to extend and optimize this framework for practical tasks, both rigorously and heuristically. For instance, one may enhance its empirical performance by introducing trainable and variational components, or by integrating it into hybrid quantum-classical data processing pipelines. While we have focused here on linear systems, classification, and dimension reduction, we expect similar quantum advantages to arise from quantum oracle sketching applied to a broader spectrum of real-world tasks, including solving ordinary and partial differential equations, large-scale optimization, signal processing, and communication. Furthermore, since exponential space advantage follows generically from super-quadratic query separation, it may extend to problems previously thought to be dequantized, such as recommendation systems, where polynomial quantum speedups persist but memory bottlenecks can be critical. 

From a fundamental physics perspective, our results are information-theoretic and unconditional, relying solely on the principle of quantum superposition, independent of any computational conjectures. This quantum space advantage persists even if classical machines are granted unbounded computation time, or even in the unlikely scenario where polynomial-time quantum computation is no more powerful than classical (i.e., BPP = BQP), in which case there would be no super-polynomial time advantage in quantum simulation or cryptanalysis. 

Consequently, experimental confirmation or disproof of our results would serve as a fundamental test of quantum mechanics at the complexity frontier [75], probing the physical reality of exponentially large Hilbert spaces [101]. This is analogous to how Bell inequalities test quantum nonlocality, or how particle colliders and cosmological observations probe the Standard Model at the energy frontier. We believe that the prospect of enabling new applications of quantum devices to massive classical data, while also probing the physical limits of quantum mechanics, marks the beginning of an exciting new frontier in science and technology. 

## **Acknowledgments** 

We thank Dolev Bluvstein, Isaac Chuang, Ronald de Wolf, Dar Gilboa, Siddhartha Jain, Stephen Jordan, Robbie King, Ruohan Shen, and Umesh Vazirani for insightful discussions. We are grateful to Richard Allen, Soonwon Choi, and Angus Lowe for bringing to our attention a mathematical error in a prior work on randomized Hamiltonian simulation. H.Z. was a Student Researcher at Google Quantum AI when part of this work was done. A.Z. is supported by a Hertz Fellowship. J.P. acknowledges support from the U.S. Department of Energy, Office of Science, Accelerated Research in Quantum Computing, Fundamental Algorithmic Research toward Quantum Utility (FAR-Qu), and the National Science Foundation (PHY-2317110). H.H. acknowledges support from the Broadcom Innovation Fund and the U.S. Department of Energy, Office of Science, National Quantum Information Science Research Centers, Quantum Systems Accelerator. The Institute for Quantum Information and Matter is an NSF Physics Frontiers Center (PHY-2317110). 

10 

- [1] Richard P Feynman. Quantum mechanical computers. _Foundations of physics_ , 16(6):507â€“531, 1986. 

- [2] Peter W Shor. Algorithms for quantum computation: discrete logarithms and factoring. In _Proceedings 35th annual symposium on foundations of computer science_ , pages 124â€“134. Ieee, 1994. 

- [3] Ryan Babbush, Robbie King, Sergio Boixo, William Huggins, Tanuj Khattar, Guang Hao Low, Jarrod R McClean, Thomas Oâ€™Brien, and Nicholas C Rubin. The grand challenge of quantum applications. _arXiv preprint arXiv:2511.09124_ , 2025. 

- [4] John Preskill. Beyond NISQ: The megaquop machine. _ACM Transactions on Quantum Computing_ , 6(3):1â€“7, 2025. 

- [5] Alexei Kitaev. Quantum measurements and the abelian stabilizer problem. _arXiv preprint quant-ph/9511026_ , 1995. 

- [6] Seth Lloyd. Universal quantum simulators. _Science_ , 273(5278):1073â€“1078, 1996. 

- [7] Scott Aaronson and Andris Ambainis. The need for structure in quantum speedups. _arXiv preprint arXiv:0911.0996_ , 2009. 

- [8] Alexander M. Dalzell, Sam McArdle, Mario Berta, Przemyslaw Bienias, Chi-Fang Chen, AndrÂ´as GilyÂ´en, Connor T. Hann, Michael J. Kastoryano, Emil T. Khabiboulline, Aleksander Kubica, and et al. _Quantum Algorithms: A Survey of Applications and End-to-end Complexities_ . Cambridge University Press, 2025. 

- [9] AndrÂ´as GilyÂ´en, Yuan Su, Guang Hao Low, and Nathan Wiebe. Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics. In _Proceedings of the 51st annual ACM SIGACT symposium on theory of computing_ , pages 193â€“204, 2019. 

- [10] John M Martyn, Zane M Rossi, Andrew K Tan, and Isaac L Chuang. Grand unification of quantum algorithms. _PRX Quantum_ , 2(4):040203, 2021. 

- [11] Jacob Biamonte, Peter Wittek, Nicola Pancotti, Patrick Rebentrost, Nathan Wiebe, and Seth Lloyd. Quantum machine learning. _Nature_ , 549(7671):195â€“202, 2017. 

- [12] Scott Aaronson. Read the fine print. _Nature Physics_ , 11(4):291â€“293, 2015. 

- [13] Vittorio Giovannetti, Seth Lloyd, and Lorenzo Maccone. Quantum random access memory. _Physical Review Letters_ , 100(16):160501, 2008. 

- [14] Connor T Hann, Gideon Lee, SM Girvin, and Liang Jiang. Resilience of quantum random access memory to generic noise. _PRX Quantum_ , 2(2):020311, 2021. 

- [15] Alexander M Dalzell, AndrÂ´as GilyÂ´en, Connor T Hann, Sam McArdle, Grant Salton, Quynh T Nguyen, Aleksander Kubica, and Fernando GSL BrandËœao. A distillation-teleportation protocol for fault-tolerant QRAM. _arXiv preprint arXiv:2505.20265_ , 2025. 

- [16] Samuel Jaques and Arthur G Rattew. QRAM: A survey and critique. _Quantum_ , 9:1922, 2025. 

- [17] Maria Schuld and Nathan Killoran. Is quantum advantage the right goal for quantum machine learning? _PRX Quantum_ , 3(3):030101, 2022. 

- [18] Marco Cerezo, Martin Larocca, Diego GarcÂ´Ä±a-MartÂ´Ä±n, Nelson L Diaz, Paolo Braccia, Enrico Fontana, Manuel S Rudolph, Pablo Bermejo, Aroosa Ijaz, Supanut Thanasilp, et al. Does provable absence of barren plateaus imply classical simulability? or, why we need to rethink variational quantum computing. _arXiv preprint arXiv:2312.09121_ , 2023. 

- [19] Elies Gil-Fuster, Casper Gyurik, AdriÂ´an PÂ´erez-Salinas, and Vedran Dunjko. On the relation between trainability and dequantization of variational quantum learning models. _arXiv preprint arXiv:2406.07072_ , 2024. 

- [20] Haimeng Zhao and Dong-Ling Deng. Entanglement-induced provable and robust quantum learning advantages. _npj Quantum Information_ , 11(1):127, 2025. 

- [21] Xun Gao, Z-Y Zhang, and L-M Duan. A quantum machine learning algorithm based on generative models. _Science advances_ , 4(12):eaat9004, 2018. 

- [22] Xun Gao, Eric R Anschuetz, Sheng-Tao Wang, J Ignacio Cirac, and Mikhail D Lukin. Enhancing generative models via quantum correlations. _Physical Review X_ , 12(2):021037, 2022. 

- [23] Eric R Anschuetz, Hong-Ye Hu, Jin-Long Huang, and Xun Gao. Interpretable quantum advantage in neural sequence learning. _PRX Quantum_ , 4(2):020338, 2023. 

- [24] Eric R Anschuetz and Xun Gao. Arbitrary polynomial separations in trainable quantum machine learning. _Quantum_ , 10:1976, 2026. 

- [25] Zhihan Zhang, Weiyuan Gong, Weikang Li, and Dong-Ling Deng. Quantum-classical separations in shallow-circuitbased learning with and without noises. _Communications Physics_ , 7(1):290, 2024. 

- [26] Yunchao Liu, Srinivasan Arunachalam, and Kristan Temme. A rigorous and robust quantum speed-up in supervised machine learning. _Nature Physics_ , 17(9):1013â€“1017, 2021. 

- [27] Casper Gyurik and Vedran Dunjko. Exponential separations between classical and quantum learners. _arXiv preprint arXiv:2306.16028_ , 2023. 

- [28] Hsin-Yuan Huang, Michael Broughton, Norhan Eassa, Hartmut Neven, Ryan Babbush, and Jarrod R McClean. Generative quantum advantage for classical and quantum problems. _arXiv preprint arXiv:2509.09033_ , 2025. 

- [29] Ewin Tang. A quantum-inspired classical algorithm for recommendation systems. In _Proceedings of the 51st annual ACM SIGACT symposium on theory of computing_ , pages 217â€“228, 2019. 

- [30] Ewin Tang. Quantum principal component analysis only achieves an exponential speedup because of its state preparation assumptions. _Physical Review Letters_ , 127(6):060503, 2021. 

- [31] Ewin Tang. _Quantum machine learning without any quantum_ . University of Washington, 2023. 

- [32] Alberto Peruzzo, Jarrod McClean, Peter Shadbolt, Man-Hong Yung, Xiao-Qi Zhou, Peter J Love, AlÂ´an AspuruGuzik, and Jeremy L Oâ€™brien. A variational eigenvalue solver on a photonic quantum processor. _Nature Commu-_ 

11 

_nications_ , 5(1):4213, 2014. 

- [33] Jarrod R McClean, Jonathan Romero, Ryan Babbush, and AlÂ´an Aspuru-Guzik. The theory of variational hybrid quantum-classical algorithms. _New Journal of Physics_ , 18(2):023023, 2016. 

- [34] Marco Cerezo, Andrew Arrasmith, Ryan Babbush, Simon C Benjamin, Suguru Endo, Keisuke Fujii, Jarrod R McClean, Kosuke Mitarai, Xiao Yuan, Lukasz Cincio, et al. Variational quantum algorithms. _Nature Reviews Physics_ , 3(9):625â€“644, 2021. 

- [35] Marco Cerezo, Guillaume Verdon, Hsin-Yuan Huang, Lukasz Cincio, and Patrick J Coles. Challenges and opportunities in quantum machine learning. _Nature Computational science_ , 2(9):567â€“576, 2022. 

- [36] Yuxuan Du, Xinbiao Wang, Naixu Guo, Zhan Yu, Yang Qian, Kaining Zhang, Min-Hsiu Hsieh, Patrick Rebentrost, and Dacheng Tao. Quantum machine learning: A hands-on tutorial for machine learning practitioners and researchers. _arXiv preprint arXiv:2502.01146_ , 2025. 

- [37] Jarrod R McClean, Sergio Boixo, Vadim N Smelyanskiy, Ryan Babbush, and Hartmut Neven. Barren plateaus in quantum neural network training landscapes. _Nature Communications_ , 9(1):4812, 2018. 

- [38] Marco Cerezo, Akira Sone, Tyler Volkoff, Lukasz Cincio, and Patrick J Coles. Cost function dependent barren plateaus in shallow parametrized quantum circuits. _Nature Communications_ , 12(1):1791, 2021. 

- [39] Samson Wang, Enrico Fontana, Marco Cerezo, Kunal Sharma, Akira Sone, Lukasz Cincio, and Patrick J Coles. Noise-induced barren plateaus in variational quantum algorithms. _Nature Communications_ , 12(1):6961, 2021. 

- [40] Martin Larocca, Supanut Thanasilp, Samson Wang, Kunal Sharma, Jacob Biamonte, Patrick J Coles, Lukasz Cincio, Jarrod R McClean, ZoÂ¨e Holmes, and Marco Cerezo. Barren plateaus in variational quantum computing. _Nature Reviews Physics_ , pages 1â€“16, 2025. 

- [41] Eric R Anschuetz and Bobak T Kiani. Quantum variational algorithms are swamped with traps. _Nature Communications_ , 13(1):7760, 2022. 

- [42] Jared Kaplan, Sam McCandlish, Tom Henighan, Tom B Brown, Benjamin Chess, Rewon Child, Scott Gray, Alec Radford, Jeffrey Wu, and Dario Amodei. Scaling laws for neural language models. _arXiv preprint arXiv:2001.08361_ , 2020. 

- [43] William Fedus, Barret Zoph, and Noam Shazeer. Switch transformers: Scaling to trillion parameter models with simple and efficient sparsity. _Journal of Machine Learning Research_ , 23(120):1â€“39, 2022. 

- [44] Amir Gholami, Zhewei Yao, Sehoon Kim, Coleman Hooper, Michael W Mahoney, and Kurt Keutzer. Ai and memory wall. _IEEE Micro_ , 44(3):33â€“39, 2024. 

- [45] Emma Strubell, Ananya Ganesh, and Andrew McCallum. Energy and policy considerations for deep learning in nlp. In _Proceedings of the 57th annual meeting of the association for computational linguistics_ , pages 3645â€“3650, 2019. 

- [46] Valentine Svensson, Roser Vento-Tormo, and Sarah A Teichmann. Exponential scaling of single-cell rna-seq in the past decade. _Nature Protocols_ , 13(4):599â€“604, 2018. 

- [47] David LÂ¨ahnemann, Johannes KÂ¨oster, Ewa Szczurek, Davis J McCarthy, Stephanie C Hicks, Mark D Robinson, Catalina A Vallejos, Kieran R Campbell, Niko Beerenwinkel, Ahmed Mahfouz, et al. Eleven grand challenges in single-cell data science. _Genome biology_ , 21(1):31, 2020. 

- [48] Koki Tsuyuzaki, Hiroyuki Sato, Kenta Sato, and Itoshi Nikaido. Benchmarking principal component analysis for large-scale single-cell rna-sequencing. _Genome biology_ , 21(1):9, 2020. 

- [49] HEP Software Foundation, Johannes Albrecht, Antonio Augusto Alves Jr, Guilherme Amadio, Giuseppe Andronico, Nguyen Anh-Ky, Laurent Aphecetche, John Apostolakis, Makoto Asai, Luca Atzori, et al. A roadmap for hep software and computing r&d for the 2020s. _Computing and software for big science_ , 3(1):7, 2019. 

- [50] I. BÂ´ejar Alonso and others (Eds.). High-Luminosity Large Hadron Collider (HL-LHC): Technical design report. Technical Report CERN-2020-010, CERN, Geneva, 2020. 

- [51] Vardan Khachatryan, Albert M Sirunyan, Armen Tumasyan, Wolfgang Adam, E Asilar, Thomas Bergauer, Johannes Brandstetter, Erica Brondolin, Marko Dragicevic, Janos ErÂ¨o, et al. Search for narrow resonances in dijet final states at s= 8 tev with the novel cms technique of data scouting. _Physical Review Letters_ , 117(3):031802, 2016. 

- [52] Peter E Dewdney, Peter J Hall, Richard T Schilizzi, and T Joseph LW Lazio. The square kilometre array. _Proceedings of the IEEE_ , 97(8):1482â€“1496, 2009. 

- [53] Shanmugavelayutham Muthukrishnan et al. Data streams: Algorithms and applications. _Foundations and TrendsÂ® in Theoretical Computer Science_ , 1(2):117â€“236, 2005. 

- [54] Noga Alon, Yossi Matias, and Mario Szegedy. The space complexity of approximating the frequency moments. In _Proceedings of the twenty-eighth annual ACM symposium on theory of computing_ , pages 20â€“29, 1996. 

- [55] Philippe Flajolet and G Nigel Martin. Probabilistic counting algorithms for data base applications. _Journal of computer and system sciences_ , 31(2):182â€“209, 1985. 

- [56] Jayadev Misra and David Gries. Finding repeated elements. _Science of computer programming_ , 2(2):143â€“152, 1982. 

- [57] Graham Cormode and Shan Muthukrishnan. An improved data stream summary: the count-min sketch and its applications. _Journal of Algorithms_ , 55(1):58â€“75, 2005. 

- [58] David P Woodruff et al. Sketching as a tool for numerical linear algebra. _Foundations and TrendsÂ® in Theoretical Computer Science_ , 10(1â€“2):1â€“157, 2014. 

- [59] Kenneth L Clarkson and David P Woodruff. Numerical linear algebra in the streaming model. In _Proceedings of the forty-first annual ACM symposium on theory of computing_ , pages 205â€“214, 2009. 

- [60] Alexandr Andoni, Collin Burns, Yi Li, Sepideh Mahabadi, and David P Woodruff. Streaming complexity of svms. _arXiv preprint arXiv:2007.03633_ , 2020. 

- [61] Ioannis Mitliagkas, Constantine Caramanis, and Prateek Jain. Memory limited, streaming pca. _Advances in neural_ 

12 

_information processing systems_ , 26, 2013. 

- [62] Shai Shalev-Shwartz. Online learning and online convex optimization. _Foundations and TrendsÂ® in Machine Learning_ , 4(2):107â€“194, 2025. 

- [63] Alexander Semenovich Holevo. Bounds for the quantity of information transmitted by a quantum communication channel. _Problemy Peredachi Informatsii_ , 9(3):3â€“11, 1973. 

- [64] John Watrous. Space-bounded quantum complexity. _Journal of Computer and System Sciences_ , 59(2):281â€“326, 1999. 

- [65] John Watrous. On the complexity of simulating space-bounded quantum computations. _computational complexity_ , 12(1):48â€“84, 2003. 

- [66] FranÂ¸cois Le Gall. Exponential separation of quantum and classical online space complexity. In _Proceedings of the eighteenth annual ACM symposium on Parallelism in algorithms and architectures_ , pages 67â€“73, 2006. 

- [67] Rahul Jain and Ashwin Nayak. The space complexity of recognizing well-parenthesized expressions in the streaming model: the index function revisited. _IEEE Transactions on Information Theory_ , 60(10):6646â€“6668, 2014. 

- [68] John Kallaugher. A quantum advantage for a natural streaming problem. In _2021 IEEE 62nd Annual Symposium on Foundations of Computer Science (FOCS)_ , pages 897â€“908. IEEE, 2022. 

- [69] John Kallaugher, Ojas Parekh, and Nadezhda Voronova. Exponential quantum space advantage for approximating maximum directed cut in the streaming model. In _Proceedings of the 56th Annual ACM Symposium on Theory of Computing_ , pages 1805â€“1815, 2024. 

- [70] John Kallaugher, Ojas Parekh, and Nadezhda Voronova. How to design a quantum streaming algorithm without knowing anything about quantum computing. In _2025 Symposium on Simplicity in Algorithms (SOSA)_ , pages 9â€“45. SIAM, 2025. 

- [71] Dar Gilboa, Hagay Michaeli, Daniel Soudry, and Jarrod McClean. Exponential quantum communication advantage in distributed inference and learning. _Advances in Neural Information Processing Systems_ , 37:30425â€“30473, 2024. 

- [72] Pradeep Niroula, Shouvanik Chakrabarti, Steven Kordonowy, Niraj Kumar, Sivaprasad Omanakuttan, Michael A Perlin, MS Allman, JP Campora III, Alex Chernoguzov, Samuel F Cooper, et al. Realization of a quantum streaming algorithm on long-lived trapped-ion qubits. _arXiv preprint arXiv:2511.03689_ , 2025. 

- [73] William Kretschmer, Sabee Grewal, Matthew DeCross, Justin A Gerber, Kevin Gilmore, Dan Gresh, Nicholas Hunter-Jones, Karl Mayer, Brian Neyenhuis, David Hayes, et al. Demonstrating an unconditional separation between quantum and classical information resources. _arXiv preprint arXiv:2509.07255_ , 2025. 

- [74] Hsin-Yuan Huang, Richard Kueng, and John Preskill. Predicting many properties of a quantum system from very few measurements. _Nature Physics_ , 16(10):1050â€“1057, 2020. 

- [75] John Preskill. Quantum computing and the entanglement frontier. _arXiv preprint arXiv:1203.5813_ , 2012. 

- [76] John S Bell. On the problem of hidden variables in quantum mechanics. _Reviews of Modern physics_ , 38(3):447, 1966. 

- [77] John F Clauser, Michael A Horne, Abner Shimony, and Richard A Holt. Proposed experiment to test local hiddenvariable theories. _Physical Review Letters_ , 23(15):880, 1969. 

- [78] John F Clauser and Abner Shimony. Bellâ€™s theorem. experimental tests and implications. _Reports on Progress in Physics_ , 41(12):1881, 1978. 

- [79] Andrew Maas, Raymond E Daly, Peter T Pham, Dan Huang, Andrew Y Ng, and Christopher Potts. Learning word vectors for sentiment analysis. In _Proceedings of the 49th annual meeting of the association for computational linguistics: Human language technologies_ , pages 142â€“150, 2011. 

- [80] Grace XY Zheng, Jessica M Terry, Phillip Belgrader, Paul Ryvkin, Zachary W Bent, Ryan Wilson, Solongo B Ziraldo, Tobias D Wheeler, Geoff P McDermott, Junjie Zhu, et al. Massively parallel digital transcriptional profiling of single cells. _Nature Communications_ , 8(1):14049, 2017. 

- [81] Mark EJ Newman. Power laws, pareto distributions and zipfâ€™s law. _Contemporary physics_ , 46(5):323â€“351, 2005. 

- [82] Pedro CS Costa, Dong An, Yuval R Sanders, Yuan Su, Ryan Babbush, and Dominic W Berry. Optimal scaling quantum linear-systems solver via discrete adiabatic theorem. _PRX Quantum_ , 3(4):040303, 2022. 

- [83] Shantanav Chakraborty, Aditya Morolia, and Anurudh Peduri. Quantum regularized least squares. _Quantum_ , 7:988, 2023. 

- [84] Lin Lin and Yu Tong. Near-optimal ground state preparation. _Quantum_ , 4:372, 2020. 

- [85] Earl Campbell. Random compiler for fast hamiltonian simulation. _Physical Review Letters_ , 123(7):070503, 2019. 

- [86] Chi-Fang Chen, Hsin-Yuan Huang, Richard Kueng, and Joel A Tropp. Concentration for random product formulas. _PRX Quantum_ , 2(4):040305, 2021. 

- [87] Shelby Kimmel, Cedric Yen-Yu Lin, Guang Hao Low, Maris Ozols, and Theodore J Yoder. Hamiltonian simulation with optimal sample complexity. _npj Quantum Information_ , 3(1):13, 2017. 

- [88] Mika GÂ¨oÂ¨os, Toniann Pitassi, and Thomas Watson. Deterministic communication vs. partition number. In _2015 IEEE 56th Annual Symposium on Foundations of Computer Science_ , pages 1077â€“1088. IEEE, 2015. 

- [89] Mika Goos, Shachar Lovett, Raghu Meka, Thomas Watson, and David Zuckerman. Rectangles are nonnegative juntas. _SIAM Journal on Computing_ , 45(5):1835â€“1869, 2016. 

- [90] Mika Goos, Toniann Pitassi, and Thomas Watson. Query-to-communication lifting for bpp. _SIAM Journal on Computing_ , 49(4):FOCS17â€“441, 2020. 

- [91] Anurag Anshu, Shalev Ben-David, and Srijita Kundu. On query-to-communication lifting for adversary bounds. _arXiv preprint arXiv:2012.03415_ , 2020. 

- [92] Arkadev Chattopadhyay, Yuval Filmus, Sajin Koroth, Or Meir, and Toniann Pitassi. Query-to-communication lifting using low-discrepancy gadgets. _SIAM Journal on Computing_ , 50(1):171â€“210, 2021. 

- [93] Guangxu Yang and Jiapeng Zhang. Communication lower bounds for collision problems via density increment 

13 

   - arguments. In _Proceedings of the 56th Annual ACM Symposium on Theory of Computing_ , pages 630â€“639, 2024. 

- [94] Yumou Fei, Dor Minzer, and Shuo Wang. Multi-pass streaming lower bounds for approximating max-cut. _arXiv preprint arXiv:2503.23404_ , 2025. 

- [95] Scott Aaronson and Andris Ambainis. Forrelation: A problem that optimally separates quantum from classical computing. In _Proceedings of the forty-seventh annual ACM symposium on theory of computing_ , pages 307â€“316, 2015. 

- [96] Nikhil Bansal and Makrand Sinha. k-forrelation optimally separates quantum and classical query complexity. In _Proceedings of the 53rd Annual ACM SIGACT Symposium on Theory of Computing_ , pages 1303â€“1316, 2021. 

- [97] Andrew C Yao. Theory and application of trapdoor functions. In _Proceedings of the 23rd Annual Symposium on Foundations of Computer Science_ , pages 80â€“91, 1982. 

- [98] Falk Unger. A probabilistic inequality with applications to threshold direct-product theorems. In _2009 50th Annual IEEE Symposium on Foundations of Computer Science_ , pages 221â€“229. IEEE, 2009. 

- [99] Sepehr Assadi and Vishvajeet N. Graph streaming lower bounds for parameter estimation and property testing via a streaming xor lemma. In _Proceedings of the 53rd Annual ACM SIGACT Symposium on Theory of Computing_ , pages 612â€“625, 2021. 

- [100] Hengyun Zhou, Madelyn Cain, and Mikhail D Lukin. Opportunities in full-stack design of low-overhead faulttolerant quantum computation. _Nature Computational Science_ , 5(12):1110â€“1119, 2025. 

- [101] David Poulin, Angie Qarry, Rolando Somma, and Frank Verstraete. Quantum simulation of time-dependent hamiltonians and the convenient illusion of hilbert space. _Physical Review Letters_ , 106(17):170501, 2011. 

- [102] James Bradbury, Roy Frostig, Peter Hawkins, Matthew James Johnson, Chris Leary, Dougal Maclaurin, George Necula, Adam Paszke, Jake VanderPlas, Skye Wanderman-Milne, and Qiao Zhang. JAX: composable transformations of Python+NumPy programs, 2018. 

- [103] Thorsten Joachims. A probabilistic analysis of the rocchio algorithm with tfidf for text categorization. Technical report, Carnegie Mellon University, 1996. 

- [104] Jason Weston, Fernando Perez-Cruz, Olivier Bousquet, Olivier Chapelle, Andre Elisseeff, and Bernhard SchÂ¨olkopf. Feature selection and transduction for prediction of molecular bioactivity for drug design. _Bioinformatics_ , 19(6):764â€“ 771, 2003. 

- [105] Volker Bergen, Marius Lange, Stefan Peidli, F. Alexander Wolf, and Fabian J. Theis. Generalizing rna velocity to transient cell states through dynamical modeling. _Nature Biotechnology_ , 38(12):1408â€“1414, August 2020. 

- [106] F. Pedregosa, G. Varoquaux, A. Gramfort, V. Michel, B. Thirion, O. Grisel, M. Blondel, P. Prettenhofer, R. Weiss, V. Dubourg, J. Vanderplas, A. Passos, D. Cournapeau, M. Brucher, M. Perrot, and E. Duchesnay. Scikit-learn: Machine learning in Python. _Journal of Machine Learning Research_ , 12:2825â€“2830, 2011. 

- [107] Isabelle Guyon, Steve Gunn, Asa Ben-Hur, and Gideon Dror. Dorothea. UCI Machine Learning Repository, 2004. DOI: https://doi.org/10.24432/C5NK6X. 

- [108] Yulong Dong, Xiang Meng, K Birgitta Whaley, and Lin Lin. Efficient phase-factor evaluation in quantum signal processing. _Physical Review A_ , 103(4):042419, 2021. 

- [109] Hsin-Yuan Huang, Michael Broughton, Jordan Cotler, Sitan Chen, Jerry Li, Masoud Mohseni, Hartmut Neven, Ryan Babbush, Richard Kueng, John Preskill, et al. Quantum advantage in learning from experiments. _Science_ , 376(6598):1182â€“1186, 2022. 

- [110] Sitan Chen, Jordan Cotler, Hsin-Yuan Huang, and Jerry Li. Exponential separations between learning with and without quantum memory. In _2021 IEEE 62nd Annual Symposium on Foundations of Computer Science (FOCS)_ , pages 574â€“585. IEEE, 2022. 

- [111] Senrui Chen, Changhun Oh, Sisi Zhou, Hsin-Yuan Huang, and Liang Jiang. Tight bounds on pauli channel learning without entanglement. _Physical Review Letters_ , 132(18):180805, 2024. 

- [112] Changhun Oh, Senrui Chen, Yat Wong, Sisi Zhou, Hsin-Yuan Huang, Jens AH Nielsen, Zheng-Hao Liu, Jonas S Neergaard-Nielsen, Ulrik L Andersen, Liang Jiang, et al. Entanglement-enabled advantage for learning a bosonic random displacement channel. _Physical Review Letters_ , 133(23):230604, 2024. 

- [113] Zheng-Hao Liu, Romain Brunel, Emil EB Ã˜stergaard, Oscar Cordero, Senrui Chen, Yat Wong, Jens AH Nielsen, Axel B Bregnsbo, Sisi Zhou, Hsin-Yuan Huang, et al. Quantum learning advantage on a scalable photonic platform. _Science_ , 389(6767):1332â€“1335, 2025. 

- [114] Dorit Aharonov, Jordan Cotler, and Xiao-Liang Qi. Quantum algorithmic measurement. _Nature Communications_ , 13(1):887, 2022. 

- [115] Richard R Allen, Francisco Machado, Isaac L Chuang, Hsin-Yuan Huang, and Soonwon Choi. Quantum computing enhanced sensing. _arXiv preprint arXiv:2501.07625_ , 2025. 

- [116] Ian Goodfellow, Yoshua Bengio, and Aaron Courville. _Deep Learning_ . MIT Press, 2016. `http://www. deeplearningbook.org` . 

- [117] Haimeng Zhao, Laura Lewis, Ishaan Kannan, Yihui Quek, Hsin-Yuan Huang, and Matthias C Caro. Learning quantum states and unitaries of bounded gate complexity. _PRX Quantum_ , 5(4):040306, 2024. 

- [118] Aram W Harrow, Avinatan Hassidim, and Seth Lloyd. Quantum algorithm for linear systems of equations. _Physical Review Letters_ , 103(15):150502, 2009. 

- [119] Iordanis Kerenidis and Anupam Prakash. Quantum recommendation systems. In _8th Innovations in Theoretical Computer Science Conference (ITCS 2017)_ , pages 49â€“1. Schloss Dagstuhlâ€“Leibniz-Zentrum fÂ¨ur Informatik, 2017. 

- [120] Patrick Rebentrost, Masoud Mohseni, and Seth Lloyd. Quantum support vector machine for big data classification. _Physical Review Letters_ , 113(13):130503, 2014. 

- [121] Seth Lloyd, Masoud Mohseni, and Patrick Rebentrost. Quantum principal component analysis. _Nature Physics_ , 10(9):631â€“633, 2014. 

14 

- [122] Seth Lloyd and Christian Weedbrook. Quantum generative adversarial learning. _Physical Review Letters_ , 121(4):040502, 2018. 

- [123] Sarah K Leyton and Tobias J Osborne. A quantum algorithm to solve nonlinear differential equations. _arXiv preprint arXiv:0812.4423_ , 2008. 

- [124] Ashley Montanaro and Sam Pallister. Quantum algorithms and the finite element method. _Physical Review A_ , 93(3):032324, 2016. 

- [125] Shouvanik Chakrabarti, Andrew M Childs, Tongyang Li, and Xiaodi Wu. Quantum algorithms and lower bounds for convex optimization. _Quantum_ , 4:221, 2020. 

- [126] Joran van Apeldoorn, AndrÂ´as GilyÂ´en, Sander Gribling, and Ronald de Wolf. Convex optimization using quantum oracles. _Quantum_ , 4:220, 2020. 

- [127] Ashley Montanaro. Quantum speedup of monte carlo methods. _Proceedings of the Royal Society A: Mathematical, Physical and Engineering Sciences_ , 471(2181):20150301, 2015. 

- [128] Aram W Harrow. Small quantum computers and large classical data sets. _arXiv preprint arXiv:2004.00026_ , 2020. 

- [129] B David Clader, Bryan C Jacobs, and Chad R Sprouse. Preconditioned quantum linear system algorithm. _arXiv preprint arXiv:1301.2340_ , 2013. 

- [130] Srinivasan Arunachalam, Vlad Gheorghiu, Tomas Jochym-Oâ€™Connor, Michele Mosca, and Priyaa Varshinee Srinivasan. On the robustness of bucket brigade quantum ram. _New Journal of Physics_ , 17(12):123010, 2015. 

- [131] Ryan Babbush, Craig Gidney, Dominic W Berry, Nathan Wiebe, Jarrod McClean, Alexandru Paler, Austin Fowler, and Hartmut Neven. Encoding electronic spectra in quantum circuits with linear T complexity. _Physical Review X_ , 8(4):041015, 2018. 

- [132] Sisi Zhou, Mengzhen Zhang, John Preskill, and Liang Jiang. Achieving the heisenberg limit in quantum metrology using quantum error correction. _Nature Communications_ , 9(1):78, 2018. 

- [133] Hsin-Yuan Huang, Soonwon Choi, Jarrod R McClean, and John Preskill. The vast world of quantum advantage. _arXiv preprint arXiv:2508.05720_ , 2025. 

- [134] Lov K Grover. A fast quantum mechanical algorithm for database search. In _Proceedings of the twenty-eighth annual ACM symposium on theory of computing_ , pages 212â€“219, 1996. 

- [135] Sitan Chen, Jordan Cotler, Hsin-Yuan Huang, and Jerry Li. The complexity of NISQ. _Nature Communications_ , 14(1):6001, 2023. 

- [136] Oded Regev and Liron Schiff. Impossibility of a quantum speed-up with a faulty oracle. In _International Colloquium on Automata, Languages, and Programming_ , pages 773â€“781. Springer, 2008. 

- [137] Sergey Bravyi, David Gosset, and Robert KÂ¨onig. Quantum advantage with shallow circuits. _Science_ , 362(6412):308â€“ 311, 2018. 

- [138] Sergey Bravyi, David Gosset, Robert KÂ¨onig, and Marco Tomamichel. Quantum advantage with noisy shallow circuits. _Nature Physics_ , 16(10):1040â€“1045, 2020. 

- [139] Scott Aaronson, Harry Buhrman, and William Kretschmer. A qubit, a coin, and an advice string walk into a relational problem. In _15th Innovations in Theoretical Computer Science Conference (ITCS 2024)_ , pages 1â€“1. Schloss Dagstuhlâ€“Leibniz-Zentrum fÂ¨ur Informatik, 2024. 

- [140] Wm A Wulf and Sally A McKee. Hitting the memory wall: Implications of the obvious. _ACM SIGARCH computer architecture news_ , 23(1):20â€“24, 1995. 

- [141] Alexandra Sasha Luccioni, Sylvain Viguier, and Anne-Laure Ligozat. Estimating the carbon footprint of bloom, a 176b parameter language model. _Journal of machine learning research_ , 24(253):1â€“15, 2023. 

- [142] Samyam Rajbhandari, Jeff Rasley, Olatunji Ruwase, and Yuxiong He. Zero: Memory optimizations toward training trillion parameter models. In _SC20: International Conference for High Performance Computing, Networking, Storage and Analysis_ , pages 1â€“16. IEEE, 2020. 

- [143] Paras Jain, Ajay Jain, Aniruddha Nrusimha, Amir Gholami, Pieter Abbeel, Joseph Gonzalez, Kurt Keutzer, and Ion Stoica. Checkmate: Breaking the memory wall with optimal tensor rematerialization. _Proceedings of Machine Learning and Systems_ , 2:497â€“511, 2020. 

- [144] Tri Dao, Dan Fu, Stefano Ermon, Atri Rudra, and Christopher RÂ´e. FlashAttention: Fast and memory-efficient exact attention with IO-awareness. _Advances in neural information processing systems_ , 35:16344â€“16359, 2022. 

- [145] Tim Dettmers, Mike Lewis, Younes Belkada, and Luke Zettlemoyer. GPT3.int8(): 8-bit matrix multiplication for transformers at scale. _Advances in neural information processing systems_ , 35:30318â€“30332, 2022. 

- [146] Tim Dettmers, Artidoro Pagnoni, Ari Holtzman, and Luke Zettlemoyer. QLoRA: Efficient finetuning of quantized LLMs. _Advances in neural information processing systems_ , 36:10088â€“10115, 2023. 

- [147] Woosuk Kwon, Zhuohan Li, Siyuan Zhuang, Ying Sheng, Lianmin Zheng, Cody Hao Yu, Joseph Gonzalez, Hao Zhang, and Ion Stoica. Efficient memory management for large language model serving with pagedattention. In _Proceedings of the 29th symposium on operating systems principles_ , pages 611â€“626, 2023. 

- [148] Joshua Ainslie, James Lee-Thorp, Michiel de Jong, Yury Zemlyanskiy, Federico Lebron, and Sumit Sanghai. GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints. In _Proceedings of the 2023 Conference on Empirical Methods in Natural Language Processing_ , pages 4895â€“4901, 2023. 

- [149] Maziar S Hemati, Matthew O Williams, and Clarence W Rowley. Dynamic mode decomposition for large and streaming datasets. _Physics of Fluids_ , 26(11), 2014. 

- [150] Eric Perlman, Randal Burns, Yi Li, and Charles Meneveau. Data exploration of turbulence simulations using a database cluster. In _Proceedings of the 2007 ACM/IEEE Conference on Supercomputing_ , pages 1â€“11, 2007. 

- [151] Zhuo Feng and Peng Li. Multigrid on GPU: Tackling power grid analysis on parallel SIMT platforms. In _2008 IEEE/ACM International Conference on Computer-Aided Design_ , pages 647â€“654. IEEE, 2008. 

- [152] Joseph N Kozhaya, Sani R Nassif, and Farid N Najm. A multigrid-like technique for power grid analysis. _IEEE_ 

15 

_Transactions on Computer-Aided Design of Integrated Circuits and Systems_ , 21(10):1148â€“1160, 2002. 

- [153] James Kirkpatrick, Razvan Pascanu, Neil Rabinowitz, Joel Veness, Guillaume Desjardins, Andrei A Rusu, Kieran Milan, John Quan, Tiago Ramalho, Agnieszka Grabska-Barwinska, et al. Overcoming catastrophic forgetting in neural networks. _Proceedings of the national academy of sciences_ , 114(13):3521â€“3526, 2017. 

- [154] Ziv Bar-Yossef, Thathachar S Jayram, Ravi Kumar, and D Sivakumar. An information statistics approach to data stream and communication complexity. _Journal of Computer and System Sciences_ , 68(4):702â€“732, 2004. 

- [155] Nachum Dershowitz, Rotem Oshman, and Tal Roth. The communication complexity of multiparty set disjointness under product distributions. In _Proceedings of the 53rd Annual ACM SIGACT Symposium on Theory of Computing_ , pages 1194â€“1207, 2021. 

- [156] Shachar Lovett and Jiapeng Zhang. Streaming lower bounds and asymmetric set-disjointness. In _2023 IEEE 64th Annual Symposium on Foundations of Computer Science (FOCS)_ , pages 871â€“882. IEEE, 2023. 

- [157] Mark Braverman, Sumegha Garg, Qian Li, Shuo Wang, David P Woodruff, and Jiapeng Zhang. A new information complexity measure for multi-pass streaming with applications. In _Proceedings of the 56th Annual ACM Symposium on Theory of Computing_ , pages 1781â€“1792, 2024. 

- [158] Ran Raz. Fast learning requires good memory: A time-space lower bound for parity learning. _Journal of the ACM (JACM)_ , 66(1):1â€“18, 2018. 

- [159] Ran Raz. A time-space lower bound for a large class of learning problems. In _2017 IEEE 58th Annual Symposium on Foundations of Computer Science (FOCS)_ , pages 732â€“742. IEEE, 2017. 

- [160] Sumegha Garg, Pravesh K Kothari, Pengda Liu, and Ran Raz. Memory-sample lower bounds for learning parity with noise. _arXiv preprint arXiv:2107.02320_ , 2021. 

- [161] Itai Dinur. Time-space lower bounds for bounded-error computation in the random-query model. In _Proceedings of the 2024 Annual ACM-SIAM Symposium on Discrete Algorithms (SODA)_ , pages 2900â€“2915. SIAM, 2024. 

- [162] Wei Zhan. _Randomness and quantumness in space-bounded computation_ . PhD thesis, Princeton University, 2023. 

- [163] Qipeng Liu, Ran Raz, and Wei Zhan. Memory-sample lower bounds for learning with classical-quantum hybrid memory. In _Proceedings of the 55th Annual ACM Symposium on Theory of Computing_ , pages 1097â€“1110, 2023. 

- [164] Alexei Yu Kitaev, Alexander Shen, and Mikhail N Vyalyi. _Classical and quantum computation_ , volume 47. American Mathematical Soc., 2002. 

- [165] Masaki Nakanishi, Kiyoharu Hamaguchi, and Toshinobu Kashiwabara. Ordered quantum branching programs are more powerful than ordered probabilistic branching programs under a bounded-width restriction. In _International Computing and Combinatorics Conference_ , pages 467â€“476. Springer, 2000. 

- [166] Farid Ablayev, Aida Gainutdinova, and Marek Karpinski. On computational power of quantum branching programs. In _International Symposium on Fundamentals of Computation Theory_ , pages 59â€“70. Springer, 2001. 

- [167] Debajyoti Bera and Tharrmashastha Sapv. A generalized quantum branching program. _arXiv preprint arXiv:2307.11395_ , 2023. 

- [168] Ran Raz. Exponential separation of quantum and classical communication complexity. In _Proceedings of the thirty-first annual ACM symposium on theory of computing_ , pages 358â€“367, 1999. 

- [169] Dmitry Gavinsky, Julia Kempe, Iordanis Kerenidis, Ran Raz, and Ronald de Wolf. Exponential separations for one-way quantum communication complexity, with applications to cryptography. In _Proceedings of the thirty-ninth annual ACM symposium on theory of computing_ , pages 516â€“525, 2007. 

- [170] Matthew B Hastings. Turning gate synthesis errors into incoherent errors. _Quantum Information & Computation_ , 17(5-6):488â€“494, 2017. 

- [171] John Watrous. _The theory of quantum information_ . Cambridge University Press, 2018. 

- [172] Armando Angrisani, Mina Doosti, and Elham Kashefi. A unifying framework for differentially private quantum algorithms. _arXiv preprint arXiv:2307.04733_ , 2023. 

- [173] ClÂ´ement L Canonne. A short note on an inequality between kl and tv. _arXiv preprint arXiv:2202.07198_ , 2022. 

- [174] Ilias Diakonikolas, Daniel M Kane, and Jelani Nelson. Bounded independence fools degree-2 threshold functions. _arXiv preprint arXiv:0911.3389_ , 2009. 

- [175] Roman Vershynin. _High-dimensional probability: An introduction with applications in data science_ , volume 47. Cambridge University Press, 2018. 

- [176] Kouhei Nakaji, Mohsen Bagherimehrab, and AlÂ´an Aspuru-Guzik. High-order randomized compiler for hamiltonian simulation. _PRX Quantum_ , 5(2):020330, 2024. 

- [177] Rolando D Somma, Guang Hao Low, Dominic W Berry, and Ryan Babbush. Quantum algorithm for linear matrix equations. _arXiv preprint arXiv:2508.02822_ , 2025. 

- [178] Troy Lee, Adi Shraibman, and Robert Spalek.[Ë‡] A direct product theorem for discrepancy. In _2008 23rd Annual IEEE Conference on Computational Complexity_ , pages 71â€“80. IEEE, 2008. 

- [179] Ethan Bernstein and Umesh Vazirani. Quantum complexity theory. In _Proceedings of the twenty-fifth annual ACM symposium on theory of computing_ , pages 11â€“20, 1993. 

- [180] Dorit Aharonov. A simple proof that Toffoli and Hadamard are quantum universal. _arXiv preprint quantph/0301040_ , 2003. 

- [181] Mauro ES Morales, LirandÂ¨e Pira, Philipp Schleich, Kelvin Koor, Pedro Costa, Dong An, AlÂ´an Aspuru-Guzik, Lin Lin, Patrick Rebentrost, and Dominic W Berry. Quantum linear system solvers: A survey of algorithms and applications. _arXiv preprint arXiv:2411.02522_ , 2024. 

- [182] Gilles Brassard, Peter Hoyer, Michele Mosca, and Alain Tapp. Quantum amplitude amplification and estimation. _arXiv preprint quant-ph/0005055_ , 2000. 

- [183] Iain M Johnstone. On the distribution of the largest eigenvalue in principal components analysis. _The Annals of Statistics_ , 29(2):295â€“327, 2001. 

16 

## **Appendices** 

## **Contents & Roadmap** 

|**A. **|**Additional numerical experiments**|18|
|---|---|---|
|**B. **|**Overview and related works**|20|
||1. Machine learning and quantum algorithms|20|
||2. The challenging quest for quantum advantage|21|
||3. Memory-efcient algorithms and quantum space advantage|23|
|**C. **|**Models of data access and computation**|25|
||1. Data generation processes|25|
||2. Classical learning algorithms|27|
||3. Quantum learning algorithms|28|
||4. Properties of hierarchical data generation processes|28|
|**D. **|**Quantum oracle sketching**|34|
||1. Preliminaries|34|
||a. Inequalities|34|
||b. Quantum singular value transform|37|
||2. Quantum oracle sketching for IID data|38|
||a. The apparent trap of decoherence|38|
||b. Evading decoherence|40|
||3. Optimality|44|
||4. Extensions|46|
||a. Multi-bit output|46|
||b. Quantum oracle sketching for correlated data|48|
||c. Unknown marginal distribution|52|
||5. Linear algebra primitives|54|
||a. Linear algebra data|54|
||b. Sparse oracles|55|
||c. Block encodings|63|
||d. Quantum state sketching|64|
|**E. **|**Classical hardness**|75|
||1. Noisy oracle property estimation|76|
||2. Recap of classical learning algorithms|77|
||3. Sample-space lower bound|77|
||a. Preliminaries|78|
||b. Simulation|86|
||c. Simulation is correct|86|
||d. Simulation does not query too much|90|
||e. Proof of Theorem E.2|91|
||4. Bootstrap with one more time scale|92|
||a. Distributional sample-space lower bound|93|
||b. Learning XOR Lemma|94|
||c. Derandomization|95|
||d. Derandomized learning XOR lemma|95|
||e. Proof of Theorem E.30|99|
||f. Low advantage leads to large sample complexity|99|
||g. Proof of Theorems E.27 and E.28|101|
||5. Connect to applications|101|
||a. Forrelation and inner product|102|
||b. Quantum circuit for dynamic NOPE|105|
||c. Connect to linear systems|107|
||d. Connect to binary classifcation|109|
||e. Connect to dimension reduction|111|
|**F. **|**Applications**|114|



17 

|1.|Linear system|114|
|---|---|---|
||a. Problem formulation|115|
||b. Main results|116|
||c. Quantum algorithm|117|
||d. Classical hardness|119|
|2.|Binary classifcation|123|
||a. Problem formulation|124|
||b. Main results|125|
||c. Quantum algorithm|126|
||d. Classical hardness|130|
|3.|Dimension reduction|134|
||a. Problem formulation|135|
||b. Main results|136|
||c. Quantum algorithm|137|
||d. Classical hardness|140|



## **Roadmap** 

We begin with a roadmap that helps the readers navigate through the appendices. For convenience, clicking the page number in the header of any page will return the reader to this roadmap. In Section A, we provide additional numerical experiments and the details. The remainder of the appendices are organized into the following three themes. 

**Background and setup.** We start with an overview and discussion of related works and our contributions in Section B. Then we set the stage by introducing our models of data access and computation in Section C. 

**Theoretical foundations.** Sections D and E are devoted to establishing the rigorous theoretical foundations of processing massive classical data on small quantum computers. This includes two parts. 

1. _Quantum algorithms (Section D)._ In Section D 2, we begin by introducing the most intuitive and simplest version of quantum oracle sketching for IID data of Boolean functions. In particular, we address the apparent trap of decoherence and how we circumvent it. Then we establish its optimality, and extend it to handle more general data distributions and data structures such as matrices and vectors. 

2. _Classical hardness (Section E)._ We develop the machinery for proving classical hardness by introducing the Noisy Oracle Property Estimation (NOPE) task and its dynamic variant. Then we prove their classical hardness and connect them to the various applications. 

**Applications.** In Section F, we apply our theoretical tools to the real-world applications including linear systems (Figure 8), binary classification (Figure 9), and dimension reduction (Figure 10). Each application starts with a self-contained introduction of the problem and the statements of our main quantum advantage results. They are written without any quantum jargon and are intended for a general audience. Detailed proofs follow, utilizing the tools we develop in the theoretical foundations. 

**Suggested reading routes.** Our figures are designed to provide intuitive understanding without going into the details. We suggest starting with Figures 8 to 10 for the applications and quantum advantage results, then Figure 5 for the formal setup. Figure 6 provides an overview of quantum oracle sketching and Figure 7 illustrates the intuition behind the classical hardness proofs. 

For more details, we suggest the following routes depending on the readerâ€™s interest: 

1. _For general readers:_ Start with the applications in Section F, which are further supported by numerical experiments in Figures 2 and 4. Section B provides more context on the various challenges in reaching quantum advantages in useful classical tasks and a semi-technical overview of how we tackle them. 

2. _For algorithm designers:_ Proceed to the quantum algorithms in Section D and in particular Section D 5 for applications related to linear algebra. The quantum algorithm parts of Section F are also good templates for applying the algorithms to potential applications. On GitHub, we provide JAX [102] implementation of quantum oracle sketching and QSVT that supports GPU/TPU and automatic differentiation for variational training, with details explained in Section A. 

3. _For readers interested in the rigorous proofs:_ The formal setup is detailed in Section C and the sample complexity and variance analysis techniques for noisy and correlated linear algebra data are developed in Sections D 4 and D 5. Theoretical computer scientists may be further interested in our technical contributions in the classical lower bound proofs (Section E), including the sample-space lower bounds via simulation, learning XOR lemma with derandomization, and the BQP-hardness of useful applications. 

18 

## **(a) Social media topic analysis (b) Pharmaceutical drug discovery** 

**==> picture [484 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
HO O<br>O CH3<br>O NH<br>NH<br>Good offer at our local dealership. N S H3C<br>O<br>O<br>H3C CH3<br>Any opinions on this new medication? OH<br>NH Active Inactive H3C<br>HN NH2<br>**----- End of picture text -----**<br>


FIG. 4: **Additional numerical experiments demonstrating exponential quantum advantage in real-world datasets.** We perform binary classification and dimension reduction for **(a)** topic analysis of posts from 20 newsgroups [103] and **(b)** chemical compound data for Thrombin binding [104]. We compare quantum oracle sketching (orange) with classical sparse-matrix algorithms (gray), quantum algorithms using QRAM (gray), and classical streaming algorithms (blue). For each algorithm, we truncate the dimension to filter out a varying number of rare features to plot the trade-off between machine size and performance, with standard error indicated by the shaded region. Machine size is defined as the total count of fundamental memory units required: logical qubits for quantum and floating-point numbers for classical. Performance is quantified by the 5-fold cross validation accuracy averaged over random category pairs and explained variance relative to the untruncated baseline. 

**Notations.** Throughout this work, we use the standard notations of asymptotics. For two positive functions _f_ ( _N_ ) and _g_ ( _N_ ), _f_ ( _N_ ) = _O_ ( _g_ ( _N_ )) if there exist _N_ 0 _, C >_ 0 such that _âˆ€N > N_ 0 _, f_ ( _N_ ) _â‰¤ Cg_ ( _N_ ). _f_ ( _N_ ) = â„¦( _g_ ( _N_ )) if _g_ ( _N_ ) = _O_ ( _f_ ( _N_ )). _f_ ( _N_ ) = Î˜( _g_ ( _N_ )) if _f_ ( _N_ ) = _O_ ( _g_ ( _N_ )) and _f_ ( _N_ ) = â„¦( _g_ ( _N_ )). _f_ ( _N_ ) = _o_ ( _g_ ( _N_ )) if lim _N â†’âˆž f_ ( _N_ ) _/g_ ( _N_ ) = 0. _f_ ( _N_ ) = _Ï‰_ ( _g_ ( _N_ )) if _g_ ( _N_ ) = _o_ ( _f_ ( _N_ )). We add a tilde (e.g., _O_[Ëœ] ( _f_ ( _N_ ))) to omit factors that scale polynomially with log _f_ ( _N_ ). We also use poly( _N_ ) = _N[O]_[(1)] to denote functions of _N_ that scale polynomially with _N_ and use polylog( _N_ ) to denote poly(log( _N_ )). Similarly, superpoly(N) means _N[Ï‰]_[(1)] . 

## **Appendix A: Additional numerical experiments** 

In this section, we provide more details of the numerical experiments presented in the main text, along with additional numerical experiments. We begin with the demonstration of exponential quantum space advantage in real-world datasets (Figures 2 and 4). Then we move on to the benchmarking of quantum oracle sketching (Figure 3). 

To validate the practical relevance of our exponential quantum space advantages, we conduct numerical experiments in four real-world datasets across diverse application domains: sentiment analysis of movie reviews (Figure 2(a)), single-cell RNA sequences analysis (Figure 2(b)), social media topic analysis (Figure 4(a)), and pharmaceutical drug discovery (Figure 4(b)). The specific datasets we consider are the standard benchmark datasets in the respective domains. For movie review sentiment analysis, we use the movie review dataset from the Internet Movie Database (IMDb) [79] available at this website. For single-cell RNA sequencing, we use the single-cell RNA sequences of 68k peripheral blood mononuclear cells (PBMC) [80] commonly known as the PBMC68k or Zheng68k dataset available through the scVelo package [105]. For social media topic analysis, we use the posts from 20 newsgroups known as the 20Newsgroup dataset [103] available through the scikit-learn package [106]. For pharmaceutical drug discovery, we use the chemical compound dataset Dorothea [107] with labels indicating binding ability to Thrombin available at the UCI Machine Learning Repository. For raw text data in IMDb and 20Newsgroup, we construct the features by the standard TF-IDF method with English stop words as default in scikit-learn. The other two datasets are used as provided. 

To mimic the realistic scenarios where we do not have enough memory to store the whole dataset, we truncate the feature dimension by abandoning rare features that do not appear in many samples. This threshold is 

19 

controlled by the minimal document frequency, which is the minimal number of samples a feature must be presented in for it to be kept. By varying the minimal document frequency, we truncate the dimension and plot the trade-off between memory consumption and performance. We leave the studies of dataset-specific heuristics to future works, as they require extensive empirical evaluation. 

We consider two tasks: binary classification and dimension reduction. The performance of binary classification is quantified by the 5-fold cross validation accuracy of the least-squares support vector machine (LS-SVM) with _â„“_ 2 regularization. To avoid overfitting, we use the _â„“_ 2 regularization strength _Î»_ = 10 _,_ 200 _,_ 1 _,_ 200 for IMDb, PBMC68k, 20Newsgroup, and Dorothea respectively. If the dataset contains more than two categories, we average the accuracy over random pairs of categories. In particular, 100 pairs are randomly sampled for both 20Newsgroup and PBMC68k. 

For dimension reduction, we perform principal component analysis (PCA) on each dataset with all categories combined. The performance is measured by how well the first principal component after truncation explains the data variance as compared to the untruncated one. Concretely, we quantify it by the explained variance of the first principal component of the truncated dataset divided by the explained variance of the first principal component of the full dataset. This is calculated by first calculate the first principal component _âƒ—w[â€²] âˆˆ_ R _[D][â€²]_ of the truncated dataset _X[â€²] âˆˆ_ R _[N][Ã—][D][â€²]_ and the first principal component _âƒ—w âˆˆ_ R _[D]_ of the full dataset _X âˆˆ_ R _[N][Ã—][D]_ . Then we lift _âƒ—w[â€²]_ back to the original space as the vector _âƒ—w[â€²â€²] âˆˆ_ R _[D]_ by padding zeroes in the truncated feature dimensions. The relative explained variance is _âƒ—w[â€²â€²][T] X[T] X âƒ—w[â€²â€²]_ divided by _âƒ—w[T] X[T] X âƒ—w_ . 

We calculate the memory consumption or machine size of the four algorithms as follows. We define memory consumption as the total count of fundamental units required to be maintained throughout the algorithm: logical qubits for quantum processors and floating-point numbers for classical machines. In particular, same as the standard definition of memory consumption in streaming [53], the size of each individual data sample is not counted because they are processed and discarded on the fly. For classical sparse-matrix algorithms and QRAM-based quantum algorithms, we use the conservative lower bound 

**==> picture [296 x 11] intentionally omitted <==**

where _N_ nnz is the number of non-zero elements in the datasets. This is because no matter how these algorithms carry out the tasks, they always store the whole sparse matrix in their memory. For classical streaming algorithms, we use the conservative lower bound 

**==> picture [278 x 12] intentionally omitted <==**

where _D_ is the feature dimension of the datasets. This is because no matter how these algorithms carry out the tasks, they always store the whole solution vector _âƒ—w âˆˆ_ R _[D]_ (i.e. the weight vector of LS-SVM or the principal component in PCA) in their memory [60, 61]. 

For quantum oracle sketching, we have memory consumption 

**==> picture [360 x 15] intentionally omitted <==**

for LS-SVM prediction of a single test sample, where _N Ã— D_ is the dimension of the data matrix _X_ and _s_ is the sparsity (i.e., the maximal number of non-zero elements in each row or column). This is because we use quantum oracle sketching to build the following components. 

**==> picture [471 x 25] intentionally omitted <==**

   - Hermitian embedding has dimension ( _N_ +2 _D_ ) _Ã—_ ( _N_ +2 _D_ ). This requires building the sparse index/element oracle for the augmented matrix, which has sparsity _s_ + 1. Hence, building its sparse index oracle requires 2 _âŒˆ_ log2( _N_ + 2 _D_ ) _âŒ‰_ + _âŒˆ_ log2( _s_ + 1) _âŒ‰_ + 2 qubits, where the additional 2 qubits are for QSVT and holding the binary search output as in Theorem D.21. Building the sparse element oracle can reuse the same qubits, so no extra qubits are needed. 

2. The state preparation unitary of the label vector _âƒ—y âˆˆ_ R _[N]_ , which requires _âŒˆ_ log2( _N_ ) _âŒ‰_ + 2 qubits, where the additional 2 qubits are for the first LCU & QSVT and the second LCU as in Theorem D.24. These qubits are contained in the previous count since they can be reused. 

Then we perform quantum ridge regression with amplitude amplification using QSVT-based quantum linear system solver, which requires 1 ancilla qubit for the QSVT, contained in the previous count because we can reuse the ancilla qubit from quantum oracle sketching. Finally, we need to perform interferometric measurement to calculate the signed overlap with test state, which requires 1 extra ancilla qubit as in Theorem F.16. The final estimate of the label is stored classically on a running average, so only 1 extra classical floating-point number is needed. This proves the formula for _S_ QOS[LS] _[âˆ’]_[SVM] . Similarly, the same calculation shows that the memory consumption for PCA and dimension reduction of a single test sample is 

_S_ QOS[PCA][= 2] _[ âŒˆ]_[log] 2[(] _[N]_[+] _[ D]_[)] _[âŒ‰]_[+] _[ âŒˆ]_[log] 2[(] _[s]_[)] _[âŒ‰]_[+ 3 + 1] _[,]_ (A4) 

20 

because there is no augmentation for regularization. 

To benchmark the performance of quantum oracle sketching, we implement the code numerically simulating it in JAX [102], which supports GPU/TPU execution and other features including automatic differentiation and vectorization. We provide the code at GitHub. We implement two versions of quantum oracle sketching: one using randomly sampled data, and one using the expected unitary. The QSVT subroutines used in quantum oracle sketching are implemented in a memory-efficient way that takes advantage of the diagonal and direct-sum structures in quantum oracle sketching. The QSVT rotation angles are generated via the pyqsp package [10] and converted to circuit phases via the map in [108]. 

The implementation using randomly sampled data calculates random instances of the implemented unitary _V_ . That means when we calculate the trace distance of the output state, the sample complexity shows a 1 _/Ïµ_[2] scaling as predicted in Theorem D.11 rather than the 1 _/Ïµ_ scaling in a quantum experimental implementation. The 1 _/Ïµ_ scaling is only recovered when we calculate the error in terms of physically measurable quantities like observable expectation values or infidelity. This feature makes the simulation extremely hard using this implementation with randomly sampled data, as it requires quadratically more samples that quickly blows up the memory for classical simulation. 

To ease numerical simulation, we mainly focus on the second implementation using the expected unitary E[ _V_ ]. Theorem D.2 guarantees that the error in diamond distance of the physical implementation is always upper bounded by the error in operator norm of the expected unitary. Hence, the reported error in Figure 3 is a conservative upper bound on the actual implementation error using the corresponding number of samples. 

We benchmark quantum oracle sketching for four kinds of oracles: Boolean functions, vectors, matrix element, and matrix index. For Boolean function, we uniformly sample 100 random truth tables of Boolean functions for each of 12 dimensions ranging from 10[2] to 10[3] and each of 10 sample sizes from 10[5] to 10[8] . We use quantum oracle sketching to assemble their phase oracles and calculate the corresponding errors in operator norm. 

For vectors, we uniformly sample 10 unit vectors for each of 12 dimensions ranging from 10[2] to 10[3] and each of 10 sample sizes from 10[5] to 10[8] . We use quantum oracle sketching to assemble their state preparation unitary without amplitude amplification and calculate the corresponding errors in Euclidean norm. The norm of the resulting un-normalized quantum states are selected to be 1 _/_ (5 arcsin(1)) _â‰ˆ_ 0 _._ 127 to ease the implementation of the arcsin function via QSVT used in quantum state sketching. 

For sparse matrix element oracles, we fix the dimension of the matrices to be 100 _Ã—_ 100. Then we randomly sample _N_ nnz coordinates and fill them with numbers sampled uniformly from [ _âˆ’_ 1 _,_ 1]. We sample 200 such random sparse matrices for each of 10 values of _N_ nnz ranging from 250 to 2000 and each of 10 sample sizes from 10[5] to 10[8] . We use quantum oracle sketching to assemble the sparse matrix element oracles and calculate the corresponding errors in operator norm. 

For matrix sparse element oracles, we consider the scenario where we have access to the whole vectors of randomly sampled rows, as in binary classification or dimension reduction. The goal is to implement the sparse row index oracle. We fix row sparsity of the matrices to be 8 and randomly sample 8 columns for each row. We fill these selected entries by values uniformly sampled from [ _âˆ’_ 1 _,_ 1]. We sample 5 such random matrices for each of 6 dimensions from 50 _Ã—_ 50 to 500 _Ã—_ 500 and each of 10 sample sizes from 10[5] to 10[8] . We use quantum oracle sketching to assemble the sparse row index oracle and calculate the errors in operator norm. 

The results in Figure 3 show that all the sample complexity scaling observed in numerical simulation agrees accurately with the theoretical prediction. To extract the constants and exponents, we take logarithm of the sample sizes, dimensions, and errors, and perform a least-squares fit. The residual error of the least-squares fit translates into the root-mean-squared relative errors, which are all below 3%. 

## **Appendix B: Overview and related works** 

In this section, we discuss the relation between our work and the existing literature and provide an overview of our results. We begin by providing background on the development of quantum algorithms for data processing tasks. Then we explain the various challenges identified in the literature in reaching quantum advantages in useful classical tasks and how we tackle them. Finally, we discuss classical space-efficient algorithms, techniques for proving space lower bounds, and how our results improve existing quantum space advantages in streaming. 

## **1. Machine learning and quantum algorithms** 

**Quantum machine learning.** Machine learning is one of the most important frontiers of modern computation, owing to the ubiquitous role of data processing and our ever-growing need for it throughout society. Hence, it is natural to expect quantum computation, as a fundamentally new paradigm of computation, to revolutionize machine learning by providing new forms of data and new approaches to data processing [11]. Indeed, in the 

21 

realm of scientific discoveries aiming to probe inherently quantum properties of Nature, people have rigorously established exponential advantages of using quantum machines to process quantum data [109â€“115]. These advantages of using quantum machines for quantum tasks are promising in facilitating science and engineering in the quantum frontier. Yet they appear too specialized to have major impacts on our everyday life, where classical data abound and directly observable quantum effects are negligible. 

In the realm of classical data processing where most real-world applications sit, whether quantum machines can deliver large advantages over classical machines is much less evident. Existing attempts to rigorously prove quantum advantages in classical data processing rely on designing contrived classical tasks by secretly embedding problems that are inherently either quantum (e.g., entanglement, contextuality, or random circuit sampling) or cryptographic (e.g., factoring) [20â€“28]. The limitation of this approach is that the proposed quantum algorithms are often designed for the specific contrived tasks to prove advantages and it is not clear how they apply to realistic problems. 

An alternative route is to empirically test the performance of heuristic quantum machine learning methods directly on realistic data, inspired by the empirical success of deep learning [116]. This approach is often referred to as variational quantum algorithms, parameterized quantum circuits, or quantum neural networks (see e.g., [34â€“36]). However, extensive studies have revealed the intrinsic hardness in training such variational quantum algorithms, manifested in the forms of exponentially vanishing gradient [37â€“40] and exponentially many bad local minima [41]. Furthermore, even if we can train them, their functional expressivity suffers from the same curse of dimensionality issue as classical neural network [117]. In fact, these discouraging results have sparked active debate on whether practical quantum advantage is even possible in classical machine learning tasks and whether trainable quantum neural networks are always classically simulatable [17â€“19]. 

Our work directly tackles the central problem of _broadly applicable and provable_ quantum advantage for classical data processing, by rigorously establishing exponential quantum advantages in a wide range of realistic classical machine learning tasks and demonstrating them on real-world datasets. A promising future direction is to further enhance it with heuristic variational methods. 

**Quantum algorithms for classical tasks.** In the quest for quantum advantages in widely-useful classical tasks, numerous quantum algorithms with rigorous performance analysis have been extensively studied. Some prominent examples include quantum algorithms for linear systems [118], recommendation systems [119], support vector machines [120], principal component analysis [121], generative adversarial learning [122], ordinary and partial differential equations [123, 124], convex optimization [125, 126], Monte Carlo sampling [127, 128], etc. Many of these algorithms can be understood in the unified framework of quantum linear algebra and quantum singular value transform (QSVT) [9, 10]. See [8] for a recent survey. The performance of these quantum algorithms are usually analyzed not in an end-to-end fashion, but in terms of the number of queries they make to specific oracles that provide coherent access to the classical data. Such oracles include quantum random access memory (QRAM), block encodings and sparse oracles of matrices, state preparation unitaries of vectors, etc. When we take into account the cost of building such oracles, whether large quantum advantage remains becomes unclear except for a few highly specialized and structured problems [129]. 

## **2. The challenging quest for quantum advantage** 

**Data loading and QRAM.** Most existing quantum algorithms for classical data processing rely on quantum random access memory (QRAM) [13], which is a primitive that models quantum coherent access to classical data. The quantum advantages of these algorithms survive only when QRAM can be efficiently realized [12]. However, how to build an efficient and fault-tolerant QRAM remains largely unclear [16]. To load _N_ classical bits into a quantum machine, it is unavoidable to use â„¦( _N_ ) gates since each gate only has a constant number of degrees of freedom. The idea of a QRAM is to parallelize these gates to reduce the circuit depth (and ideally the wall-clock time) to poly(log _N_ ) by using _O_ ( _N_ ) ancilla qubits. This makes QRAM extremely memory inefficient, even worse than classical machines. It is also unclear how to make QRAM fault tolerant with efficient control [14, 130], as _O_ ( _N_ ) classical co-processors and classical computation might be needed to perform error correction on these _O_ ( _N_ ) ancilla qubits [15]. These many classical co-processors might as well be repurposed to perform classical parallel computation and solve the target classical tasks themselves classically [16]. An alternative route, called circuit QRAM or QROM, circumvents this issue by working in the standard fault-tolerant circuit model and apply _O_ ( _N_ ) gates with few or no ancilla qubits [131]. This makes it fault-tolerant at the expense of killing large time advantages. Moreover, it is still space inefficient since the _O_ ( _N_ ) bits specifying these gates have to be stored somewhere classically, and therefore the total space (classical and quantum) is still _O_ ( _N_ ), despite that the qubit count may be only poly(log _N_ ). As a result, existing quantum algorithms that rely on QRAM have total space _O_ ( _N_ ) in general. 

In contrast, our quantum oracle sketching algorithm circumvents QRAM and achieves its goal of loading classical data into a quantum machine in a space-efficient and fault-tolerant way. Our results can be viewed as 

22 

a canonical data loading scheme that only consumes poly(log _N_ ) space in total, improving exponentially over QRAM. Moreover, in the space-efficient regime, the _O_[Ëœ] ( _N_ ) gate complexity is optimal up to logarithmic factors due to the counting argument above. 

**Dequantization and noisy query.** Even if we abstract away the implementation of QRAM, the mere assumption that we have efficient (i.e., poly(log _N_ ) time) coherent access to classical data might be too strong. An equivalent classical data access model, called sample and query access, have been shown to allow classical algorithms with only polynomial slowdown compared to the quantum algorithms. Such classical algorithms can be systematically designed through the program of dequantization [29â€“31]. The existence of these quantuminspired classical algorithms reduces many exponential quantum advantages to polynomial ones, making them less practically relevant. 

Another source of quantum advantage diminishment is noise. Despite that we can perform error correction to suppress the noise in our computing machines, we may not have full control over the entity providing the data. As examples, one may think of typographical errors in a piece of text, the ubiquitous 1 _/f_ noise in electronics, or fluctuations in a magnetic field that we are trying to sense. It has been shown that such noisy data may lead to the decrease or complete loss of quantum advantages. For example, Heisenberg-limit quantum sensing is reduced to the standard quantum limit when noise exists parallel to the signal [132, 133]. The computational speedup of Groverâ€™s algorithm for unstructured search [134] is also lost in certain noise models [135, 136]. 

Our results show that even with noisy data, exponential quantum space advantages persist in useful classical tasks. Moreover, we show that any super-quadratic query separation leads to exponential space advantage. This means that many dequantized quantum algorithms, although they might only have polynomial query speedup, they may still have exponential space advantage and hence worth revisiting. 

**Readout.** Another bottleneck of solving classical tasks with quantum algorithms is the readout of classical results from the quantum states [12]. Holevoâ€™s bound asserts that one can extract at most poly(log _N_ ) classical bits from poly(log _N_ ) qubits [63]. That means, for example, one can never hope to write out the whole solution vector _âƒ—x âˆˆ_ R _[N]_ of an _N_ -dimensional linear system using a poly(log _N_ )-qubit quantum machine without repeating â„¦([Ëœ] _N_ ) times. Hence, it has been widely believed that quantum algorithms can only be used to extract certain quantum-friendly properties of the solution (e.g, a quadratic form specified by an efficiently measurable observable). 

However, the takeaway drastically changes when we aim for quantum advantages in memory efficiency. In fact, a memory-efficient classical machine with poly(log _N_ ) bits suffers from the same â€œreadout issueâ€: one can only extract poly(log _N_ ) bits from it. Moreover, any property that one can efficiently extract from a poly(log _N_ )-bit classical machine can be efficiently extracted from a poly(log _N_ )-qubit quantum machine as well, meaning that the target properties of the solution need not be quantum-friendly anymore. In that sense, the readout issue is no longer a caveat of quantum algorithms when we aim for memory efficiency. 

For our purposes, we need to efficiently extract the properties we want without destroying sign information, which is critical in applications such as classification and dimension reduction. To this end, we develop a technique termed _interferometric classical shadow_ in Theorem F.16, where we combine the idea of the Hadamard test with the efficient offline prediction capability of classical shadows. It allows us to construct a completely classical model capable of predicting any number of sparse test data. Remarkably, this demonstrates that quantum technology enables us to construct accurate and exponentially smaller classical models out of classical data, which is provably impossible with any classical machine without exponentially larger memory. This highly condensed classical model is only efficiently obtainable through quantum technology. 

**Utility of quantum computation and provable quantum advantages.** Building quantum computers that are useful in real-world applications is one of the central goals of quantum computation. Yet despite decades of extensive effort, conclusive evidence of useful quantum advantages has only been established in a few specialized fields such as cryptanalysis and quantum simulation [3]. This is largely because known computational advantages stem from highly specialized structures in the problems (e.g., Abelian hidden subgroup structures exploited by Shorâ€™s algorithm [2, 5] and the quantum nature of quantum simulation [1, 6]). 

Computational advantages are especially hard to rigorously prove due to the notorious hardness of proving separations between computational complexity classes. In fact, an unconditionally proved exponential quantum computational advantage directly implies BPP _Ì¸_ = BQP and hence P _Ì¸_ = PSPACE, a major open conjecture in theoretical computer science. As a result, existing useful quantum advantage claims are either proved assuming computational complexity conjectures that are widely-believed but unproven, or proved relative to the use of oracles that suffers from the data loading issue (i.e., how to instantiate the oracles), with a few relatively weaker exceptions designed based on quantum nonlocality [137, 138]. 

Our work unconditionally proves exponential quantum space advantages in useful classical tasks, rigorously establishing memory savings as a widely-applicable utility of quantum computation. From a fundamental perspective, these advantages persist even in the unlikely event that quantum computers turn out to be polynomially 

23 

equivalent to classical computers in time (i.e., BPP = BQP). Our proof is information-theoretic and only relies on the exponential vastness of the Hilbert space enabled by quantum superposition. It reveals that this quantum advantage of exponential vastness, sometimes called quantum information supremacy [139], is a generic feature of super-quadratic query separation, rather than specialized structures embedded in contrived tasks. An experimental confirmation of our results may serve as a witness of the exponential dimension of the quantum state space [73, 133], similar to how Bell inequalities witness quantum nonlocality [76]. 

## **3. Memory-efficient algorithms and quantum space advantage** 

**Hitting the memory wall.** Our burgeoning need to process massive classical data has exposed memory capacity as a bottleneck more critical than computational speed, primarily due to its significantly slower advancement. This observation, colloquially put as â€œhitting the memory wallâ€ [140], has become increasingly relevant as large language models prosper; these models, now scaling to trillions of parameters [43], have grown 410-fold every two years, whereas memory capacity has only doubled over the same period [44]. Increasing amounts of energy are being consumed for hosting these gigantic models and maintaining massive data centers [45, 141]. Extensive studies have been devoted to optimizing memory consumption to enable longer context window and better inference performance, even at the expense of increased computation time [142â€“148]. While better models require larger training data [42], our storage capability limits the amount of data accessible, placing data such as internet traffic or global market activities beyond reach. This memory wall also appears in many other areas of science and technology, such as large particle colliders [49â€“51], astronomical sky surveys [52], single-cell RNA sequencing [46â€“48], the simulation of fluid dynamics [149, 150] and power grids [151, 152]. 

**Classical memory-efficient algorithms.** To cope with massive classical data, algorithmic techniques such as sketching [58â€“61], streaming [53â€“57], and online learning [62] have been developed. These techniques usually save memory by incrementally updating a model with fresh data samples without ever storing them. Various simple statistical properties, such as frequency moments [54], distinct elements [55], and heavy hitters [56, 57], can be estimated with high probability using exponentially smaller memory. See [53] for a survey. This framework has been extended to numerical linear algebra via random projection techniques based on JohnsonLindenstrauss transforms [59]. These classical sketching or streaming algorithms approximately solves matrix multiplication, linear regression, and low-rank approximation using space significantly smaller than standard classical algorithms. See [58] for a recent review. More recent studies have proposed streaming algorithms for SVM [60], PCA [61], etc. Similarly, online machine learning algorithms also provide memory efficiency, albeit with the main goal of minimizing regret [62]. However, these algorithms often suffer from compromised accuracy or fail to capture hidden correlations in practice [48, 149, 153]. Their space complexity all scales at least as order _D_ for a data matrix _X âˆˆ_ R _[N][Ã—][D]_ . A space lower bound of â„¦( _D_ ) for classical machines can be proved in the streaming model via adversarially ordering of the data [58], but it is unknown in the more realistic scenario where data are randomly sampled. In contrast, our quantum algorithms achieve space complexity poly(log _D_ ), exponentially improving over these classical streaming or online algorithms. Our classical lower bounds prove the â„¦( _D_[1] _[âˆ’][Î¶]_ ) _, âˆ€Î¶ >_ 0 lower bound for classical machines with random data access. 

**Sample-space lower bounds and communication complexity.** Space complexity lower bounds of classical streaming algorithms are often proved via reduction to one-way communication complexity [58], where we consider the past and future of the algorithm as two parties transmitting the memory in the forward direction. In the streaming model, we are allowed to adversarially choose the order of the data sequence, and hence we can design the hard instance by sequentially concatenating the inputs of the two parties. This proof strategy no longer works when we have multiple passes over the data or have random sample access as in our learning setting, because the order may be randomly shuffled and one-way communication lower bounds no longer suffice. We need communication complexity lower bounds for stronger communication models. 

A rich suite of techniques has been developed in proving multi-party communication complexity lower bounds. One route is via information complexity [154]. But its applicability is restricted to specific problems where information quantities can be explicitly calculated [155â€“157]. An alternative approach is via query-to-communication lifting, which is a general framework that lower bounds communication complexity by classical query complexity using the density restoring partition technique [88â€“94]. Another related line of work directly proves classical sample-space lower bounds for various learning problems involving parity in the random query setting [158â€“162], which is the IID version of our data access for Boolean functions. However, such problems is hard to quantum computers as well [163] and their relation to real-world tasks is unclear. 

Contrary to these existing approaches, we consider a learning task of estimating the property of some Boolean function _f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ using noisy random data samples. We call this task Noisy Oracle Property Estimation (NOPE) and formally define it in Section E 1. The desired property is specified as a query problem of the Boolean function, while the input data are random samples of a noisy version of its oracle. For this task, we develop a 

24 

communication complexity proof technique in Section E 3 based on a modified query-to-communication lifting and density restoring partition [88â€“94], proving that any classical algorithm solving the task with sample size _M_ and memory _S_ must satisfy _MS â‰¥_ â„¦( _NQC_ ), where _QC_ is the classical query complexity of the target property. Combined with the optimal sample complexity _M_ = Î˜( _NQ_[2] ) of quantum oracle sketching, this allows us to reveal the fundamental relation between space advantage and oracle query separation: _S â‰¥_ â„¦( _QC/Q_[2] ). If the classical query complexity is exponential, and quantum machines can solve the query problem in poly(log _N_ ) space with a slightly larger than quadratic query advantage (e.g., _QC_ = Î˜( _N_ ) _, Q_ = _O_ ( _N_[0] _[.]_[49] ), which implies _S â‰¥_ â„¦( _N_[0] _[.]_[02] )), this result unconditionally proves an exponential quantum space advantage. 

**Super-polynomial sample advantage and XOR lemmas.** We further bootstrap our sample-space lower bound into a super-polynomial sample complexity lower bound when space is constrained. This is proved using a hybrid approach combined with a new learning XOR lemma in Section E 4, which is similar in spirit with Yaoâ€™s XOR lemma [97] that amplifies hardness by taking the XOR of multiple independent problem instances. A streaming XOR lemma was developed in [99], but it is not applicable to our learning setting since their proof heavily relies on the ability to adversarially choose the ordering of the data (i.e., sequentially concatenate all problem instances). We circumvent this issue by developing a derandomization technique that allows us to prove the learning XOR lemma. In particular, we consider a dynamic version of the NOPE task, in which we repetitively try to solve log[2] _N_ independent instances of NOPE simultaneously. Our learning XOR lemma gives a 1 _/_ 2[log][2] _[ N]_ = 1 _/_ superpoly( _N_ ) bound on the progress in doing so with each repetition. Via a hybrid argument, this implies a superpoly( _N_ ) lower bound on the number of repetitions needed and thus the total sample complexity. Finally, we instantiate these classical hardness results with the Forrelation property of Boolean functions [95, 96] that provides the maximal average-case query separation. 

**Lower bounds for real-world applications.** All the above classical hardness results are proved for Boolean function problems with heavy theoretical computer science flavor. In Section E 5, we connect them to classical data processing and machine learning applications such as linear systems, binary classification, and dimension reduction, by embedding NOPE into these applications. In particular, we construct a polynomial size quantum circuit that solves the NOPE task of estimating the Forrelation [95, 96] property. We embed it into linear system tasks using the BQP-hardness of matrix inversion [118]. We follow a similar idea to prove the BQP-hardness of binary classification and uses a modified Feynman-Kitaev circuit Hamiltonian construction [164] to prove the BQP-hardness of dimension reduction. Consequently, the classical hardness results of Forrelation NOPE translates into the desired classical hardness results of the various applications. 

**Models of memory-bounded computation.** Our model of classical learning algorithms is the same as that of branching programs, which is the standard non-uniform model for space-bounded classical computation. It is stronger than online Turing machine and hence our classical lower bounds carries over directly. Our formal model of quantum learning algorithms can be viewed as a model of quantum branching programs that is allowed to apply arbitrary quantum channels depending on the input data. This model improves over existing proposals of quantum branching programs [165â€“167] that are too restricted to be realistic, as they can only apply unitary channels and hence cannot even simulate irreversible classical computation. 

**Quantum space advantage in streaming.** In the standard Turing machine model, where the data storage costs are ignored, a path integral argument shows that no super-quadratic quantum space advantage exists [64, 65]. In the streaming model where we take into account the costs of storing the input data, but the order of the data may be adversarially chosen, one-way quantum communication advantage can be used to prove exponential quantum space advantage in streaming. Examples of such one-way quantum communication advantage include the vector in subspace problem [71, 168] and the Boolean Hidden Matching problem [169]. Such quantum communication advantages lead to exponential space advantage in some specialized tasks such as Max Directed Cut [66â€“70]. Variants of Boolean Hidden Matching were recently demonstrated experimentally with trapped-ion systems [72, 73]. However, these tasks are specialized and many of their proof strategies heavily rely on the adversarial ordering of the data. Many of the quantum space advantages proved there become classically easy when the data are randomly sampled. In contrast, our quantum space advantages persist when the data are randomly sampled and apply to widely-useful applications such as linear systems, binary classification, and dimension reduction. 

# 25 

**==> picture [484 x 276] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a) (b)<br>D [0] root<br>Ï‰ 1 z 0 Â· Â· Â·<br>Â· Â· Â·<br>Ï‰ 2 DÂ· Â· Â·â†’TÏ‰ [1] 11 DÂ· Â· Â·â†’TÏ‰ [1] 11 situationlevel   â†’ 1 T 1 configs2 [S] z 1 z 2 zM â†’ 1<br>situation (c)<br>DÏ‰ [l][â†’] lâ†’ [1] 1 level   l â†’ 1<br>Ï‰l â†’Tlâ†’ 1<br>DÏ‰ [l] l â†’Â· Â· Â·Tlâ†’ 1 DÏ‰ [l] l situationlevel   l S Cz [0] 0 Cz [1] 1 Â· Â· Â· Mh<br>qubits<br>â†’Tl<br>â†’Tl â†’Tl<br>z z Â· Â· Â· z Â· Â· Â· z Â· Â· Â· z z data<br>FIG. 5: Overview of the models of data access and computation. (a) Illustration of the tree structure of<br>a hierarchical data generation process with l situation levels, each has time scale T 1 , . . . , Tl . Random variables within<br>the same box are IID conditioned on their shared latent situations. (b) The model of classical learning algorithms<br>with size S (i.e., 2 [S] possible configurations) and sample complexity M . The computation path when the algorithm is<br>given a sequence of data z 0 , . . . , zM âˆ’ 1 is highlighted in blue. (c) The model of quantum learning algorithms with size S<br>and sample complexity M . Upon receiving a sequence of data z 0 , . . . , zM âˆ’ 1, the algorithm applies a series of quantum<br>channels Cz [0] 0 [, . . . , C] z [M] M [âˆ’] âˆ’ [1] 1 [and] [measures] [the] [final] [state] [to] [compute] [the] [outcome.]<br>Â· Â· Â·<br>Â· Â· Â·<br>Â· Â· Â·<br>Â· Â· Â· Â· Â· Â· Â· Â· Â· Â· Â· Â·<br>Â· Â· Â· Â· Â· Â·<br>Â· Â· Â· Â· Â· Â· Â· Â· Â·<br>Â· Â· Â·<br>Â· Â· Â·<br>Â· Â· Â·<br>**----- End of picture text -----**<br>


**==> picture [247 x 9] intentionally omitted <==**

**----- Start of picture text -----**<br>
Appendix C: Models of data access and computation<br>**----- End of picture text -----**<br>


In this section, we formally introduce the models of data access and computation that we consider in this work. They are summarized in Figure 5. In Section C 1, we describe a model, dubbed hierarchical data generation processes, of how (classical) data samples are generated in the world in a dynamic and possibly correlated way. This includes IID data as a special case, and also includes data that have time-varying features and correlation with multiple time scales (e.g., the 1 _/f_ noise ubiquitous in electronics, user activity that changes over time, etc.). The goal of learning is to use these data samples to infer some property of the underlying data generation process (e.g., some rule for prediction or classification). This general data access model will be specialized to various applications in Section F. Some useful properties of such data generation processes are proved in Section C 4. 

To model the computation in learning, we formally define classical learning algorithms in Section C 2 and quantum learning algorithms in Section C 3. We define their key properties such as size (i.e., space complexity), sample complexity, and time complexity. In later sections, we will see that our quantum learning algorithm works for any hierarchical data generation processes and we will rigorously prove that any classical learning algorithm cannot work unless they have exponentially larger size. 

**1. Data generation processes** 

The world is full of randomness and noise and in general has to be modeled probabilistically. In a typical data processing or learning task, one collects _M_ data samples _z_ 1 _, . . . , zM_ from some underlying distribution in the world that generates the data. The goal is to learn some property of the underlying distribution based on these data samples. The data could represent a set of experimental observations for scientific discoveries, coefficients of a differential equation in simulation or real world, user data from internet activities, stock prices from financial markets, health care data from biomedical sensors, or interaction activities from an embodied robot. The property could be as simple as some statistical property (e.g., mean and variance) of the data, or as complicated as a model of how to predict the next data sample (e.g., predicting the next word in language modeling) or a rule for classification. As a starting point, one may model the underlying data generation process as drawing a sequence of independent and identically distributed (IID) data points 

**==> picture [282 x 11] intentionally omitted <==**

where _D_ is the underlying distribution whose property we want to learn about. 

26 

We can take a binary classification task as an example. In a typical binary classification task, one may think of the data points _zi_ as 

**==> picture [280 x 11] intentionally omitted <==**

where _âƒ—xi âˆˆ_ R _[D]_ is the _D_ -dimensional feature vector of a training data point that we collect from the world and _yi âˆˆ{Â±_ 1 _}_ is the corresponding label. The task is to generate a model that allows us to predict the label of another set of _m_ test data points _âƒ—x[â€²] j[, j][âˆˆ]_[[] _[m]_[].][For][example,][the][simplest][least-square][support][vector][machine] (LS-SVM) algorithm aggregates the training data into the form _X_ = ( _âƒ—x_ 1 _, . . . , âƒ—xM_ ) _, âƒ—y_ = ( _y_ 1 _, . . . , yM_ ) and makes the prediction using the following rule 

**==> picture [323 x 14] intentionally omitted <==**

This classification rule is the property of the underlying distribution _D_ that we want to learn about. 

Another cleaner, yet more theoretical example is learning properties of a Boolean function. Consider an unknown Boolean function _f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ . We want to learn its properties, but we do not have query access to this function. Instead, we have a sequence of data points of the form 

**==> picture [324 x 11] intentionally omitted <==**

that are random queries to the function _f_ . The goal is to learn some property of this function _f_ , specified by say a query algorithm _A_ ( _f_ ). In this example, the distribution _D_ of the data samples _zi_ = ( _xi, f_ ( _xi_ )) is in one-to-one correspondence with the underlying function _f_ . The property of _f_ is the property of _D_ that we want to learn about. 

The real world is dynamic and the IID assumption is often broken by correlation among the data samples. Such correlation could arise from a time-dependent data generation process (e.g., big things happen in the real world and the distribution changes correspondingly). It could also come from time-correlated noise in the data that may have multiple time scales (e.g., 1 _/f_ noise that is ubiquitous in electronic devices). 

To model data samples having noisy, time-varying features with multiple time scales, we consider the following hierarchical data generation process, where the way data are generated at each time step depends on the current _situation_ . The situation changes with time and has multiple time scales specified in a hierarchical way. We start from a root (highest level) probability distribution _D_[0] supported on a finite set of possible labels _A_ 1 that labels a set of probability distributions on the first level 

**==> picture [279 x 13] intentionally omitted <==**

We sample a random _Î±_ 1 _âˆˆ A_ 1 from _D_[0] , which specifies a distribution _DÎ±_[1] 1[.][We][will][make] _[T]_[1][independent][draws] from this _DÎ±_[1] 1[and][after][that][we][will][resample][a][fresh][instance][of] _[Î±]_[1][from] _[D]_[0][.][In][this][way,][the][parameter] _[T]_[1] specifies the first time scale of the data generation process. 

Each distribution _DÎ±_[1] 1[on][the][first][level][is][supported][on][another][finite][set][of][possible][labels] _[A]_[2][that][labels][a] set of probability distributions in the second level 

**==> picture [279 x 13] intentionally omitted <==**

Similar to the first level, now we sample a random _Î±_ 2 _âˆˆ A_ 2 from _DÎ±_[1] 1[,][which][specifies][a][distribution] _[D] Î±_[2] 2[.][We] will make _T_ 2 independent draws from this _DÎ±_[2] 2[and][after][that][we][will][resample][a][fresh][instance][of] _[Î±]_[2][from] _[D] Î±_[1] 1[.] Hence, the parameter _T_ 2 characterizes a second time scale of the data generation process. Suppose this goes on until we reach the _l_ -th level and we have sampled a distribution _DÎ±[l] l_[that][is][supported] on the data space _Z_ . We define the current _situation_ to be the sampled labels ( _Î±_ 1 _, . . . , Î±l_ ). For simplicity, we assume that we have included the information of the current situation (i.e., which distribution we are sampling from) into the data by including all _Î±_ 1 _, . . . , Î±l_ in _z_ . For example, _Z_ = _X Ã— Y Ã— A_ 1 _Ã— Â· Â· Â· Ã— Al_ and the generated samples are of the form _zi_ = ( _xi, yi, Î±_ 1 _,i, . . . , Î±l,i_ ). In practice, we may not have access to the situations and our quantum algorithm extends straightforwardly to these scenarios. 

We will make _Tl_ independent draws of _z_ â€™s from this _DÎ±[l] l_[and][after][that][we][will][resample][a][fresh][instance][of] _Î±l_ from _DÎ±[l][âˆ’] lâˆ’_[1] 1[.][All][together,][this][describes][an] _[l]_[-level][hierarchical][data][generating][process][with] _[l]_[different][time] scales ( _T_ 1 _, . . . , Tl_ ). We use the following notation to denote this data generation process: 

**==> picture [371 x 13] intentionally omitted <==**

Note that in such a hierarchical data generating process _D_ , the marginal distribution of each individual data sample _zi_ is the same. This ensures that there is a persistent signal present in the data. Yet they are not independently distributed as there may be correlation mediated by higher levels of the hierarchy with the corresponding time scales. This poses an apparent challenge for learning. 

27 

We can define a few characteristic properties of a hierarchical data generating process _D_ . We define the _refreshing time Ï„D_ of _D_ to be the product of all time scales 

**==> picture [274 x 11] intentionally omitted <==**

_Ï„D_ characterizes the largest timescale of correlation in the data generation process _D_ . In particular, two data points that are at least _Ï„D_ far apart from each other are independent. We also use _D â†’[Ã—][Ï„][D] z_ to denote the process of generating a single refreshing block of data from _D_ . 

We define the _repetition number RD_ of _D_ as follows 

**==> picture [320 x 14] intentionally omitted <==**

where _Nz_ =[ï¿½] _[Ï„] i_ =1 _[D][Î´][z] i[,z]_[is][the][number][of] _[z]_[â€™s][in][a][refreshing][block][of][data.][In][other][words,] _[R][D]_[is][the][expected] number of extra _z_ â€™s one gets in a refreshing time block if we condition on the first sample being _z_ , maximized over all _z âˆˆZ_ . We note that it is always non-negative because by construction our data generation process can only enhance the correlation between data samples by sharing common situations (Theorem C.1). When the data samples _zi_ do not contain the full information of the situations, we need to include the situations in the condition of definition. 

The repetition number _RD_ controls the variance of the number of samples one get on each _z_ , which determines the rate of convergence in our quantum oracle sketching algorithm. Intuitively, the more frequent the samples repeat themselves, the more redundant the data are. Effectively, the _RD_ repetitive samples is only as good as a single sample, and therefore we expect that the sample complexity to blow up by a factor of _RD_ . 

To illustrate these concepts, we give two examples of data generation processes: the repetitive process _D_ rep and the alternating process _D_ alt. The repetitive process _D_ rep is defined as 

**==> picture [302 x 12] intentionally omitted <==**

where _D_[0] = Uniform([ _N_ ]) and _Dx_[1][always][outputs][its][label] _[x][âˆˆ]_[[] _[N]_[]][repetitively] _[N]_[times.][We][have][refreshing] time _Ï„D_ rep = _N_ and repetition number _RD_ rep = _N âˆ’ N Ã—_ 1 _/N_ = _N âˆ’_ 1. This is intuitive as _D_ rep repeats the same output _N âˆ’_ 1 times. In contrast, the alternating process is defined as 

**==> picture [301 x 12] intentionally omitted <==**

where _D_[0] = Bern(1 _/_ 2), _Î± âˆˆ{_ 0 _,_ 1 _}_ , and _DÎ±_[1][samples] _[ x][ âˆ¼]_[Uniform([] _[N]_[]) randomly] _[ N]_[times and outputs] _[ z]_[= (] _[x, Î±]_[).] We still have refreshing time _Ï„D_ alt = _N_ , but the repetition number is _RD_ alt = (1+( _N âˆ’_ 1) _Ã—_ 1 _/N_ ) _âˆ’N Ã—_ 1 _/_ (2 _N_ ) = 3 _/_ 2 _âˆ’_ 1 _/N_ . This is also intuitive since the data are generated uniformly random and the expected number of repetitions is small. 

In Section C 4, we prove some useful properties of general hierarchical data generation processes. 

## **2. Classical learning algorithms** 

Now we introduce our computational model of classical learning algorithms. In defining such learning algorithms, we need to take into account restrictions on the size of the classical machine. 

We define classical learning algorithms as follows. We use _S_ to denote the size of the classical machine (also called the space complexity), and use _M_ to denote the number of samples this learning algorithm takes in (i.e., sample complexity). Let _I_ be the set of all possible inputs to the learning algorithm at each time step. For our data generation process defined above, _I_ = _Z_ . A classical learning algorithm _L_ with size _S_ , sample complexity _M_ , and input form _I_ is defined as a directed graph with vertices arranged in _M_ + 1 layers (0 to _M_ ). Each layer consists of at most 2 _[S]_ vertices, each labeled by _S_ bits. There is only one vertex called the root in layer 0. In layer _M_ , each vertex _v_ has no outgoing edges and is called a leaf. Each leaf _v_ is attached with an output _hv_ . For each layer _i_ = 0 _, . . . , M âˆ’_ 1, the outgoing edge from each vertex in layer _i_ only goes to vertices in layer _i_ +1. Each vertex has _|I|_ outgoing edges, labeled by each element of _I_ . 

The computation of the learning algorithm _L_ proceeds as follows. Upon receiving a sequence of data _Ii âˆˆ I, i_ = 0 _, . . . , M âˆ’_ 1, the algorithm starts from the root, follows the edge given by each data point _Ii_ in layer _i_ until reaching a leaf _v_ in layer _M_ , and outputs _hv_ . 

To keep track of the information flow during learning, we define the _transcript Ï€L_ ( _I, Î±_ ) of the learning algorithm _L_ upon receiving the data sequence _I_ = ( _I_ 0 _, . . . , IM âˆ’_ 1) _âˆˆI[M]_ with respect to a situation record _Î±_ = ( _Î±_ 0 _, . . . , Î±M âˆ’_ 1) to be the concatenation of the length- _S_ bitstrings that label the vertices traversed by the computation path at layers _i_ where the situation changes _Î±i_ = _Î±i_ +1, followed by the output of _L_ . For our data generation process, suppose that the situation changes in total _r_ times and the output is a single bit _hv âˆˆ{_ 0 _,_ 1 _}_ , the transcript _Ï€L_ ( _I, Î±_ ) is a bitstring with total length _|Ï€L_ ( _I, Î±_ ) _|_ = ( _r_ + 1) _S_ + 1. 

28 

Furthermore, we define the data processing time per sample to be the time complexity of the computation per layer. The total time complexity of the learning algorithm is equal to the sample complexity times the data processing time per sample. 

Since any randomized algorithm can always be regarded as first sampling all the random numbers and then execute the corresponding deterministic algorithm (i.e., de-randomized), the deterministic definition above suffices. We note that our definition of classical learning algorithms resemble the notion of branching programs. They are non-uniform models of space-bounded computation (the most general form), more general than uniform ones such as online Turing machines with bounded space. Therefore, the classical hardness results we prove also applies to uniform computational models. 

## **3. Quantum learning algorithms** 

Our model for quantum learning algorithms (with classical data inputs) is similar to that of classical learning algorithms, but the computation is done via a quantum circuit. Note that since we are considering the task of processing classical data, the data that we feed into quantum learning algorithms are completely classical and the data access model is the same as that of classical learning algorithms. 

In particular, we define quantum learning algorithms as follows. We use _S_ to denote the size of the quantum machine (also called the space complexity), and use _M_ to denote the number of samples this learning algorithm takes in (i.e., sample complexity). Let _I_ be the set of all possible inputs to the quantum learning algorithm at each time step. For our data generation process _I_ = _Z_ . A quantum learning algorithm _L_ with size _S_ , sample complexity _M_ , and input form _I_ is defined as an initial _S_ -qubit quantum state _Ï_ 0 and a sequence of _M_ sets of _S_ -qubit quantum channels ( _C_[0] _, . . . , C[M][âˆ’]_[1] ), where each set _C[i]_ = _{CI[i]_[:] _[ I][âˆˆI}]_[contains] _[|I|]_[quantum][channels] on _S_ qubits that are labeled by the elements of _I_ . At the end, there is an _S_ -qubit positive operator-valued measurement (POVM) _{Mh},_[ï¿½] _h[M][h]_[=] _[I]_[whose][output][labeled][by] _[h]_[is][the][output][of][the][quantum][learning] algorithm. 

The computation of the learning algorithm _L_ proceeds as follows. Upon receiving a sequence of data _Ii âˆˆ I, i_ = 0 _, . . . , M âˆ’_ 1, the algorithm starts from the initial state _Ï_ 0, sequentially applies the quantum channel _CI[i] i_ given by each data point _Ii_ in step _i_ until reaching the _M_ -th step. Finally, the algorithm measures _{Mh}_ on the resulting state 

**==> picture [303 x 14] intentionally omitted <==**

and output the measurement outcome _h_ with probability tr( _MhÏM_ ) as the output of the learning algorithm. 

Similar to classical learning algorithms, we define the data processing time per sample as the time complexity of implementing the quantum channel per layer. The total time complexity is equal to the sample complexity times the data processing time per sample. 

We remark that although this formal definition of quantum learning algorithm here is a non-uniform computational model, we will see that the quantum learning algorithms designed in this work all have program descriptions that can be generated by a polynomial-time classical Turing machine and therefore fit into uniform computational models. We define (uniform) quantum learning algorithms with the additional requirement that the initial state _Ï_ 0, the quantum channel sets ( _C_[1] _, . . . , C[M][âˆ’]_[1] ), and the final measurement _{Mh}_ can be generated by a polynomial-time classical Turing machine. 

## **4. Properties of hierarchical data generation processes** 

In this section, we prove some useful properties of the hierarchical data generation processes defined in Section C 1. We will study some fundamental properties of the repetition number and use it to characterize statistical properties of the data samples. 

Let 

**==> picture [370 x 14] intentionally omitted <==**

be a hierarchical data generation process with refreshing time _Ï„D_ = _Tl Â· Â· Â· T_ 1 and repetition number 

**==> picture [353 x 31] intentionally omitted <==**

An equivalent probability formulation of repetition number is 

**==> picture [346 x 28] intentionally omitted <==**

29 

The structure of the data generation process induces correlation between data samples. For any two data samples _zi, zj_ , we define their _correlation depth K_ ( _i, j_ ) _âˆˆ{_ 0 _, . . . , l}_ to be the number of situation levels that they share. In other words, _zi, zj_ shares the situation ( _Î±_ 1 _, . . . , Î±K_ ( _i,j_ )). Clearly _K_ ( _i, j_ ) = _K_ ( _j, i_ ). If _K_ ( _i, j_ ) = 0, then _zi, zj_ are independent and belong to different refreshing blocks of data. The following lemma formalizes the intuition that sharing situations enhances correlation, which immediately implies _RD â‰¥_ 0. 

**Lemma C.1** (Sharing situations enhances correlation) **.** _Let zi, zj âˆˆZ, i, j â‰¥_ 1 _be any two random data samples from a hierarchical data generation process D. Then,_ 

**==> picture [307 x 12] intentionally omitted <==**

_for any z âˆˆZ._ 

_Proof._ Let _K_ ( _i, j_ ) be the correlation depth between _zi, zj_ . Let _Ïƒ_ = ( _Î±_ 1 _, . . . , Î±K_ ( _i,j_ )) be the random shared situation. By construction, _zi|Ïƒ_ and _zj|Ïƒ_ are IID with the same distribution that we call _qÏƒ_ ( _z_ ). Hence, 

**==> picture [348 x 107] intentionally omitted <==**

Applying Jensenâ€™s inequality on _f_ ( _w_ ) = _w_[2] , we have 

**==> picture [378 x 13] intentionally omitted <==**

This gives us 

**==> picture [335 x 12] intentionally omitted <==**

as desired, where we have used the fact that all data samples have the same marginal. 

Moreover, the following result shows that correlation does not decrease with correlation depth. 

**Lemma C.2** (Correlation is non-decreasing with correlation depth) **.** _For any fixed z âˆˆZ and four time steps i, j, i[â€²] , j[â€²] â‰¥_ 1 _, if K_ ( _i, j_ ) _â‰¤ K_ ( _i[â€²] , j[â€²]_ ) _, then_ Pr[ _zj_ = _z|zi_ = _z_ ] _â‰¤_ Pr[ _zjâ€²_ = _z|ziâ€²_ = _z_ ] _._ 

_Proof._ Let _Ïƒ_ = ( _Î±_ 1 _, . . . , Î±K_ ( _i,j_ )) and _Ïƒ[â€²]_ = ( _Î±_ 1 _[â€²][, . . . , Î±] K[â€²]_ ( _i[â€²] ,j[â€²]_ )[) be the random situations shared by] _[ z][i][, z][j]_[and] _[ z][i][â€²][, z][j][â€²]_ respectively. By construction, _zi|Ïƒ_ and _zj|Ïƒ_ are IID with the same distribution that we call _qÏƒ_ ( _z_ ). We define _qÏƒ[â€²][â€²]_[(] _[z]_[)][similarly.][Let][the][marginal][be] _[p]_[(] _[z]_[).][Then][we][have] 

**==> picture [384 x 26] intentionally omitted <==**

They are clearly equal if _K_ ( _i, j_ ) = _K_ ( _i[â€²] , j[â€²]_ ). If instead _K_ ( _i, j_ ) _< K_ ( _i[â€²] , j[â€²]_ ), we can define a hybrid situation 

**==> picture [342 x 13] intentionally omitted <==**

Note that by construction, the (marginal) distribution of situations only depends on the levels. Therefore, we have that the marginal distribution of _Ïƒ[â€²â€²]_ is the same as that of _Ïƒ[â€²]_ . This means that 

**==> picture [347 x 25] intentionally omitted <==**

Further note that for any _k_ , 

**==> picture [351 x 15] intentionally omitted <==**

30 

Hence, we have 

**==> picture [375 x 160] intentionally omitted <==**

where we have used Jensenâ€™s inequality for _f_ ( _w_ ) = _w_[2] . This proves Theorem C.2. 

Although the repetition number _RD_ is defined with a starting time of _t_ = 1, the following lemma shows that _RD_ upper bounds the repetition number of any starting time. This property allows us to collect data starting at any time point. 

**Lemma C.3** (Repetition number bound is agnostic to starting time) **.** _For any t â‰¥_ 1 _, the repetition number starting at time t_ 

**==> picture [356 x 30] intentionally omitted <==**

_satisfies_ 

**==> picture [271 x 11] intentionally omitted <==**

_Proof._ Note that 

**==> picture [360 x 28] intentionally omitted <==**

where we have changed the variable and used the marginal being the same. We only need to show 

**==> picture [332 x 11] intentionally omitted <==**

for any _z âˆˆZ, s â‰¥_ 0 _, t â‰¥_ 1, then we are done. Using Theorem C.2, it suffices to show that the correlation depth satisfies 

**==> picture [332 x 11] intentionally omitted <==**

To show this, note that the tree structure of the data generation process implies that for any _k âˆˆ{_ 1 _, . . . , l}_ , the data samples (1 _,_ 1 + _s_ ) share situations at level _k_ as long as _s < Tl . . . Tk_ . But in order for ( _t, t_ + _s_ ) to share situations at level _k_ , they need to satisfy extra conditions on _s, t_ (e.g., the effect of crossing boundaries, etc.). Therefore, any situation level shared by ( _t, t_ + _s_ ) must also be shared by (1 _,_ 1 + _s_ ). In other words, we have _K_ ( _t, t_ + _s_ ) _â‰¤ K_ (1 _,_ 1 + _s_ ) as desired. This proves Theorem C.3. 

As we will see in Section D, the frequency of collecting a specific data sample _z âˆˆZ_ , 

**==> picture [289 x 30] intentionally omitted <==**

in a sequence of _M_ data samples _zt, . . . , zt_ + _M âˆ’_ 1 will play a crucial role in quantum oracle sketching. In the following, we characterize the statistical properties of _mz_ using properties of the data generation process. Since the marginal of each data sample _p_ ( _z_ ) is fixed, we always have E[ _mz_ ] = _p_ ( _z_ ). The following lemma shows that the variance of _mz_ is upper bounded by the repetition number _RD_ . 

31 

**Lemma C.4** (Repetition number bounds variance) **.** _Let t â‰¥_ 1 _be any starting time. Let zt, . . . , zt_ + _M âˆ’_ 1 _be a sequence of M data samples drawn from the hierarchical data generation process D with marginal p_ ( _z_ ) _and repetition number RD. Let_ 

**==> picture [309 x 31] intentionally omitted <==**

_be the frequency of having the value z in these data samples. Then, we have_ 

**==> picture [285 x 22] intentionally omitted <==**

_for any z âˆˆZ._ 

_Proof._ Let the marginal be _p_ ( _z_ ). The variance can be decomposed as 

**==> picture [342 x 63] intentionally omitted <==**

If _zt_ + _iâˆ’_ 1 _, zt_ + _jâˆ’_ 1 are not in the same refreshing block, they are independent and Cov( _Î´z,zt_ + _iâˆ’_ 1 _, Î´z,zt_ + _jâˆ’_ 1) = 0. On the other hand, if _zt_ + _iâˆ’_ 1 _, zt_ + _jâˆ’_ 1 are in the same refreshing block, since each block has the same distribution, we may as well assume that they are both in the first block at time steps _i, j âˆˆ_ [ _Ï„D_ ]. Then the covariance is equal to 

**==> picture [358 x 74] intentionally omitted <==**

Note that from Theorem C.1, we have Cov( _Î´z,zi, Î´z,zj_ ) _â‰¥_ 0. By construction of the data generation process _D_ , the joint distribution of any two data samples _zi, zj_ only depends on the there correlation depth _K_ ( _i, j_ ). Hence, the conditional probability Pr[ _zj_ = _z|zi_ = _z_ ] only depends on _K_ ( _i, j_ ), and we use _qK_ ( _i,j_ )( _x_ ) to denote it. Summing over all _j âˆˆ_ [ _Ï„D_ ] (which includes _i_ itself), we can regroup the sum according to the correlation depth _k_ and obtain 

**==> picture [401 x 74] intentionally omitted <==**

which is independent of _i_ . In particular, we can set _i_ = 1: 

**==> picture [352 x 24] intentionally omitted <==**

Plugging it back into the variance expression, we obtain 

**==> picture [364 x 111] intentionally omitted <==**

where the first inequality uses the non-negativity of the covariances and the second inequality uses the definition of _RD_ . This proves Theorem C.4. 

32 

When we have already processed a previous sequence of data _z_ 1 _, . . . , ztâˆ’_ 1 (i.e., condition on them), the distribution of _mz_ shifts. In particular, the (conditional) expectation of _mz_ no longer matches _p_ ( _z_ ). Luckily, the following lemma shows that the expected drift is controlled by the repetition number _RD_ . Note that the bound scales as 1 _/M_ , much better than the usual 1 _/âˆšM_ from concentration. 

**Lemma C.5** (Repetition number bounds conditional drift) **.** _Let t â‰¥_ 1 _be the starting time of this round of data processing. Let z_ 1 _, . . . , ztâˆ’_ 1 _, zt, . . . , zt_ + _M âˆ’_ 1 _be a sequence of data samples drawn from the hierarchical data generation process D with marginal p_ ( _z_ ) _and repetition number RD. Let_ 

**==> picture [314 x 30] intentionally omitted <==**

_be the frequency of having the value z in this round of data processing. Then, we have_ 

**==> picture [407 x 26] intentionally omitted <==**

_Proof._ Note that the conditional independence structure in the hierarchical data generation process implies that the data samples in this round _zt, . . . , zt_ + _M âˆ’_ 1 can only correlate with the previous samples _z_ 1 _, . . . , ztâˆ’_ 1 through the situation _Ïƒt_ = ( _Î±_ 1 _,t, . . . , Î±l,t_ ) of _zt_ , which is a part of _zt_ by construction. This means that 

**==> picture [422 x 141] intentionally omitted <==**

where we have used triangle inequality. Hence, it suffices to prove that 

**==> picture [350 x 24] intentionally omitted <==**

To this end, we express this quantity in covariances as 

**==> picture [363 x 224] intentionally omitted <==**

33 

where we have defined the aggregated cross-covariance matrix 

**==> picture [315 x 30] intentionally omitted <==**

Next, we invoke the structural properties of the data generation process. For any 0 _â‰¤ i â‰¤ M âˆ’_ 1, we define the conditional expectation 

**==> picture [306 x 12] intentionally omitted <==**

where _Ïƒt,t_ + _i_ is the situation shared by the data samples _zt, zt_ + _i_ . Since the data are sampled IID once conditioned on the shared situation, we have 

**==> picture [357 x 12] intentionally omitted <==**

The law of total covariance then implies that 

**==> picture [429 x 40] intentionally omitted <==**

where we have used the fact that conditioned on the shared situation _Ïƒt,t_ + _i_ , the data samples are independent and their conditional covariance vanishes. This shows that this cross-covariance is secretly a covariance. This covariance can be further upper bounded by variances as 

**==> picture [434 x 19] intentionally omitted <==**

Plugging this back into the expression of Î£, we apply Cauchy-Schwarz inequality and obtain 

**==> picture [473 x 37] intentionally omitted <==**

The variances can again be written as cross-covariance using the law of total covariance in reverse: 

**==> picture [431 x 68] intentionally omitted <==**

Summing over 0 _â‰¤ i â‰¤ M âˆ’_ 1 gives us 

**==> picture [398 x 65] intentionally omitted <==**

where we have used Theorem C.1 in the first inequality and Theorem C.3 in the second. This gives us 

Î£( _z, z[â€²]_ ) _â‰¤_ ~~ï¿½~~ _p_ ( _z_ ) _RD_ ï¿½ _p_ ( _z[â€²]_ ) _RD_ = _RD_ ~~ï¿½~~ _p_ ( _z_ ) _p_ ( _z[â€²]_ ) _._ (C51) 

As a result, we arrive at 

**==> picture [393 x 123] intentionally omitted <==**

as desired. This completes the proof of Theorem C.5. 

34 

**==> picture [484 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a) _-_ M - (b) <_< Q â€”><br>Quantum oracle sketching<br>with random samples @ =<br>log  N Instantiate any<br>. x  = 10100 t sass ea]<br>quantum algorithm<br>eoeoo Â«86+ 138 Es that makes         uses of Q<br>1<br>f ( x ) = e (ece O, O [â€ ] , cO, cO [â€ ]<br>0 O with<br># samples M = !( N/Ï‰ ) M = !( NQ [2] /Ï‰ )<br>samples<br>Data O<br>Ï‰v O<br>O<br>noisy correlated structured<br>Ww Ge \ [i =a | |<br>FIG. 6: Schematic overview of quantum oracle sketching. (a) Illustration of quantum oracle sketching for<br>Boolean function data ( x, f ( x )) , f : [ N ] â†’{ 0 ,  1 } . We build the phase oracle O = > x [(] [âˆ’] [1)] [f] [(] [x] [)] [ |][x][âŸ©âŸ¨][x][|] [of] [f] [using] [multi-]<br>controlled phase gates with control patterns given by x and phase values given by f ( x ) from the data. M = Î˜( N/Ïµ )<br>samples guarantee Ïµ approximation of the phase oracle in diamond distance. We generalize this to accommodate noisy<br>and correlated data inputs with generic data structures including state preparation unitaries of any vectors and block<br>encodings of sparse matrices. (b)  We use quantum oracle sketching to load data into a quantum computer and instantiate<br>the oracle queries in any quantum algorithm. M = Î˜( NQ [2] /Ïµ ) samples guarantee Ïµ approximation in diamond distance<br>of any quantum algorithm that makes Q queries to the oracle O , its inverse O [â€ ] , or the controlled versions cO, cO [â€ ] .<br>**----- End of picture text -----**<br>


## **Appendix D: Quantum oracle sketching** 

In this section, we provide a detailed description of the proposed quantum oracle sketching scheme, summarized in Figure 6. In Section D 1, we introduce necessary preliminaries including basic inequalities and techniques from quantum singular value transform (QSVT). In Section D 2, we introduce quantum oracle sketching starting from the simplest case of IID data samples of the form ( _x, f_ ( _x_ )), where _x âˆ¼_ Uniform([ _N_ ]) and _f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ is a Boolean function whose property we want to estimate. We show how to construct the phase oracle of _f_ using the random data samples and use it to run quantum query algorithms that estimate the properties of _f_ . Hence the name quantum oracle sketching. Along the way, we discuss the apparent trap of decoherence that seems to rule out the possibility of quantum oracle sketching and explain how we evade decoherence. In Section D 3, we show that the sample complexity of quantum oracle sketching is optimal, by proving a matching lower bound. 

Building upon this simplest case, in Section D 4, we introduce several extensions of quantum oracle sketching. In particular, we show how to handle functions with multi-bit outputs, time-varying data generation processes that are correlated and not IID, and unknown marginal distributions. In Section D 5, we use quantum oracle sketching to construct various linear algebra primitives, such as the sparse oracles and block encodings of sparse matrices, and quantum states corresponding to arbitrary vectors, all from random data samples of the matrices and vectors. Since the state preparation algorithm requires significantly more algorithmic ingredients, we give it a standalone name of quantum state sketching. These subroutines will be used in various applications detailed in Section F. 

## **1. Preliminaries** 

_a. Inequalities_ 

We begin by introducing some preliminary results that we will use and reprove some of them for accessibility. The diamond distance between unitary channels is bounded by the operator distance between the unitaries. This is also true for channels built from isometries. 

**Lemma D.1** (Diamond distance and operator distance, [86, Lemma 3.4]) **.** _Let U, V be isometries from_ C _[d][i] to_ C _[d][o] with do â‰¥ di. That is, U[â€ ] U_ = _V[â€ ] V_ = _I. Let U_ : _Ï â†’ UÏU[â€ ] and V_ : _Ï â†’ V ÏV[â€ ] be the corresponding channels. Then we have_ 

**==> picture [293 x 21] intentionally omitted <==**

35 

_Proof._ Note that to compute the diamond distance between unitary channels, it is not necessary to stabilize them with identity on an auxiliary space. Meanwhile, the isometry channels _U, V_ can be viewed as unitary channels over an enlarged input Hilbert space. Therefore, we have 

**==> picture [372 x 140] intentionally omitted <==**

This proves Theorem D.1. 

A similar bound holds for the expectation value of random unitary channels. This extends to channels built from isometries as well. In the literature, this relation is often referred to as the mixing lemma [86, 170]. We thank Angus Lowe and Richard Allen for pointing out a subtle mathematical flaw in the original proof presented in an earlier version of [86, Lemma 3.4], and for the insightful discussion that led to the corrected proof presented here with the additional factor of 2. 

**Lemma D.2** (Diamond distance and operator distance in expectation) **.** _Let U be an isometry from_ C _[d][i] to_ C _[d][o] with do â‰¥ di. That is, U[â€ ] U_ = _I. Let V be a random isometry from_ C _[d][i] to_ C _[d][o] with V[â€ ] V_ = _I. Let U_ : _Ï â†’ UÏU[â€ ] and V_ : _Ï â†’ V ÏV[â€ ] be the corresponding channels. Then we have_ 

**==> picture [308 x 22] intentionally omitted <==**

_Proof._ Let ( _pi, Vi_ ) be any random isometry ensemble. For any pure state _|ÏˆâŸ©_ , we expand the action of the expected channel by centering it around E[ _V_ ] as 

**==> picture [400 x 29] intentionally omitted <==**

where we have used E[ _V âˆ’_ E[ _V_ ]] = 0 to remove the cross terms. By triangle inequality, we have 

**==> picture [421 x 59] intentionally omitted <==**

The bias term is bounded as 

**==> picture [468 x 58] intentionally omitted <==**

where we have used triangle inequality and Holderâ€™s inequality with 1 _/_ 2 + 1 _/_ 2 = 1. Since _U, Vi_ are isometries, we have _âˆ¥U |ÏˆâŸ©âˆ¥_ 2 = 1 and _âˆ¥_ E[ _V_ ] _|ÏˆâŸ©âˆ¥_ 2 _â‰¤_[ï¿½] _i[p][i][âˆ¥][V][i][ |][Ïˆ][âŸ©âˆ¥]_[2][= 1.][Therefore,][the][bias][term][is][bounded][by] 

**==> picture [371 x 22] intentionally omitted <==**

To bound the variance term, note that ( _V âˆ’_ E[ _V_ ]) _|ÏˆâŸ©âŸ¨Ïˆ|_ ( _V âˆ’_ E[ _V_ ]) _[â€ ]_ is positive semi-definite and so is its expectation. Thus, its trace norm is the same as its trace. Using _V[â€ ] V_ = _I_ , we obtain: 

**==> picture [411 x 45] intentionally omitted <==**

36 

Now we use _U[â€ ] U_ = _I_ and obtain 

**==> picture [437 x 57] intentionally omitted <==**

where we have used Cauchy-Schwarz inequality and _U, Vi_ being isometries. Therefore, the variance term is bounded as 

**==> picture [373 x 21] intentionally omitted <==**

Combining the bias and variance term, we have 

**==> picture [367 x 21] intentionally omitted <==**

Using this, we have 

**==> picture [414 x 74] intentionally omitted <==**

as desired. 

We will also use the subadditivity of diamond distance. 

**Lemma D.3** (Subadditivity of diamond distance, [171, Proposition 3.48]) **.** _For any channels C_ 1 _, C_ 2 _and C_ 1 _[â€²][,][ C]_ 2 _[â€²][,] we have_ 

**==> picture [336 x 12] intentionally omitted <==**

The following lemma is useful in relating trace distance and relative entropy. We will use it in proving the optimality of quantum oracle sketching in Section D 3. 

**Lemma D.4** (Quantum Bretagnolle-Huber inequality, [172, Lemma B.1], [173]) **.** _Let Ï, Ïƒ âˆˆ_ C _[N][Ã—][N] be two quantum states. Then,_ 

**==> picture [305 x 22] intentionally omitted <==**

_where D_ ( _Ïâˆ¥Ïƒ_ ) = tr( _Ï_ log2 _Ï âˆ’ Ï_ log2 _Ïƒ_ ) _is the relative entropy between Ï and Ïƒ._ 

We will also make use of the following moment bound for quadratic forms of random vectors [174]. This would be useful in bounding the error of quantum state sketching (Theorem D.24). 

**Lemma D.5** (Moment bound for quadratic forms [174, Theorem 5.1]) **.** _Let A âˆˆ_ R _[N][Ã—][N] be a symmetric matrix. Let v âˆˆ{Â±_ 1 _}[N] be a uniformly distributed random sign vector. Then for all integer k â‰¥_ 2 _, we have_ 

**==> picture [355 x 21] intentionally omitted <==**

_where C >_ 0 _is a universal constant, âˆ¥Aâˆ¥F is the Frobenius norm of A, and âˆ¥Aâˆ¥ is the operator norm of A._ 

Another useful lemma used is the following moment bound for a sum with random signs. 

**Lemma D.6** (Khintchineâ€™s inequality, [175, Exercise 2.6.5]) **.** _Let b_ 1 _, . . . , bN âˆˆ_ R _be fixed numbers and v_ 1 _, . . . , vN âˆˆ{Â±_ 1 _} be uniformly distributed random signs. Then for all integers k â‰¥_ 2 _, we have_ 

**==> picture [325 x 43] intentionally omitted <==**

_where C >_ 0 _is a universal constant._ 

37 

The following lemma relates the error of exchanging expectation value and matrix exponentiation on a random diagonal matrix with the variance of its matrix elements. It will be used to bound the error of quantum oracle sketching by the variance of the data. As a special case, we note that it can be used to improve the constant factor in the qDrift error bound analysis in [86]. 

**Lemma D.7** (Expected error and variance) **.** _Let X_ = diag( _X_ 1 _, . . . , Xd_ ) _âˆˆ_ R _[d][Ã—][d] be a random diagonal matrix, where X_ 1 _, . . . , Xd âˆˆ_ R _are random variables. Then, we have_ 

**==> picture [322 x 22] intentionally omitted <==**

_where âˆ¥Â· âˆ¥ is the operator norm._ 

_Proof._ Since _X_ and E[ _X_ ] are all diagonal matrices, they commute with each other. Moreover, _e[i]_[E][[] _[X]_[]] _âˆ’_ E[ _e[iX]_ ] is also a diagonal matrix with diagonal elements _e[i]_[E][[] _[X][j]_[]] _âˆ’_ E[ _e[iX][j]_ ] _,_ 1 _â‰¤ j â‰¤ d_ . Note that for any _j âˆˆ_ [ _d_ ], 

**==> picture [364 x 99] intentionally omitted <==**

where we have used triangle inequality _|_ E[ _Â·_ ] _| â‰¤_ E[ _| Â· |_ ] and _|e[iw] âˆ’ w âˆ’_ 1 _| â‰¤ w_[2] _/_ 2 _, âˆ€w âˆˆ_ R. Hence, we arrive at 

**==> picture [379 x 22] intentionally omitted <==**

This proves Theorem D.7. 

## _b. Quantum singular value transform_ 

We will make use of the following result from quantum singular value transform (QSVT) [9, 10]. 

**Lemma D.8** (Quantum eigenvalue transform, [10, Theorem 3], [9, Corollary 18, Lemma 19]) **.** _Let A_ = ï¿½ _Î»[Î»][ |][Î»][âŸ©âŸ¨][Î»][|][âˆˆ]_[C][2] _[n][Ã—]_[2] _[n][be][a][Hermitian][matrix][with][âˆ¥][A][âˆ¥â‰¤]_[1] _[.] Given query access to the_ ( _n_ + 1) _-qubit unitary U and its inverse U[â€ ] such that âŸ¨_ 0 _a| U |_ 0 _aâŸ©_ = _A where |_ 0 _aâŸ© is on the ancilla qubit a. For any Ï• âˆˆ_ [0 _,_ 2 _Ï€_ ) _, we use_ Î  _Ï•_ = _e[iÏ•Z][a] to denote the single-qubit Z rotation on the ancilla a. Then, for any real polynomial P_ : R _â†’_ R _and even integer d satisfying_ 

_1. the degree of P is at most d,_ 

_2. P is an even function, and_ 

_3. |P_ ( _x_ ) _| â‰¤_ 1 _, âˆ€x âˆˆ_ [ _âˆ’_ 1 _,_ 1] _,_ 

_there exists a set of rotation angles Ï•i âˆˆ_ [0 _,_ 2 _Ï€_ ) _, i âˆˆ_ [ _d_ ] _, such that the unitary_ 

**==> picture [324 x 31] intentionally omitted <==**

_satisfies_ 

**==> picture [348 x 22] intentionally omitted <==**

_Moreover, the controlled version of the constructed unitary P_ QSVT( _U, Ï•_ ) _can be constructed by replacing_ Î  _Ï• with their controlled version c_ Î  _Ï•_ = _|_ 0 _aâ€²âŸ©âŸ¨_ 0 _aâ€²| âŠ— I_ + _|_ 1 _aâ€²âŸ©âŸ¨_ 1 _aâ€²| âŠ—_ Î  _Ï•:_ 

**==> picture [427 x 32] intentionally omitted <==**

_where a[â€²] is the control qubit._ 

38 

We will use Theorem D.8 to apply threshold functions, which can be approximated using a polynomial as follows. 

**Lemma D.9** (Polynomial approximation of threshold functions, [10, Page 14]) **.** _For any Î»[â‹†] âˆˆ_ (0 _,_ 1) _and Ïµ âˆˆ_ (0 _,_ 2 ~~ï¿½~~ 2 _/_ ( _eÏ€_ ) _, there exists a real polynomial P_ : R _â†’_ R _such that_ 

_1. the degree of P is O_ (log(1 _/Ïµ_ ) _/Î»[âˆ—]_ ) _,_ 

_2. P is an even function,_ 

_3. |P_ ( _x_ ) _| â‰¤_ 1 _, âˆ€x âˆˆ_ [ _âˆ’_ 1 _,_ 1] _, and_ 

_4. |P_ ( _x_ ) _âˆ’_ 1 _| â‰¤ Ïµ, âˆ€x âˆˆ_ [0 _, Î»[â‹†] /_ 2] _and |P_ ( _x_ ) + 1 _| â‰¤ Ïµ, âˆ€x âˆˆ_ [ _Î»[â‹†] ,_ 1] _._ 

## **2. Quantum oracle sketching for IID data** 

We introduce quantum oracle sketching starting from the simplest case of learning properties of an unknown Boolean function based on its random data samples. Let _f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ be a Boolean function. Let _p_ : [ _N_ ] _â†’_ R be a probability distribution over [ _N_ ]. We show how to construct the phase oracle 

**==> picture [293 x 30] intentionally omitted <==**

to _Ïµ_ -error in diamond distance given a sequence of data ( _xi, yi_ ) _iâˆˆ_ N, where _xi_ â€™s are sampled IID from _p_ ( _x_ ) and _yi_ = _f_ ( _xi_ ). 

In Algorithm 1, we give the simplest version of quantum oracle sketching that constructs 

**==> picture [302 x 30] intentionally omitted <==**

for arbitrary evolution time _t â‰¥_ 0. When the data distribution is uniform _p_ ( _x_ ) = 1 _/N_ , we take _t_ = _NÏ€_ and obtain _U_ ( _NÏ€_ ) = _O_ =[ï¿½] _x_[(] _[âˆ’]_[1)] _[f]_[(] _[x]_[)] _[ |][x][âŸ©âŸ¨][x][|]_[.] 

**Algorithm 1** Quantum oracle sketching 

**Input:** An input state _Ï âˆˆ_ C _[N][Ã—][N]_ ; a stream of _M_ data samples ( _xi, yi_ ) _i[M]_ =1[,][where] _[x][i][âˆ¼][p]_[(] _[x]_[)][and] _[y][i]_[=] _[f]_[(] _[x][i]_[)][for][some] probability distribution _p_ : [ _N_ ] _â†’_ R _â‰¥_ 0 and Boolean function _f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ ; _t â‰¥_ 0. **Output:** An output state _Mi_ =1 _[V][i] Ï Mi_ =1 _[V][i] â€ _ . ï¿½ï¿½ ï¿½ ï¿½ï¿½ ï¿½ 1: **for** _i_ = 1 _, . . . , M_ **do** 2: Get a data sample ( _xi, yi_ ) from the stream. 3: Apply the multi-controlled phase gate _Vi_ = _e[ity][i][/M][|][x][i][âŸ©âŸ¨][x][i][|]_ . 4: **end for** 

Quantum oracle sketching in this case is very simple. Upon seeing a data point ( _xi, yi_ ), we apply a small, incremental quantum rotation, which is a multi-controlled phase gate 

**==> picture [295 x 19] intentionally omitted <==**

and repeat for all the _M_ data points. We call this sequence of gates ( _V_ 1 _, . . . , VM_ ) the quantum oracle sketch of the classical data ( _xi, yi_ ) _, i_ = 1 _, . . . , M_ . These gates are applied on the fly. That means we never store these data points after the corresponding gate application so as to minimize memory consumption. If we want to query _U_ ( _t_ ) again, we simply collect a fresh set of data samples and run Algorithm 1 again. In this case, the number of qubits used is only _âŒˆ_ log2( _N_ ) _âŒ‰_ , whereas any QRAM based algorithm stores the whole dataset and hence uses _O_ ( _N_ ) memory. 

_a. The apparent trap of decoherence_ 

This idea of applying incremental quantum rotations based on data samples naturally resembles the classical incremental updates in streaming algorithms that bypass the need to store the entire dataset. However, the 

39 

coherence requirement of quantum computation seems to immediately rule out its plausibility: the randomness and entropy in the data are continuously pumped into the quantum machine, causing it to decohere quickly. This intuition is quantitatively confirmed by the error and sample complexity analysis presented below. In particular, we will see that an analysis applicable to generic quantum rotations leads to decoherence and gives performance with no advantage over classical algorithms. This means that the decoherence trap is real and we have to carefully design the quantum rotations for any quantum advantage to be possible. In Theorem D.12, we will use the intuition provided by this failed analysis to develop a variance analysis technique that gives the optimal sample complexity and quantum advantage. 

When the quantum rotations are generic, the process of quantum oracle sketching resembles the qDrift method of Hamiltonian simulation [85], in which one randomly samples a term in the Hamiltonian and apply a short-time evolution generated by that term. In the following, we show that the optimal qDrift analysis gives a sample complexity bound that is far too bad for any meaningful quantum advantage to exist. 

More precisely, in the usual qDrift setting, we aim to simulate the time evolution _e[iHt]_ of some target Hamiltonian _H_ =[ï¿½] _x[p]_[(] _[x]_[)] _[h][x]_[where][each][term] _[h][x]_[has][constant][norm.][In][the][case][of][quantum][oracle][sketching,][we] have _hx_ = _f_ ( _x_ ) _|xâŸ©âŸ¨x|_ and _âˆ¥hxâˆ¥â‰¤_ 1. The total interaction strength _Î»_ =[ï¿½] _x[p]_[(] _[x]_[)] _[âˆ¥][h][x][âˆ¥]_[=][1.][The][idea][of][qDrift] is to sample _M_ random terms of the Hamiltonian _hx_ 1 _, . . . , hxM_ according to the distribution _xi âˆ¼ p_ ( _x_ ) and apply the corresponding single-term time evolution _e[iÎ»th][xi][/M]_ = _e[itf]_[(] _[x][i]_[)] _[/M][|][x][i][âŸ©âŸ¨][x][i][|]_ , which exactly concides with the procedure of quantum oracle sketching in this case. Using the standard gate complexity bound for qDrift, we obtain the sample complexity bound Theorem D.10. Note that if we take _p_ ( _x_ ) = 1 _/N_ and _t_ = _NÏ€_ to build a single query to the phase oracle, this bound gives us a sample complexity of _M_ = _O_ ( _N_[2] ), which is quadratic in _N_ and thus provides no quantum advantage. 

To see that this offers no advantage over classical algorithms, we consider the sample complexity of classical algorithms when their memory is limited. As one extreme, if the classical algorithm has _SC_ = _O_ ( _N_ ) memory, it can store the entire data set using _MC_ = _O_ ( _N_ ) samples and build a complete description of the function, which allows it to estimate any property of the function. The other extreme is when the classical algorithm has little memory _SC_ = _O_ (1), it can still obtain the information of any query it wants by waiting for _O_[Ëœ] ( _N_ ) samples to get lucky. Since any property of a Boolean function can be decided with at most _N_ queries, this classical algorithm can solve any problem using _MC_ = _N Â· O_[Ëœ] ( _N_ ) samples and _SC_ = _O_ (1) memory. In fact, in Section E, we will prove that for a classical algorithm to solve generic query problems, these two extreme cases are connected by a sample-space lower bound _MCSC â‰¥_ â„¦( _N_[2] ). 

This means that if our quantum algorithm consumes _O_ ( _N_[2] ) samples to make a single query, a classical machine can already solve any query problem with the same number of samples and little memory. However, if we only use _O_ ( _N_ ) samples, then the error given in Theorem D.10 will be large, signifying decoherence. In fact, Refs. [86, 87] proves that this sample complexity bound in Theorem D.10 is already optimal and cannot be improved for generic Hamiltonians. In other words, decoherence is inevitable in general. 

**Lemma D.10** (Sample complexity upper bound via qDrift) **.** _Let t â‰¥_ 1 _,_ 0 _< Ïµ â‰¤_ 1 _. Let f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _} be a Boolean function and p_ : [ _N_ ] _â†’_ R _â‰¥_ 0 _be a probability distribution. Let_ ( _xi, yi_ ) _[M] i_ =1 _[be][a][sequence][of][IID][data] samples where xi âˆ¼ p_ ( _x_ ) _and yi_ = _f_ ( _xi_ ) _. Let Vi_ = _e[ity][i][/M][|][x][i][âŸ©âŸ¨][x][i][|] and U_ =[ï¿½] _x[e][ip]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[t][ |][x][âŸ©âŸ¨][x][|][.][Then,]_ 

**==> picture [263 x 22] intentionally omitted <==**

_samples suffice to guarantee that_ 

**==> picture [296 x 11] intentionally omitted <==**

_where Vi_ : _Ï â†’ ViÏVi[â€ ][and][U]_[:] _[ Ï][ â†’][UÏU][ â€ ][are][the][corresponding][unitary][channels.]_ 

_Proof of Theorem D.10._ Let _Ïµ âˆˆ_ (0 _,_ 1] and _t â‰¥_ 1. Let _hx_ = _f_ ( _x_ ) _|xâŸ©âŸ¨x|_ . Since the samples are IID, we have 

**==> picture [324 x 12] intentionally omitted <==**

where _E_ 0 is the average channel of a single sample: 

**==> picture [381 x 30] intentionally omitted <==**

Here, we have defined _Lx_ ( _Ï_ ) = [ _hx, Ï_ ] with _âˆ¥Lxâˆ¥â‹„ â‰¤_ 2 _âˆ¥hxâˆ¥â‰¤_ 2. On the other hand, the target unitary we want to implement is 

**==> picture [358 x 22] intentionally omitted <==**

40 

where _H_ =[ï¿½] _x[p]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[ |][x][âŸ©âŸ¨][x][|]_[ =][ ï¿½] _x[p]_[(] _[x]_[)] _[h][x]_[.][Its action can be divided into] _[ M]_[repetition of the unitary channel] 

**==> picture [364 x 30] intentionally omitted <==**

where _U_ 0 = _e[itH/M] , L_ ( _Ï_ ) = [ _H, Ï_ ] with _âˆ¥Lâˆ¥â‹„ â‰¤_ 2 _âˆ¥Hâˆ¥â‰¤_ 2. Note that 

**==> picture [330 x 31] intentionally omitted <==**

The diamond distance between the single-sample channels reads 

**==> picture [423 x 245] intentionally omitted <==**

From the subadditivity of diamond distance, the overall distance is bounded by 

**==> picture [385 x 23] intentionally omitted <==**

To get an _Ïµ_ error, we choose _M â‰¥_ 8 _t_[2] _/Ïµ_ and obtain 

**==> picture [340 x 23] intentionally omitted <==**

where we have used _Ïµ â‰¤_ 1 and _t â‰¥_ 1. This completes the proof of Theorem D.10. 

## _b. Evading decoherence_ 

As we have seen, the qDrift bound in Theorem D.10 gives us an undesirable sample complexity of _O_ ( _N_[2] ) when _p_ ( _x_ ) = 1 _/N_ and _t_ = _NÏ€_ . This signifies the inevitable decoherence for generic quantum rotations. 

The mathematical origin of this decoherence is that in our case the total interaction strength _Î»_ = 1 and thus the qDrift bound yields _O_ ( _Î»_[2] _t_[2] _/Ïµ_ ) = _O_ ( _t_[2] _/Ïµ_ ) = _O_ ( _N_[2] _/Ïµ_ ). For general randomized Hamiltonian simulation problems, this bound is already optimal [86, 87]. The reason is that the total interaction strength characterizes the average effect of randomly sampling Hamiltonian terms, and the random samples are all that we have. To go beyond this analysis, we have to carefully design the Hamiltonians and exploit their features, so that we can bypass this average effect. 

The first idea that helps to go beyond this average effect is to note that our Hamiltonian terms are all diagonal in the computational basis _hx_ = _f_ ( _x_ ) _|xâŸ©âŸ¨x|_ , and they are orthogonal to each other. Intuitively, as the number of samples increases, the phase accumulated on each basis _|xâŸ©_ does not interfere with each other and should accumulate by themselves, following a binomial distribution with _M_ repetitions and probability _p_ ( _x_ ). 

41 

From standard concentration inequalities, this phase should concentrate to _Ïµ_ error with a number of samples _Mx_ = _O_ ( _p_ ( _x_ ) _t_[2] _/Ïµ_[2] ). Let _p_ max = max _x p_ ( _x_ ). A union bound then implies that _M_ = _O_ ( _p_ max _t_[2] log _N/Ïµ_[2] ) suffice to _Ïµ_ -approximate _U_ ( _t_ ) in operator norm with high probability. When _p_ ( _x_ ) = 1 _/N_ and _t_ = _NÏ€_ , this analysis gives a sample complexity of _M_ = _O_ ( _N_ log _N/Ïµ_ ), which bypasses the _O_ ( _N_[2] ) barrier for generic Hamiltonians. 

**Lemma D.11** (Sample complexity upper bound via concentration) **.** _Let t >_ 0 _,_ 0 _< Ïµ, Î´ <_ 1 _. Let f_ : [ _N_ ] _â†’ {_ 0 _,_ 1 _} be a Boolean function and p_ : [ _N_ ] _â†’_ R _â‰¥_ 0 _be a probability distribution. Let p_ max = max _xâˆˆ_ [ _N_ ] _p_ ( _x_ ) _. Let_ ( _xi, yi_ ) _[M] i_ =1 _[be][a][sequence][of][IID][data][samples][where][x][i][âˆ¼][p]_[(] _[x]_[)] _[and][y][i]_[=] _[f]_[(] _[x][i]_[)] _[.][Let][V][i]_[=] _[e][ity][i][/M][|][x][i][âŸ©âŸ¨][x][i][|][and] U_ =[ï¿½] _x[e][ip]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[t][ |][x][âŸ©âŸ¨][x][|][.][Then,]_ 

**==> picture [295 x 23] intentionally omitted <==**

_samples suffice to guarantee that, with probability at least_ 1 _âˆ’ Î´, we have_ 

**==> picture [290 x 11] intentionally omitted <==**

_where Vi_ : _Ï â†’ ViÏVi[â€ ][and][U]_[:] _[ Ï][ â†’][UÏU][ â€ ][are][the][corresponding][unitary][channels.] Proof of Theorem D.11._ For any _x âˆˆ_ [ _N_ ], define _mx_ =[ï¿½] _[M] i_ =1 _[Î´][x,x] i_[to][be][the][number][of][samples] _[x][i]_[that][is][equal] to _x_ . Then the constructed unitary is 

**==> picture [329 x 22] intentionally omitted <==**

We aim to show that _V_ approximates _U_ =[ï¿½] _x[e][ip]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[t][ |][x][âŸ©âŸ¨][x][|]_[with][high][probability.] To this end, we note that _mx_ follows a binomial distribution with _M_ repetitions and probability _p_ ( _x_ ). Therefore, it has mean E[ _mx_ ] = _Mp_ ( _x_ ) and the standard Chernoff bound yields that for any _Ïµ_ 1 _âˆˆ_ (0 _,_ 1), 

**==> picture [324 x 25] intentionally omitted <==**

Let _Ïµ_ 1 = _Ïµ/_ (2 _tp_ ( _x_ )). We have 

**==> picture [329 x 25] intentionally omitted <==**

Since _M â‰¥[p]_[max] _Ïµ_[2] _[t]_[2] _Â·_ 12 log[2] _Î´[N]_[,][we][have][that][for][any][given] _[x][ âˆˆ]_[[] _[N]_[],] 

**==> picture [312 x 25] intentionally omitted <==**

Therefore, the union bound implies that with probability at least 1 _âˆ’ Î´_ , 

**==> picture [371 x 26] intentionally omitted <==**

This implies that 

**==> picture [358 x 108] intentionally omitted <==**

where we have used _|_ sin( _z_ ) _| â‰¤ z, âˆ€z >_ 0. Theorem D.1 then yields the desired result: 

**==> picture [318 x 10] intentionally omitted <==**

with probability at least 1 _âˆ’ Î´_ . 

42 

When _p_ ( _x_ ) = 1 _/N_ and _t_ = _NÏ€_ , the sample complexity in Theorem D.11 gives us a _O_ ( _N_ log _N/Ïµ_[2] ) scaling that is better than the _O_ ( _N_[2] _/Ïµ_ ) from Theorem D.10 in terms of _N_ , but not in _Ïµ_ . The scaling exponent in _Ïµ_ significantly impacts the sample efficiency when we make multiple queries to the constructed oracle. For example, when we have a query algorithm with query complexity _Q_ . In order to get a final error _Ïµ_ , we need the error in each oracle to be bounded by _Ïµ/Q_ . Since we are sampling fresh data each time we query, the total sample complexity is 

**==> picture [309 x 25] intentionally omitted <==**

incurring a cubic slowdown in _Q_ . But if the scaling is 1 _/Ïµ_ instead of 1 _/Ïµ_[2] , there will only be a quadratic slowdown in _Q_ . As we will see in Section E, this also makes the desired space complexity separation harder to achieve. 

In the following, we introduce a second idea that improves on the _Ïµ_ dependence. The key is to give up on having a worst-case error bound as in Theorem D.11, and instead only demand the random unitary channel to be close to the target in expectation as in Theorem D.10. This leads to a quadratic suppression of error known as mixing in the literature [86, 170]. However, we need to bound the error more carefully in order to recover the _p_ max factor, which is crucial in bypassing _O_ ( _N_[2] ) to reach _O_ ( _N_ ). 

**Theorem D.12** (Quantum oracle sketching for IID data) **.** _Let t, Ïµ >_ 0 _. Let f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _} be a Boolean function and p_ : [ _N_ ] _â†’_ R _â‰¥_ 0 _be a probability distribution. Let p_ max = max _xâˆˆ_ [ _N_ ] _p_ ( _x_ ) _. Let_ ( _xi, yi_ ) _[M] i_ =1 _[be][a][sequence][of][IID][data][samples][where][x][i][âˆ¼][p]_[(] _[x]_[)] _[and][y][i]_[=] _[ f]_[(] _[x][i]_[)] _[.][Let][V][i]_[=] _[ e][ity][i][/M][|][x][i][âŸ©âŸ¨][x][i][|][and] U_ =[ï¿½] _x[e][ip]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[t][ |][x][âŸ©âŸ¨][x][|][.][Then,]_ 

**==> picture [257 x 23] intentionally omitted <==**

_samples suffice to guarantee that_ 

**==> picture [280 x 11] intentionally omitted <==**

_where Vi_ : _Ï â†’ ViÏVi[â€ ][and][U]_[:] _[Ï][â†’][UÏU][ â€ ][are][the][corresponding][unitary][channels.][The][data][processing] time per sample is O_ (log _N_ ) _._ 

_Proof of Theorem D.12._ Let _hx_ = _f_ ( _x_ ) _|xâŸ©âŸ¨x|_ . Then we have _Vi_ = _e[ith][xi][/M]_ and _U_ = _e[it]_[E] _[x]_[[] _[h][x]_[]] , where _x âˆ¼ p_ ( _x_ ). The gate complexity of each _Vi_ is _O_ (log _N_ ). Let 

**==> picture [282 x 30] intentionally omitted <==**

be the empirical frequency of a given _x_ appearing in the data. Note that since the _hx_ â€™s are orthogonal and commute with each other, we have 

**==> picture [330 x 30] intentionally omitted <==**

From Theorem D.2, we have 

**==> picture [406 x 21] intentionally omitted <==**

_M_ Let _X_ = _t M_[1] ï¿½ _i_ =1 _[h][x] i_[=] _[ t]_[ ï¿½] _x[m][x][h][x]_[be][the][random][matrix][in][the][exponent.][Note][that][the][linearity][of][expecta-] tion implies 

**==> picture [352 x 30] intentionally omitted <==**

where we have used the fact that the marginal distribution of each individual _xi_ is the same _x âˆ¼ p_ ( _x_ ). Note 

43 

also that the _X_ and E[ _X_ ] matrices are all diagonal matrices, so they commute with each other. Thus we have 

**==> picture [472 x 131] intentionally omitted <==**

**==> picture [471 x 23] intentionally omitted <==**

where we have used the triangle inequality, the inequality that _|e[iw] âˆ’ iw âˆ’_ 1 _| â‰¤ w_[2] _/_ 2 _, âˆ€w âˆˆ_ R, and _{|xâŸ©}_ being orthonormal bases. Note that this essentially reproves Theorem D.7, but we include it to highlight how the diagonal structure helps avoid the averaging effect in the usual qDrift analysis. 

Since the samples are IID, we have the variance 

**==> picture [416 x 30] intentionally omitted <==**

where we have used _Î´x,xi_ being a Bernoulli variable with probability _p_ ( _x_ ). Plugging the variance bound back in, we arrive at 

**==> picture [354 x 23] intentionally omitted <==**

Choosing 

**==> picture [274 x 23] intentionally omitted <==**

we have _âˆ¥_ E[ _VM Â· Â· Â· V_ 1] _âˆ’Uâˆ¥â‹„ â‰¤ Ïµ_ . This concludes the proof of Theorem D.12. 

We remark that here we circumvent the averaging effect in the usual qDrift analysis by taking advantage of the fact that different _hx_ are orthogonal to each other, similar to Theorem D.11. This allows us to explicitly bound the operator norm by the maximum variance of _mx_ , which gives us the _p_ max factor. Otherwise, all we can do is to use _âˆ¥_ E[ _Â·_ ] _âˆ¥â‰¤_ E[ _âˆ¥Â· âˆ¥_ ] which will lead to the _Î»_ =[ï¿½] _x[p]_[(] _[x]_[) = 1][factor][in][the][usual][qDrift][analysis][and] a final _O_ ( _t_[2] _/Ïµ_ ) sample complexity as in Theorem D.10. 

Using Theorem D.12, we can instantiate the quantum oracle queries in a query algorithm using a sequence of classical data samples. In particular, we have the following result. 

**Theorem D.13** (Query algorithms with quantum oracle sketching) **.** _There is a classical algorithm that, for any Boolean function f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _} and probability distribution p_ : [ _N_ ] _â†’_ R _â‰¥_ 0 _with p_ max = max _xâˆˆ_ [ _N_ ] _p_ ( _x_ ) _, any t, Ïµ >_ 0 _, takes as input any quantum query algorithm A that queries U_ =[ï¿½] _x[e][ip]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[t][ |][x][âŸ©âŸ¨][x][|][ , U][ â€ ][, cU]_[=] _[|]_[0] _[âŸ©âŸ¨]_[0] _[| âŠ—][I]_[+] _[ |]_[1] _[âŸ©âŸ¨]_[1] _[| âŠ—][U][,][or][cU][â€ ][in][total][Q][times,][and][outputs][a] quantum learning algorithm A[â€²] with sample complexity_ 

**==> picture [311 x 26] intentionally omitted <==**

_and input form I_ = [ _N_ ] _Ã—{_ 0 _,_ 1 _}. Upon receiving IID data samples of the form_ ( _xi, yi_ ) _[M] i_ =1 _[where][x][i][âˆ¼][p]_[(] _[x]_[)] _and yi_ = _f_ ( _xi_ ) _, the quantum learning algorithm A[â€²] satisfies_ 

**==> picture [266 x 12] intentionally omitted <==**

_where the expectation is over random data samples. Meanwhile, the space complexity of A[â€²] is the same as that of A and the data processing time of A[â€²] is bounded by the time complexity of A._ 

44 

_Proof of Theorem D.13._ We prove Theorem D.13 by explicitly constructing the algorithm _A[â€²]_ using Algorithm 1. For any unitary _U âˆˆ U_ ( _N_ ), we use _U_ : _Ï â†’ UÏU[â€ ]_ to denote its corresponding unitary channel. We use _cU_ : _Ï â†’ cUÏ_ ( _cU_ ) _[â€ ]_ to denote the unitary channel of the controlled unitary. Let _A_ = _CQUQ Â· Â· Â· C_ 1 _U_ 1 _C_ 0 be the quantum channel of the quantum query algorithm with query complexity _Q_ , where _C_ 1 _, . . . , CQ_ are fixed quantum channels and _U_ 1 _, . . . , UQ âˆˆ{U, U[â€ ] , cU, cU[â€ ] }_ . Theorem D.12 implies that we can use _M_ 0 = ï¿½2 _p_ max _t_[2] _/Ïµ_ 1ï¿½ samples to construct a random unitary _V âˆˆ U_ ( _N_ ) by Algorithm 1 such that 

**==> picture [282 x 11] intentionally omitted <==**

where _V_ : _Ï â†’ V ÏV[â€ ]_ is the unitary channel corresponding to _V_ . Similarly, by changing the random unitary in Algorithm 1 to its controlled version or replace _t_ by _âˆ’t_ , we can implement _U[â€ ] , cU, cU[â€ ]_ to _Ïµ_ 1 error using the same number of samples as well. 

We construct _A[â€²]_ as follows. We draw _M_ = _QM_ 0 samples from the data stream and use Algorithm 1 to construct _V_ 1 _, . . . , VQ âˆˆ U_ ( _N_ ). Theorem D.12 guarantees that _âˆ¥_ E[ _Vi_ ] _âˆ’Uiâˆ¥â‹„ â‰¤ Ïµ_ 1 for any _i âˆˆ_ [ _Q_ ]. We define 

**==> picture [291 x 12] intentionally omitted <==**

By construction, the space complexity of _A[â€²]_ is the same as that of _A[â€²]_ . Since _V_ 1 _, . . . , VQ_ are independent because the data samples are, we have 

**==> picture [374 x 61] intentionally omitted <==**

where we have used Theorem D.3. Let _Ïµ_ 1 = _Ïµ/Q_ , then we arrive at 

**==> picture [280 x 11] intentionally omitted <==**

with 

**==> picture [342 x 25] intentionally omitted <==**

This concludes the proof of Theorem D.13. 

## **3. Optimality** 

In Theorem D.13, we have shown that we can execute any quantum query algorithm with query complexity _Q_ by performing quantum oracle sketching using classical data samples on each query. The total number of samples has at most a quadratic slow down _âˆ¼ Q_[2] . A natural question is whether we can further improve this to linear in _Q_ and if the dependence on other parameters is tight. One may think that it could be possible to use a â€œhigher-orderâ€ version of qDrift to improve the scaling [176]. Yet in the following, we show that this is impossible, which also implies that the method developed in [176] does not support sequential queries to the simulated Hamiltonian evolution. 

In particular, we show in Theorem D.14 that the sample complexity given in Theorem D.13 is tight and the quadratic slow down is necessary. This quadratic slow down is fundamentally tied to the incoherent random sampling access to data that we have. 

We also note that the assumption _p_ max _tQ â‰¥_ 8 _Ï€Ïµ_ in Theorem D.14 is indispensable. If instead _p_ max _tQ <_ 8 _Ï€Ïµ_ , then we can always draw no sample at all and replace every query to _U_ by the identity. The resulting error is bounded by _O_ ( _âˆ¥U âˆ’ Iâˆ¥Â· Q_ ) _â‰¤ O_ ( _p_ max _tQ_ ) _â‰¤ O_ ( _Ïµ_ ). In other words, in this case there is always an algorithm that achieves the goal without using any samples. 

45 

**Theorem D.14** (Quantum oracle sketching is sample optimal) **.** _Let t >_ 0 _, Ïµ âˆˆ_ (0 _,_ 1 _/_ 12) _. Suppose there is a (possibly quantum) algorithm that, for any Boolean function f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _} and probability distribution p_ : [ _N_ ] _â†’_ R _â‰¥_ 0 _with p_ max = max _xâˆˆ_ [ _N_ ] _p_ ( _x_ ) _, takes any quantum query algorithm A that queries U_ =[ï¿½] _x[e][ip]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[t][ |][x][âŸ©âŸ¨][x][|][in][total][Q][times,][and][outputs][a][quantum][learning][algorithm][A][â€²][with][input][form] I_ = [ _N_ ] _Ã— {_ 0 _,_ 1 _} such that_ 

**==> picture [264 x 12] intentionally omitted <==**

_upon receiving M IID data samples_ ( _xi, yi_ ) _[M] i_ =1 _[where][x][i][âˆ¼][p]_[(] _[x]_[)] _[and][y][i]_[=] _[f]_[(] _[x][i]_[)] _[.][Suppose][p]_[max] _[tQ][â‰¥]_[8] _[Ï€Ïµ][,] then we must have_ 

**==> picture [274 x 25] intentionally omitted <==**

_Proof of Theorem D.14._ We use _M_ ( _t, Q, Ïµ_ ) to denote the sample complexity. We prove Theorem D.14 by connecting the task of oracle construction to the task of quantum state discrimination. We show that the oracle construction algorithm described in Theorem D.14 can be used to distinguish two different quantum states using _M_ copies of the states. Then a sample complexity lower bound for quantum state discrimination translates into the desired sample complexity bound for oracle construction. 

In particular, we note that drawing _M_ samples from the distribution _p_ ( _x_ ) is weaker than having access to _M_ copies of the diagonal state _Ï_ =[ï¿½] _x[p]_[(] _[x]_[)] _[ |][x][âŸ©âŸ¨][x][|]_[.][Choose] _[p]_[max] _[â‰¥]_[2] _[/N]_[.][Let] _[K]_[=] _[âŒˆ]_[2] _[/p]_[max] _[âŒ‰âˆˆ]_[[2] _[, N]_[]][and] _p_ = 1 _/K_ . Note that _p_ = 1 _/K â‰¤ p_ max _/_ 2 _< p_ max and _p_ = 1 _/K â‰¥_ 1 _/_ (2 _/p_ max + 1) = _p_ max _/_ ( _p_ max + 2) _â‰¥ p_ max _/_ 3. Let _Î³_ = _Ï€/_ (2 _tQ_ ). We first assume that _tQ â‰¥_ 2 _Ï€/p_ max such that _Î³ â‰¤ p_ max _/_ 4 and hence _p_ + _Î³ â‰¤_ 3 _p_ max _/_ 4. We consider the following two states: 

**==> picture [319 x 30] intentionally omitted <==**

and 

**==> picture [391 x 30] intentionally omitted <==**

Indeed, we have max _x p_ 1( _x_ ) = _p < p_ max and max _x p_ 2( _x_ ) = _p_ + _Î³ â‰¤ p_ max. The relative entropy between _Ï_ 1 _, Ï_ 2 is 

**==> picture [398 x 25] intentionally omitted <==**

where we have used the inequality log(1 _/_ (1 _âˆ’ z_ )) _â‰¤_ 1 _._ 5 _z/_ (1 _âˆ’ z_ ) _, âˆ€z âˆˆ_ [0 _,_ 1). Suppose we have _M_ 0 copies of either _Ï_ 1 or _Ï_ 2 and we want to distinguish the two cases with success probability at least 2 _/_ 3. Theorem D.4 and the operational meaning of trace distance then implies that 

**==> picture [413 x 23] intentionally omitted <==**

Therefore, we have 

**==> picture [431 x 26] intentionally omitted <==**

where we have used _Î³/p â‰¤_ ( _p_ max _/_ 4) _/_ ( _p_ max _/_ 3) = 3 _/_ 4. Since _p â‰¥ p_ max _/_ 3 and _Î³_ = _Ï€/_ (2 _tQ_ ), we arrive at 

**==> picture [294 x 23] intentionally omitted <==**

In other words, we have proved that if _tQ â‰¥_ 2 _Ï€/p_ max, then any algorithm that can distinguish _Ï_ 1 and _Ï_ 2 with success probability at least 2 _/_ 3 must use _M_ 0 samples. 

Now we construct an algorithm to distinguish _Ï_ 1 and _Ï_ 2 using the oracle construction algorithm in Theorem D.14. This resembles the idea used in proving the sample complexity lower bound of quantum principle component analysis [87]. We first let _Ïµ_ = 1 _/_ 3. Let _|_ + _âŸ©_ = ( _|_ 1 _âŸ©_ + _|_ 2 _âŸ©_ ) _/âˆš_ 2 and _|âˆ’âŸ©_ = ( _|_ 1 _âŸ©âˆ’|_ 2 _âŸ©_ ) _/âˆš_ 2. Specifically, we set the query algorithm _A_ to be the simple algorithm that prepares the initial state _|_ + _âŸ©_ , applies _U_ consecutively 

46 

_Q_ times, and perform the two-outcome measurements _{_ Î 0 = _|_ + _âŸ©âŸ¨_ + _| ,_ Î 1 = _I âˆ’_ Î 0 _}_ . If the state that generates the data stream is _Ï_ 1, then 

**==> picture [345 x 23] intentionally omitted <==**

Thus _A_ will output 0 with certainty. On the other hand, if the state that generates the data stream is _Ï_ 2, then 

**==> picture [460 x 23] intentionally omitted <==**

which is orthogonal to _|_ + _âŸ©_ . Hence _A_ will output 1 with certainty. That is, _A_ can distinguish _Ï_ 1 and _Ï_ 2 with certainty. Meanwhile, the oracle construction algorithm in Theorem D.14 uses _M_ ( _t, Q,_ 1 _/_ 3) samples and gives us a an algorithm _A[â€²]_ such that _âˆ¥_ E[ _A[â€²]_ ] _âˆ’Aâˆ¥â‹„ â‰¤_ 1 _/_ 3. Since the output of _A_ is a random bitstring, the diamond norm reduces to the total variation distance of the distributions of the outputs. This implies that _A[â€²]_ can distinguish _Ï_ 1 and _Ï_ 2 with probability at least 2 _/_ 3. Therefore, we must have 

**==> picture [327 x 24] intentionally omitted <==**

if _tQ â‰¥_ 2 _Ï€/p_ max. 

For general _t, Q, Ïµ_ , recall that we have _p_ max _tQ/Ïµ â‰¥_ 8 _Ï€_ . Note that 

**==> picture [301 x 11] intentionally omitted <==**

for any positive integer _k_ , because we can always construct _kQ_ queries to _U_ with error _kÏµ_ by constructing _k_ chunks of _Q_ queries to _U_ with error _Ïµ_ . Therefore, taking _k_ = _âŒŠ_ 1 _/_ (3 _Ïµ_ ) _âŒ‹_ and using the fact that _M_ ( _t, Q, Ïµ_ ) decreases with _Ïµ_ , we have 

**==> picture [458 x 23] intentionally omitted <==**

where we have used that _k â‰¥_ 1 _/_ (3 _Ïµ_ ) _âˆ’_ 1 _â‰¥_ 1 _/_ (4 _Ïµ_ ) when _Ïµ <_ 1 _/_ 12 and _tkQ â‰¥ tQ/_ (4 _Ïµ_ ) _â‰¥_ 2 _Ï€/p_ max so that we can apply Equation (D84). This completes the proof of Theorem D.14. 

## **4. Extensions** 

We have shown how to quantum oracle sketching to construct a unitary _U_ ( _t_ ) =[ï¿½] _x[e][ip]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[t][ |][x][âŸ©âŸ¨][x][|]_[from][a] sequence of random data samples ( _xi, f_ ( _xi_ )) where _xi âˆ¼ p_ ( _x_ ) and _f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ . When the data distribution is uniform _p_ ( _x_ ) = 1 _/N_ , the _t_ = _NÏ€_ unitary _U_ ( _NÏ€_ ) gives the desired phase oracle _O_ =[ï¿½] _x_[(] _[âˆ’]_[1)] _[f]_[(] _[x]_[)] _[ |][x][âŸ©âŸ¨][x][|]_[.][We] have also shown that the sample complexity for querying this oracle _Q_ times is 

**==> picture [321 x 25] intentionally omitted <==**

In this section, we discuss several extensions to this simplest version of quantum oracle sketching. We first study the cases when we have multi-bit outputs _f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}[b]_ , when the data are non-IID and generated from a general hierarchical data generation process with multiple time scales, and when the underlying distribution is non-uniform and unknown. 

## _a. Multi-bit output_ 

We first generalize quantum oracle sketching to handle multi-bit outputs. Let _b_ be the length of the output bitstrings. We assume that the data samples are of the form ( _xi, yi_ ) with _yi_ = _f_ ( _xi_ ) _, f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}[b]_ . There are many equivalent ways to define oracles for functions with multi-bit outputs (e.g., the standard XOR oracle that operates on log _N_ + _b_ qubits and maps _|xâŸ©|yâŸ©_ to _|xâŸ©|y âŠ• f_ ( _x_ ) _âŸ©_ ). For our purposes, we aim to minimize the space overhead, and therefore we consider the multi-bit phase oracle 

**==> picture [345 x 13] intentionally omitted <==**

that operates on log _N_ + log _b_ qubits. 

47 

One can equivalently consider the Boolean function 

**==> picture [347 x 14] intentionally omitted <==**

whose standard phase oracle is 

**==> picture [323 x 15] intentionally omitted <==**

which is the same as the multi-bit phase oracle of _f_ . This identification immediately implies a (sample wasteful) way of using Algorithm 1 to construct the multi-bit phase oracle: we simply subsample each data point ( _xi, yi_ ) with a single uniformly random coordinate _j âˆˆ_ [ _b_ ]. This is the same as sampling random ( _z_ = ( _x, j_ ) _, f_[Ë†] ( _z_ )). This enlarges the domain from [ _N_ ] to [ _N_ ] _Ã—_ [ _b_ ]. Theorem D.12 then shows that when _p_ ( _x_ ) = 1 _/N_ is uniform, _p_ ( _z_ ) = 1 _/_ ( _bN_ ) and we can construct the desired oracle using _O_ ( _bN/Ïµ_ ) samples. Here, the additional factor _b_ comes from the fact that due to our wasteful use of each sample, we need _b_ samples to gather all the coordinates of each _y âˆˆ{_ 0 _,_ 1 _}[b]_ . Nevertheless, as long as _b_ = polylog( _N_ ), this sampling overhead is still tolerable. 

**Algorithm 2** Quantum oracle construction (multi-bit version) 

**Input:** An input state _Ï âˆˆ_ C[(] _[N][Ã—][b]_[)] _[Ã—]_[(] _[N][Ã—][b]_[)] ; a stream of _M_ data samples ( _xi, yi_ ) _i[M]_ =1[,][where] _[x][i][âˆ¼][p]_[(] _[x]_[)][and] _[y][i]_[=] _[f]_[(] _[x][i]_[)][for] some probability distribution _p_ : [ _N_ ] _â†’_ R _â‰¥_ 0 and function _f_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}[b] , b âˆˆ_ Z _â‰¥_ 1; _t â‰¥_ 0. **Output:** An output state _Mi_ =1 _[V][i] Ï Mi_ =1 _[V][i] â€ _ . ï¿½ï¿½ ï¿½ ï¿½ï¿½ ï¿½ 1: **for** _i_ = 1 _, . . . , M_ **do** 2: Get a data sample ( _xi, yi_ ) from the stream. 3: **for** _j_ = 1 _, . . . , b_ **do** 4: Apply the multi-controlled phase gate _Vi_ = _e[it]_[(] _[y][i]_[)] _[j][/M][|][x][i][âŸ©âŸ¨][x][i][|âŠ—|][j][âŸ©âŸ¨][j][|]_ . 5: **end for** 6: **end for** 

Algorithm 2 further improves the sample complexity by making use of more information in each sample. Theorem D.15 shows that Algorithm 2 has no sampling overhead compared to the single-bit output case. In particular, when _p_ ( _x_ ) = 1 _/N_ and _t_ = _NÏ€_ , the sample complexity for constructing the multi-bit phase oracle is still _O_ ( _N/Ïµ_ ). 

**Lemma D.15** (Quantum oracle sketching for multi-bit functions) **.** _Let t, Ïµ >_ 0 _. Let b âˆˆ_ Z _â‰¥_ 1 _Let f_ : [ _N_ ] _â†’ {_ 0 _,_ 1 _}[b] be a function and p_ : [ _N_ ] _â†’_ R _â‰¥_ 0 _be a probability distribution. Let p_ max = max _xâˆˆ_ [ _N_ ] _p_ ( _x_ ) _. Let_ ( _xi, yi_ ) _[M] i_ =1 _be a sequence of IID data samples where xi âˆ¼ p_ ( _x_ ) _and yi_ = _f_ ( _xi_ ) _âˆˆ{_ 0 _,_ 1 _}[b] . Let Vij_ = _e[it]_[(] _[y][i]_[)] _[j][/M][|][x][i][âŸ©âŸ¨][x][i][|âŠ—|][j][âŸ©âŸ¨][j][|] for j âˆˆ_ [ _b_ ] _and let U_ =[ï¿½] _x,j[e][ip]_[(] _[x]_[)] _[f][j]_[(] _[x]_[)] _[t][ |][x, j][âŸ©âŸ¨][x, j][|][.][Then,]_ 

**==> picture [270 x 23] intentionally omitted <==**

_samples suffice to guarantee that_ 

**==> picture [338 x 37] intentionally omitted <==**

_where Vij_ : _Ï â†’ VijÏVij[â€ ][and][U]_[:] _[Ï][â†’][UÏU][ â€ ][are][the][corresponding][unitary][channels.][The][data][processing][time] per sample is_ polylog( _N_ ) _._ 

_Proof of Theorem D.15._ Let _hx,j_ = _fj_ ( _x_ ) _|xâŸ©âŸ¨x|âŠ—|jâŸ©âŸ¨j|_ . Note that since different _hx,j_ commute with each other, we have 

**==> picture [334 x 32] intentionally omitted <==**

Also note that for _x âˆ¼ p_ ( _x_ ), we have E[[ï¿½] _[b] j_ =1 _[h][x,j]_[]][=][ï¿½] _x,j[p]_[(] _[x]_[)] _[f][j]_[(] _[x]_[)] _[ |][x, j][âŸ©âŸ¨][x, j][|]_[and][thus] _[U]_[=] _[e][it]_[E][[][ï¿½] _j[b]_ =1 _[h][x,j]_[]] . Therefore, the rest of the proof follows verbatim as the proof of Theorem D.12 by setting _hx_ =[ï¿½] _[b] j_ =1 _[h][x,j]_[.] 

48 

## _b. Quantum oracle sketching for correlated data_ 

In this section, we generalize quantum oracle sketching to handle correlated data. In particular, we consider general hierarchical data generation processes with multiple time scales described in Section C 1. We will heavily use the statistical properties of data generation processes that we proved in Section C 4. Let 

**==> picture [370 x 13] intentionally omitted <==**

be a hierarchical data generation process. For simplicity, we assume that the data samples are of the form 

**==> picture [339 x 11] intentionally omitted <==**

for some Boolean function _f_ : _X â†’{_ 0 _,_ 1 _}_ . Note that we include all the situations ( _Î±_ 1 _,i, . . . , Î±l,i_ ) inside _xi âˆˆX_ . This easily generalizes to functions with multi-bit output using the techniques from the previous section. Since _z_ and _x_ are in one-to-one correspondence, the repetition number _RD_ defined with respect to _z_ in _D_ is the same as that of _x_ . 

Our goal is to construct the unitary 

**==> picture [300 x 12] intentionally omitted <==**

where _p_ ( _x_ ) is the marginal distribution of _x_ shared by all data samples. However, unlike the IID case, there may be correlation among data mediated by higher levels of the hierarchy. This poses an apparent challenge to the simplest version of quantum oracle sketching described in Algorithm 1. The main obstacle is that when we have already processes some previous data, the posterior/conditional distribution of later data samples shifts. In order for quantum oracle sketching to work, we have to prove two guarantees: (1) after processing previous data samples, the posterior change is not too large such that we can still construct new queries using subsequent data samples; and (2) the errors of multiple queries do not correlate too much so that the total error still accumulates linearly. 

Guarantee (1) is formalized in Theorem D.16, which shows that we can extend quantum oracle sketching to handle any hierarchical data generating process _D_ , with a per-query sample complexity overhead equal to its repetition number _RD_ . This is intuitive, since the more repetitive a data generation process is, the more samples we need to collect to gather enough information. If every sample is repeated _RD_ times, we need _RD_ times as many samples as before. 

It is informative to apply Theorem D.16 to the two examples introduced in Section C 1: the repetitive process _D_ rep and the alternating process _D_ alt. Recall that the repetitive process _D_ rep is defined as 

**==> picture [302 x 12] intentionally omitted <==**

where _D_[0] = Uniform([ _N_ ]) and _Dx_[1][always][outputs][its][label] _[x][âˆˆ]_[[] _[N]_[]][and][repeats][in][total] _[N]_[times.][We][have] refreshing time _Ï„D_ rep = _N_ and repetition number _RD_ rep _â‰¤ N_ . The alternating process is defined as 

**==> picture [301 x 12] intentionally omitted <==**

where _D_[0] = Bern(1 _/_ 2), _Î± âˆˆ{_ 0 _,_ 1 _}_ , and _DÎ±_[1][samples] _[x][ âˆˆ]_[[] _[N]_[]][uniformly][random] _[N]_[times][and][outputs] _[z]_[= (] _[x, Î±]_[).] We still have refreshing time _Ï„D_ alt = _N_ , but the repetition number is _RD_ alt _â‰¤ O_ (1). 

Suppose we fix _t_ = _NÏ€_ as before in Theorem D.16. Then for the alternating process _D_ alt, the oracle can still be constructed using _O_ ( _N/Ïµ_ ) samples since _p_ max = 1 _/_ (2 _N_ ) and _RD_ alt = _O_ (1). In contrast, for the repetitive process _D_ rep, we need _O_ ( _N_[2] _/Ïµ_ ) samples since _p_ max = 1 _/N_ but _RD_ rep = _N_ . This _N_[2] scaling is unavoidable, since we can only get to see all _N_ inputs after â„¦( _N_[2] ) samples in the repetitive process _D_ rep. 

49 

**Theorem D.16** (Quantum oracle sketching for correlated data) **.** _Let t, Ïµ >_ 0 _. Let X be a finite set and let f_ : _X â†’{_ 0 _,_ 1 _} be a Boolean function. Let D be a hierarchical data generation process with repetition number RD that generates a sequence of M data samples zi_ = ( _xi, yi_ ) _where yi_ = _f_ ( _xi_ ) _, i_ = _t_ 0 _, . . . , t_ 0 + _M âˆ’_ 1 _starting from any time step t_ 0 _â‰¥_ 1 _. Let p_ max = max _xâˆˆX p_ ( _x_ ) _where p_ ( _x_ ) _is the marginal distribution of data. Let Vi_ = _e[ity][i][/M][|][x][i][âŸ©âŸ¨][x][i][|] and let U_ =[ï¿½] _x[e][ip]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[t][ |][x][âŸ©âŸ¨][x][|][.][Then,]_ 

**==> picture [296 x 24] intentionally omitted <==**

_samples suffice to guarantee that_ 

**==> picture [346 x 12] intentionally omitted <==**

_where Vi_ : _Ï â†’ ViÏVi[â€ ] and U_ : _Ï â†’ UÏU[â€ ] are the corresponding unitary channels, and z_ 1 _, . . . , zt_ 0 _âˆ’_ 1 _are the previously processed data samples. The data processing time per sample is_ polylog( _N,_ 1 _/Ïµ_ ) _. In particular, for a uniform marginal p_ ( _x_ ) = 1 _/N, |X|_ = _N and t_ = _O_ ( _N_ ) _, M_ = _O_ ( _NRD/Ïµ_ ) _samples suffice._ 

_Proof of Theorem D.16._ The main difficulty of this extension is that the data are not IID anymore. When we have processed previous data samples, the (posterior/conditional) distribution of new data samples shifts due to the correlation. In particular, the posterior expectation of the random Hamiltonian no longer matches the target Hamiltonian. Therefore, we have to decompose the error into two parts: a variance part same as before, and a new bias part caused by the correlation. We will bound the two parts separately to prove Theorem D.16. Concretely, let _hx_ = _f_ ( _x_ ) _|xâŸ©âŸ¨x|_ . Then we have _Vi_ = _e[ith][xi][/M]_ and _U_ = _e[it]_[E] _[x]_[[] _[h][x]_[]] , where the expectation is over the marginal distribution _x âˆ¼ p_ ( _x_ ). Let 

**==> picture [290 x 31] intentionally omitted <==**

be the empirical frequency of a given _x_ appearing in this block of samples _zt_ 0 _, . . . , zt_ 0+ _M âˆ’_ 1. Note that since the _hx_ â€™s are orthogonal and commute with each other, we have 

**==> picture [375 x 32] intentionally omitted <==**

From Theorem D.2, we have 

**==> picture [349 x 56] intentionally omitted <==**

Let _X_ = _t M_[1] ï¿½ _ti_ =0+ _t_ 0 _M âˆ’_ 1 _hxi_ = _t_[ï¿½] _x[m][x][h][x]_[be][the][random][matrix][in][the][exponent.][Note][that][the][linearity][of] expectation implies 

**==> picture [369 x 31] intentionally omitted <==**

where we have used the fact that the marginal distribution of each individual _xi_ is the same _x âˆ¼ p_ ( _x_ ). Now we separate the bias part and the variance part via triangle inequality 

**==> picture [409 x 101] intentionally omitted <==**

50 

where we use the fact that _X,_ E[ _X_ ] _,_ E[ _X|z_ 1 _, . . . , zt_ 0 _âˆ’_ 1] are all diagonal matrices and thus commuting, and _|e[iw] âˆ’_ 1 _| â‰¤|w|, âˆ€w âˆˆ_ R. 

Next, we bound the two parts separately. For the bias part, we have 

**==> picture [421 x 85] intentionally omitted <==**

where we have used Theorem C.5 with _|Z|_ = 2 _|X|_ . For the variance part, we apply Theorem D.7 to the diagonal random matrix _X|z_ 1 _, . . . , zt_ 0 _âˆ’_ 1 with diagonal elements _tmxf_ ( _x_ ) and obtain 

**==> picture [420 x 58] intentionally omitted <==**

where _x[â€²]_ is the maximizer of Var[ _tmxf_ ( _x_ ) _|z_ 1 _, . . . , zt_ 0 _âˆ’_ 1]. The law of total variance states that 

**==> picture [447 x 21] intentionally omitted <==**

where we have used the non-negativity of variance and the variance bound from Theorem C.4. Therefore, the variance part is bounded by 

**==> picture [361 x 32] intentionally omitted <==**

Combining the bias part and the variance part, we arrive at 

**==> picture [479 x 42] intentionally omitted <==**

Choosing 

**==> picture [316 x 23] intentionally omitted <==**

we have E _âˆ¥_ E [ _Vt_ 0+ _M âˆ’_ 1 _Â· Â· Â· Vt_ 0 _|z_ 1 _, . . . , zt_ 0 _âˆ’_ 1] _âˆ’Uâˆ¥â‹„ â‰¤ Ïµ_ as desired. For uniform marginal _p_ ( _x_ ) = 1 _/N, |X|_ = _N_ and _t_ = _O_ ( _N_ ), we have _p_ max = 1 _/N_ and 

**==> picture [372 x 30] intentionally omitted <==**

samples suffice. This concludes the proof of Theorem D.16. 

After showing that we can still perform quantum oracle sketching with reasonable per-query sample complexity. We move on to prove Theorem D.17 that formalizes guarantee (2): the total error still accumulates linearly. Moreover, we show that the expected conditional errors also compound additively. This showcases that the expected conditional error is the correct notion of error when we have correlated data and, in particular, it reduces to the diamond error of expected channel in the IID case. Together, Theorem D.17 allows us to keep track of error accumulation easily by simply adding them up as usual, even when the data used to construct the quantum channels have correlation. 

51 

**Lemma D.17** (Error accumulation for correlated quantum channels) **.** _Let Z_ 1 _, . . . , ZQ be Q correlated random variables. Let V_[(1)] _, . . . , V_[(] _[Q]_[)] _be quantum channels, where each V_[(] _[i]_[)] _depends only on Zi. Let U_[(1)] _, . . . , U_[(] _[Q]_[)] _and C_[(1)] _, . . . , C_[(] _[Q]_[)] _be fixed quantum channels. Then, we have_ 

**==> picture [453 x 44] intentionally omitted <==**

_Moreover, for any time interval_ 1 _â‰¤ t_ 0 _< t_ 1 _â‰¤ Q, we have_ 

**==> picture [422 x 66] intentionally omitted <==**

**==> picture [31 x 11] intentionally omitted <==**

_That is, the total error of replacing U_[(] _[j]_[)] _â€™s with V_[(] _[j]_[)] _â€™s in any time interval is bounded by the sum of individual errors, measured in expected diamond distance of conditional channels._ 

_Proof of Theorem D.17._ We only need to prove the second claim for any time interval 1 _â‰¤ t_ 0 _< t_ 1 _â‰¤ Q_ . The first claim follows directly when we take the whole time interval _t_ 0 = 1 _, t_ 1 = _Q_ . The first inequality is a direct consequence of triangle inequality 

**==> picture [413 x 13] intentionally omitted <==**

To prove the second inequality, consider the hybrid quantum channels 

**==> picture [479 x 13] intentionally omitted <==**

and _At_ 1+1 = E[ _V_[(] _[t]_[1][)] _â—¦C_[(] _[t]_[1][)] _â—¦Â· Â· Â· â—¦V_[(] _[t]_[0][)] _â—¦C_[(] _[t]_[0][)] _|V_[(1)] _, . . . , V_[(] _[t]_[0] _[âˆ’]_[1)] ] _, At_ 0 = _U_[(] _[t]_[1][)] _â—¦C_[(] _[t]_[1][)] _â—¦Â· Â· Â· â—¦U_[(] _[t]_[0][)] _â—¦C_[(] _[t]_[0][)] . Then we can expand the left hand side as a telescoping sum 

**==> picture [468 x 55] intentionally omitted <==**

Each term is be bounded by 

**==> picture [487 x 125] intentionally omitted <==**

**==> picture [32 x 11] intentionally omitted <==**

where we have used the sub-multiplicativity of diamond norm _âˆ¥_ Î¦1 _â—¦_ ( _Â·_ ) _â—¦_ Î¦2 _âˆ¥â‹„ â‰¤âˆ¥_ Î¦1 _âˆ¥â‹„âˆ¥Â· âˆ¥â‹„âˆ¥_ Î¦2 _âˆ¥â‹„_ = _âˆ¥Â· âˆ¥â‹„_ with quantum channels _âˆ¥_ Î¦1 _âˆ¥â‹„_ = _âˆ¥_ Î¦2 _âˆ¥â‹„_ = 1 twice, and the triangle inequality _âˆ¥_ E[ _Â·_ ] _âˆ¥â‹„ â‰¤_ E _âˆ¥Â· âˆ¥â‹„_ . Lastly, we replace the conditioning on _V_[(1)] _, . . . , V_[(] _[j][âˆ’]_[1)] by conditioning on the _Z_ â€™s: 

**==> picture [453 x 64] intentionally omitted <==**

52 

where we have used the fact that _V_[(1)] _, . . . , V_[(] _[j][âˆ’]_[1)] only depends on _Z_ 1 _, . . . , Zjâˆ’_ 1 and the triangle inequality. Plugging this back into the sum gives us the desired result. This completes the proof of Theorem D.17. 

**==> picture [143 x 9] intentionally omitted <==**

In previous sections, we have shown how to prepare 

**==> picture [302 x 22] intentionally omitted <==**

from any hierarchical data generation process using quantum oracle sketching. When the data has uniform marginal _p_ ( _x_ ) = 1 _/N_ , we can set _t_ = _Ï€N_ and obtain access to the phase oracle 

**==> picture [336 x 22] intentionally omitted <==**

that we want. However, the marginal distribution _p_ ( _x_ ) _âˆˆ_ [ _p_ min _, p_ max] may be non-uniform and unknown in general. In this case, we need a way to remove _U_ ( _t_ )â€™s dependence on _p_ ( _x_ ) without knowing it. 

One may attempt to first learn _p_ ( _x_ ) (or assuming that _p_ ( _x_ ) is known), and then multiply the phase rotation angle by 1 _/p_ ( _x_ ) when performing the multi-controlled phase gate corresponding to ( _x, f_ ( _x_ )). This does not work when the distribution is unknown, because learning _p_ ( _x_ ) would require an exponentially large memory to store the values of _p_ ( _x_ ) for all _x âˆˆX_ . 

In the following, we show how to use techniques from quantum singular value transform (QSVT) to accommodate unknown and non-uniform marginal with only one ancilla qubit. Assume _p_ ( _x_ ) _âˆˆ_ [ _p_ min _, p_ max]. The key is to note that the rotation angles in _U_ ( _t_ ) are 0 for those _x_ with _f_ ( _x_ ) = 0, and are in [ _p_ min _, p_ max] and thus bounded away from 0 for those _x_ with _f_ ( _x_ ) = 1. So all we need to do is to apply a threshold function that is equal to 1 when the rotation angle is below a threshold value and is equal to _âˆ’_ 1 when the rotation angle is above the threshold. This would give us the desired oracle _O_ =[ï¿½] _x_[(] _[âˆ’]_[1)] _[f]_[(] _[x]_[)] _[ |][x][âŸ©âŸ¨][x][|]_[.][We][formalize][this][idea] in the following lemma. In particular, when _X_ = [ _N_ ], as long as the distribution _p_ ( _x_ ) is not too tilted (e.g., _p_ max _/p_ min _â‰¤_ polylog( _N_ ) and _p_ min _â‰¥_ â„¦(1 _/N_ )), the sample complexity is still _O_[Ëœ] ( _N_ ). 

**Lemma D.18** (Sample complexity upper bound for unknown distributions) **.** _Let t, Ïµ >_ 0 _. Let X be a finite set and let f_ : _X â†’{_ 0 _,_ 1 _} be a Boolean function. Let D_ = ( _D_[0] _â†’DÎ±_[1] 1 _[â†’][Ã—][T]_[1] _[Â· Â· Â· â†’][Ã—][T][l][âˆ’]_[1] _[D] Î±[l] l[â†’][Ã—][T][l][z]_[)] _[ be a hierarchi-] cal data generation process with repetition number RD that generates a sequence of M data samples zi_ = ( _xi, yi_ ) _where yi_ = _f_ ( _xi_ ) _, i_ = _t_ 0 _, . . . , t_ 0 + _M âˆ’_ 1 _starting from any time step t_ 0 _â‰¥_ 1 _. Let p_ max = max _xâˆˆX p_ ( _x_ ) _, p_ min = min _xâˆˆX p_ ( _x_ ) _, where p_ ( _x_ ) _is the marginal distribution of data. Let O_ =[ï¿½] _xâˆˆX_[(] _[âˆ’]_[1)] _[f]_[(] _[x]_[)] _[ |][x][âŸ©âŸ¨][x][|][be][the][phase][oracle] of f . Then, we can use_ 

**==> picture [332 x 31] intentionally omitted <==**

_samples zt_ 0 _, . . . , zt_ 0+ _M âˆ’_ 1 _to construct a random unitary V acting on the original system and one ancilla qubit a such that its corresponding channel_ 

**==> picture [301 x 13] intentionally omitted <==**

_satisfies_ 

**==> picture [312 x 12] intentionally omitted <==**

_where O_ : _Ï â†’|_ 0 _aâŸ©âŸ¨_ 0 _a| âŠ— OÏO[â€ ] and z_ 1 _, . . . , zt_ 0 _âˆ’_ 1 _are previously processed data samples. The data processing time per sample is_ polylog( _N_ ) _. Similarly, one can implement the controlled oracle cO_ = _|_ 0 _âŸ©âŸ¨_ 0 _| âŠ— I_ + _|_ 1 _âŸ©âŸ¨_ 1 _| âŠ— O with the same guarantees. Moreover, when the data are sampled IID,_ 

**==> picture [299 x 26] intentionally omitted <==**

_samples suffices._ 

_Proof of Theorem D.18._ We prove Theorem D.18 by first constructing the unitary _U_ ( _t_ ) =[ï¿½] _x[e][ip]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[t][ |][x][âŸ©âŸ¨][x][|]_ using Theorem D.16 and then applying a threshold function on the rotation angles using QSVT (Theorems D.8 and D.9). 

53 

Concretely, fix _t_ = 1 _/p_ max. Theorem D.16 asserts that we can use 

**==> picture [365 x 25] intentionally omitted <==**

samples to construct one query to a (random) unitary _V_[0] such that 

**==> picture [314 x 12] intentionally omitted <==**

where _U_ =[ï¿½] _x[e][ip]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[/p]_[max] _[ |][x][âŸ©âŸ¨][x][|]_[.][Note][that][we][can][also][implement] _[U][ â€ ]_[with][the][same][number][of][samples][by] setting _t_ = _âˆ’_ 1 _/p_ max. Similarly, we can implement _cU_ and _cU[â€ ]_ by adding control to the multi-controlled phase gates in Theorem D.16. In the following, we will keep track of how many queries we make to _U_ , _U[â€ ]_ , _cU_ , and _cU[â€ ]_ to construct the _V_ that approximates _O_ . 

_âˆ’i_ 0 Let Î› =[ï¿½] _x[p]_[(] _[x]_[)] _[f]_[(] _[x]_[)] _[/p]_[max] _[ |][x][âŸ©âŸ¨][x][|]_[and][therefore] _[U]_[=] _[e][i]_[Î›][.][Let] _[S]_[=] 0 1 be a single qubit gate. We ï¿½ ï¿½ introduce an ancilla qubit _a_ and use two queries to construct 

**==> picture [315 x 12] intentionally omitted <==**

where the subscript indicate which qubit the gate or the control acts on. Then we have 

**==> picture [379 x 155] intentionally omitted <==**

Therefore, we have 

**==> picture [309 x 23] intentionally omitted <==**

Note that we also have access to _W[â€ ]_ using a similar construction. Since _p_ ( _x_ ) _f_ ( _x_ ) is zero when _f_ ( _x_ ) = 0 and in [ _p_ min _, p_ max] when _f_ ( _x_ ) = 1, we know that the eigenvalues of sin Î› is 0 on the basis _{|xâŸ© , f_ ( _x_ ) = 0 _}_ and is in [sin( _p_ min _/p_ max) _,_ sin(1)] on the basis _{|xâŸ© , f_ ( _x_ ) = 1 _}_ , as sin( _x_ ) is increasing on [0 _,_ 1]. 

Now we invoke Theorem D.8 to apply a polynomial function _P_ to _W_ . We choose the polynomial _P_ to approximate the threshold function with threshold value _Î»[â‹†]_ = sin( _p_ min _/p_ max) as in Theorem D.9. In particular, Theorem D.9 implies that the degree of _P_ is at most _d_ = _O_ (log(1 _/Ïµ_ 2) _/Î»[â‹†]_ ) (we choose _d_ to be even), _P_ is an even function, _|P_ ( _w_ ) _| â‰¤_ 1 _, âˆ€w âˆˆ_ [ _âˆ’_ 1 _,_ 1], and _|P_ ( _w_ ) _âˆ’_ 1 _| â‰¤ Ïµ_ 2 _, âˆ€w âˆˆ_ [0 _, Î»[â‹†] /_ 2] and _|P_ ( _w_ ) + 1 _| â‰¤ Ïµ_ 2 _, âˆ€w âˆˆ_ [ _Î»[â‹†] ,_ 1]. This means that 

**==> picture [355 x 19] intentionally omitted <==**

Then Theorem D.8 tells us that there exists a set of rotation angles _Ï•i âˆˆ_ [0 _,_ 2 _Ï€_ ) _, i âˆˆ_ [ _d_ ] such that the unitary 

**==> picture [327 x 32] intentionally omitted <==**

satisfies 

**==> picture [315 x 12] intentionally omitted <==**

The error of approximating _O_ is therefore 

**==> picture [411 x 19] intentionally omitted <==**

54 

To convert this into a diamond norm bound, note that 

**==> picture [417 x 55] intentionally omitted <==**

Also, 

_âˆ¥âŸ¨_ 1 _a| P_ QSVT( _W, Ï•_ ) _|_ 0 _aâŸ©âˆ¥_[2] 

**==> picture [454 x 54] intentionally omitted <==**

**==> picture [396 x 57] intentionally omitted <==**

Hence, the error is 

**==> picture [379 x 12] intentionally omitted <==**

when we choose _Ïµ_ 2 = ( _Ïµ/_ 12)[2] . The total number of queries to _U, U[â€ ] , cU_ and _cU[â€ ]_ is 

**==> picture [399 x 25] intentionally omitted <==**

where we have used the fact that sin( _x_ ) _/x â‰¥_ sin(1) _/_ 1 _>_ 0 _._ 8 _, âˆ€x âˆˆ_ [0 _,_ 1]. 

Finally, we construct the desired unitary _V_ by replacing all the _U, U[â€ ] , cU_ and _cU[â€ ]_ in _P_ QSVT( _W, Ï•_ ) with the random unitaries constructed from samples using Theorem D.16. Since there are _Q_ queries in total, the error of approximating _P_ QSVT( _W, Ï•_ ) is bounded by _QÏµ_ 1, using Theorem D.17. 

We set _Ïµ_ 1 = _Ïµ/_ (4 _Q_ ). Then triangle inequality implies the desired property: 

**==> picture [311 x 11] intentionally omitted <==**

The total number of samples used is 

**==> picture [484 x 43] intentionally omitted <==**

Similarly, one can construct the controlled oracle _cO_ using the controlled version of the QSVT construction as in Theorem D.8 and the same guarantees hold. When the data are sampled IID, we have _M_ 0 = _p_ max _t_[2] _/Ïµ_ 1 from Theorem D.12 and _M_ = _O_ ( _p_ max _/p_[2] min _[Â·]_[ log][2][(1] _[/Ïµ]_[)] _[/Ïµ]_[).][This][completes][the][proof][of][Theorem][D.18][.] 

## **5. Linear algebra primitives** 

In this section, we utilize quantum oracle sketching to construct several useful primitives for linear algebra data (e.g., vectors, matrices, etc.). In particular, we show how to construct the sparse oracles and block encodings for sparse matrices, and prepare quantum states corresponding to arbitrary vectors. 

**==> picture [95 x 9] intentionally omitted <==**

We begin by introducing our data access model for linear algebra data such as matrices and vectors. For an _N_ -dimensional matrix _A âˆˆ_ R _[N][Ã—][N]_ , we define its matrix data generation process _DA_ as a hierarchical data generation process that generates random non-zero matrix elements as data 

**==> picture [366 x 15] intentionally omitted <==**

55 

The matrix elements _Aij_ are specified by bitstrings of length _b_ = polylog( _N_ ) to sufficient accuracy. For simplicity, we assume that this binary representation is exact and use _Aij_ to stand for the corresponding value. From the data generation process of _A_ , one can easily generate that of _A[T]_ by switching _i â†” j_ and that of the symmetrized 0 _A_ matrix _A_ sym = _A[T]_ 0 by randomly transforming ( _i, j_ ) to ( _i, j_ + _N_ ) or ( _j_ + _N, i_ ) with equal probability. It ï¿½ ï¿½ is also straightforward to generalize to complex matrices. 

We note that this encompasses rectangular matrices _A âˆˆ_ R _[D]_[1] _[Ã—][D]_[2] by defining _N_ = max( _D_ 1 _, D_ 2) and embed the rectangular matrix into a larger square one with zeroes padded in. The data generation process remains completely unchanged since zero matrix elements are never sampled. For this reason, we always assume that _A_ is a square matrix in algorithmic constructions, because rectangular matrices are automatically handled by setting _N_ = max( _D_ 1 _, D_ 2). 

Similarly, for a _N_ -dimensional vector _[âƒ—] b_ = ( _b_ 1 _, . . . , bN_ ) _[T] âˆˆ_ R _[N]_ , we define its vector data generation process _Dâƒ—b_ as a hierarchical data generation process that generates random components of the vector as data 

**==> picture [323 x 15] intentionally omitted <==**

For simplicity, we also assume that the components _bj_ are specified by bitstrings of length _b_ = polylog( _N_ ) exactly and use _bj_ to stand for the corresponding value. 

In the following, we always assume _N_ = 2 _[n]_ for some integer _n_ . We can always do so, because even if _N_ is not a power of two, we can still embed the matrix/vector into a larger matrix/vector of dimension 2 _[âŒˆ]_[log] _[ N][âŒ‰] âˆˆ_ [ _N,_ 2 _N_ ] by padding zeroes. The matrix data generation process stays exactly the same since it only generates non-zero elements. The block encoding of the larger matrix is also automatically a block encoding of the original, possibly rectangular matrix. For vectors, although the vector data generation process will be diluted with a constant fraction of zeroes after the embedding, we will see that the same quantum oracle sketching algorithm works without any modification, because it does nothing upon seeing a zero component. Therefore, we assume without loss of generality that _N_ = 2 _[n]_ for some integer _n_ . 

**==> picture [74 x 9] intentionally omitted <==**

In this section, we show how to implement the standard sparse oracles of sparse matrices using quantum oracle sketching. The sparse oracles of an row _sr_ -sparse and column _sc_ -sparse matrix _A_ are defined as 

**==> picture [472 x 14] intentionally omitted <==**

where _j_ ( _i, k_ ) _âˆˆ{_ 0 _,_ 1 _}[n] â‰ƒ_ [ _N_ ] _, k âˆˆ_ [ _sr_ ] is the column index (in binary form) of the _k_ -th non-zero element in row _i_ and _i_ ( _j, k_ ) _âˆˆ{_ 0 _,_ 1 _}[n] â‰ƒ_ [ _N_ ] _, k âˆˆ_ [ _sc_ ] is the row index of the _k_ -th non-zero element in column _j_ . The sparsity _s_ of _A_ is _s_ = max( _sr, sc_ ). 

In the following, we show that for _s_ = polylog _N_ , we can implement these sparse oracles with polylog( _N_ ) qubits and _O_[Ëœ] ( _RN/Ïµ_ ) samples from the matrix data generation process _DA_ with repetition number _R_ . 

We begin with the sparse element oracle _OA_[ele][that][is][relatively][straightforward][to][implement][using][quantum] oracle sketching. 

**Lemma D.19** (Sparse element oracle) **.** _Let A âˆˆ_ R _[N][Ã—][N] be an N -dimensional, row sr-sparse, and column sc-sparse matrix. Let OA_[ele][:] _[Ï][â†’][O] A_[ele] _[ÏO] A_[ele] _[â€ ] be the unitary channel corresponding to its sparse element oracle OA_[ele] _[.][Then,][we][can][use]_[2] _[ âŒˆ]_[log] _[ N][âŒ‰]_[+] _[ b][qubits][and]_ 

**==> picture [285 x 25] intentionally omitted <==**

_samples starting at any time t_ 0 _â‰¥_ 1 _from its matrix data generation process DA with repetition number R to implement a random unitary channel V satisfying_ 

**==> picture [300 x 13] intentionally omitted <==**

_where z_ 1 _, . . . , zt_ 0 _âˆ’_ 1 _are previously processed data samples. The data processing time per sample is_ polylog( _N,_ 1 _/Ïµ_ ) _. The same guarantee holds for implementing OA_[ele] _[â€ ] and their controlled version cOA_[ele] _[, cO] A_[ele] _[â€ ] with one more qubit._ 

56 

_Proof._ Let ( _Aij_ ) _a, a âˆˆ_ [ _b_ ] denote the _a_ -th bit in the binary representation of _Aij_ . Let _K_ = _{_ ( _i, j_ ) : _Aij_ = 0 _}_ be the set of nonzero elements with cardinality _K_ = _|K| â‰¤ N_ min( _sr, sc_ ). We first prepare the phase oracle of the _a_ -th bit 

**==> picture [309 x 25] intentionally omitted <==**

by applying the (2 _n_ )-qubit multi-controlled phase gate 

**==> picture [321 x 25] intentionally omitted <==**

for all _a âˆˆ_ [ _b_ ] when the sample ( _i, j, Aij_ ) is drawn from the stream. We use _Va_ to denote the resulting random unitary channel. Now we invoke Theorem D.16 with _p_ ( _i, j_ ) = 1 _/K_ , _t_ = _Ï€K_ , _|X|_ = _K_ , and repetition number _R_ , obtaining 

**==> picture [349 x 14] intentionally omitted <==**

with 

**==> picture [329 x 25] intentionally omitted <==**

samples. To implement _OA_[ele][, we use the standard conversion from phase oracles to XOR oracles:][we add control] to the individual gates, obtain channel approximations to controlled- _Ua_ , and implement ( _H âŠ— I_ ) _cUa_ ( _H âŠ— I_ ) for each _a âˆˆ_ [ _b_ ] to obtain a (2 _n_ + _b_ )-qubit quantum channel that _Ïµ_ -approximates 

**==> picture [309 x 12] intentionally omitted <==**

thereby proving Theorem D.19. The same results hold for implementing _OA_[ele] _[â€ ][, cO] A_[ele] _[, cO] A_[ele] _[â€ ]_ by adding additional control to the individual gates or negating the phases in them. 

The column and row index oracles _OA_[ind] _[,]_[col] _, OA_[ind] _[,]_[row] are more technically involved to implement. We only need to describe how to implement the row index oracle _OA_[ind] _[,]_[row] , and then the implementation of the column index oracle _OA_[ind] _[,]_[col] follows verbatim by swapping the roles of _i_ and _j_ . To prepare the row index oracle, we consider an intermediate oracle that we call the _cumulative counter oracle_ , defined as 

**==> picture [405 x 11] intentionally omitted <==**

where 

**==> picture [306 x 12] intentionally omitted <==**

is the number of non-zero columns in row _i âˆˆ{_ 0 _,_ 1 _}[n]_ that have column indices strictly smaller than _l âˆˆ{_ 0 _,_ 1 _}[n]_ . The purpose of this cumulative counter oracle is to count the cumulative number of non-zero columns in a row _i_ up to a given trial column _l_ . We will use quantum oracle sketching to construct this cumulative counter oracle. 

After we have constructed the cumulative counter oracle, we can use it to perform a binary search over the non-zero columns by progressively refine our trial column _l âˆˆ{_ 0 _,_ 1 _}[n]_ until it converges to the target column index _j_ ( _i, k_ ). Suppose we have found the first _m âˆˆ_ [ _n_ ] bits _lm_ of the target column _j_ ( _i, k_ ) and set _l_ = _lm_ 00 _. . ._ 0. Now we want to find the ( _m_ + 1)-th bit. We first flip the ( _m_ + 1)-th bit and obtain _|lm_ 10 _. . ._ 0 _âŸ©_ . Then we apply the cumulative counter oracle _Oc_ to _|iâŸ©|kâŸ©|lm_ 10 _. . ._ 0 _âŸ©|_ 0 _âŸ©_ and get 

**==> picture [332 x 11] intentionally omitted <==**

Note that if the ( _m_ + 1)-th bit of the target _j_ ( _i, k_ ) is 1 (i.e., _j_ ( _i, k_ ) has prefix _lm_ 1), then there must be less than _k_ non-zero columns with prefix _lm_ 0, because the _k_ -th non-zero column _j_ ( _i, k_ ) has prefix _lm_ 1. This means that 1[ _C_ ( _i, lm_ 10 _. . ._ 0) _< k_ ] = 1. On the other hand, if the ( _m_ + 1)-th bit of _j_ ( _i, k_ ) is 0, then there must be at least _k_ non-zero columns with prefix _lm_ 0 and hence 1[ _C_ ( _i, lm_ 10 _. . ._ 0) _< k_ ] = 0. In both cases, we have 

**==> picture [319 x 11] intentionally omitted <==**

where _j_ ( _i, k_ ) _m_ +1 is the ( _m_ + 1)-th bit of the target _j_ ( _i, k_ ). Therefore, the state reads 

**==> picture [307 x 11] intentionally omitted <==**

57 

Finally, we flip the ( _m_ + 1)-th bit of the _|lâŸ©_ register to reset it back to 0 and swap it with _|j_ ( _i, k_ ) _m_ +1 _âŸ©_ . This gives us the state 

**==> picture [307 x 11] intentionally omitted <==**

Now we have found the ( _m_ +1)-th bit of the target _j_ ( _i, k_ ). We repeat this procedure _n_ times in total and obtain the state 

**==> picture [281 x 11] intentionally omitted <==**

It remains to erase the _|kâŸ©_ register. We do so by a similar binary search using the cumulative counter oracle _Oc_ but on _|kâŸ©_ . This constructs the desired row index oracle. 

It remains to show how to construct the cumulative counter oracle _Oc_ with quantum oracle sketching. We first construct an intermediate object called the cumulative counter unitary _Uc_ , that has the _C_ ( _i, l_ ) _âˆ’ k_ information encoded in its phase. Then we use QSVT to apply a threshold function that calculates the binary value 1[ _C_ ( _i, l_ ) _âˆ’ k <_ 0] as required in the cumulative counter oracle. In Theorem D.20, we show how to construct _Uc_ with quantum oracle sketching. Later in Theorem D.21, we show how to use _Uc_ to construct the sparse index oracles. 

**Lemma D.20** (Cumulative counter unitary) **.** _Let A âˆˆ_ R _[N][Ã—][N] be an N -dimensional and row sr-sparse matrix. We define the cumulative counter unitary Uc of A as_ 

**==> picture [355 x 13] intentionally omitted <==**

_where the phase_ 

**==> picture [413 x 25] intentionally omitted <==**

_Then, we can use_ 2 _âŒˆ_ log( _N_ ) _âŒ‰_ + _âŒˆ_ log( _sr_ ) _âŒ‰_ + _b qubits and_ 

**==> picture [281 x 25] intentionally omitted <==**

_samples starting at any time t_ 0 _â‰¥_ 1 _from the matrix data generation process DA with repetition number R to implement a random unitary channel Vc satisfying_ 

**==> picture [326 x 12] intentionally omitted <==**

_where z_ 1 _, . . . , zt_ 0 _âˆ’_ 1 _are previously processed data samples. The data processing time per sample is_ polylog( _N_ ) _. The same holds for implementing Uc[â€ ][, cU][c][, cU] c[ â€ ][.]_ 

_Proof._ For convenience, we define the shorthand 

**==> picture [266 x 11] intentionally omitted <==**

with the corresponding set 

**==> picture [303 x 11] intentionally omitted <==**

and projector 

**==> picture [290 x 11] intentionally omitted <==**

Note that 

**==> picture [297 x 11] intentionally omitted <==**

because _A_ is row _sr_ -sparse. We define the fixed offset gate 

**==> picture [330 x 13] intentionally omitted <==**

which can be easily implemented using single-qubit phase gates on each bit of _k_ . We then rewrite _Uc_ as 

**==> picture [414 x 30] intentionally omitted <==**

58 

Meanwhile, the marginal distribution of ( _i, j_ ) from the sparse matrix stream is 

**==> picture [300 x 31] intentionally omitted <==**

where _K_ = _|K|, K_ = _{_ ( _i, j_ ) : _Aij_ = 0 _}_ with _K â‰¤_ 2 _[n] sr_ . Therefore, we have 

**==> picture [364 x 150] intentionally omitted <==**

This representation allows us to implement _Uo[â€ ][U][c]_[and hence] _[ U][c]_[using quantum oracle sketching (Theorem][ D.16][).] In particular, with each one of the _M_ samples ( _i, j, Aij_ ), we apply the unitary 

**==> picture [344 x 36] intentionally omitted <==**

This gate _V_ ( _i, j_ ) can be implemented efficiently (i.e., in polylog _N_ time) because it is a controlled phase gate where the control rule defined by _Sa_ can be efficiently checked. Now we follow the notations in Theorem D.16 and define the Hamiltonian 

**==> picture [315 x 28] intentionally omitted <==**

Then _V_ ( _i, j_ ) = _e[ih][ij][/M]_ . Since _hij_ â€™s are diagonal and commute with each other, the joint action of the gates corresponding to all _M_ samples ( _ik, jk_ ) _[M] k_ =1[,][followed][by][a][fixed][gate] _[U][o]_[,][is][a][random][unitary] 

**==> picture [389 x 32] intentionally omitted <==**

where we define a random matrix _X_ = _M_ 1 ï¿½ _tk_ 0=+ _tM_ 0 _âˆ’_ 1 _hikjk_ as a shorthand. Meanwhile, we can rewrite the target cumulative counter unitary as 

**==> picture [328 x 11] intentionally omitted <==**

since 

**==> picture [321 x 31] intentionally omitted <==**

The matrix _X_ can be written in the _|aâŸ©_ basis as 

**==> picture [355 x 129] intentionally omitted <==**

59 

_Ï€K_ where we have introduced _t_ = 2( _sr_ +1 _/_ 2)[and][random][variables] 

**==> picture [312 x 31] intentionally omitted <==**

to be the empirical frequency of phase accumulation on the basis _|aâŸ©_ . 

To bound the error, we need to bound the variance part and bias part separately as in Theorem D.16. We first bound the variance part. Since _X_ is a diagonal random matrix with diagonal elements _tma_ , Theorem D.7 implies that 

**==> picture [452 x 32] intentionally omitted <==**

where _a[â€²]_ is the maximizer of Var[ _ma|z_ 1 _, . . . , zt_ 0 _âˆ’_ 1] and we have used the law of total variance. Now we define 

**==> picture [318 x 32] intentionally omitted <==**

and note that 

**==> picture [333 x 135] intentionally omitted <==**

Therefore, the variance can be upper bounded by 

**==> picture [345 x 101] intentionally omitted <==**

On the other hand, the variance upper bound in Theorem C.4 implies that 

**==> picture [279 x 24] intentionally omitted <==**

where _R_ is the repetition number of the matrix data generation process. Thus, we have 

**==> picture [380 x 32] intentionally omitted <==**

where we have used _t_ = _Ï€K/_ (2( _sr_ + 1 _/_ 2)). Next, we bound the bias part. Note that since _X,_ E[ _X|z_ 1 _, . . . , zt_ 0 _âˆ’_ 1] are diagonal and thus commuting, we 

60 

have 

**==> picture [409 x 173] intentionally omitted <==**

where we have used Theorem C.5, _|Sa| â‰¤ sr_ , and _t_ = _Ï€K/_ (2( _sr_ + 1 _/_ 2)). Combining the variance and bias part, we have 

**==> picture [409 x 87] intentionally omitted <==**

where we have invoked Theorem D.2. Since _K â‰¤ Nsr_ , we conclude that 

**==> picture [287 x 23] intentionally omitted <==**

samples ensures 

**==> picture [336 x 12] intentionally omitted <==**

Note that the same analysis holds for implementing _Uc[â€ ][, cU][c][, cU] c[ â€ ]_[by][adding][additional][control][to][the][individual] gates or negating the phases in them. This completes the proof of Theorem D.20. 

Now we use the cumulative counter unitary _Uc_ to build the sparse row index oracle 

**==> picture [360 x 14] intentionally omitted <==**

where _j_ ( _i, k_ ) _âˆˆ{_ 0 _,_ 1 _}[n]_ is the column index of the _k_ -th nonzero element of _A_ in row _i_ . The implementation of the sparse column index oracle follows similarly by swapping rows and columns. 

61 

**Lemma D.21** (Sparse index oracles) **.** _Let A âˆˆ_ R _[N][Ã—][N] be an N -dimensional and row sr-sparse matrix. Let OA_[ind] _[,]_[row] : _Ï â†’ OA_[ind] _[,]_[row] _ÏOA_[ind] _[,]_[row] _[â€ ] be the unitary channel corresponding to the sparse row index oracle OA_[ind] _[,]_[row] _. Then, we can use_ 2 _âŒˆ_ log( _N_ ) _âŒ‰_ + _âŒˆ_ log( _s_ ) _âŒ‰_ + 2 + _b qubits and_ 

**==> picture [349 x 27] intentionally omitted <==**

_samples starting at any time t_ 0 _â‰¥_ 1 _from the matrix data generation process DA with repetition number R to implement a random unitary channel V satisfying_ 

**==> picture [309 x 13] intentionally omitted <==**

_where z_ 1 _, . . . , zt_ 0 _âˆ’_ 1 _are previously processed data samples. The data processing time per sample is_ polylog( _N,_ 1 _/Ïµ_ ) _. The same guarantee holds for implementing OA_[ind] _[,]_[row] _[â€ ] , cOA_[ind] _[,]_[row] _, and cOA_[ind] _[,]_[row] _[â€ ] . Similar results apply to implementing OA_[ind] _[,]_[col] _, OA_[ind] _[,]_[col] _[â€ ] , cOA_[ind] _[,]_[col] _, cOA_[ind] _[,]_[col] _[â€ ] with row sr-sparse replaced by column sc-sparse._ 

_Proof._ In the following we show how to implement _OA_[ind] _[,]_[row] with the claimed complexity. The implementation of _OA_[ind] _[,]_[col] and its cousins follows verbatim by swapping rows and columns. Recall our earlier intuition that 

**==> picture [341 x 12] intentionally omitted <==**

for any _i âˆˆ{_ 0 _,_ 1 _}[n] , k âˆˆ_ [ _sr_ ] _, m âˆˆ_ [ _n_ ]. To calculate 1[ _C_ ( _i, l_ ) _âˆ’ k <_ 0] using the counter 

**==> picture [404 x 25] intentionally omitted <==**

that we have from Theorem D.20, we need to implement a threshold function that maps positive phases to ( _âˆ’_ 1)[0] and negative phases to ( _âˆ’_ 1)[1] . To this end, we employ QSVT similar to the techniques used in Theorem D.18 _âˆ’i_ 0 as follows. Let _S_ = be a single qubit gate. We introduce an ancilla qubit _a_ and use two queries to 0 1 ï¿½ ï¿½ construct 

**==> picture [318 x 13] intentionally omitted <==**

where the subscript _a_ indicates that the gate or the control acts on an ancilla qubit. Then we have 

**==> picture [383 x 155] intentionally omitted <==**

Therefore, we have a block encoding 

**==> picture [364 x 30] intentionally omitted <==**

Note that we also have access to _Wc[â€ ]_[using][a][similar][construction.] Now we apply a polynomial function _P_ to _Wc_ . Since sin( _Î¸_ ( _i, k, l_ )) _âˆˆ_ [sin( _Ï€/_ (4 _sr_ + 2)) _,_ 1] corresponds to 1[ _C_ ( _i, l_ ) _< k_ ] = 0 and sin( _Î¸_ ( _i, k, l_ )) _âˆˆ_ 

62 

[ _âˆ’_ 1 _, âˆ’_ sin( _Ï€/_ (4 _sr_ + 2))] corresponds to 1[ _C_ ( _i, l_ ) _< k_ ] = 1, we choose the polynomial _P_ to _Ïµ_ 1-approximate the sign function with threshold value _Î»[â‹†]_ = sin( _Ï€/_ (4 _sr_ + 2)). The degree of _P_ is at most _d_ = _O_ (log(1 _/Ïµ_ 1) _/Î»[â‹†]_ ) (we choose _d_ to be odd), _P_ is an odd function, _|P_ ( _w_ ) _| â‰¤_ 1 _, âˆ€w âˆˆ_ [ _âˆ’_ 1 _,_ 1], and _|P_ ( _w_ ) _âˆ’_ 1 _| â‰¤ Ïµ_ 1 _, âˆ€w âˆˆ_ [ _Î»[â‹†] ,_ 1] and _|P_ ( _w_ ) + 1 _| â‰¤ Ïµ_ 1 _, âˆ€w âˆˆ_ [ _âˆ’_ 1 _, âˆ’Î»[â‹†]_ ]. This means that 

**==> picture [350 x 19] intentionally omitted <==**

Then Theorem D.8 tells us that there exists a set of rotation angles _Ï•k âˆˆ_ [0 _,_ 2 _Ï€_ ) _, k âˆˆ_ [ _d_ ] such that the unitary 

**==> picture [330 x 32] intentionally omitted <==**

satisfies 

**==> picture [367 x 24] intentionally omitted <==**

The QSVT target is the phase oracle 

**==> picture [318 x 13] intentionally omitted <==**

The same error analysis as in Theorem D.18 implies that 

**==> picture [484 x 32] intentionally omitted <==**

**==> picture [388 x 25] intentionally omitted <==**

where we have used the fact that sin( _x_ ) _/x â‰¥_ sin( _Ï€/_ 2) _/_ ( _Ï€/_ 2) = 2 _/Ï€, âˆ€x âˆˆ_ [0 _, Ï€/_ 2]. The same results hold for implementing _Vc[â€ ][, cV][c][, cV] c[â€ ]_[.][We][implement] _[U][c]_[and][its][cousins][using][samples][from][the][matrix][data][generation] process as in Theorem D.20. Similar to the analysis in Theorem D.18, we obtain an _Ïµ_ 2-approximation to _Vc_ using a total number of samples 

**==> picture [395 x 26] intentionally omitted <==**

Next, we convert this into the cumulative counter oracle 

**==> picture [331 x 12] intentionally omitted <==**

via the standard phase oracle to XOR oracle conversion by introducing an output ancilla _o_ : 

**==> picture [304 x 11] intentionally omitted <==**

where the Hadamard gate and the control are on the ancilla qubit. 

We now proceed to construct the sparse index oracle using the cumulative counter oracle. As discussed earlier, we start from _|iâŸ©|kâŸ©|_ 0 _. . ._ 0 _âŸ©l |_ 0 _âŸ©o_ , flip the first bit of the _l_ register, apply _Oc_ , flip the first bit of _l_ again, and swap that bit with the output register _o_ of _Oc_ . This writes the first bit of _j_ ( _i, k_ ) into the first bit of the _l_ register. Then we proceed and repeat the same procedure to all the _n_ bits in the _l_ register. This results in the following circuit 

**==> picture [424 x 12] intentionally omitted <==**

that finds the desired column index. 

It remains to erase the _|kâŸ©_ register. We do so by a similar binary search using the cumulative counter oracle _Oc_ , but over the _|kâŸ©_ register. From the definition of _C_ ( _i, l_ ) = _|{j_ : _Aij_ = 0 _, j < l}|_ , we have that 

**==> picture [298 x 11] intentionally omitted <==**

where we have defined _k[â€²]_ = _k âˆ’_ 1. Let _m_ = _âŒˆ_ log( _sr_ ) _âŒ‰_ be the binary representation length of the _|kâŸ©_ register. We have that 

**==> picture [461 x 12] intentionally omitted <==**

63 

where the subscripts mark the positions of the bits. 

We begin by subtracting 1 from _|kâŸ©_ , add 1 to _|_ 0 _âŸ©o_ , and obtain _|iâŸ©|k[â€²] âŸ©|j_ ( _i, k_ ) _âŸ©|_ 1 _âŸ©o_ . Now suppose we have obtained _|iâŸ©|k_ 1 _[â€²][. . . k] t[â€²]_[0] _[ . . .]_[ 0] _[âŸ©|][j]_[(] _[i, k]_[)] _[âŸ©|]_[1] _[âŸ©] o_[.][We][apply][SWAP] _[k] t[,o]_[and][obtain] _[|][i][âŸ©]_ ï¿½ï¿½ _k_ 1 _â€²[. . . k] t[â€²] âˆ’_ 1[1] _[t]_[0] _[ . . .]_[ 0] ï¿½ _|j_ ( _i, k_ ) _âŸ©|kt[â€²][âŸ©] o_[.] Then we apply _Oc_ to write 1[ _C_ ( _i, j_ ( _i, k_ )) _< k_ 1 _[â€²][. . . k] t[â€²] âˆ’_ 1[1] _[t]_[0] _[t]_[+1] _[. . .]_[ 0] _[m]_[]][=] _[k] t[â€²][âŠ•]_[1][into][the] _[o]_[register][and][obtain] _|iâŸ©_ ï¿½ï¿½ _k_ 1 _â€²[. . . k] t[â€²] âˆ’_ 1[1] _[t]_[0] _[ . . .]_[ 0] ï¿½ _|j_ ( _i, k_ ) _âŸ©|_ 1 _âŸ©o_ . Finally, we apply _Xkt_ to get _|iâŸ©_ ï¿½ï¿½ _k_ 1 _â€²[. . . k] t[â€²] âˆ’_ 1[0] _[t]_[0] _[ . . .]_[ 0] ï¿½ _|j_ ( _i, k_ ) _âŸ©|_ 1 _âŸ©o_ . Repeat this for all _m_ bits of the _k_ register gives us 

**==> picture [473 x 30] intentionally omitted <==**

where SUB[1] _k_[means][subtracting][1][from][the] _[k]_[register.][This][is][the][desired][sparse][index][oracle.] In total, this circuit requires 

**==> picture [391 x 23] intentionally omitted <==**

qubits and _n_ + _âŒˆ_ log( _sr_ ) _âŒ‰â‰¤_ 2 _n_ uses of _cVc_ . We implement all these _cVc_ using data samples. To obtain a final error of _Ïµ_ , we set _Ïµ_ 2 = _Ïµ/n_ and therefore the total number of samples needed is 

**==> picture [440 x 27] intentionally omitted <==**

This completes the proof of Theorem D.21. 

## _c. Block encodings_ 

Apart from sparse oracles, block encodings are also widely used as the default access model for matrices in many quantum algorithms. Theorems D.19 and D.21 allows us to implement the sparse oracles of an _N_ - dimensional and _s_ -sparse matrix _A_ with error _Ïµ_ using _O_[Ëœ] ( _RNs_[3] _/Ïµ_ ) samples and _O_ (log _N_ ) qubits. In this section, we build on these to construct the block encoding of _A_ with essentially the same guarantees. We use the following lemma from [9] to convert sparse oracles into block encodings. 

**Lemma D.22** (Block encodings from sparse oracles [9, Lemma 48]) **.** _Let A âˆˆ_ C[2] _[n][Ã—]_[2] _[n] be an s-sparse matrix where each matrix element is bounded by one. Then, we can implement a unitary VA such that_ 

**==> picture [331 x 13] intentionally omitted <==**

_with one query to each of the sparse index oracles OA_[ind] _[,]_[row] _and OA_[ind] _[,]_[col] _and sparse element oracle OA_[ele] _[and][its] inverse OA_[ele] _[â€ ][,][using][O]_[(] _[n]_[ + log][2] _[.]_[5][(1] _[/Ïµ]_[))] _[additional][two][qubit][gates][and][O]_[(] _[b]_[ + log][2] _[.]_[5][(1] _[/Ïµ]_[))] _[ancilla][qubits.]_ This gives use the following result. 

**Lemma D.23** (Block encodings) **.** _Let A âˆˆ_ R _[N][Ã—][N] be an N -dimensional and s-sparse matrix with âˆ¥Aâˆ¥â‰¤_ 1 _. There is a unitary UA and its corresponding channel UA_ : _Ï â†’ UAÏUA[â€ ][that][block][encodes][A][with][Ïµ] error and âŒˆ_ log( _N_ ) _âŒ‰_ + 3 _ancilla qubits_ 

**==> picture [337 x 13] intentionally omitted <==**

_such that we can use O_ (log( _N_ ) + _b_ + log[2] _[.]_[5] (1 _/Ïµ_ )) _qubits and_ 

**==> picture [319 x 27] intentionally omitted <==**

_samples starting at any time t_ 0 _â‰¥_ 1 _from the matrix data generation process DA with repetition number R to implement a random unitary channel V satisfying_ 

**==> picture [298 x 11] intentionally omitted <==**

_where z_ 1 _, . . . , zt_ 0 _âˆ’_ 1 _are previously processed data samples. The data processing time per sample is_ polylog( _N,_ 1 _/Ïµ_ ) _. The same guarantee holds for implementing UA[â€ ][, cU][A][and][cU] A[ â€ ][.]_ 

64 

_Proof of Theorem D.23._ We instantiate the sparse oracles in Theorem D.22 using Theorems D.19 and D.21. In particular, Theorem D.22 asserts that we can construct a unitary _VA_ such that 

**==> picture [333 x 13] intentionally omitted <==**

with one query to each of the sparse index oracles _OA_[ind] _[,]_[row] and _OA_[ind] _[,]_[col] and sparse element oracle _OA_[ele][and][its] inverse _OA_[ele] _[â€ ]_[,][using] _[O]_[(] _[n]_[ + log][2] _[.]_[5][(1] _[/Ïµ]_[1][))][additional][two][qubit][gates][and] _[O]_[(] _[b]_[ + log][2] _[.]_[5][(1] _[/Ïµ]_[1][))][ancilla][qubits.][We] use QSVT to apply a linear function _f_ ( _x_ ) = _sx, x âˆˆ_ [ _âˆ’_ 1 _/s,_ 1 _/s_ ] with error _Ïµ_ 2 to _A/s_ . Since _âˆ¥Aâˆ¥â‰¤_ 1, we have _f_ ( _A/s_ ) = _A_ . The degree of this QSVT is _d_ = _O_ (log(1 _/Ïµ_ 2) _/_ (1 _/s_ )) = _O_ ( _s_ log(1 _/Ïµ_ 2)). This means that we can construct a unitary _UA_ such that 

**==> picture [411 x 13] intentionally omitted <==**

where we choose _Ïµ_ 2 = _Ïµ/_ 2 and _Ïµ_ 1 = Î˜( _Ïµ/_ ( _s_ log(1 _/Ïµ_ ))). This construction queries the sparse oracles _O_ ( _d_ ) = _O_ ( _s_ log(1 _/Ïµ_ )) times and uses _O_ ( _b_ + log[2] _[.]_[5] ( _s_ log(1 _/Ïµ_ ) _/Ïµ_ )) _â‰¤ O_ ( _b_ + log[2] _[.]_[5] ( _s/Ïµ_ )) ancilla qubits. 

Now, we instantiate these oracles in the construction of _UA_ by the quantum oracle sketching using Theorems D.19 and D.21 with _Ïµ_ 3 error in diamond distance. This yields a random unitary channel _V_ satisfying 

**==> picture [353 x 11] intentionally omitted <==**

where we choose _Ïµ_ 3 = Î˜( _Ïµ/_ ( _s_ log(1 _/Ïµ_ ))). The total number of samples needed is 

**==> picture [351 x 84] intentionally omitted <==**

The number of qubits needed is 

**==> picture [362 x 12] intentionally omitted <==**

The same guarantee holds for implementing _UA[â€ ][, cU][A]_[and] _[cU] A[ â€ ]_[by][reversing][the][evolution][time][or][adding][control] in each random gate. This completes the proof of Theorem D.23. 

**==> picture [117 x 9] intentionally omitted <==**

In addition to matrices, in many applications we also need to load in vectors of the form _[âƒ—] b_ = ( _b_ 1 _, . . . , bN_ ) _[T] âˆˆ_ R _[N]_ as quantum state. For example, to solve a linear system _Aâƒ—x_ = _[âƒ—] b_ , we need to prepare the state 

**==> picture [287 x 27] intentionally omitted <==**

sometimes referred to as the amplitude encoding of _[âƒ—] b_ . Such vectors are usually dense. In this section, we show that we can prepare the state corresponding to any vector _[âƒ—] b_ using an extension of quantum oracle sketching, which we call quantum state sketching. 

Before detailing our quantum state sketching algorithm, we first explain the challenge in reaching a unified state preparation procedure for any vector _[âƒ—] b_ . Using the techniques from previous sections, we can build the block encoding of the diagonal matrix diag( _[âƒ—] b/âˆ¥[âƒ—] bâˆ¥âˆž_ ) using _O_[Ëœ] ( _N_ ) samples. But preparing the state _|bâŸ©_ =[ï¿½] _[N] j_ =1 _[b][j][ |][j][âŸ©][/][âˆ¥][âƒ—b][âˆ¥]_[2][is][still][hard][if][we][only][have][access][to][this][block][encoding.][To][see][this,][consider][the] special case of _[âƒ—] b_ = (0 _, . . . ,_ 1 _, . . . ,_ 0) where the position of 1 is arbitrary yet unknown. Then the task of preparing _|bâŸ©_ using the block encoding is equivalent to Groverâ€™s unstructured search problem, which necessarily requires queryingËœ the block encoding â„¦( _âˆšN_ ) times. This will result in an undesirable total sample complexity of _O_ ( _N Â·_ ( _âˆšN_ )[2] ) = _O_[Ëœ] ( _N_[2] ). We note, however, that in this case _[âƒ—] b_ is a computational basis state and easy to prepare directly. This incomparability between block encoding access and state preparation access was also observed and elaborated in a recent work [177]. 

65 

On the other hand, if _[âƒ—] b_ is flat (i.e., _bj âˆˆ{Â±_ 1 _/âˆšN }_ ), we can directly apply diag( _[âƒ—] b/âˆ¥[âƒ—] bâˆ¥âˆž_ ) to _|_ + _[n] âŸ©_ and obtain diag( _[âƒ—] b/âˆ¥[âƒ—] bâˆ¥âˆž_ ) _|_ + _[n] âŸ©_ = _âˆšN_ diag( _[âƒ—] b_ ) _Â·_ ~~_âˆš_~~ 1 _N_ ï¿½ _Nj_ =1 _[|][j][âŸ©]_[=][ï¿½] _[N] j_ =1 _[b][j][ |][j][âŸ©]_[=] _[|][b][âŸ©]_[.][This][means][that][with][one][query][to][the] block encoding and thus _O_[Ëœ] ( _N_ ) samples, we can prepare the state _|bâŸ©_ , which is in sharp contrast to the previous case. Therefore, it is a priori unclear if there is a unified state preparation algorithm that works for any _[âƒ—] b_ , regardless of how flat it is. 

_âƒ—b_ usingIn the following, we answer this question in the affirmative and show how to prepare the state _O_ Ëœ( _N_ ) samples from its vector data generation process. Together with the block encoding _|bâŸ©_ for any vectorconstruction in the last section, this shows that vector data access is strictly stronger than both the diagonal block encoding access and access to the state preparation unitary. 

**Theorem D.24** (Quantum state sketching) **.** _Let[âƒ—] b_ = ( _b_ 1 _, . . . , bN_ ) _[T] âˆˆ_ R _[N] be any N -dimensional vector and |bâŸ©_ =[ï¿½] _jâˆˆ_ [ _N_ ] _[b][j][ |][j][âŸ©][/][âˆ¥][âƒ—b][âˆ¥]_[2] _[be][its][quantum][state.] There is a state preparation unitary U on S_ = _O_ (log _N_ ) _qubits and its corresponding channel U_ : _Ï â†’ UÏU[â€ ] satisfying_ 

**==> picture [276 x 12] intentionally omitted <==**

**==> picture [370 x 11] intentionally omitted <==**

**==> picture [303 x 27] intentionally omitted <==**

_samples starting at any time t_ 0 _â‰¥_ 1 _from the vector data generation process Dâƒ—b with repetition number R to implement a random unitary channel V that depends on the samples zt_ 0 _, . . . , zt_ 0+ _M âˆ’_ 1 _and some internal randomness Î¾ and satisfies_ 

**==> picture [315 x 13] intentionally omitted <==**

_where z_ 1 _, . . . , zt_ 0 _âˆ’_ 1 _are previously processed data samples and the inner expectation is over zt_ 0 _, . . . , zt_ 0+ _M âˆ’_ 1 _, Î¾. The data processing time per sample is_ polylog( _N,_ 1 _/Ïµ_ ) _. The same guarantee holds for implementing U[â€ ] and the controlled versions cU, cU[â€ ] ._ 

We motivate quantum state sketching by reexamining the above naive attempt in greater details. In the naive algorithm, we first assemble queries to the block encoding of diag( _[âƒ—] b/âˆ¥[âƒ—] bâˆ¥âˆž_ ) by approximating ï¿½ _j[e][itb][j][/][âˆ¥][âƒ—b][âˆ¥][âˆž][|][j][âŸ©âŸ¨][j][|][ , t]_[ =] _[ O]_[(] _[N]_[)][with][random][multi-controlled][phase][gates][of][the][form] _[e][itb][j][/][âˆ¥][âƒ—b][âˆ¥][âˆž][|][j][âŸ©âŸ¨][j][|]_[.][From][Theo-] rem D.16, we know that the sample complexity of doing so is controlled by the variance of the phase accumulation. Since the phase on each basis _|jâŸ©_ accumulates independently, the sample complexity is given by the sample size needed for the basis with the largest variance, which is _O_ ( _t_[2] (max _bj/âˆ¥[âƒ—] bâˆ¥âˆž_ )[2] _Â·_ 1 _/N_ ) = _O_ ( _N_ (max _bj/âˆ¥[âƒ—] bâˆ¥âˆž_ )[2] ). Then we apply the block encoding to _|_ + _[n] âŸ©_ and perform amplitude amplification to get _|bâŸ©_ . In doing so, we need to query the block encoding _O_ ( _âˆšN âˆ¥[âƒ—] bâˆ¥âˆž/âˆ¥[âƒ—] bâˆ¥_ 2) times. Due to the quadratic slowdown, this amounts to a total sample complexity of 

**==> picture [382 x 36] intentionally omitted <==**

Therefore, this algorithm only works when _[âƒ—] b_ is flat (max _j bj/âˆ¥[âƒ—] bâˆ¥_ 2 = 1 _/âˆšN_ ) and fails when there is a large gap between the 2-norm and infinite-norm (say when _[âƒ—] b_ is a computational basis, max _j bj/âˆ¥[âƒ—] bâˆ¥_ 2 = 1). 

From this detailed analysis, we see that the normalization in the block encoding _âˆ¥[âƒ—] bâˆ¥âˆž_ is actually not important (as long as it gives a valid block encoding) because it eventually cancels out. The reason that this algorithm fails is because the variance is controlled by max _j bj_ rather than _âˆ¥[âƒ—] bâˆ¥_ 2, which introduces a gap that impacts the total sample complexity. To circumvent this issue, an ideal state preparation algorithm should have its variance controlled by _âˆ¥[âƒ—] bâˆ¥_ 2 instead, in which case the total sample complexity amounts to _O_ ( _N_ ) as desired. 

The key idea in achieving this goal is to perform a Hadamard transform. Instead of preparing the state _|bâŸ©_ via block encoding, we first prepare the state _|b[â€²] âŸ©_ for the Hadamard transformed vector 

**==> picture [267 x 13] intentionally omitted <==**

and then apply the quantum gates _H[âŠ—][n]_ to obtain _|bâŸ©_ . We prepare _|b[â€²] âŸ©_ by performing amplitude amplification on _|_ + _[n] âŸ©_ using the block encoding of diag( _[âƒ—] b[â€²] /B_ ) with some normalization factor _B_ . This time, when we assemble 

66 

the block encoding, we are not using random samples of the diagonal matrix elements _[âƒ—] b[â€²]_ any more. Instead, we are using random samples of _[âƒ—] b_ , which is related to _[âƒ—] b[â€²]_ via a Hadamard transform. We will show that we can still implement the block encoding using _Z_ -string rotations (rather than multi-controlled phase gates), and the resulting variance is controlled by _âˆ¥[âƒ—] bâˆ¥_ 2 as desired. As a result, we obtain a unified state preparation algorithm with _O_[Ëœ] ( _N_ ) sample complexity for any vector. 

When the data samples are no longer IID, but coming from a hierarchical data generation process with repetition number _R_ , the above strategy does not work anymore. The reasons are as follows. As we have seen in quantum oracle sketching, there are two sources of error: the variance part and the bias part. Due to the Hadamard transformed variance structure, the variance can blow up by a factor much larger than the repetition number _R_ . Another issue comes from the different scaling of variance ( _âˆ¼ t_[2] _R/_ ( _MN_ )) and bias ( _âˆ¼ tR/M_ ) with evolution time _t_ . We need to choose _t_ at least _âˆ¼ N_ so that the bias part does not exceed the variance part too much. But such a large _t_ may forbid _t_ diag( _[âƒ—] b[â€²]_ ) from being a valid block encoding. We need _[âƒ—] b[â€²]_ to be roughly flat so that we can accommodate _t âˆ¼ N_ while ensuring the validity of block encoding. 

With these obstacles in mind, we introduce an additional random diagonal gate _Oh_ =[ï¿½] _jâˆˆ_ [ _N_ ][(] _[âˆ’]_[1)] _[h]_[(] _[j]_[)] _[ |][j][âŸ©âŸ¨][j][|]_ defined by a random Boolean function _h_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ . In particular, we prepare the state _|b[â€²] âŸ©_ for the randomized Hadamard transformed vector 

**==> picture [274 x 13] intentionally omitted <==**

We show that instantiating _Oh_ with _O_ (log _N_ )-wise independent functions suffice to make the whole procedure efficient and we arrive at Theorem D.24. Intuitively, these inserted random phases decouple different data samples to keep the variance controlled, and make _[âƒ—] b[â€²]_ roughly flat with high probability, thereby solving the issues caused by correlated data. 

Before diving into the quantum state sketching algorithm, we first introduce the standard _k_ -wise independent function based on polynomials and use it to prove some useful lemmas. 

**Lemma D.25** ( _k_ -wise independent functions with polynomials) **.** _Let n, k be positive integers. Let_ F2 _n be the finite field with_ 2 _[n] elements. Let c_ 0 _, . . . , ckâˆ’_ 1 _âˆˆ_ F2 _n be k uniformly random elements of_ F2 _n. We define the polynomial function_ 

**==> picture [301 x 30] intentionally omitted <==**

_to be the k-wise independent function seeded by_ ( _c_ 0 _, . . . , ckâˆ’_ 1) _. Then, for any k distinct inputs x_ 1 _, . . . , xk âˆˆ_ F2 _n, the distribution of_ ( _h[â€²]_ ( _x_ 1) _, . . . , h[â€²]_ ( _xk_ )) _is uniform over_ (F2 _n_ ) _[k] . Consequently, if we define h_ ( _x_ ) _âˆˆ{_ 0 _,_ 1 _} to be the first bit of h[â€²]_ ( _x_ ) _âˆˆ_ F2 _n, the distribution of_ ( _h_ ( _x_ 1) _, . . . , h_ ( _xk_ )) _is uniform over {_ 0 _,_ 1 _}[k] . Moreover, given kn bits that specify c_ 0 _, . . . , ckâˆ’_ 1 _, the phase oracle of the Boolean function h_ ( _x_ ) 

**==> picture [293 x 13] intentionally omitted <==**

_can be implemented using an O_ ( _n_ ) _-qubit quantum circuit with O_ ( _kn_[2] ) _two-qubit gates._ 

_Proof of Theorem D.25._ Note that from Lagrange interpolation, we know that the mapping from coefficients ( _c_ 0 _, . . . , ckâˆ’_ 1) _âˆˆ_ F2 _n_ to function values ( _h[â€²]_ ( _x_ 1) _, . . . , h[â€²]_ ( _xk_ )) _âˆˆ_ F2 _n_ is a bijection for fixed, distinct inputs ( _x_ 1 _, . . . , xk_ ). Therefore, ( _h[â€²]_ ( _x_ 1) _, . . . , h[â€²]_ ( _xk_ )) is uniformly distributed because ( _c_ 0 _, . . . , ckâˆ’_ 1) is. Consequently, the first bits of ( _h[â€²]_ ( _x_ 1) _, . . . , h[â€²]_ ( _xk_ )) are also uniformly distributed. 

Moreover, given _kn_ bits that specify _c_ 0 _, . . . , ckâˆ’_ 1, we can use _O_ ( _n_ ) working bits (iterative, in-place computation _z â† zx_ + _cl_ ) and _O_ ( _kn_[2] ) two-bit gates ( _O_ ( _n_[2] ) for a single multiplication) to compute the arithmetic in the polynomial. Promoting the classical circuit to a quantum circuit gives the desired implementation of _Oh_ . 

Using this _k_ -wise independent function _h_ , we prove that the vector _[âƒ—] b[â€²]_ = _H[âŠ—][n] Oh[âƒ—] b_ is roughly flat with high probability. 

**Lemma D.26** (Flattening with seeded randomized Hadamard transform) **.** _Let n be a positive integer and N_ = 2 _[n] . Let Î´ âˆˆ_ (0 _,_ 1 _/_ 2) _and k_ = _âŒŠ_ log( _N/Î´_ ) _âŒ‹. Let[âƒ—] b âˆˆ_ R _[N] be any vector. Let h_ : [ _N_ ] _â†’{_ 0 _,_ 1 _} be a_ (2 _k_ ) _- wise independent function with a length-_ (2 _kn_ ) _seed uniformly distributed over {_ 0 _,_ 1 _}_[2] _[kn] . Then, the randomized Hadamard transformed vector_ 

**==> picture [273 x 14] intentionally omitted <==**

_satisfies_ 

**==> picture [300 x 25] intentionally omitted <==**

_with probability at least_ 1 _âˆ’ Î´._ 

67 

_Proof of Theorem D.26._ Note that the components of _[âƒ—] b[â€²]_ reads 

**==> picture [371 x 28] intentionally omitted <==**

where _l Â· j_ is the inner product in the binary form and _h_ ( _j_ ) is the only source of randomness. For simplicity, we define 

**==> picture [284 x 23] intentionally omitted <==**

and therefore 

**==> picture [332 x 32] intentionally omitted <==**

We begin by bounding the moments of _b[â€²] l_[using][the][multinomial][expansion:] 

**==> picture [369 x 138] intentionally omitted <==**

where we have defined a truly random bitstring _r âˆˆ{_ 0 _,_ 1 _}[N]_ and used the fact that _h_ is a (2 _k_ )-wise independent pseudorandom function (Theorem D.25) and that within each expectation value there is at most 2 _k h_ ( _j_ )â€™s. Next, we note that in order for the expectation value to be non-zero, the _sj_ â€™s must be even, and in that case the expectation value is one. Let _sj_ = 2 _tj_ and we have 

**==> picture [445 x 110] intentionally omitted <==**

where we have used (2 _t_ )! = (2 _t_ ) _Â· Â· Â·_ ( _t_ + 1) _t_ ! _â‰¥_ 2 _[t] t_ !, the multinomial expansion,[ï¿½] _j[a]_[2] _lj_[=] _[âˆ¥][âƒ—b][âˆ¥]_[2] 2 _[/N]_[,][and][(] 2[2] _[k][k] k_[)] ![!][=] (2 _k_ ) _Â·Â·Â·_ 2 _[k]_ ( _k_ +1) _â‰¤_[(][2] 2 _[k][k]_[)] _[k]_ = _k[k]_ . Now, we invoke Markovâ€™s inequality: 

**==> picture [360 x 25] intentionally omitted <==**

Plugging in _w_ = _âˆ¥[âƒ—] bâˆ¥_ 2ï¿½2 log( _N/Î´_ ) _/N_ and _k_ = _âŒŠ_ log( _N/Î´_ ) _âŒ‹_ gives us 

**==> picture [345 x 31] intentionally omitted <==**

for each _l âˆˆ_ [ _N_ ]. Finally, a union bound over _l âˆˆ_ [ _N_ ] implies that 

**==> picture [343 x 31] intentionally omitted <==**

This proves Theorem D.26. 

68 

Now we are ready to prove Theorem D.24. 

_Proof of Theorem D.24._ We begin with a high level overview of the quantum state sketching algorithm. The first step is to run a space-efficient procedure to estimate _âˆ¥[âƒ—] bâˆ¥_ 2, which will be used later to ensure that block encodings are properly normalized. In particular, we take _M[â€²]_ samples _zt_ 0 _,...,t_ 1 _âˆ’_ 1 _, t_ 1 = _t_ 0 + _M[â€²]_ and maintain an empirical average _B_ of _b_[2] _j_[.][We][will][show][that,][with][high][probability,] _[B]_[concentrates][around] _[âˆ¥][âƒ—b][âˆ¥]_[2] 2[.] 

Next, to prepare _|bâŸ©_ , we first sample a random seed ( _c_ 0 _, . . . , c_ 2 _k_ ) uniformly from _{_ 0 _,_ 1 _}_[2] _[kn]_ with _k_ = _âŒŠ_ log( _N/Î´_ ) _âŒ‹_ ( _Î´_ will be chosen later) and store the random seed in the classical memory, which uses 2 _kn_ = _O_ ( _n_ log( _N/Î´_ )) bits of space. This specifies a (2 _k_ )-wise independent function _h_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ that we can efficiently compute (classically or quantumly) with _O_ ( _n_ ) (qu)bits and _O_ ( _kn_[2] ) gates (Theorem D.25). Then we draw _M_ 0 samples ( _jl, bjl_ ) _[t] l_ =[1][+] _t_ 1 _[M]_[0] _[âˆ’]_[1] from the vector stream of _[âƒ—] b_ . With each sample, we compute _h_ ( _jl_ ) on the fly and apply a gate 

**==> picture [331 x 37] intentionally omitted <==**

for some _t_ = _O_ ( _N/_ ~~ï¿½~~ 2 _B_ log( _N/Î´_ )) (cf. Theorem D.26), where supp( _jl_ ) = _{w âˆˆ_ [ _n_ ] : ( _jl_ ) _w_ = 0 _}_ is the support of the bitstring _jl_ , and _Zw_ is the Pauli _Z_ on the _w_ -th qubit. Note that these _Vl_ gates commute with each other. We will show that with _M_ 0 = _O_[Ëœ] ( _RN/Ïµ_ 1) samples, this gives us _Ïµ_ 1-approximate oracle access to the unitary 

**==> picture [332 x 25] intentionally omitted <==**

_N_ Next, we use linear combination of unitaries and QSVT to build the block encoding of ï¿½ 4 _B_ log( _N/Î´_ )[diag(] _[âƒ—b][â€²]_[).] We then apply it to _|_ + _[n] âŸ©_ and perform amplitude amplification to get _|b[â€²] âŸ©_ . Finally, we apply the quantum gates ( _H[âŠ—][n] Oh_ ) _[â€ ]_ = _OhH[âŠ—][n]_ and arrive at _|bâŸ©_ . We will show that with a total sample complexity of _M_ = _O_[Ëœ] ( _RN/Ïµ_ ), this algorithm prepares a state that is _O_ ( _Ïµ_ )-close to _|bâŸ©_ with probability at least 1 _âˆ’ O_ ( _Ïµ_ ). This implies that the overall error in trace distance is _O_ ( _Ïµ_ ). 

**Norm estimation.** To show the correctness of this algorithm, we first analyze the norm estimation step, where we maintain an empirical sum 

**==> picture [287 x 32] intentionally omitted <==**

This estimator has expectation value 

**==> picture [313 x 31] intentionally omitted <==**

To bound its variance, we rearrange the terms in _B_ as 

**==> picture [341 x 33] intentionally omitted <==**

where 

**==> picture [299 x 33] intentionally omitted <==**

is the frequency of seeing a particular _j_ from time _t_ 0 to _t_ 0 + _M[â€²] âˆ’_ 1. According to Theorem C.4, the repetition number _R_ guarantees that the variance of _nj_ is bounded by 

**==> picture [278 x 21] intentionally omitted <==**

with expectation value E[ _nj_ ] = 1 _/N_ . Then, the variance of _B_ is bounded by 

**==> picture [479 x 31] intentionally omitted <==**

69 

Markovâ€™s inequality then implies that 

**==> picture [446 x 29] intentionally omitted <==**

We take _M[â€²]_ = 4 _RN/Î´_ , we have that with probability at least 1 _âˆ’ Î´_ , 

**==> picture [287 x 21] intentionally omitted <==**

In the following, we assume that this condition is satisfied and take the failure probability 

Pr[fail on norm estimation] _â‰¤ Î´_ (D248) 

into account at the end. Note that here this failure probability is not conditioned on and therefore is averaged over previously processed data samples _z<t_ 0 = ( _z_ 1 _, . . . , zt_ 0 _âˆ’_ 1). 

**Quantum oracle sketching.** Next, we explain why the _Vl_ gates can be used to build the block encoding of diag( _[âƒ—] b[â€²]_ ). The components of the two vectors _[âƒ—] b,[âƒ—] b[â€²]_ are connected via the following relation: 

**==> picture [366 x 27] intentionally omitted <==**

where _u Â· j_ is the bit-wise inner product of the bitstring representations of _u, j âˆˆ_ [ _N_ ] _â‰ƒ{_ 0 _,_ 1 _}[n]_ . Note that for any basis state _|uâŸ© , u âˆˆ{_ 0 _,_ 1 _}[n]_ , 

**==> picture [408 x 25] intentionally omitted <==**

Therefore, 

**==> picture [316 x 24] intentionally omitted <==**

This means that the gate _Vl_ that we apply for each sample can be rewritten as _Vl_ = exp[ _iHl_ ] with the Hamiltonian 

**==> picture [328 x 55] intentionally omitted <==**

The point of this rewriting is to show that the expectation value of this Hamiltonian is 

**==> picture [367 x 128] intentionally omitted <==**

where we used _b[â€²] u_[=][ ï¿½] _j_ ~~_âˆš_~~ 1 _N_[(] _[âˆ’]_[1)] _[h]_[(] _[j]_[)] _[b][j]_[(] _[âˆ’]_[1)] _[j][Â·][u]_[.][Now][we][invoke][quantum][oracle][sketching][to][show][that][the][gate] sequence we apply _Vt_ 1+ _M_ 0 _âˆ’_ 1 _Â· Â· Â· Vt_ 1 approximates _U_ in expectation. For simplicity, we introduce the following notations 

**==> picture [359 x 32] intentionally omitted <==**

70 

where the random matrix _X_ satisfies 

**==> picture [357 x 31] intentionally omitted <==**

In other words, for any sampled function _h_ , we have 

**==> picture [282 x 11] intentionally omitted <==**

We can also decompose _X_ in the computational basis _|uâŸ© , u âˆˆ_ [ _N_ ] as 

**==> picture [345 x 95] intentionally omitted <==**

where we have defined 

**==> picture [325 x 31] intentionally omitted <==**

to be the empirical phase accumulation on the basis _|uâŸ©_ . The approximation error conditioned on any fixed _h_ can again be decomposed into a variance part and a bias part using Theorem D.2 as 

**==> picture [414 x 133] intentionally omitted <==**

where _u[â€²]_ is the maximizer of Var[ _muâ€²|h, z<t_ 1] and we have used triangle inequality to change the condition from _z<t_ 0 to _z<t_ 1. We have also used Theorem D.7 and the law of total variance. 

**Variance bound.** Now we upper bound the variance part. For any _u_ , we first rewrite _mu_ as 

**==> picture [444 x 33] intentionally omitted <==**

According to Theorem C.4, the repetition number _R_ guarantees that the variance of _mj_ is bounded by 

**==> picture [285 x 23] intentionally omitted <==**

For simplicity, we define a vector _vu âˆˆ{Â±_ 1 _}[N]_ with components _vuj_ = ( _âˆ’_ 1) _[h]_[(] _[j]_[)+] _[j][Â·][u]_ and therefore _mu_ = ï¿½ _j[v][uj][b][j][m][j]_[.][Then][we][have] 

**==> picture [366 x 25] intentionally omitted <==**

where the matrix Î£ = Î£ _[T] âˆˆ_ R _[N][Ã—][N]_ has matrix elements 

**==> picture [300 x 13] intentionally omitted <==**

71 

Note that the matrix Î£ has trace 

**==> picture [325 x 28] intentionally omitted <==**

Frobenius norm 

**==> picture [465 x 31] intentionally omitted <==**

and operator norm 

**==> picture [300 x 23] intentionally omitted <==**

This allows us to invoke the moment bound for quadratic forms in Theorem D.5 (the randomness is over _vuj_ = ( _âˆ’_ 1) _[h]_[(] _[j]_[)+] _[j][Â·][u]_ where _h_ : [ _N_ ] _â†’{_ 0 _,_ 1 _}_ is a (2 _k_ )-wise independent function): 

**==> picture [419 x 34] intentionally omitted <==**

for some universal constant _C >_ 0. This is because the (2 _k_ )-th moment only involves (2 _k_ )-order terms of _h_ and therefore the (2 _k_ )-wise independence of _h_ ensures that moment is the same as when _h_ is truly random, which is given by Theorem D.5. Markovâ€™s inequality then implies that 

**==> picture [410 x 34] intentionally omitted <==**

**==> picture [484 x 56] intentionally omitted <==**

Taking a union bound over _u âˆˆ_ [ _N_ ], we obtain 

**==> picture [370 x 31] intentionally omitted <==**

This implies that with probability at least 1 _âˆ’ Î´_ over the choice of _h_ , 

**==> picture [468 x 47] intentionally omitted <==**

**Bias bound.** Next, for any _u_ , we express the bias term as 

**==> picture [463 x 83] intentionally omitted <==**

where we have defined the random variable 

**==> picture [299 x 12] intentionally omitted <==**

The 2 _k_ -th moment over the randomness of _h_ can be bounded by Theorem D.6 as 

**==> picture [410 x 42] intentionally omitted <==**

72 

for some universal constant _C >_ 0, where we have used the fact that _h_ is (2 _k_ )-wise independent. Note also that we have 

**==> picture [381 x 37] intentionally omitted <==**

Markovâ€™s inequality then implies that 

**==> picture [472 x 109] intentionally omitted <==**

Now we plug in _k_ = _âŒŠ_ log( _N/Î´_ ) _âŒ‹_ and choose _Ï‰_ = 2(max _j |_ âˆ† _j|_ ) _C[â€²] âˆ¥[âƒ—] bâˆ¥_ 2 log( _N/Î´_ ). Then we have 

Taking a union bound over _u âˆˆ_ [ _N_ ], we obtain that with probability at least 1 _âˆ’ Î´_ over the choice of _h_ , 

**==> picture [358 x 38] intentionally omitted <==**

for any _u_ . This means that 

**==> picture [404 x 32] intentionally omitted <==**

On the other hand, we have 

**==> picture [397 x 26] intentionally omitted <==**

from Theorem C.5. Hence, the bias part is bounded by 

**==> picture [369 x 32] intentionally omitted <==**

**Variance and bias combined.** Therefore, from the union bound we know that with probability at least 1 _âˆ’_ 2 _Î´_ over the random choice of _h_ , we have 

**==> picture [458 x 26] intentionally omitted <==**

If we choose 

**==> picture [330 x 31] intentionally omitted <==**

for some universal constant _C[â€²â€²] >_ 0, then with probability at least 1 _âˆ’_ 2 _Î´_ over _h_ , we have 

**==> picture [333 x 15] intentionally omitted <==**

In particular, we take 

**==> picture [339 x 31] intentionally omitted <==**

Note that we always have _M_ 0 _â‰¥_ 1 even when _t_ is very small. The same guarantee holds for implementing _U[â€ ] , cU, cU[â€ ]_ by setting _t â†’âˆ’t_ or adding control. 

73 

**Block encoding.** Now, we use this _Ïµ_ 1-approximation to _U_ = exp _it_ diag( _[âƒ—] b[â€²]_ ) _/âˆšN_ to implement a block ï¿½ ï¿½ encoding of ï¿½ 4 _B_ log( _N N/Î´_ )[diag(] _[âƒ—b][â€²]_[).][Thanks][to][Theorem][D.17][,][even][though][we][have][correlated][data,][the][error] still accumulates additively. Note that ~~ï¿½~~ 4 _B_ log( _N N/Î´_ )[diag(] _[âƒ—b][â€²]_[) can be block encoded without further normalization] with probability at least 1 _âˆ’ Î´_ over _h_ , because its norm is bounded by 

**==> picture [459 x 32] intentionally omitted <==**

where we have used _B â‰¥_ 2[1] _[âˆ¥][âƒ—b][âˆ¥]_ 2[2][and][the][fact][that] _[ âƒ—b][â€²]_[is][flat][with][high][probability][(Theorem][D.26][).][To][implement] the block encoding, we set 

**==> picture [286 x 26] intentionally omitted <==**

**==> picture [484 x 148] intentionally omitted <==**

samples, where we have used _B â‰¥_[1] 2 _[âˆ¥][âƒ—b][âˆ¥]_ 2[2][.] 

**Amplitude amplification.** Note that if we apply the block encoding of ï¿½ 4 _B_ log( _N N/Î´_ )[diag(] _[âƒ—b][â€²]_[)][to][the][state] _|_ + _âŸ©[n]_ , we obtain 

**==> picture [448 x 68] intentionally omitted <==**

That is, we can prepare the state _|b[â€²] âŸ©_ with probability _âˆ¥[âƒ—] bâˆ¥_ 2[2] _[/]_[(4] _[B]_[ log(] _[N/Î´]_[)).][To][prepare] _[ |][b][â€²][âŸ©]_[deterministically,][we] employ the standard (fixed-point) amplitude amplification [10] against the state _|_ + _âŸ©[n]_ (which can be efficiently prepared by _H[âŠ—][n] |_ 0 _[n] âŸ©_ ). This allows us to prepare the state _|b[â€²] âŸ©_ with _Ïµ_ 3 error in trace distance using 

**==> picture [393 x 73] intentionally omitted <==**

queries to the block encoding of ~~ï¿½~~ 4 _B_ log( _N N/Î´_ )[diag(] _[âƒ—b][â€²]_[).][We][implement][these][block][encoding][queries][with][the] above (2 _Ïµ_ 2)-approximations and set _Ïµ_ 2 = _Ïµ_ 3 _/Q[â€²]_ . This gives us a (2 _Ïµ_ 3)-approximation to the state _|b[â€²] âŸ©_ using 

**==> picture [411 x 60] intentionally omitted <==**

74 

samples. Finally, we apply the gate _OhH[âŠ—][n]_ and obtain a (2 _Ïµ_ 3)-approximation to the state _|bâŸ©_ . This is possible because we are storing the seed of _h_ in classical memory all along, and _Oh_ can be efficiently implemented on _O_ ( _n_ ) qubits with _O_ ( _kn_[2] ) = _O_ ( _n_[2] log( _N/Î´_ )) gates. 

The above error analysis applies with probability _p_ succ _â‰¥_ 1 _âˆ’_ 4 _Î´_ over the random choice of _h_ and the random estimation of _B_ . We use _Ï_ succ to denote the output state when the error analysis applies (i.e., the variance bound, bias bound, and flattening hold) and use _Ï_ fail to denote the output state when it does not apply. Then the overall output state is 

**==> picture [311 x 11] intentionally omitted <==**

where we have shown 

**==> picture [312 x 11] intentionally omitted <==**

This implies that 

**==> picture [440 x 54] intentionally omitted <==**

where we set _Ïµ_ 3 = _Î´_ = _Ïµ/_ 10. The total sample complexity is 

**==> picture [441 x 27] intentionally omitted <==**

The same holds for state unpreparation and the controlled versions by inverting the above state preparation procedure and adding control to each gate. This concludes the proof of Theorem D.24. 

75 

**==> picture [484 x 334] intentionally omitted <==**

**----- Start of picture text -----**<br>
(a) Noisy Oracle Property Estimation (NOPE) (b) M samples situation 0 situation 1 situation 0<br>1 1010100 0 0001011 samples â†’ N samples â†’ N samples â†’ N<br>... ... ... ... Â· Â· Â· Â· Â· Â· Â· Â· Â· Â· Â· Â·<br>S  bits<br>memory<br>x 0101001 1 1110100<br>Information flow between situations  â†’ O ( M/N )  Â· S<br>... ... ... ...<br>(c) A query algorithm that simulates learning deficiency<br>N 0001011 0 1000111 query query<br>oracle fake fake<br>Y [(0)] o Y [(1)] Â· Â· Â· progress<br>still good<br>Data: situation Ï‰Ï‰  = 0 = 1 â†’N ( x, Y sample x [(] [Ï‰] [)] , Ï‰ ) query Â· Â· Â· querytoo fake # query â‰¤ ignor. of info flowâ‰¤  O ( M/N )  Â· S<br>oracle  o fake samples<br>Task: given data, estimate some property of  o o MS â†’ !( NQC )<br># query â‰¥ QC fix and update<br>FIG. 7: Overview of the classical hardness proof strategy. (a)  Illustration of the Noisy Oracle Property Estimation<br>(NOPE) task. We encode the truth table of an oracle o âˆˆ{ 0 ,  1 } [N] as noisy encodings Y [(0)] , Y [(1)] . The task is to estimate<br>some property of the oracle o using random query data of the noisy encoding ( x, Yx [(] [Î±] [)] , Î± ) that depends on the current<br>situation Î± which changes with time scale N . (b) Visualization of the information flow during the learning process of<br>a classical learning algorithm that has memory size S and sample complexity M . The information flow between the<br>two situations is bounded by the number of situation changes O ( M/N ) times S , the communicated number of bits per<br>situation change. (c) Reduction from query algorithms to learning algorithms. We construct a query algorithm that<br>calculates the desired oracle property by simulating a learning algorithm that solves the corresponding NOPE task. The<br>query algorithm fakes data samples to feed into the learning algorithm and occasionally queries the oracle to update its<br>data forging strategy. The number of queries it makes is lower bounded by the classical query complexity QC , while<br>upper bounded by its ignorance of the information flow within the learning algorithm. This leads to the sample-space<br>lower bound MS â‰¥ â„¦( NQC ).<br>**----- End of picture text -----**<br>


## **Appendix E: Classical hardness** 

In this section, we develop the machinery for proving classical hardness in classical data processing tasks, summarized in Figure 7. We will define a learning task and prove that any classical machine that solves this task with a reasonable amount of samples must have exponentially large size, and moreover if it has slightly smaller size, it will need super-polynomially more samples. Later in Section F, we will reduce various application tasks (e.g., solving linear systems, classification, dimension reduction, etc.) to this learning task and therefore show the classical hardness of these applications. In particular, we focus on a specific family of learning tasks called Noisy Oracle Property Estimation (NOPE). It can be viewed as a noisy learning version of any oracle query problem. We introduce NOPE and its data generation process in Section E 1. In Section E 2, we provide a brief recap of the formal model of classical learning algorithms that we defined in Section C and will prove hardness against. 

In Section E 3, we prove a sample-space lower bound that shows any classical machine solving NOPE with a reasonable amount of data must have a size lower bounded by the classical query complexity of the oracle property estimation task, which is usually exponential. 

Then, in Section E 4, we build upon this sample-space lower bound and bootstrap it by adding one more time scale into the task. In particular, we define a new task called dynamic NOPE, where the oracle changes dynamically over time and yet the property that we want to estimate remains fixed. This allow us to prove that any classical machine with a slightly smaller size must need a super-polynomially larger sample size to solve the task. 

Finally, in Section E 5, we specialize NOPE tasks to the query problem of Forrelation, and prove several useful lemmas that connect NOPE to the various applications. These results will be used in Section F to reduce application tasks to NOPE and dynamic NOPE, whose classical hardness is already established in this section. 

76 

## **1. Noisy oracle property estimation** 

We begin by formally introduce the Noisy Oracle Property Estimation (NOPE) task. Intuitively, the task is to estimate some property of an oracle (i.e., a Boolean function) 

**==> picture [295 x 11] intentionally omitted <==**

based on noisy data samples generated from it. The oracle _o_ can be equivalently represented by its truth table 

**==> picture [267 x 12] intentionally omitted <==**

where _ox_ = _o_ ( _x_ ) _, âˆ€x âˆˆ_ [ _N_ ]. Suppose the property that we are interested in is binary and is specified by a property function 

**==> picture [309 x 13] intentionally omitted <==**

that takes an oracle _o âˆˆ{_ 0 _,_ 1 _}[N]_ as input and outputs its property _f_ ( _o_ ) _âˆˆ{_ 0 _,_ 1 _}_ . Here, this property function may be a partial function, meaning that it may be defined only for a subset of possible oracles _O âŠ†{_ 0 _,_ 1 _}[N]_ . One can equivalently think of this property function _f_ as a query algorithm that queries the oracle _o_ and computes the property _f_ ( _o_ ). 

In a learning task, we do not have direct knowledge of the underlying oracle _o_ and cannot make queries as we wish. Instead, we have access to a sequence of noisy data samples _zi_ generated according to _o_ , based on which we need to estimate the property _f_ ( _o_ ). In general, the data generation process may have correlation with multiple time scales, as described by hierarchical data generation processes introduced in Section C 1. A good learning algorithm should be able to process the data samples _zi_ and output the desired property _f_ ( _o_ ) with high probability, for any oracle _o_ . 

To define NOPE, we consider a noisy hierarchical data generation process. We first introduce our noise model by defining a _noisy encoding_ ( _Y_[(0)] _, Y_[(1)] ) of the oracle _o_ according to a noisy encoding function _g_ . Let _b_ be a positive integer specifying the encoding length. We define the noisy encoding function 

**==> picture [304 x 12] intentionally omitted <==**

to be a function that obfuscates the oracle value _ox âˆˆ{_ 0 _,_ 1 _}_ (i.e., the output of _g_ ) by providing a bipartite length-2 _b_ encoding of it (i.e., the two input arguments of _g_ ). This encoding function _g_ is noisy (or obfuscating), in the sense that we require _g_ to have a low discrepancy disc( _g_ ) _â‰¤_ 2 _[âˆ’][Î·b]_ for some constant _Î· >_ 0. This condition will be formally defined later (Theorem E.9), and it intuitively means that a partial input of _g_ (e.g., its first argument) cannot reveal too much information about the value of _g_ . An example of a noisy encoding function is the inner product function. We use 

**==> picture [335 x 12] intentionally omitted <==**

to denote the parallel application of _g_ across all _x âˆˆ_ [ _N_ ]. When _G_ maps some pair of inputs ( _Y_[(0)] _, Y_[(1)] ) into the oracle _o âˆˆ{_ 0 _,_ 1 _}[N]_ , we say that the input pair ( _Y_[(0)] _, Y_[(1)] ) is a noisy encoding of _o_ . 

Now we specify the data generation process. Given an oracle _o âˆˆ{_ 0 _,_ 1 _}[N]_ , we sample a noisy encoding 

**==> picture [312 x 13] intentionally omitted <==**

uniformly random, where _G[âˆ’]_[1] ( _o_ ) _âŠ†{_ 0 _,_ 1 _}[N][Ã—][b] Ã— {_ 0 _,_ 1 _}[N][Ã—][b]_ is the set of noisy encodings of the oracle and _Y_[(0)] _, Y_[(1)] _âˆˆ{_ 0 _,_ 1 _}[N][Ã—][b]_ . This noisy encoding ( _Y_[(0)] _, Y_[(1)] ) is fixed from now on and is used to generate the data samples. We consider the following hierarchical data generation process (defined in Section C 1) 

**==> picture [308 x 14] intentionally omitted <==**

where the data sample generated at each time point depends on the current binary situation _Î± âˆˆ{_ 0 _,_ 1 _}_ sampled from _D_[0] = Bern(1 _/_ 2). The situation changes slowly in time and only has a single time scale _T_ . For each situation _Î± âˆˆ{_ 0 _,_ 1 _}_ , we define _DÎ±_[1][to][sample][data][of][the][form] 

**==> picture [362 x 13] intentionally omitted <==**

where _x_ is a random query to the oracle and _y_ is a noisy encoding of the queries oracle value that depends on the situation _Î±_ . We choose the time scale _T â‰¥_ â„¦( _N_ ) to avoid the situation changing too rapidly so that the learning algorithm does not have the time to gather enough information about the current situation _Î±_ (i.e., about the noisy encoding _Y_[(] _[Î±]_[)] ). The notation _Dg,T[N]_[(] _[o]_[)][highlights][the][input][size] _[N]_[,][noisy][encoding][map] _[g]_[,][and] time scale _T_ of this data generation process. 

77 

With the noisy data generation process _Dg,T[N]_[(] _[o]_[),][we][define][the][Noisy][Oracle][Property][Estimation][(NOPE)] task as follows. 

**Task E.1** (Noisy Oracle Property Estimation (NOPE)) **.** _Let N, T, b be positive integers. Let f_ : _O â†’ {_ 0 _,_ 1 _} be a function that specifies the target property for a set of possible oracles O âŠ†{_ 0 _,_ 1 _}[N] . Let g_ : _{_ 0 _,_ 1 _}[b] Ã—{_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be a noisy encoding function. The task of Noisy Oracle Property Estimation is to calculate the desired property f_ ( _o_ ) _using data samples generated from the noisy hierarchical data generation process Dg,T[N]_[(] _[o]_[)] _[with][some][success][probability][for][any][o][ âˆˆO][.]_ 

In the following, we will prove classical hardness of NOPE. In particular, we will show sample and space lower bounds for any classical learning algorithms that solves NOPE with some success probability. 

## **2. Recap of classical learning algorithms** 

Before going into the classical hardness proofs, we first give a brief recap on the definition of classical learning algorithms that we will prove hardness for. More details can be found in Section C 2. 

Recall that in our definition of classical learning algorithms, there are two key resources that we keep track of: the size or space complexity of the classical machine _S_ and the sample complexity _M_ . We use _I_ to denote the set of all possible inputs to the learning algorithm at each time step. For NOPE defined above, _I_ = [ _N_ ] _Ã— {_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}_ , since the data is of the form _z_ = ( _x, y, Î±_ ). Throughout Section E 3, we assume such _I_ unless otherwise stated. It will change in Section E 4 when we introduce the dynamic version of NOPE. A classical learning algorithm _L_ with size _S_ , sample complexity _M_ , and input form _I_ is defined as a directed graph with vertices arranged in _M_ + 1 layers (0 to _M_ ). Each layer consists of at most 2 _[S]_ vertices, each labeled by _S_ bits. There is only one vertex called the root in layer 0. In layer _M_ , each vertex _v_ has no outgoing edges and is called a leaf. Each leaf _v_ is attached with an output _hv_ . For each layer _i_ = 0 _, . . . , M âˆ’_ 1, the outgoing edge from each vertex in layer _i_ only goes to vertices in layer _i_ + 1. Each vertex has _|I|_ outgoing edges, labeled by the possible input data at this time step. Upon receiving a sequence of data _Ii âˆˆI, i_ = 0 _, . . . , M âˆ’_ 1, the algorithm starts from the root, follows the edge given by each data point _Ii_ in layer _i_ until reaching a leaf _v_ in layer _M_ , and outputs _hv_ . 

To keep track of the information flow during learning, we define the _transcript Ï€L_ ( _I, Î±_ ) of the learning algorithm _L_ upon receiving the data sequence _I_ = ( _I_ 0 _, . . . , IM âˆ’_ 1) _âˆˆI[M]_ with respect to a situation record _Î±_ = ( _Î±_ 0 _, . . . , Î±M âˆ’_ 1) to be the concatenation of the length- _S_ bitstrings that label the vertices traversed by the computation path at layers _i_ where the situation changes _Î±i_ = _Î±i_ +1, followed by the output of _L_ . For our data generation process, suppose that the situation changes in total _r_ times and the output is a single bit _hv âˆˆ{_ 0 _,_ 1 _}_ , the transcript _Ï€L_ ( _I, Î±_ ) is a bitstring with total length _|Ï€L_ ( _I, Î±_ ) _|_ = ( _r_ + 1) _S_ + 1. Intuitively, it records a history of the state of the learning algorithm when situation changes. 

Since any randomized algorithm can always be regarded as first sampling all the random numbers and then execute the corresponding deterministic algorithm, the deterministic definition above suffices. Our definition of classical learning algorithms resemble the notion of branching programs. They are non-uniform models of space-bounded computation, more general than uniform ones such as online Turing machines with bounded space. Therefore, the classical hardness results we prove also applies to other weaker computational models. 

## **3. Sample-space lower bound** 

In this section, we prove a sample-space lower bound for any classical learning algorithms solving NOPE. The key quantity that will appear in the bound is the classical query complexity _QC_ of the property function _f_ ( _o_ ). This relates space complexity _S_ to query complexity _QC_ . We will show that the higher _QC_ is, the larger the sample-space product _MS_ has to be to solve NOPE. 

78 

**Theorem E.2** (Classical sample-space lower bound) **.** _Let N be a large integer. Let the time scale T be a positive integer. Let Î· âˆˆ_ (0 _,_ 2] _be a constant and c_ = (865 _/Î·_[2] ) logï¿½865 _/Î·_[2][ï¿½] _. Let g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’ {_ 0 _,_ 1 _} be a noisy encoding function with encoding length b â‰¥ c_ log _N and discrepancy_ disc( _g_ ) _â‰¤_ 2 _[âˆ’][Î·b] . Let f_ : _O â†’{_ 0 _,_ 1 _}, O âŠ†{_ 0 _,_ 1 _}[N] be a function that specifies the target property. Then, any randomized classical learning algorithm L that solves NOPE with probability at least_ 1 _âˆ’ Î´_ + 2 _[âˆ’][Î·b/]_[8] _must satisfy_ 

**==> picture [264 x 12] intentionally omitted <==**

_where Q[Î´] C[is][the][Î´][-error][classical][randomized][query][complexity][of][f][,][M][is][the][sample][complexity][of][L] and S is the space complexity of L._ 

We prove this with a simulation argument [92]. The intuition is as follows. We construct a query algorithm _A_ that simulates the learning algorithm _L_ by randomly guessing appropriate data and feed them into the learning algorithm. Intuitively, since the data generation process is sufficiently obfuscating, randomly guessing the data should be good enough even when we do not make queries to obtain any information about the underlying oracle. But as the algorithm proceeds, we have forged more fake data, and the state of the simulated learning algorithm gradually drifts away from the correct state. When the difference is significant enough, we query the oracle to fix this issue. We will show that with this strategy, the query algorithm correctly outputs _f_ ( _o_ ) with high probability, while the total query _Q_ it makes is bounded by the transcript length of the learning algorithm. On the other hand, any query algorithm satisfies _Q â‰¥ QC_ . Therefore, we have 

**==> picture [326 x 13] intentionally omitted <==**

In the following, we first prove some useful lemmas in Section E 3 a that will be used in the simulation argument. Then, we formalize the simulation argument in Section E 3 b and detail the constructed query algorithm in Algorithm 3. In Sections E 3 c and E 3 d, we prove the correctness and the query complexity bound of the constructed query algorithm. Finally, in Section E 3 e, we combine these ingredients to prove Theorem E.2. 

## _a. Preliminaries_ 

We use the notion of min-entropy and density [89, 90, 92] to characterize how uniform the distribution of a random string is. Intuitively, a random string is dense if every segment of it looks roughly uniform. 

**Definition E.3** (Min-entropy) **.** _Let Y âˆˆY be a discrete random variable. The min-entropy of Y , denoted as Hâˆž_ ( _Y_ ) _, is defined as_ 

**==> picture [351 x 12] intentionally omitted <==**

**Definition E.4** (Dense random variable) **.** _Let Y âˆˆ{_ 0 _,_ 1 _}[N][Ã—][b] be a random variable. Let Î´ âˆˆ_ (0 _,_ 1] _. We say Y is Î´-dense if for every I âŠ†_ [ _N_ ] _, it holds that Hâˆž_ ( _YI_ ) _â‰¥ Î´b|I|._ 

We can further keep track of finer structures of a dense random variable by the following notion of excess entropy [92]. It is non-negative because Pr[ _YI_ = _yI_ ] _â‰¤_ 2 _[âˆ’][Î´b][|][I][|]_ for any _I âŠ†_ [ _N_ ], by definition of _Î´_ -dense random variables. 

**Definition E.5** (Excess entropy) **.** _Let Y âˆˆ{_ 0 _,_ 1 _}[N][Ã—][b] be a Î´-dense random variable. Let I âŠ†_ [ _N_ ] _be a subset of coordinates. For every yI âˆˆ{_ 0 _,_ 1 _}[|][I][|Ã—][b] , we use eyI to denote the non-negative number that satisfies_ 

**==> picture [299 x 13] intentionally omitted <==**

The following are some useful properties of min-entropy. 

**Lemma E.6** (Conditional min-entropy) **.** _Let Y be a discrete random variable and let E be an event. Then,_ 

**==> picture [314 x 24] intentionally omitted <==**

**Lemma E.7** (Min-entropy of marginal) **.** _Let Y_ 1 _âˆˆY_ 1 _, Y_ 2 _âˆˆY_ 2 _be two discrete random variables. We have_ 

**==> picture [315 x 11] intentionally omitted <==**

79 

**Lemma E.8** (Min-entropy and flat distribution [92, Fact 2.4]) **.** _If a random variable has min-entropy at least k, then its distribution is a convex combination of k-flat distributions, where k-flat distributions are distributions that are uniformly distributed over a subset of the sample space of size at least_ 2 _[k] ._ 

We use discrepancy to describe how obfuscating the noisy encoding function _g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _}_ is. 

**Definition E.9** (Discrepancy) **.** _Let_ Î› _be a finite set. Let g_ : Î› _Ã—_ Î› _â†’{_ 0 _,_ 1 _} be a function. Let U, V be independent random variables uniformly sampled from_ Î› _. Given a rectangle R_ = _R_ 1 _Ã— R_ 2 _âŠ†_ Î› _Ã—_ Î› _, the discrepancy of g with respect to R, denoted as_ disc _R_ ( _g_ ) _, is_ 

**==> picture [396 x 11] intentionally omitted <==**

_The discrepancy of g, denoted as_ disc( _g_ ) _, is the maximum of_ disc _R_ ( _g_ ) _over all rectangles R_ = _R_ 1 _Ã— R_ 2 _âŠ†_ Î› _Ã—_ Î› _._ 

For any Boolean random variable _B_ , we use bias( _B_ ) = _|_ Pr[ _B_ = 0] _âˆ’_ Pr[ _B_ = 1] _|_ to denote its bias. Given a low discrepancy map _g_ , one would expect that its output is not very biased. So if the input variables _Y_[(0)] _, Y_[(1)] are roughly uniformly distributed, we expect the output to be roughly uniform as well. And the more uniform _Y_[(0)] _, Y_[(1)] are, the more uniform _g_ ( _Y_[(0)] _, Y_[(1)] ) will be. The tolerance of how biased _Y_[(0)] _, Y_[(1)] can be such that the above holds is limited by the discrepancy of _g_ . This idea is formalized in the following lemma. 

**Lemma E.10** (Low discrepancy maps preserve uniformity, [92, Lemma 2.9]) **.** _Let_ Î› _be a finite set. Let g_ : Î› _Ã—_ Î› _â†’{_ 0 _,_ 1 _} be a function with discrepancy_ disc( _g_ ) _â‰¤|_ Î› _|[âˆ’][Î·] , where Î· >_ 0 _. For any_ 0 _< Î» â‰¤ Î·, let Y_[(0)] _, Y_[(1)] _be independent random variables on_ Î› _with_ 

**==> picture [339 x 13] intentionally omitted <==**

## _Then_ 

**==> picture [303 x 12] intentionally omitted <==**

_Proof of Theorem E.10._ Due to Theorem E.8, we only need to prove the case when _Y_[(0)] _, Y_[(1)] have a flat distribution over a rectangle _R_ = _R_ 1 _Ã— R_ 2 with _|R| â‰¥|_ Î› _|_[2] _[âˆ’][Î·]_[+] _[Î»]_ . Let _U, V_ be independent random variables uniformly sampled from Î›. Then _U |U âˆˆ R_ 1 and _V |V âˆˆ R_ 2 have distribution the same as _Y_[(0)] and _Y_[(1)] . Therefore, 

**==> picture [415 x 45] intentionally omitted <==**

This proves Theorem E.10. 

One can also formalize this property in terms of sampling. When _Y_[(0)] _, Y_[(1)] are sufficiently uniform, if we sample an _Y_[(0)] = _y_ , then the bit _g_ ( _y, Y_[(1)] ) is roughly unbiased. 

**Lemma E.11** (Low discrepancy maps with random partial input preserve uniformity, [92, Lemma 2.10]) **.** _Let_ Î› _be a finite set. Let g_ : Î› _Ã—_ Î› _â†’{_ 0 _,_ 1 _} be a function with discrepancy_ disc( _g_ ) _â‰¤|_ Î› _|[âˆ’][Î·] , where Î· >_ 0 _. For any Î», Î³ >_ 0 _with Î»_ + _Î³ â‰¤ Î·, let Y_[(0)] _, Y_[(1)] _be independent random variables on_ Î› _with_ 

**==> picture [372 x 24] intentionally omitted <==**

_Then, the probability that Y_[(0)] _takes a value y âˆˆ_ Î› _such that_ 

**==> picture [295 x 13] intentionally omitted <==**

_is less than |_ Î› _|[âˆ’][Î³] ._ 

_Proof of Theorem E.11._ For every _y âˆˆ_ Î›, denote _py_ = Prï¿½ _g_ ( _y, Y_[(1)] ) = 1ï¿½. Our goal is to prove 

**==> picture [318 x 17] intentionally omitted <==**

We first show Prï¿½ _pY_ (0) _>_ 2[1][+][1] 2 _[|]_[Î›] _[|][âˆ’][Î»]_[ï¿½] _â‰¤|_ Î› _|[âˆ’][Î³] /_ 2; a symmetric argument implies Prï¿½ _pY_ (0) _<_[1] 2 _[âˆ’]_[1] 2 _[|]_[Î›] _[|][âˆ’][Î»]_[ï¿½] _â‰¤ |_ Î› _|[âˆ’][Î³] /_ 2. Then a union bound completes the proof. 

80 

Let _E_ = _{y âˆˆ_ Î› : _py >_ 2[1][+][1] 2 _[|]_[Î›] _[|][âˆ’][Î»][}]_[.][In][other][words,][Pr] ï¿½ _g_ ( _Y_[(0)] _, Y_[(1)] ) = 1 _|Y_[(0)] _âˆˆE_ ï¿½ _>_[1] 2[+][1] 2 _[|]_[Î›] _[|][âˆ’][Î»]_[.][Assume,] for the sake of contradiction, that Prï¿½ _Y_[(0)] _âˆˆE_ ï¿½ _â‰¥_ 2[1] _[|]_[Î›] _[|][âˆ’][Î³][.]_[This][implies] 

**==> picture [426 x 68] intentionally omitted <==**

By Theorem E.10, we have Prï¿½ _g_ ( _Y_[(0)] _, Y_[(1)] ) = 1 _|Y_[(0)] _âˆˆE_ ï¿½ _â‰¤_[1] 2[+][1] 2 _[|]_[Î›] _[|][âˆ’][Î»]_[,][which][contradicts][the][definition][of] _E_ . 

Sometimes it is easier to work with the parity of the output of _g_ over some coordinates. For any _I âŠ†_ [ _N_ ], we define _g[âŠ•][I]_ ( _y_[0] _, y_[1] ) _âˆˆ{_ 0 _,_ 1 _}_ to be the parity of _g[I]_ ( _y_[0] _, y_[1] ). The discrepancy of _g[âŠ•][I]_ is bounded by the discrepancy of _g_ . 

**Lemma E.12** (Discrepancy of parity, [178], [92, Theorem 2.11]) **.** _For any I âŠ†_ [ _N_ ] _, we have_ 

**==> picture [329 x 13] intentionally omitted <==**

This immediately implies properties of _g[âŠ•][I]_ that are similar to Theorems E.10 and E.11. 

**Corollary E.13.** _Let_ Î› _be a finite set. Let I âŠ†_ [ _N_ ] _. Let g_ : Î› _Ã—_ Î› _â†’{_ 0 _,_ 1 _} be a function with discrepancy_ disc( _g_ ) _â‰¤|_ Î› _|[âˆ’][Î·] , where Î· >_ 0 _. For any_ 0 _< Î» â‰¤ Î·, let Y_[(0)] _, Y_[(1)] _be independent random variables on_ Î› _[I] with_ 

**==> picture [363 x 25] intentionally omitted <==**

## _Then_ 

**==> picture [312 x 13] intentionally omitted <==**

**Corollary E.14.** _Let_ Î› _be a finite set. Let I âŠ†_ [ _N_ ] _. Let g_ : Î› _Ã—_ Î› _â†’{_ 0 _,_ 1 _} be a function with discrepancy_ disc( _g_ ) _â‰¤|_ Î› _|[âˆ’][Î·] , where Î· >_ 0 _. For any Î», Î³ >_ 0 _with Î»_ + _Î³ â‰¤ Î·, let Y_[(0)] _, Y_[(1)] _be independent random variables on_ Î› _[I] with_ 

**==> picture [372 x 25] intentionally omitted <==**

_Then, the probability that Y_[(0)] _takes a value y âˆˆ_ Î› _such that_ 

**==> picture [304 x 12] intentionally omitted <==**

_is less than |_ Î› _|[âˆ’][Î³][|][I][|] ._ 

The bias of parity is the Fourier coefficient of the distribution of random bitstrings. In particular, for a random bitstring _Z âˆˆ{_ 0 _,_ 1 _}[m]_ , let _Âµ_ : _{_ 0 _,_ 1 _}[m] â†’_ R be is probability mass function. We consider its Fourier transform _Âµ_ ( _z_ ) =[ï¿½] _SâŠ†_ [ _m_ ] _[Âµ]_[Ë†][(] _[S]_[)] _[Ï‡][S]_[(] _[z]_[),][where][the][character] _[Ï‡][S]_[(] _[z]_[)][=][(] _[âˆ’]_[1)] _[âŠ•][i][âˆˆ][S][z][i]_[and][the][Fourier][coefficient] _Âµ_ Ë†( _S_ ) = 21 _[m]_ ï¿½ _zâˆˆ{_ 0 _,_ 1 _}[m][ Âµ]_[(] _[z]_[)] _[Ï‡][S]_[(] _[z]_[).][We][define] _[âŠ•][i][âˆˆ][S][z][i]_[=][0][if] _[S]_[=] _[âˆ…]_[,][which][implies] _[Âµ]_[Ë†][(] _[âˆ…]_[)][=][2] _[âˆ’][m]_[.][We][have][the] following lemma. 

**Lemma E.15** (Fourier coefficient and parity bias) **.** _Let Z âˆˆ{_ 0 _,_ 1 _}[m] be a random variable with probability mass function Âµ_ : _{_ 0 _,_ 1 _}[m] â†’_ R _. Then for any S âŠ†_ [ _m_ ] _, we have_ 

**==> picture [297 x 26] intentionally omitted <==**

_Proof of Theorem E.15._ We have _|Âµ_ Ë†( _S_ ) _|_ = 21 _[m][|]_[ ï¿½] _z[Âµ]_[(] _[z]_[)(] _[âˆ’]_[1)] _[âŠ•][i][âˆˆ][S][z][i][|]_ = 21 _[m][|]_[ ï¿½] _z_ : _âŠ•iâˆˆS zi_ =0 _[Âµ]_[(] _[z]_[)] _[âˆ’]_ ï¿½ _z_ : _âŠ•iâˆˆS zi_ =1 _[Âµ]_[(] _[z]_[)] _[|]_[ =] 21 _[m][|]_[ Pr[] _[âŠ•][i][âˆˆ][S][z][i]_[= 0]] _[ âˆ’]_[Pr[] _[âŠ•][i][âˆˆ][S][z][i]_[= 1]] _[|]_[ =] 21 _[m]_[bias(][ï¿½] _iâˆˆS[Z][i]_[).] The following lemma shows that a rapidly decaying bias in the parity of subsets of coordinates (i.e., rapidly decaying Fourier coefficients) implies a nearly uniform distribution. 

81 

**Lemma E.16** (Variant of Vaziraniâ€™s lemma, [89], [92, Lemma 2.5]) **.** _Let Ïµ >_ 0 _and let Z âˆˆ{_ 0 _,_ 1 _}[m] be a random variable. If for every non-empty set S âŠ†_ [ _m_ ] _we have_ 

**==> picture [383 x 13] intentionally omitted <==**

_then for every z âˆˆ{_ 0 _,_ 1 _}[m] ,_ 

**==> picture [322 x 21] intentionally omitted <==**

_Proof of Theorem E.16._ Let _Âµ_ ( _z_ ) = Pr[ _Z_ = _z_ ]. Using Theorem E.15, we have 

**==> picture [335 x 225] intentionally omitted <==**

Therefore, (1 _âˆ’ Ïµ_ ) 2[1] _[m][â‰¤][Âµ]_[(] _[z]_[)] _[ â‰¤]_[(1 +] _[ Ïµ]_[)] 2[1] _[m]_[.] 

The above lemma can also be formulated in terms of min-entropy. 

**Lemma E.17** (Variant of Vaziraniâ€™s lemma in min-entropy, [92, Lemma 2.6]) **.** _Let t â‰¥_ 1 _be an integer and let Z âˆˆ{_ 0 _,_ 1 _}[m] be a random variable. If for every set S âŠ†_ [ _m_ ] _with |S| â‰¥ t we have_ 

**==> picture [381 x 12] intentionally omitted <==**

_then_ 

**==> picture [300 x 11] intentionally omitted <==**

_Proof of Theorem E.17._ The result holds trivially if _m_ = 1. Suppose _m â‰¥_ 2. Let _Âµ_ ( _z_ ) = Pr[ _Z_ = _z_ ]. By Theorem E.15, we have 

**==> picture [385 x 54] intentionally omitted <==**

Note that for _|S| â‰¥ t â‰¥_ 1, we have 

**==> picture [476 x 94] intentionally omitted <==**

For _|S| < t_ , we have 

where we have used _m â‰¥_ 2 in the last inequality. Therefore, _Âµ_ ( _z_ ) _â‰¤_ 2 _[âˆ’][m]_ ( _m[t] âˆ’_ 1 + 1) = 2 _[âˆ’][m]_[+] _[t]_[ log] _[ m]_ . Thus, we arrive at _Hâˆž_ ( _Z_ ) _â‰¥ m âˆ’ t_ log _m > m âˆ’ t_ log _m âˆ’_ 1. 

82 

We also need the following definition to fix certain coordinates of our estimate of the oracle _o âˆˆ{_ 0 _,_ 1 _}[N]_ when we query the true oracle. 

**Definition E.18** (Restriction) **.** _A restriction Ï is a string in {_ 0 _,_ 1 _, âˆ—}[N] . We say that a coordinate i âˆˆ_ [ _N_ ] _is free in Ï if Ïi_ = _âˆ—, and otherwise we say itâ€™s fixed. Given a restriction Ï we use_ free( _Ï_ ) _and_ fix( _Ï_ ) _to denote the free and fixed coordinates in Ï. We say that a string o âˆˆ{_ 0 _,_ 1 _}[N] is consistent with a restriction Ï if o_ fix( _Ï_ ) = _Ï_ fix( _Ï_ ) _._ 

Now we define a property that we want to keep during the simulation of the learning algorithm. This property ensures that our guessed encodings of the oracle are proper encoding consistent with the queried coordinates and are jointly dense. 

**Definition E.19** (Structure) **.** _Let Ï âˆˆ{_ 0 _,_ 1 _, âˆ—}[N] be a restriction. Let Ï„ âˆˆ_ (0 _,_ 1] _. Let Y_[(0)] _, Y_[(1)] _âˆˆ{_ 0 _,_ 1 _}[N][Ã—][b] be independent random variables. Let g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be a function. We say that Y_[(0)] _, Y_[(1)] _are_ ( _Ï, Ï„_ ) _-structured if there exist Î´_ 0 _, Î´_ 1 _>_ 0 _with Î´_ 0 + _Î´_ 1 _â‰¥ Ï„ such that_ 

**==> picture [97 x 17] intentionally omitted <==**

_2. Y_ free([(1)] _Ï_ ) _[is][Î´]_[1] _[-dense;]_ 

**==> picture [297 x 17] intentionally omitted <==**

The following uniform marginals lemma from [92, Lemma 3.4] formalizes the idea that for sufficiently obfuscating encoding map _g_ , randomly guessed encodings are good enough (in marginals) even when we know nothing about the true underlying oracle. 

**Lemma E.20** (Uniform marginals lemma, [92, Lemma 3.4]) **.** _Let b â‰¥ c_ log _N with some constant c >_ 0 _. Let g_ : _{_ 0 _,_ 1 _}[b] Ã—{_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be a function with_ disc( _g_ ) _â‰¤_ 2 _[âˆ’][Î·b] , and let G_ = _g[N]_ : _{_ 0 _,_ 1 _}[N][Ã—][b] Ã—{_ 0 _,_ 1 _}[N][Ã—][b] â†’{_ 0 _,_ 1 _}[N] . Let Ï âˆˆ{_ 0 _,_ 1 _, âˆ—}[N] be a restriction. Let_ 0 _< Î³ < Î· âˆ’_ 11 _/c. Let Y_[(0)] _, Y_[(1)] _be independent random variables uniformly distributed over Y_[(0)] _, Y_[(1)] _âŠ†{_ 0 _,_ 1 _}[N][Ã—][b] . Suppose they are_ ( _Ï, Ï„_ ) _-structured with_ 

**==> picture [290 x 11] intentionally omitted <==**

_Then, for any o âˆˆ{_ 0 _,_ 1 _}[N] consistent with Ï, consider the random variable_ ( _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] ) _uniformly distributed over G[âˆ’]_[1] ( _o_ ) _âˆ©_ ( _Y_[(0)] _Ã— Y_[(1)] ) _. We have that Y_[(0)] _, Y_[(1)] _are_ 2 _[âˆ’][Î³b] -close to Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] _in total variation distance, respectively._ 

We provide a proof of Theorem E.20 with refined constants for completeness. 

Ëœ _Proof of Theorem E.20._ We want to show that for any event _E âŠ†Y_[(0)] , ï¿½ï¿½ï¿½Prï¿½ _Y_[(0)] _âˆˆE_ ï¿½ _âˆ’_ Prï¿½ _Y_[(0)] _âˆˆE_ ï¿½[ï¿½] ï¿½ï¿½ _â‰¤_ 2 _âˆ’Î³b_ , which implies that the total variation distance is at most 2 _[âˆ’][Î³b]_ . Then the same holds for _Y_[(1)] by swapping _Y_[(0)] _, Y_[(1)] , and we are done. Without loss of generality, we can assume Prï¿½ _Y_[(0)] _âˆˆE_ ï¿½ _â‰¥_ 1 _/_ 2, since otherwise we can redefine _E_ to be the complement of _E_ . 

We first prove that when _Y_[(0)] _, Y_[(1)] are ( _Ï, Ï„_ )-structured, the random variable _g_[free(] _[Ï]_[)] ( _Y_ free([(0)] _Ï_ ) _[, Y]_ free([(1)] _Ï_ )[)][is] roughly uniformly distributed. Let _I_ = free( _Ï_ ). Let _S_ be any non-empty subset of _I_ . Since _b â‰¥ c_ log _N â‰¥ c_ , we have _Ï„ â‰¥_ 2 + 11 _/c âˆ’ Î·_ + _Î³ â‰¥_ 2 + 6 _/b âˆ’ Î·_ + _Î³_ + 2 _/c_ + 3 _/b_ . By Theorem E.19 and Theorem E.4, we have 

**==> picture [390 x 15] intentionally omitted <==**

By Theorem E.13, we have 

**==> picture [421 x 14] intentionally omitted <==**

where the last step follows from _N_[2] _â‰¥_ 2 _N â‰¥_ 2 _|I|_ and _|S| â‰¥_ 1. This holds for any non-empty _S âŠ† I_ . Therefore, by Theorem E.16, we have 

**==> picture [337 x 21] intentionally omitted <==**

Next, note that by Theorem E.6, we have that for any _I âŠ†_ [ _N_ ], _Hâˆž_ ( _YI_[(0)] _|Y_[(0)] _âˆˆE_ ) _â‰¥ Hâˆž_ ( _YI_[(0)] ) _âˆ’_ 1 log Pr[ _Y_[(0)] _âˆˆE_ ] _[â‰¥][H][âˆž]_[(] _[Y] I_[(0)] ) _âˆ’_ 1 _â‰¥ Hâˆž_ ( _YI_[(0)] ) _âˆ’_[1] _b[b][|][I][|]_[.][Therefore,][the][density][of] _[Y]_[(0)] _[|][Y]_[(0)] _[âˆˆE]_[is][at][most][1] _[/b]_ 

83 

lower than the density of _Y_[(0)] . This means that ( _Y_[(0)] _|Y_[(0)] _âˆˆE, Y_[(1)] ) is ( _Ï, Ï„ âˆ’_ 1 _/b_ )-structured. By the same reasoning above, we have 

**==> picture [357 x 21] intentionally omitted <==**

Note that from the Bayes formula, 

**==> picture [467 x 179] intentionally omitted <==**

where we have used 1 _/_ (1 _âˆ’ x_ ) _â‰¤_ 1 + 2 _x, âˆ€x âˆˆ_ (0 _,_ 1 _/_ 2]. Similarly, 

**==> picture [476 x 35] intentionally omitted <==**

**==> picture [466 x 19] intentionally omitted <==**

Theorem E.20 ensures that as long as our guesses of the encodings are dense, we can safely use them to generate fake data and feed them into the learning algorithm without knowing anything about the oracle. However, as the learning algorithm proceeds, the (posterior) distributions of our guesses will change since they are conditioned on the past computational path of the learning algorithm. This will cause them to lose density, and we need the following lemma to query the oracle and restore the density of our guesses. 

**Lemma E.21** (Density restoring partition, [89, Lemma 3.5][92, Lemma 3.7]) **.** _Let Î´ âˆˆ_ (0 _,_ 1] _. Let Y âˆˆ{_ 0 _,_ 1 _}[N][Ã—][b] be a random variable with support Y âŠ†{_ 0 _,_ 1 _}[N][Ã—][b] . Then there exists a partition Y_ = _Y_[1] _âˆªÂ· Â· Â· âˆªY[l] where every Y[j] is associated with a set of coordinates Ij âŠ†_ [ _N_ ] _and a value yIj âˆˆ_ ( _{_ 0 _,_ 1 _}[b]_ ) _[I][j] such that_ 

**==> picture [129 x 33] intentionally omitted <==**

_Moreover, if we use pâ‰¥j to denote_ Prï¿½ _Y âˆˆY[j] âˆªÂ· Â· Â· âˆªY[l]_[ï¿½] _, then_ 

**==> picture [352 x 24] intentionally omitted <==**

Moreover, note that we have two variables _Y_[(0)] _, Y_[(1)] to take care of. When we partition _Y_[(0)] and fix some of its values _YI_[(0)] = _yI_ to restore its density, we may destroy the density of _Y_[(1)] because we must keep consistency with _Ï, o_ (i.e., condition on _g[I]_ ( _yI , YI_[(1)] ) = _oI_ ). Such _yI_ â€™s that destroy the density of the other variable are called dangerous. We follow [92] and define them as follows. 

**Definition E.22** (Dangerous value) **.** _Let Î´ âˆˆ_ (0 _,_ 1] _, Ïµ âˆˆ_ (0 _, Î´_ ) _. Let Y âˆˆ{_ 0 _,_ 1 _}[N][Ã—][b] be a Î´-dense random variable. Let g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be a function. We say that a value y âˆˆ{_ 0 _,_ 1 _}[N][Ã—][b] is Ïµ-dangerous to Y if any one of the following conditions hold:_ 

**==> picture [374 x 12] intentionally omitted <==**

**==> picture [295 x 14] intentionally omitted <==**

84 

_2. there exists a set of coordinates I âŠ†_ [ _N_ ] _and an assignment oI âˆˆ{_ 0 _,_ 1 _}[|][I][|] such that_ 

**==> picture [281 x 13] intentionally omitted <==**

**==> picture [88 x 11] intentionally omitted <==**

The following lemma shows that as long as our guesses are structured, it is very unlikely for them to take a dangerous value. 

**Lemma E.23** (Dangerous values are unlikely, [92, Lemma 3.9]) **.** _Let b â‰¥ c_ log _N with some constant c >_ 0 _Let g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be a function with_ disc( _g_ ) _â‰¤_ 2 _[âˆ’][Î·b] . Let_ 0 _< Ï„, Ïµ, Î³ â‰¤_ 1 _with Ï„ â‰¥_ 2 + 17 _/_ ( _cÏµ_ ) _âˆ’ Î·_ + _Î³ and Ïµ >_ 4 _/b. Let Ï be a restriction. Let Y_[(0)] _, Y_[(1)] _be independent variables that are_ ( _Ï, Ï„_ ) _-structured. Then the probability that Y_ free([(0)] _Ï_ ) _[takes][a][value][that][is][Ïµ][-dangerous][to][Y]_ free([(1)] _Ï_ ) _[is][at][most]_[2] _[âˆ’][Î³b][.]_ 

We provide a proof of Theorem E.23 with refined constants for completeness. 

_Proof of Theorem E.23._ Without loss of generality, we assume that _Ï_ is all free. We introduce an auxiliary notion of _Ïµ_ -biasing values such that any values that are not _Ïµ_ -biasing are also not _Ïµ_ -dangerous. We will show that _Ïµ_ -biasing values are unlikely, and therefore so are _Ïµ_ -dangerous values. Let _Y_[(1)] be _Î´_ -dense. 

In particular, we say that a value _y_[0] _âˆˆ{_ 0 _,_ 1 _}[N][Ã—][b]_ is _Ïµ_ -biasing if there exists disjoint subsets _S âŠ†_ [ _N_ ] _, J âŠ†_ [ _N_ ] _âˆ’S_ and a value _yJ_[1] _[âˆˆ{]_[0] _[,]_[ 1] _[}][|][J][|Ã—][b]_[with] _[|][S][| â‰¥]_[(] _[Ïµb][|][J][|]_[ +] _[ e] yJ_[1] _[âˆ’]_[2)] _[/]_[ log] _[ N]_[such][that] 

**==> picture [338 x 21] intentionally omitted <==**

Here, _eyJ_ 1[is][the][excess][entropy][defined][in][Theorem][E.5][.] We first prove that if a value _y_[0] is not _Ïµ_ -biasing, then for any _I âŠ†_ [ _N_ ], we have Prï¿½ _g[I]_ ( _yI_[0] _[, Y]_[(1)][) =] _[ o][I]_ ï¿½ _â‰¥_ 2 _[âˆ’|][I][|âˆ’]_[1] , which violates the first condition in Theorem E.22. To this end, let _y_[0] be not _Ïµ_ -biasing. We take _J_ = _âˆ…_ in the definition of _Ïµ_ -biasing, and have bias( _g[âŠ•][S]_ ( _yS_[0] _[, Y] S_[(1)] )) _â‰¤_ 2[1][(2] _[N]_[)] _[âˆ’|][S][|]_[for][any] _[S][âŠ†]_[[] _[N]_[].][Theorem][E.16][then][implies] that 

**==> picture [350 x 25] intentionally omitted <==**

Therefore, non- _Ïµ_ -biasing implies violation of the first condition in Theorem E.22. 

Next, we show that non- _Ïµ_ -biasing also implies violation of the second condition in Theorem E.22. Suppose not, for the sake of contradiction. Then there exists a set of coordinates _I âŠ†_ [ _n_ ] and an assignment _oI âˆˆ{_ 0 _,_ 1 _}[|][I][|]_ such that _Y_ [[(1)] _N_ ] _âˆ’I[|]_[(] _[g][I]_[(] _[y] I_[0] _[, Y] I_[(1)] ) = _oI_ ) is not ( _Î´ âˆ’ Ïµ_ )-dense. By the definition of dense random variables and the definition of min-entropy, there exists _J âŠ†_ [ _N_ ] _âˆ’ I_ and a value _yJ_[1] _[âˆˆ{]_[0] _[,]_[ 1] _[}][|][J][|Ã—][b]_[such][that] 

**==> picture [342 x 19] intentionally omitted <==**

On the other hand, the left hand side satisfies 

**==> picture [421 x 72] intentionally omitted <==**

where we have used the violation of the first condition that we proved above. Therefore, 

**==> picture [356 x 19] intentionally omitted <==**

On the other hand, from the definition of non- _Ïµ_ -biasing, we know that for any disjoint non-empty sets _S, J âŠ†_ [ _N_ ] and value _yJ_[1] _[âˆˆ{]_[0] _[,]_[ 1] _[}][|][J][|Ã—][b]_[with] _[|][S][| â‰¥]_[(] _[Ïµb][|][J][|]_[ +] _[ e] yJ_[1] _[âˆ’]_[2)] _[/]_[ log] _[ N]_[,][we][have] 

**==> picture [364 x 21] intentionally omitted <==**

85 

Theorem E.17 (taking _m_ = _|I|, t_ = ( _Ïµb|J|_ + _eyJ_ 1 _[âˆ’]_[2)] _[/]_[ log] _[ N]_[)][then][implies][that] 

**==> picture [428 x 25] intentionally omitted <==**

where we have used log _|I| â‰¤_ log _N_ . This contradicts Equation (E51). Therefore, non- _Ïµ_ -biasing also violates the second condition in Theorem E.22. 

At this point, we have shown that non- _Ïµ_ -biasing implies violation of both conditions in Theorem E.22, which means that non- _Ïµ_ -biasing implies non- _Ïµ_ -dangerous. All we are left to show is that _Ïµ_ -biasing values are unlikely. To prove that _Ïµ_ -biasing values appear with probability at most 2 _[âˆ’][Î³b]_ , we use an union bound over the choice of _S, J, yJ_[1][.][We][assume] _[J]_[to][be][non-empty][(the][empty][case][works][similarly).] Let _S, J, yJ_[1][satisfy] 

**==> picture [324 x 27] intentionally omitted <==**

where we used _Ïµ â‰¥_ 4 _/b_ and _|J| â‰¥_ 1 in the second inequality. 

Since _Y_[(0)] _, Y_[(1)] are ( _Ï, Ï„_ )-structured, there exist _Î´_ 0 + _Î´_ 1 _â‰¥ Ï„_ such that _Y_[(0)] _, Y_[(1)] are _Î´_ 0 _, Î´_ 1-dense. So _Hâˆž_ ( _YS_[(1)] ) _â‰¥ Î´_ 1 _b|S|_ . Conditioning on _YJ_[(1)] = _yJ_[1][,][by][Theorem][E.6][,][we][have] 

**==> picture [404 x 137] intentionally omitted <==**

Therefore, 

**==> picture [472 x 22] intentionally omitted <==**

Then, by Theorem E.14 with _Î»_ = 3 _/_ ( _cÏµ_ ) _, Î³_ = _Î³_ + 5 _/_ ( _cÏµ_ ), we have that the probability of _YS_[(0)] taking a value _yS_[0] _[âˆˆ{]_[0] _[,]_[ 1] _[}][|][S][|Ã—][b]_[such][that] 

**==> picture [483 x 52] intentionally omitted <==**

Now we take the union bound. First we take the union bound over _J, yJ_[1][for][given] _[S]_[.] Note that _|J| â‰¤_ 1 _[âˆ’][e][y]_[1][We][have][the][upper][bound][for][having][large][bias][with][some] _[J, y][J]_[:] _Ïµb_[(] _[|][S][|]_[ log] _[ N] J[âˆ’]_[2)] _[ â‰¤]_[lo] _Ïµb_[g] _[ N][|][S][| â‰¤] Ïµc_[1] _[|][S][|][.]_ 

**==> picture [416 x 97] intentionally omitted <==**

where we have used _b â‰¥ c_ log _N, c â‰¥_ 1 _,[|] cÏµ[S][|][â‰¥]_[1][in][the][last][inequality.] Finally, we take union bound over non-empty _S âŠ†_ [ _N_ ]: 

**==> picture [421 x 29] intentionally omitted <==**

86 

where we used _cÏµb[â‰¥]_[log] _[ N]_[and][1] 2[2][(] _[Î³]_[+] _cÏµ_[1][)] _[b] â‰¥_ 2[1][2][log(] _[N]_[)] _[/Ïµ][â‰¥]_[1 for] _[ N][â‰¥]_[2.][This completes the proof of Theorem][ E.23][.] 

We will also need the following progress function called deficiency to prove query complexity bounds. 

**Definition E.24** (Deficiency) **.** _Let Y_[(0)] _, Y_[(1)] _âˆˆ{_ 0 _,_ 1 _}[N][Ã—][b] be two random variables. Given a restriction Ï âˆˆ {_ 0 _,_ 1 _, âˆ—}[N] , the deficiency of Y_[(0)] _, Y_[(1)] _is defined as_ 

**==> picture [386 x 16] intentionally omitted <==**

## _b. Simulation_ 

We are now ready to formalize the simulation argument and prove the following result. 

**Theorem E.25** (Simulation) **.** _Let N be a large integer. Let the time scale T be a positive integer. Let Î· âˆˆ_ (0 _,_ 2] _be a constant and c_ = (865 _/Î·_[2] ) logï¿½865 _/Î·_[2][ï¿½] _. Let g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be a noisy encoding function with encoding length b â‰¥ c_ log _N and discrepancy_ disc( _g_ ) _â‰¤_ 2 _[âˆ’][Î·b] . For any randomized classical learning algorithm L that has space complexity S and sample complexity M â‰¤_ 2 _NTb, there exists a randomized parallel decision tree A with query complexity_ 

**==> picture [259 x 24] intentionally omitted <==**

_such that given any input o âˆˆ{_ 0 _,_ 1 _}[N] , A outputs a random bitstring Ï€ whose distribution is_ 2 _[âˆ’][Î·b/]_[8] _-close in total variation distance with the distribution of the transcript of L when given data generated from Dg,T[N]_[(] _[o]_[)] _[.]_ 

It suffices to prove this for deterministic classical learning algorithms, since any randomized algorithm can always be regarded as first sampling all the random numbers and then execute the corresponding deterministic algorithm. Thus we can always construct the randomized decision tree by first sampling the random numbers and execute the decision tree obtained by applying the theorem to the corresponding deterministic learning algorithm. 

Given any deterministic classical learning algorithm _L_ , we construct the randomized decision tree _A_ as in Algorithm 3. Intuitively, we maintain a rectangle (i.e., a Cartesian product of two subsets) _Y_[(0)] _Ã— Y_[(1)] _âŠ† {_ 0 _,_ 1 _}[N][Ã—][b] Ã— {_ 0 _,_ 1 _}[N][Ã—][b]_ that represents guesses of the noisy encodings of the underlying oracle. We use the random variables _Y_[(0)] _, Y_[(1)] uniformly distributed on _Y_[(0)] _Ã— Y_[(1)] to generate fake data according to our guesses and feed them into the learning algorithm _L_ . Whenever the situation changes, we record the state of the learning algorithm _L_ and append it to the transcript _Ï€_ . Theorem E.20 ensures that this strategy works as long as our guesses _Y_[(0)] _, Y_[(1)] are dense. When they lose density, we invoke the density restoring partition from Theorem E.21 to restore their density. This requires us to query the oracle _o_ on the fixed coordinates to keep our guesses consistent with the true oracle. During the simulation, we also keep track of several error accumulation metric ( _K_ and _qji_ in Algorithm 3) to prevent extreme cases from happening: if they happen, we halt and declare error. We will show that such extreme cases happen rarely and this simulation outputs a transcript that is close to the correct transcript of _L_ (Section E 3 c) with the total query complexity bounded (Section E 3 d). We note that by construction, _Y_[(0)] _, Y_[(1)] are always ( _Ï, Ï„_ )-structured at the end of each iteration. 

## _c. Simulation is correct_ 

In this section, we prove that the output of the query algorithm _A_ matches the transcript of the learning algorithm _L_ in distribution. 

We first calculate the number of situation changes _r_ . Note that in the data generation process, each time we sample a new situation _Î±_ , we will keep using it to generate the data for _T_ time steps. Hence we must have _r â‰¤âŒŠM/T âŒ‹âˆ’_ 1. 

We aim to prove the correctness of Algorithm 3: for any input _o âˆˆ{_ 0 _,_ 1 _}[N]_ , the distribution of _A_ â€™s output _Ï€_ is 2 _[âˆ’][Î·b/]_[8] -close in total variation distance to the distribution of the transcript of _L_ given data generated from _Dg,T[N]_[(] _[o]_[).][We][follow][[][92][]][and][prove][this][in][two][steps.][We][define][three][different][transcripts:] 

1. _Ï€_ , the output of the query algorithm _A_ ; 

87 

## **Algorithm 3** Simulation 

**Input:** A deterministic classical learning algorithm _L_ with space complexity _S_ , sample complexity _M_ , and input form _I_ = [ _N_ ] _Ã— {_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}_ ; the data generation process _Dg,T[N]_[;][an][input] _[o][ âˆˆ{]_[0] _[,]_[ 1] _[}][N]_[.] **Output:** A learning algorithm transcript _Ï€_ . 

1: _Ïµ â†_ (96 log _c_ ) _/_ ( _cÎ·_ ). _Î´ â†_ 1 _âˆ’ Î·/_ 4 + _Ïµ/_ 2. _Ï„ â†_ 2 _Î´ âˆ’ Ïµ_ . 

2: Let _Ï€_ be the empty string. _Ï â†{âˆ—}[n]_ . _Y_[(0)] _, Y_[(1)] _â†{_ 0 _,_ 1 _}[N][Ã—][b]_ . 

3: Let _Y_[(0)] _âˆ¼_ Uniform( _Y_[(0)] ), _Y_[(1)] _âˆ¼_ Uniform( _Y_[(1)] ) be two independent random variables. 

4: _v â†_ root of _L_ . _K â†_ 0. 

5: Sample a full situation record _Î± â†_ ( _Î±_ 0 _, . . . , Î±M âˆ’_ 1) at time points 0 _, . . . , M âˆ’_ 1 from _Dg,T[N]_[.] 6: Compute the situation changing time 0 = _t_ 0 _< . . . < tr â‰¤ M âˆ’_ 1 where _Î±tiâˆ’_ 1 = _Î±ti , âˆ€i_ = 1 _, . . . , r_ . 7: **for** _i_ = 0 _, . . . , r âˆ’_ 1 **do** 8: Let _A â† Î±ti_ , _B â† Î±ti âŠ•_ 1. 9: _Y_[(] _[A]_[)] _â†Y_[(] _[A]_[)] _âˆ’{y âˆˆY_[(] _[A]_[)] : _y_ free( _Ï_ ) is _Ïµ_ -dangerous to _Y_ free([(] _[B]_[)] _Ï_ ) _[}]_[.][Let] _[Y]_[(] _[A]_[)] _[âˆ¼]_[Uniform(] _[Y]_[(] _[A]_[)][).] 10: **for** _t_ = _ti, . . . , ti_ +1 _âˆ’_ 1 **do** 11: Randomly sample _xt âˆ¼_ Uniform([ _N_ ]). Let _yt â† Yx_[(] _t[A]_[)] _âˆˆ{_ 0 _,_ 1 _}[b]_ . 12: _v â†_ the end point of the edge from _v_ in _L_ labeled by _It_ = ( _xt, yt, A_ ). 13: **end for** 14: Let _Âµi_ be the length- _S_ bitstring that labels _v_ in _L_ . Append _Âµi_ to _Ï€_ . 15: Let _pi_ be the probability of reaching _v_ in the above sampling process. _K â† K_ + log(1 _/pi_ ) 16: _Y_[(] _[A]_[)] _â†Y_[(] _[A]_[)] _âˆ’{y âˆˆY_[(] _[A]_[)] : the probability of reaching _v_ conditioned on _Y_[(] _[A]_[)] = _y_ is zero _}_ . Let _Y_[(] _[A]_[)] _âˆ¼_ Uniform( _Y_[(] _[A]_[)] ). 17: **if** _K >_ ( _r_ + 1) _S_ + _b_ **then** 18: **halt** and declare error 19: **end if** 20: Find the density restoring partition of the random variable _Y_[(] _[A]_[)] supported on _Y_[(] _[A]_[)] : ( _Y[j] , Ij, yIj_ ) _jâˆˆ_ [ _l_ ]. 21: Sample _ji âˆˆ_ [ _l_ ] with probability Prï¿½ _Y_ free([(] _[A]_[)] _Ï_ ) _[âˆˆY][j][i]_ ï¿½. 22: **if** _qji_ = Prï¿½ _Y_ free([(] _[A]_[)] _Ï_ ) _[âˆˆ]_[ï¿½] _kâ‰¥ji[Y][k]_[ï¿½] _<_ 8[1][2] _[âˆ’][Î·b/]_[8] _[ Â·]_ 2 _Nb_ 1 **[then]** 23: **halt** and declare error 24: **end if** 25: _Y_[(] _[A]_[)] _â†Y_[(] _[A]_[)] _âˆ’{y âˆˆY_[(] _[A]_[)] : _y_ free( _Ï_ ) _âˆˆY/[j][i] }_ . Let _Y_[(] _[A]_[)] _âˆ¼_ Uniform( _Y_[(] _[A]_[)] ). 26: Query _oIji_ and set _ÏIji â† oIji_ . 27: _Y_[(] _[B]_[)] _â†Y_[(] _[B]_[)] _âˆ’{y[B] âˆˆY_[(] _[B]_[)] : _g[I][ji]_ ( _yIji , yI[B] ji_[)] _[ Ì¸]_[=] _[ Ï][I] ji[}]_[.][Let] _[Y]_[(] _[B]_[)] _[âˆ¼]_[Uniform(] _[Y]_[(] _[B]_[)][).] 28: **end for** 29: Let _A â† Î±r_ , _B â† Î±r âŠ•_ 1 30: **for** _t_ = _tr, . . . , M âˆ’_ 1 **do** 31: Randomly sample _xt âˆ¼_ Uniform([ _N_ ]). Let _yt â† Yx_[(] _t[A]_[)] _âˆˆ{_ 0 _,_ 1 _}[b]_ . 32: _v â†_ the end point of the edge from _v_ in _L_ labeled by _It_ = ( _xt, yt, A_ ). 33: **end for** 

34: Append the output label _hv âˆˆ{_ 0 _,_ 1 _}_ of leaf _v_ in _L_ to _Ï€_ . 

35: **return** _Ï€_ 

2. _Ï€[â€²]_ , the output of a modified query algorithm _A[â€²]_ which is the same as _A_ except that it skips Lines 17-19 in Algorithm 3; and 

3. _Ï€[â‹†]_ , the target transcript of _L_ on the data generated from _Dg,T[N]_[(] _[o]_[).] 

We will first prove that _Ï€_ and _Ï€[â€²]_ are 2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] -close, and then prove that _Ï€[â€²]_ and _Ï€[â‹†]_ are 2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] -close. This immediately implies that _Ï€_ and _Ï€[â‹†]_ are 2 _[âˆ’][Î·b/]_[8] -close by triangle inequality. 

We start by showing that _Ï€_ and _Ï€[â€²]_ are 2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] -close. Let _EK_ be the event that _A_ halts in Lines 17-19. Then _âˆ€Ï„,_ Pr[ _Ï€_ = _Ï„ |Â¬EK_ ] = Pr[ _Ï€[â€²]_ = _Ï„_ ]. We have 

**==> picture [412 x 91] intentionally omitted <==**

To bound Pr[ _EK_ ], we note that in Algorithm 3, the value of _K_ at some iteration _i_ is calculated in the following sequential way: _Âµ_ 0 _â†’ p_ 0 _â†’ j_ 0 _â†’Â· Â· Â· â†’ Âµi â†’ pi â†’ K_ , where latter variables depend on every preceding 

88 

variables. We denote _Âµ<i_ = ( _Âµ_ 0 _, . . . , Âµiâˆ’_ 1) _, j<i_ = ( _j_ 0 _, . . . , jiâˆ’_ 1). If _A_ halts before _r_ , we set all the subsequent _Âµi_ = 0 _[S]_ and _ji_ = 1. Also note that _pi_ = Pr[ _Âµi|Âµ<i, j<i_ ]. Therefore, we have 

**==> picture [452 x 186] intentionally omitted <==**

Since _b â‰¥ c_ log _N_ is large and _Î· â‰¤_ 2, we have 2 _[âˆ’][b] â‰¤_ 2 _[âˆ’][b/]_[4] _[âˆ’]_[1] _â‰¤_ 2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] . Thus, we arrive at 

**==> picture [327 x 12] intentionally omitted <==**

Next, we show that _Ï€[â€²]_ and _Ï€[â‹†]_ are 2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] -close. We first fix any _Î±_ = ( _Î±_ 0 _, . . . , Î±M âˆ’_ 1) _âˆˆ{_ 0 _,_ 1 _}[M]_ and any _x_ = ( _x_ 0 _, . . . , xM âˆ’_ 1) _âˆˆ_ [ _N_ ] _[M]_ . Let _Ï€[â€²]_ ( _Î±, x_ ) be the transcript of _A[â€²]_ when the _Î±_ and _xt_ â€™s in _A[â€²]_ are replaced by corresponding entries in _Î±_ and _x_ . Similarly, let _Ï€[â‹†]_ ( _Î±, x_ ) be the transcript of _L_ when the _Î±_ and _xt_ â€™s in the generated data are replaced by corresponding entries in _Î±_ and _x_ . We will prove that _Ï€[â€²]_ ( _Î±, x_ ) and _Ï€[â‹†]_ ( _Î±, x_ ) are 2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] -close for any _x_ . Then averaging over random _Î±_ and _x_ over the fixed distributions (i.e., Bern(1 _/_ 2) and repeat _T_ times for _Î±_ , and Uniform([ _N_ ]) for _x_ ) immediately gives the desired result. 

We prove this by going through the simulation step by step and constructing a coupling between _Ï€[â€²]_ ( _Î±, x_ ) and _Ï€[â‹†]_ ( _Î±, x_ ) such that Pr[ _Ï€[â€²]_ ( _Î±, x_ ) _Ì¸_ = _Ï€_ ( _Î±, x_ ) _[â‹†]_ ] _â‰¤_ 2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] , which implies that _Ï€[â€²]_ ( _Î±, x_ ) and _Ï€[â‹†]_ ( _Î±, x_ ) are 2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] - close. Let ( _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] ) be the ideal random encodings uniformly distributed over _G[âˆ’]_[1] ( _o_ ). Let _Yi_[(0)] _Ã— Yi_[(1)] be the rectangle maintained in Algorithm 3 at the end of iteration _i_ = 0 _, . . . , r_ . If _A[â€²]_ halts early, we set subsequent _Yi_[(0)] _Ã— Yi_[(1)] to be the same as the last one before halting. Let _Yi_[(0)] _, Yi_[(1)] be uniformly distributed over _Yi_[(0)] _Ã— Yi_[(1)] (i.e., they are the _Y_[(0)] _, Y_[(1)] in Algorithm 3 at the end of iteration _i_ ). The idea is that, due to Theorem _Y_ Ëœ[(1)] . However, E.20, we should be able to construct good coupling betweenwe cannot use Theorem E.20 directly, because _Y_ Ëœ[(0)] and _Yi_[(0)] _Y_ Ëœ[(1)] andmay _Y_[Ëœ][(0)] not, and also betweenbe uniformly distributed _Yi_[(1)] and over _G[âˆ’]_[1] ( _o_ ) _âˆ©_ ( _Yi_[(0)] _Ã— Yi_[(1)] ). To address this issue, we introduce an intermediate random rectangle _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] coupled with _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] such that the distribution of _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] conditioned on a specific rectangle _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] is the uniform distribution over _G[âˆ’]_[1] ( _o_ ) _âˆ©_ ( _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] ). Then we show that with high probability, _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] coincides with _Yi_[(0)] _Ã— Yi_[(1)] . This allows us to use Theorem E.20 and construct the desired coupling. Concretely, we construct _Y_[Ëœ] _i_[(0)] _Ã—Y_[Ëœ] _i_[(1)] and the relevant coupling by induction. We set _Y_[Ëœ] _âˆ’_[(0)] 1 _[Ã—]_[ Ëœ] _[Y] âˆ’_[(1)] 1[=] _[ Y] âˆ’_[(0)] 1 _[Ã—Y] âˆ’_[(1)] 1[=] _{_ 0 _,_ 1 _}[N][Ã—][b] Ã— {_ 0 _,_ 1 _}[N][Ã—][b]_ . Suppose we have constructed _Y_[Ëœ] _i_[(0)] _âˆ’_ 1 _[Ã—][Y]_[Ëœ] _i_[(1)] _âˆ’_ 1[such][that][(1)][the][distribution][of] _[Y]_[Ëœ][(0)] _[,][Y]_[Ëœ][(1)] conditioned on a specific rectangle _Y_[Ëœ] _i_[(0)] _âˆ’_ 1 _[Ã—][Y]_[Ëœ] _i_[(1)] _âˆ’_ 1[is][the][uniform][distribution][over] _[G][âˆ’]_[1][(] _[o]_[)] _[ âˆ©]_[( Ëœ] _[Y] i_[(0)] _âˆ’_ 1 _[Ã—][Y]_[Ëœ] _i_[(1)] _âˆ’_ 1[),][and][(2)] Ëœ _[i][âˆ’]_[1] Prï¿½ _Yi_[(0)] _âˆ’_ 1 _[Ã—][Y]_[Ëœ] _i_[(1)] _âˆ’_ 1[=] _[ Y] i_[(0)] _âˆ’_ 1 _[Ã— Y] i_[(1)] _âˆ’_ 1ï¿½ _â‰¤_ 2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] 2 _Nb_[.][We][construct] _[Y]_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] as follows. Firstly, we sample _Y_[Ëœ] _i_[(0)] _âˆ’_ 1 _[Ã—][Y]_[Ëœ] _i_[(1)] _âˆ’_ 1[and] _[Y] i_[(0)] _âˆ’_ 1 _[Ã— Y] i_[(1)] _âˆ’_ 1[.][If][they][are][different,][we][set] _[Y]_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] = _{_ ( _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] ) _}_ and say that the coupling fails. Now suppose _Y_[Ëœ] _i_[(0)] _âˆ’_ 1 _[Ã—][Y]_[Ëœ] _i_[(1)] _âˆ’_ 1[=] _[ Y] i_[(0)] _âˆ’_ 1 _[Ã— Y] i_[(1)] _âˆ’_ 1[.][If] _[A][â€²]_[has][halted][at][this][point,][we][set] Ëœ _Yi_[(0)] _Ã— Y_[Ëœ] _i_[(1)] = _Yi_[(0)] _âˆ’_ 1 _[Ã— Y] i_[(1)] _âˆ’_ 1[.][Then][we][proceed][by][following][Algorithm][3][closely.][Let] _[A, B]_[be][the][corresponding] values in iteration _i_ . In Line 9, if either _Yi_[(] _âˆ’[A]_ 1[)][or] _[Y]_[Ëœ] _i_[(] _âˆ’[A]_ 1[)][is] _[Ïµ]_[-dangerous][to] _[Y] i_[(] _âˆ’[B]_ 1[)][,][we][set] _[Y]_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] = _{_ ( _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] ) _}_ . We note that 

89 

since _Yi_[(] _âˆ’[A]_ 1[)] _[, Y] i_[(] _âˆ’[B]_ 1[)][are][(] _[Ï, Ï„]_[)-structured][with] 

**==> picture [339 x 79] intentionally omitted <==**

where we have used _Ïµ_ =[96 lo] _cÎ·_[g] _[ c]_ , _Ïµ â‰¤_ 1, _b â‰¥ c_ log _N â‰¥ c_ , and log( _c_ ) _â‰¥_ log(2) = 1. Using Theorem E.23, we have that the probability of _Yi_[(] _âˆ’[A]_ 1[)][being] _[Ïµ]_[-dangerous][to] _[Y] i_[(] _âˆ’[B]_ 1[)][is][at][most] 

**==> picture [346 x 94] intentionally omitted <==**

where we have used log( _c_ ) _â‰¥_ 1, _b â‰¥ c_ log _N_ , and 2 _b â‰¥ c_ log( _b_ ) for large _N_ . Meanwhile, by Theorem E.20, _Yi_[(] _âˆ’[A]_ 1[)] is ( 8[1][2] _[âˆ’][Î·b/]_[8] 2 _Nb_ 1[)-close][to] _[Y]_[Ëœ] _i_[(] _âˆ’[A]_ 1[)][in][total][variation][distance.][Therefore,][the][total][probability][of][this][failure][is][at] most 2 _Â·_[1] 8[2] _[âˆ’][Î·b/]_[8] 2 _Nb_ 1[.][Suppose][this][failure][does][not][happen][and][neither] _[Y] i_[(] _âˆ’[A]_ 1[)][nor] _[Y]_[Ëœ] _i_[(] _âˆ’[A]_ 1[)][is] _[Ïµ]_[-dangerous][to] _[Y] i_[(] _âˆ’[B]_ 1[)][.] Since this event happens with probability larger than 1 _/_ 2, by Theorem E.6, conditioning random variables on this event decreases their min-entropy by at most 1 bit and their density by at most 1 _/b_ . Therefore, after conditioning, ( _Yi_[(0)] _âˆ’_ 1 _[, Y] i_[(1)] _âˆ’_ 1[)][is][still][(] _[Ï, Ï„][âˆ’]_[1] _[/b]_[)-structured.][Note][that][here][we][are][slightly][abusing][notation][in] reusing the same notation after conditioning. 

Now we proceed to the steps of sampling _Âµi_ and _ji_ . Let _Âµi, ji_ be sampled based on _Yi_[(] _âˆ’[A]_ 1[)][.][Let] _[Âµ]_[Ëœ] _[i][,]_[ Ëœ] _[j][i]_[be sampled] based on _Y_[Ëœ] _i_[(] _âˆ’[A]_ 1[)][.][Since][(] _[Y] i_[(0)] _âˆ’_ 1 _[, Y] i_[(1)] _âˆ’_ 1[)][is][still][(] _[Ï, Ï„][âˆ’]_[1] _[/b]_[)-structured,][by][Theorem][E.20][,][we][have][that] _[Y] i_[(0)] _âˆ’_ 1[and] _[Y]_[Ëœ] _i_[(0)] _âˆ’_ 1 are ([1] 8[2] _[âˆ’][Î·b/]_[8] 2 _Nb_ 1[)-close][to][each][other][in][total][variation][distance.][This][implies][that][the][sampled][(] _[Âµ][i][, j][i]_[)][and] (Ëœ _Âµi,_[Ëœ] _ji_ ) are also ([1] 8[2] _[âˆ’][Î·b/]_[8] 2 _Nb_ 1[)-close][to][each][other.][Thus][there][exists][a][coupling][such][that] 

**==> picture [324 x 21] intentionally omitted <==**

We sample from this coupling and if they differ, we set _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] = _{_ ( _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] ) _}_ . Now suppose they are the same. We proceed with Algorithm 3 and condition _Yj_[(] _âˆ’[A]_ 1[)][and] _[Y]_[Ëœ] _j_[(] _âˆ’[A]_ 1[)][on][being][consistent][with] _[Âµ][i][, j][i]_[.][Lastly,][if] _qji <_[1] 8[2] _[âˆ’][Î·b/]_[8] 2 _Nb_ 1[(i.e.,] _[A][â€²]_[halts),][we][set] _[Y]_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] = _{_ ( _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] ) _}_ . Note that the probability of this failure is at most 8[1][2] _[âˆ’][Î·b/]_[8] 2 _Nb_ 1[because][the][probability][of][sampling][such] _[j][i]_[is] 

**==> picture [384 x 36] intentionally omitted <==**

Then we condition _Yi_[(] _âˆ’[B]_ 1[)] _[,][Y]_[Ëœ] _i_[(] _âˆ’[B]_ 1[)][on being consistent with the oracle query.][Now we have completed a full iteration] and we set _Y_[Ëœ] _i_[(0)] and _Y_[Ëœ] _i_[(1)] to be the support of the processed _Yi_[(0)] _âˆ’_ 1[and] _[Y] i_[(1)] _âˆ’_ 1[,][respectively.][This][completes][the] construction of _Y_[Ëœ] _i_[(0)] _, Y_[Ëœ] _i_[(1)] . Now we prove that the induction properties are satisfied. Since we have conditioned on the random variables with and without tildes being the same in every step, _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] = _Yi_[(0)] _Ã— Yi_[(1)] by construction if the coupling succeed. The probability of failure is 

**==> picture [464 x 78] intentionally omitted <==**

90 

as desired. Finally, we show that conditioned on _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] , _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] are uniform on _G[âˆ’]_[1] ( _o_ ) _âˆ©_ ( _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] ). Note that when the coupling fails, this is automatically true since we have set _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] = _{_ ( _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] ) _}_ . When the coupling succeed, since all the coupling does to _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] is to condition them on being in _Y_[Ëœ] _i_[(0)] _Ã—_ Ëœ _Yi_[(1)] . Therefore, the induction hypothesis implies that the desired property is still true. This completes the induction and we have proven that for all _i_ = 0 _, . . . , r_ , it holds true that (1) the distribution of _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] conditioned on a specific rectangle _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] is the uniform distribution over _G[âˆ’]_[1] ( _o_ ) _âˆ©_ ( _Y_[Ëœ] _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] ), and (2) Prï¿½ _Y_ Ëœ _i_[(0)] _Ã— Y_[Ëœ] _i_[(1)] = _Yi_[(0)] _Ã— Yi_[(1)] ï¿½ _â‰¤_ 2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] 2 _Nbi_[.] 

Finally, we prove that _Ï€[â€²]_ ( _Î±, x_ ) and _Ï€[â‹†]_ ( _Î±, x_ ) are (2 _[âˆ’][Î·b/]_[8] _[âˆ’]_[1] )-close. Suppose _Yr_[(0)] _Ã—Yr_[(1)] = _Y_[Ëœ] _r_[(0)] _Ã— Y_[Ëœ] _r_[(1)][.][Since we] have fixed _Î±, x_ and the learning algorithm is completely deterministic, any specific encoding _Y_[(0)] _, Y_[(1)] can only lead to a single possible transcript. In particular, the ideal encoding ( _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] ) can only lead to the target transcript _Ï€[â‹†]_ ( _Î±, x_ ). We have also proved that the ideal encoding ( _Y_[Ëœ][(0)] _, Y_[Ëœ][(1)] ) falls inside _Y_[Ëœ] _r_[(0)] _Ã— Y_[Ëœ] _r_[(1)][,][and][thus] _Yr_[(0)] _Ã— Yr_[(1)][.][Note][that][Algorithm][3][by][construction][ensures][that][all][the][elements][in][the][rectangle] _[Y] i_[(0)] _Ã— Yi_[(1)] are consistent with the transcript _Ï€_ , because otherwise they must have been removed. Therefore, we must have _Ï€[â‹†]_ ( _Î±, x_ ) = _Ï€[â€²]_ ( _Î±, x_ ). In other words, _Yr_[(0)] _Ã— Yr_[(1)] = _Y_[Ëœ] _r_[(0)] _Ã— Y_[Ëœ] _r_[(1)] implies _Ï€[â‹†]_ ( _Î±, x_ ) = _Ï€[â€²]_ ( _Î±, x_ ). This means that 

**==> picture [363 x 81] intentionally omitted <==**

where we have used _r â‰¤âŒŠM/T âŒ‹âˆ’_ 1 and the assumption that _M â‰¤_ 2 _NTb_ . This completes the proof that _Ï€_ and _Ï€[â‹†]_ are 2 _[âˆ’][Î·b/]_[8] -close in total variation distance. 

## _d. Simulation does not query too much_ 

In this section, we show that the query _A_ makes is bounded by the sample-space product. To bound the query complexity of Algorithm 3, we keep track of the deficiency of _Y_[(0)] _, Y_[(1)] through out the simulation. Initially, since _Y_[(0)] = _Y_[(1)] = _{_ 0 _,_ 1 _}[N][Ã—][b]_ and _Ï_ = _âˆ—[N]_ , we have _Dâˆž_ ( _Y_[(0)] _, Y_[(1)] _, Ï_ ) = 2 _bN âˆ’ bN âˆ’ bN_ = 0. 

Now we go through the steps of Algorithm 3. In Line 9, we condition _Y_[(] _[A]_[)] on being not _Ïµ_ -dangerous to _Y_[(] _[B]_[)] , which changes the distribution of _Y_[(] _[A]_[)] . In Section E 3 c, we have shown that the probability of not being dangerous is at least 1 _/_ 2. Thus by Theorem E.6, the min-entropy of _Y_[(] _[A]_[)] decreases by at most 1 bit. Then we condition _Y_[(] _[A]_[)] on being consistent with reaching vertex _v_ labeled by _Âµi_ , which happens with probability _pi_ . This decreases the min-entropy of _Y_[(] _[A]_[)] by at most log(1 _/pi_ ). Therefore, up to this point, the deficiency increases by at most log(1 _/pi_ ) + 1. 

Next, we proceed to the density restoring step. We first condition _Y_[(] _[A]_[)] on being in the selected subset _Y[j][i]_ . From Theorem E.21, we know that this conditioning decreases the min-entropy of _Y_[(] _[A]_[)] by at most _Î´b|Iji|_ + log(1 _/qji_ ) bits. Then we query the oracle on _Iji_ and fix the corresponding coordinates in _Ï, Y_[(] _[A]_[)] _.Y_[(] _[B]_[)] . This decreases _|_ free( _Ï_ ) _|_ by _|Iji|_ . Also, from Theorem E.7, the min-entropy of _Y_[(] _[B]_[)] decreases by at most _b|Iji|_ while the min-entropy of _Y_[(] _[A]_[)] does not change since it is already fixed on _Iji_ . Finally, we condition _Y_[(] _[B]_[)] on being consistent with _YI_[(] _ji[A]_[)] and _ÏIji_ and change the distribution of _Y_[(] _[B]_[)] . Since _Y_ free([(] _[A]_[)] _Ï_ )[is][not] _[Ïµ]_[-dangerous] to _Y_ free([(] _[B]_[)] _Ï_ )[,][by][definition][we][have][Pr] ï¿½ _g[I][ji]_ ( _yIji , yI[B] ji_[) =] _[ Ï][I] ji_ ï¿½ _â‰¥_ 2 _[âˆ’|][I][ji][|âˆ’]_[1] . Thus this conditioning decreases the min-entropy of _Y_[(] _[B]_[)] by at most _|Iji|_ + 1 bits. This completes the density restoring step and the decrease in 

91 

deficiency is at least 

**==> picture [353 x 124] intentionally omitted <==**

where we have used _b â‰¥ c_ log _N â‰¥ c_ , _|Iji| â‰¥_ 1, _b/c â‰¥_ log _b_ for large _N_ . Note that using _Î´_ = 1 _âˆ’ Î·/_ 4 + _Ïµ/_ 2, _Ïµ_ = (96 log _c_ ) _/_ ( _cÎ·_ ), 0 _< Î· â‰¤_ 2 and _c â‰¥_ 2, we have 

**==> picture [326 x 101] intentionally omitted <==**

if we choose _c_ =[865] _Î·_[2][log] ï¿½ 865 _Î·_[2] ï¿½ such that _c/_ log _c â‰¥_ 432 _._ 5 _/Î·_[2] . This means that the decrease in deficiency during the density restoring step is at least _Î·b|Iji|/_ 6920. 

To summarize, in a single complete iteration, the deficiency is increased by at most log(1 _/pi_ )+1 _âˆ’Î·b|Iji|/_ 6920. Since initially the deficiency is zero, the deficiency at the end is upper bounded by 

**==> picture [470 x 28] intentionally omitted <==**

which must be non-negative since deficiency is. Therefore, we have _âŒŠM/T âŒ‹ S_ + _b_ + _âŒŠM/T âŒ‹âˆ’ Î·bQ/_ 6920 _â‰¥_ 0 and thus 

**==> picture [339 x 25] intentionally omitted <==**

This completes the proof of Theorem E.25. 

## _e. Proof of Theorem E.2_ 

Finally, we are ready to prove Theorem E.2. 

_Proof of Theorem E.2._ Let _L_ be any randomized classical learning algorithm with space complexity _S_ , sample complexity _M_ , and input form _I_ = [ _N_ ] _Ã—{_ 0 _,_ 1 _}[b] Ã—{_ 0 _,_ 1 _}_ such that given data generated from _Dg,T[N]_[(] _[o]_[),] _[ L]_[ outputs] _f_ ( _o_ ) with probability at least 1 _âˆ’ Î´_ + 2 _[âˆ’][Î·b/]_[8] . Since _f_ : _{_ 0 _,_ 1 _}[N] â†’{_ 0 _,_ 1 _}_ , its query complexity satisfies _Q[Î´] C[â‰¤][N]_[.] If _M >_ 2 _NTb_ , then we immediately have 

**==> picture [332 x 13] intentionally omitted <==**

as required. 

Suppose otherwise that _M â‰¤_ 2 _NTb_ . From Theorem E.25, we know that there exists a randomized parallel decision tree _A_ with query complexity _Q_ = _O_ ( _MS/_ ( _Tb_ )) such that given any input _o âˆˆ{_ 0 _,_ 1 _}[N]_ , _A_ outputs a random bitstring _Ï€_ whose distribution is 2 _[âˆ’][Î·b/]_[8] -close in total variation distance to the distribution of the transcript of _L_ when given data generated from _Dg,T[N]_[(] _[o]_[).][In][particular,][let] _[a]_[be][the][last][bit][of][the][transcript][of] _L_ , which is the output of _L_ . Then the last bit of _Ï€_ must be equal to _a_ with probability at least 1 _âˆ’_ 2 _[âˆ’][Î·b/]_[8] . On the other hand, Pr[ _a_ = _f_ ( _o_ )] _â‰¥_ 1 _âˆ’ Î´_ + 2 _[âˆ’][Î·b/]_[8] from the guarantee of _L_ . Thus we have that the last bit of _Ï€_ is 

92 

equal to _f_ ( _o_ ) with probability at least 1 _âˆ’ Î´_ + 2 _[âˆ’][Î·b/]_[8] _âˆ’_ 2 _[Î·b/]_[8] = 1 _âˆ’ Î´_ by the union bound. This gives us a query algorithm (executing _A_ and outputting the last bit of its output) with query complexity _Q_ = _O_ ( _MS/_ ( _Tb_ )) that outputs _f_ ( _o_ ) with probability at least 1 _âˆ’ Î´_ . From the definition of _Î´_ -error classical randomized query complexity, we have 

**==> picture [292 x 25] intentionally omitted <==**

Therefore, we arrive at _MS â‰¥_ â„¦( _Q[Î´] C[Tb]_[),][as][required.][This][completes][the][proof][of][Theorem][E.2][.] 

## **4. Bootstrap with one more time scale** 

In this section, we build upon Theorem E.2 and bootstrap it to a much stronger lower bound by introducing a new task called dynamic Noisy Oracle Property Estimation (dynamic NOPE). We design this new task by adding one more time scale into the original NOPE. We call it dynamic NOPE, because the oracle becomes dynamic: it changes over time, but the property that we want to estimate stays fixed. 

Recall that our interested oracle property is given by a property function _f_ : _O â†’{_ 0 _,_ 1 _}, O âŠ†{_ 0 _,_ 1 _}[N]_ . To make the oracle dynamic, we consider randomly sampled oracles from two distributions _p_ 0 _, p_ 1 supported on _O âŠ†{_ 0 _,_ 1 _}[N]_ , where _o âˆ¼ pB_ satisfies _f_ ( _o_ ) = _B_ for _B âˆˆ{_ 0 _,_ 1 _}_ . The relevant notion of query complexity in this case is the (1 _/_ 3)-error classical distributional query complexity, which we denote as _QC_ . We introduce noise in the same way as before. We consider a noisy encoding function _g_ : _{_ 0 _,_ 1 _}[b] Ã—{_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _}_ with encoding length _b_ = _âŒˆc_ log _N âŒ‰_ and discrepancy disc( _g_ ) _â‰¤_ 2 _[âˆ’][Î·b]_ , where _c_ = (865 _/Î·_[2] ) logï¿½865 _/Î·_[2][ï¿½] for some constant _Î· âˆˆ_ (0 _._ 1 _,_ 2]. We will call such encoding functions _good noisy encoding functions_ . 

In a dynamic setting, we introduce two time scales _T_ 1 _, T_ 2 and another parameter _L_ that characterize how dynamic the oracle can be. They are positive integers and their relation with _N_ will be specified later. We consider a 2-level hierarchical data generation process _Dg,f[N]_[(] _[B]_[)][that][depends][on][the][binary][property] _[B][âˆˆ{]_[0] _[,]_[ 1] _[}]_ we want to estimate: 

**==> picture [396 x 17] intentionally omitted <==**

where we have _L_ sampled oracles _oj âˆˆ{_ 0 _,_ 1 _}[N] , j âˆˆ_ [ _L_ ], each with its own property _Î³j_ = _f_ ( _oj_ ) _âˆˆ{_ 0 _,_ 1 _}_ and noisy encoding _Y_[(0] _[,j]_[)] _, Y_[(1] _[,j]_[)] _âˆˆ{_ 0 _,_ 1 _}[N][Ã—][b]_ . The situation _Î² âˆˆ_ [ _L_ ] labels which oracle we are currently getting samples from, and _Î± âˆˆ{_ 0 _,_ 1 _}_ specifies which part of the noisy encoding we are looking at. The data sample is of the form 

**==> picture [340 x 12] intentionally omitted <==**

where _xi_ is a random query and _yi_ is the corresponding noisy oracle value. We set _L_ = ï¿½log[2] _N_ ï¿½ _â‰¥_ 5 and _T_ 2 = _N_ . _T_ 1 is tunable but scales as _T_ 1 = polylog( _N_ ). The sampling distributions are defined as follows. _DB_[0][samples][a][length-] _[L]_[bitstring] _[Î³]_[with][parity] 

**==> picture [267 x 32] intentionally omitted <==**

uniformly random. This means that the final property that we want to estimate is the XOR of the properties of all the _L_ oracles. For each _j âˆˆ_ [ _L_ ], we set _Î³j_ to be the _j_ -th bit of the sampled bitstring _Î³_ , sample a random oracle _oj âˆ¼ pÎ³j_ and sample a noisy encoding pair ( _Y_[(0] _[,j]_[)] _, Y_[(1] _[,j]_[)] ) _âˆ¼_ Uniform(( _g[N]_ ) _[âˆ’]_[1] ( _oj_ )). These meta-data ( _Î³j, oj, Y_[(0] _[,j]_[)] _, Y_[(1] _[,j]_[)] ) _[L] j_ =1[will][be][used][to][generate][the][data][samples.][Now][we][define] _[D]_ ([1] _Î³j ,oj ,Y_[(0] _[,j]_[)] _,Y_[(1] _[,j]_[)] ) _[L] j_ =1[.][We] first sample a uniformly random oracle label _Î² âˆ¼_ Uniform([ _L_ ]) and a random bit _Î± âˆ¼_ Bern(1 _/_ 2). Then we pick out _Y_[(] _[Î±,Î²]_[)] and use it to generate the data samples. In particular, we define _D_ ([2] _Î²,Î±,Y_[(] _[Î±,Î²]_[)] )[as][sampling][a][random] query _x âˆ¼_ Uniform([ _N_ ]) and its corresponding noisy oracle value _y_ = _Yx_[(] _[Î±,Î²]_[)] _âˆˆ{_ 0 _,_ 1 _}[b]_ . This gives us a data sample _z_ = ( _x, y, Î±, Î²_ ). 

The task of dynamic NOPE, is to estimate the binary property _B_ using these data samples. 

**Task E.26** (Dynamic Noisy Oracle Property Estimation (dynamic NOPE)) **.** _Let N, T_ 1 _be positive integers. Let f_ : _O â†’{_ 0 _,_ 1 _} be a function that specifies the target property for a set of possible oracles O âŠ†{_ 0 _,_ 1 _}[N] . Let g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be a noisy encoding function. The task of dynamic Noisy Oracle Property Estimation is to calculate the desired property B âˆˆ{_ 0 _,_ 1 _} using data samples generated from the noisy hierarchical data generation process Dg,f[N,T]_[1] ( _B_ ) _, for any B âˆˆ{_ 0 _,_ 1 _}._ 

93 

Intuitively, in dynamic NOPE, the target property _B_ that we are trying to estimate is the parity of the length- _L_ bitstring _Î³_ . In order to predict the parity of _Î³_ , we effectively need to predict all its _L_ components _Î³j, j âˆˆ_ [ _L_ ] simultaneously. Meanwhile, information about _Î³j_ is encoded as the property of the generated oracle _oj_ . Hence, we are trying to solve _L_ independent instances of NOPE described in Theorem E.2. 

Dynamic NOPE is hard to solve, because Theorem E.2 tells us that if the classical learning algorithm does not have enough memory size (determined by _N, QC_ ), its success probability on a single NOPE instance is at most 2 _/_ 3 + _o_ (1) _â‰¤_ 1 _/_ 2 + _Î´_ for some _Î´_ . We will build upon this and show that its success probability of solving dynamic NOPE is at most 1 _/_ 2 + (2 _Î´_ ) _[L]_ = 1 _/_ 2 + _N[âˆ’]_[â„¦(log(] _[N]_[))] . Finally, we use a hybrid argument to convert this success probability upper bound into a sample complexity lower bound of _N_[â„¦(log] _[ N]_[)] = _N[Ï‰]_[(1)] . Together, this means that any classical learning algorithm with insufficient memory would need a tremendous amount of samples to solve dynamic NOPE. 

Formally, we prove the following two classical hardness results. They hold for any _T_ 1 of our choice. The first result shows that given only the data from one refreshing block (i.e., _M_ = _Ï„D_ where _Ï„D_ = _T_ 1 _T_ 2 is the refreshing time of _Dg,f[N,T]_[1] ( _B_ )), any classical learning algorithm with insufficient size cannot perform much better than random guessing at dynamic NOPE. 

**Theorem E.27** (Classical single-block hardness of dynamic NOPE) **.** _Let N, T_ 1 _be large integers. Let f_ : _O â†’{_ 0 _,_ 1 _}, O âŠ†{_ 0 _,_ 1 _}[N] be a function that specifies the target property with_ (1 _/_ 3) _-error classical distributional query complexity QC â‰¥_ â„¦( _T_ 1[2][log][2][(] _[N]_[) log log(] _[N]_[))] _[.][Let][g][be][a][good][noisy][encoding][function.] Then, for any randomized classical learning algorithm L with sample complexity M_ = _Ï„D, if its space complexity_ 

**==> picture [275 x 77] intentionally omitted <==**

_its success probability of solving dynamic NOPE is at most_ 

The second result shows that if we want to solve dynamic NOPE with high probability, but our classical machine does not have sufficient size, we must collect a super-polynomial amount of samples. 

**Theorem E.28** (Classical sample complexity of dynamic NOPE) **.** _Let N, T_ 1 _be large integers. Let f_ : _O â†’{_ 0 _,_ 1 _}, O âŠ†{_ 0 _,_ 1 _}[N] be a function that specifies the target property with_ (1 _/_ 3) _-error classical distributional query complexity QC â‰¥_ â„¦( _T_ 1[2][log][2][(] _[N]_[) log log(] _[N]_[))] _[.][Let][g][be][a][good][noisy][encoding][function.] Then, for any randomized classical learning algorithm L that solves dynamic NOPE with probability at least_ 2 _/_ 3 _, if its space complexity_ 

**==> picture [137 x 10] intentionally omitted <==**

**==> picture [275 x 67] intentionally omitted <==**

_where Ï„D_ = _T_ 1 _N is the refreshing time of dynamic NOPE._ 

The remaining parts of this section are devoted to prove Theorems E.27 and E.28. Since we are randomly sampling oracles, we first prove a distributional version of the sample-space lower bound in Section E 4 a. Then, in Sections E 4 b to E 4 e, we use a derandomization technique to prove a learning XOR lemma that suppresses the advantage of any algorithm exponentially. In Section E 4 f, we use a hybrid argument to show that an super-polynomially small advantage leads to a super-polynomial sample complexity. Finally, we complete the proof in Section E 4 g. 

## _a. Distributional sample-space lower bound_ 

We begin by noting that the sample-space lower bound we prove for NOPE (Theorem E.2) applies only to algorithms that are required to work for any input oracle _o âˆˆ{_ 0 _,_ 1 _}[N]_ . But in dynamic NOPE, the learning 

94 

algorithm only needs to succeed on average for random oracles drawn from _p_ 0 _, p_ 1. Nevertheless, we can still prove a sample-space lower bound as follows by replacing randomized query complexity with distributional query complexity. 

**Lemma E.29** (Distributional sample-space lower bound) **.** _Let N be a large integer. Let the time scale T be a positive integer. Let Î· âˆˆ_ (0 _,_ 2] _be a constant and c_ = (865 _/Î·_[2] ) logï¿½865 _/Î·_[2][ï¿½] _. Let b â‰¥ c_ log _N . Let g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be an encoding map with_ disc( _g_ ) _â‰¤_ 2 _[âˆ’][Î·b] . Let f_ : _O â†’{_ 0 _,_ 1 _}, O âŠ†{_ 0 _,_ 1 _}[N] be any function with Î´-error classical distributional query complexity Q[Î´] C[with respect to the distributions][ p]_[0] _[, p]_[1] _[supported] on O. Let L be any randomized classical learning algorithm with space complexity S, sample complexity M , and input form I_ = [ _N_ ] _Ã— {_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _} such that for any Î³ âˆˆ{_ 0 _,_ 1 _}, given data generated from Dg,T[N]_[(] _[o]_[)] _[, o][ âˆ¼][p][Î³][,][L] outputs Î³ with probability at least_ 1 _âˆ’ Î´_ + 2 _[âˆ’][Î·b/]_[8] _. Then, L must satisfy_ 

**==> picture [280 x 13] intentionally omitted <==**

_Proof of Theorem E.29._ The proof resembles the proof of Theorem E.2. Let _L_ be any randomized classical learning algorithm with space complexity _S_ , sample complexity _M_ , and input form _I_ = [ _N_ ] _Ã— {_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}_ such that for any _Î³ âˆˆ{_ 0 _,_ 1 _}_ , given data generated from _Dg,T[N]_[(] _[o]_[)] _[, o][âˆ¼][p][Î³]_[,] _[L]_[outputs] _[Î³]_[with][probability][at][least] 1 _âˆ’ Î´_ + 2 _[âˆ’][Î·b/]_[8] . Since _f_ : _{_ 0 _,_ 1 _}[N] â†’{_ 0 _,_ 1 _}_ , its distributional query complexity satisfies _Q[Î´] C[â‰¤][N]_[.][If] _[M][>]_[ 2] _[NTb]_[,] then we immediately have _MS â‰¥ M >_ 2 _NTb â‰¥_ 2 _Q[Î´] C[Tb]_[ = â„¦(] _[Q][Î´] C[Tb]_[)][as][required.] 

Suppose otherwise that _M â‰¤_ 2 _NTb_ . From Theorem E.25, we know that there exists a randomized parallel decision tree _A_ with query complexity _Q_ = _O_ ( _MS/_ ( _Tb_ )) such that given any input _o âˆˆ{_ 0 _,_ 1 _}[N]_ , _A_ outputs a random bitstring _Ï€_ whose distribution is 2 _[âˆ’][Î·b/]_[8] -close in total variation distance to the distribution of the transcript of _L_ when given data generated from _Dg,T[N]_[(] _[o]_[).][In][particular,][let] _[a]_[be][the][last][bit][of][the][transcript][of] _L_ , which is the output of _L_ . Then the last bit of _Ï€_ must be equal to _a_ with probability at least 1 _âˆ’_ 2 _[âˆ’][Î·b/]_[8] . On the other hand, Pr[ _a_ = _Î³_ ] _â‰¥_ 1 _âˆ’ Î´_ + 2 _[âˆ’][Î·b/]_[8] . Thus we have that the last bit of _Ï€_ is equal to _Î³_ with probability at least 1 _âˆ’ Î´_ + 2 _[âˆ’][Î·b/]_[8] _âˆ’_ 2 _[Î·b/]_[8] = 1 _âˆ’ Î´_ . This gives us a query algorithm (executing _A_ and outputting the last bit of its output) with query complexity _Q_ = _O_ ( _MS/_ ( _Tb_ )) that outputs _Î³_ with probability at least 1 _âˆ’ Î´_ , when the input oracle is drawn randomly from _pÎ³_ . From the definition of _Î´_ -error classical distributional query complexity, we have 

**==> picture [292 x 25] intentionally omitted <==**

Therefore, we arrive at _MS â‰¥_ â„¦( _Q[Î´] C[Tb]_[),][as][required.] 

In the following, we focus on the case of _T_ = _N_ as in dynamic NOPE. 

## _b. Learning XOR Lemma_ 

Theorem E.29 shows that if our classical machine does not have enough size, it cannot solve a single problem instance of NOPE. In dynamic NOPE, we further reduce the advantage (i.e., success probability increase over random guessing) exponentially by requiring the algorithm to predict the XOR of _L_ instances. This is formalized in the following result that we call the learning XOR lemma. 

**Lemma E.30** (Learning XOR lemma) **.** _Let N be a large integer. Let T_ 1 _, L be positive integers. Let Î· âˆˆ_ (0 _,_ 2] _be a constant and c_ = (865 _/Î·_[2] ) logï¿½865 _/Î·_[2][ï¿½] _. Let g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be a noisy encoding function with encoding length b â‰¥ c_ log _N and discrepancy_ disc( _g_ ) _â‰¤_ 2 _[âˆ’][Î·b] . Let f_ : _O â†’ {_ 0 _,_ 1 _}, O âŠ†{_ 0 _,_ 1 _}[N] be any function. Suppose that any randomized classical learning algorithm L with space complexity T_ 1 _L_ ( _S_ + _âŒˆ_ log _LâŒ‰_ ) _, sample complexity T_ 1 _N , and input form I_ = [ _N_ ] _Ã—{_ 0 _,_ 1 _}[b] Ã—{_ 0 _,_ 1 _}, given data generated from Dg,N[N]_[(] _[o]_[)] _[, o][ âˆ¼][p][Î³][,][cannot][output][Î³][âˆˆ{]_[0] _[,]_[ 1] _[}][with][success][probability][more][than]_[1] _[/]_[2+] _[Î´][.] Then, any randomized classical learning algorithm L[âŠ•] with space complexity S, sample complexity T_ 1 _N , and input form I Ã—_ [ _L_ ] _, given data generated from_ ( _D_ ([1] _Î³j ,oj ,Y_[(0] _[,j]_[)] _,Y_[(1] _[,j]_[)] ) _[L] j_ =1 _[â†’][Ã—][T]_[1] _[D]_ ([2] _Î²,Î±,Y_[(] _[Î±,Î²]_[)] ) _[â†’][Ã—][N][z]_[)] _[as] in dynamic NOPE, cannot output B_ =[ï¿½] _[L] j_ =1 _[Î³][j][âˆˆ{]_[0] _[,]_[ 1] _[}][with][success][probability][more][than]_ 

**==> picture [249 x 23] intentionally omitted <==**

There are two challenges in proving Theorem E.30. The first challenge is that the random sampling of _Î²_ may allow the algorithm to see more samples that belong to the same problem instance labeled by _Î²_ . For 

95 

example, if two consecutive _Î²_ â€™s are the same, then the algorithm effectively have twice as many samples, and thus have a higher success probability than usual. The second challenge is that the _L_ problem instances are actually not independent, because the algorithm can carry information through the computation and may be able to solve several instances in a joint way. In other words, the algorithm does not have to approach each problem instances independently. The random sampling of _Î²_ â€™s, moreover, allows the algorithm to introduce more correlation between problem instances, as compared to a case where streams of different instances are concatenated sequentially in an adversarial order (cf. the streaming XOR lemma as in [99, Theorem 1]). 

To overcome these challenges, we proceed in two steps to prove Theorem E.30. Firstly, we derandomize _Î²_ by showing that any learning algorithm _L[âŠ•]_ can be used to construct a learning algorithm _L[â€²]_ with the same success probability, but increased space complexity _S_ + _âŒˆ_ log _LâŒ‰_ and sample complexity _T_ 1 _NL_ , for a different data generation process where _Î²_ appears in a fixed ordering _Î²_ = 1 _, . . . , L,_ 1 _, . . . , L, . . ._ rather than randomly sampled (there are still _N_ samples under each _Î²_ ). Next, we show that the learning algorithm _L[â€²]_ cannot have success probability more than 1 _/_ 2 + (2 _Î´_ ) _[L] /_ 2 even if it can correlate different instances, by analyzing a corresponding communication problem that takes into account the correlation between different problem instances generated by the algorithm. Together, this shows that the success probability of _L[âŠ•]_ cannot exceed 1 _/_ 2 + (2 _Î´_ ) _[L] /_ 2. 

## _c. Derandomization_ 

In the first step of proving Theorem E.30, we consider the data generation process _D_ ([order] _Î³j_ ) _[L] j_ =1[that][gener-] ates _T_ 1 _NL_ samples _z_ 1 _, . . . , zT_ 1 _NL_ as follows. Instead of sampling random _Î² âˆˆ_ [ _L_ ] and _T_ 1 _N_ samples as in ( _D_ ([1] _Î³j ,oj ,Y_[(0] _[,j]_[)] _,Y_[(1] _[,j]_[)] ) _[L] j_ =1 _[â†’][Ã—][T]_[1] _[D]_ ([2] _Î²,Î±,Y_[(] _[Î±,Î²]_[)] ) _[â†’][Ã—][N][z]_[),][we][sample] _[T]_[1] _[N]_[samples] _[z]_ 1 _[Î²][, . . . , z] T[Î²]_ 1 _N_[in][the][same][way][but] for every _Î² âˆˆ_ [ _L_ ]. This means that for a given _Î²_ , _z_ 1 _[Î²][, . . . , z] T[Î²]_ 1 _L_[have][the][same] _[Î²]_[values,][while][their] _[Î±]_[values] are re-sampled after each _N_ consecutive samples. This gives us _LT_ 1 _N_ samples in total. We order them in a round-robin way (in terms of _Î²_ ) such that the _Î²_ â€™s appear sequentially as 

**==> picture [342 x 39] intentionally omitted <==**

and within the data samples that have the same _Î²_ value, their ordering stays the same. More formally, we define 

_z_ ( _aâˆ’_ 1) _NL_ +( _bâˆ’_ 1) _N_ + _c_ = _za[b] Â·c[,] âˆ€a âˆˆ_ [ _T_ 1] _, b âˆˆ_ [ _L_ ] _, c âˆˆ_ [ _N_ ] _._ (E87) This defines the data generation process _D_ ([order] _Î³j_ ) _[L] j_ =1[with][derandomized] _[Î²]_[.] Now, we use _L[âŠ•]_ to construct _L[â€²]_ that process data from _D_[order][prove][the][following][lemma.] ( _Î³j_ ) _[L] j_ =1[and] 

**Lemma E.31** (Derandomize _Î²_ ) **.** _Let L[âŠ•] be any randomized classical learning algorithm with space complexity S and sample complexity T_ 1 _N that given data generated from_ ( _D_ ([1] _Î³j ,oj ,Y_[(0] _[,j]_[)] _,Y_[(1] _[,j]_[)] ) _[L] j_ =1 _[â†’][Ã—][T]_[1] _[D]_ ([2] _Î²,Î±,Y_[(] _[Î±,Î²]_[)] ) _[â†’][Ã—][N][z]_[)] _as in dynamic NOPE, outputs B_ =[ï¿½] _[L] j_ =1 _[Î³][j][âˆˆ{]_[0] _[,]_[ 1] _[}][with][probability][p]_[succ] _[.][Then,][there][exists][a][randomized] classical learning algorithm L[â€²] with space complexity S_ + _âŒˆ_ log _LâŒ‰ and sample complexity T_ 1 _NL that given data generated from D_ ([order] _Î³j_ ) _[L] j_ =1 _[,][outputs][B]_[=][ ï¿½] _[L] j_ =1 _[Î³][j][âˆˆ{]_[0] _[,]_[ 1] _[}][with][the][same][probability][p]_[succ] _[.]_ 

_Proof of Theorem E.31._ We prove this lemma by explicitly constructing the learning algorithm _L[â€²]_ from _L[âŠ•]_ . The constructed algorithm _L[â€²]_ process the data in chunks of size _NL_ . At the beginning of each chunk, _L[â€²]_ randomly selects a _Î² âˆ¼_ Uniform([ _L_ ]) and keeps it in its memory. This uses _âŒˆ_ log _LâŒ‰_ bits of memory. It waits until the data block of size _N_ that corresponds to this particular _Î²_ arrives, and then feeds these _N_ samples sequentially into _L[âŠ•]_ , which operates on the remaining memory of size _S_ . After processing these _N_ samples, _L[â€²]_ waits until the end of this _NL_ -size chunk and erases its selection of _Î²_ . Then it proceeds to the next _NL_ -size chunk and randomly selects a new _Î²_ . After processing all the _T_ 1 chunks of size _NL_ , _L[â€²]_ has already given _T_ 1 _N_ data samples to _L[âŠ•]_ and _L[âŠ•]_ generates an output bit in return, which is then outputted by _L[â€²]_ as the final outcome. Note that since the _Î²_ â€™s are selected uniformly, the data samples that are fed into _L[âŠ•]_ follow exactly the same distribution as ( _D_ ([1] _Î³j ,oj ,Y_[(0] _[,j]_[)] _,Y_[(1] _[,j]_[)] ) _[L] j_ =1 _[â†’][Ã—][T]_[1] _[D]_ ([2] _Î²,Î±,Y_[(] _[Î±,Î²]_[)] ) _[â†’][Ã—][N][z]_[),][by][definition][of] _[D]_ ([order] _Î³j_ ) _[L] j_ =1[in][Equation][(][E86][).][This][implies] that the success probability of _L[â€²]_ is the same as that of _L[âŠ•]_ . 

## _d. Derandomized learning XOR lemma_ 

In the second step of proving Theorem E.30, we show that the success probability of _L[â€²]_ cannot exceed 1 _/_ 2+(2 _Î´_ ) _[L] /_ 2. The proof idea follows that of [99, Theorem 1], but the structure of our data generation processes 

96 

are very different from the adversarial ordering there. Therefore, we adopt a different technical construction. In particular, their data streams are concatenated sequentially whereas ours are interleaved as in Equation (E86). This interleaved structure is inherent in our learning setting, because our problem instance labels _Î²_ are sampled randomly. 

**Lemma E.32** (Derandomized learning XOR lemma) **.** _Suppose that any randomized classical learning algorithm L with space complexity T_ 1 _LS and sample complexity T_ 1 _N , given data generated from Dg,N[N]_[(] _[o]_[)] _[, o][âˆ¼][p][Î³][,][cannot] output Î³ âˆˆ{_ 0 _,_ 1 _} with success probability more than_ 1 _/_ 2 + _Î´. Then, any randomized classical learning algorithm L[â€²] with space complexity S and sample complexity T_ 1 _NL, given data generated from D_[order] _[cannot][output]_ ( _Î³j_ ) _[L] j_ =1 _[,] B_ =[ï¿½] _[L] j_ =1 _[Î³][j][âˆˆ{]_[0] _[,]_[ 1] _[}][with][success][probability][more][than]_[1] _[/]_[2 + (2] _[Î´]_[)] _[L][/]_[2] _[.]_ 

To prove Theorem E.32, we consider an _L_ -player communication game. In particular, there are _L_ players _Q_ 1 _, . . . , QL_ where the player _QÎ²_ receives the data _z_ 1 _[Î²][, . . . , z] T[Î²]_ 1 _N_[in] _[D]_ ([order] _Î³j_ ) _[L] j_ =1[.][Their][goal][is][to][communicate][and] output a final bit _B_[Ë†] _âˆˆ{_ 0 _,_ 1 _}_ that matches _B_ =[ï¿½] _[L] j_ =1 _[Î³][j]_[.] Recall that _z_ 1 _[Î²][, . . . , z] T[Î²]_ 1 _N_[are][the][data][samples] corresponding to the problem instance _Î² âˆˆ_ [ _L_ ]. Intuitively, these players will execute a communication protocol _Ï€_ based on the learning algorithm _L[â€²]_ , and the communication between different players will characterize the correlation between problem instances induced by the learning algorithm. Without loss of generality, we assume that the learning algorithm _L[â€²]_ and the communication protocol _Ï€_ are both deterministic, since there always exists a way of fixing the random numbers in a randomized algorithm such that the resulting success probability is the same as that of the randomized algorithm. 

We work in the blackboard model for communication in this game. In other words, the players each write a message on the blackboard in the order _Q_ 1 _, . . . , QL_ and the messages written on the blackboard are visible to all players afterwards. This constitutes one round of communication, and the messages are never erased. The next round starts again from _Q_ 1. We use _M[j] i_[to][denote][the][message][written][by][player] _[Q][i]_[in][round] _[j]_[.][Let] _[B] i[j]_ be the content of the blackboard before player _Qi_ communicates in round _j_ , and let _B[j]_ be the content of the blackboard after round _j_ completes. Suppose that there are _r_ rounds in total. 

For any _Î² âˆˆ_ [ _L_ ] and blackboard content _B_ , we define 

**==> picture [362 x 12] intentionally omitted <==**

to be the bias of _Î³Î²_ conditioned on the final blackboard displaying _B_ . This intuitively characterizes the progress _Ï€_ makes in solving the _Î²_ -th problem instance. Similarly, we define 

**==> picture [383 x 37] intentionally omitted <==**

to be the bias of[ï¿½] _[L] Î²_ =1 _[Î³][Î²]_[conditioned][on][the][final][blackboard][displaying] _[B]_[.][This][characterizes][the][progress] _Ï€_ makes in solving the XOR problem. In particular, the success probability (i.e., the output _B_[Ë†] of _Ï€_ matches _B_ =[ï¿½] _[L] j_ =1 _[Î³][j]_[)] 

**==> picture [364 x 75] intentionally omitted <==**

where we have used the fact that the final output _B_[Ë†] conditioned on the final blackboard content _B[r]_ = _B_ is a deterministic value _Î¸_ , since _Ï€_ is deterministic. 

Now we focus on a specific communication protocol _Ï€_ given by the learning algorithm _L[â€²]_ with the same success probability. We will describe a randomized protocol, but we make it deterministic by fixing the randomness as described earlier. The communication protocol proceeds as follows. The player _Q_ 1 feeds its data _z_ 1[1] _[, . . . , z] N_[1] sequentially into _L[â€²]_ , which produces a memory state of _L[â€²]_ that the player _Q_ 1 writes as the message _M_[1] 1[onto the] blackboard. Then player _Q_ 2 reads the message _M_[1] 1[and][use][it][as][the][memory][state][of] _[L][â€²]_[after][one][data][block] of size _N_ is fed in. _Q_ 2 now feeds its data _z_ 1[2] _[, . . . , z] N_[2][into] _[L][â€²]_[,][which][again][produces][a][memory][state][of] _[L][â€²]_[that] the player _Q_ 2 writes as the message _M_[1] 2[onto][the][blackboard.][We][proceed][like][this][and][when][player] _[Q][L]_[writes] its message _M_[1] _L_[,][the][algorithm] _[L][â€²]_[has][received][the][first][data][chunk][of][size] _[NL]_[(compare][with][Equation][(][E86][))] and we proceed to the next round to read in the next data chunk of size _NL_ . After all the _T_ 1 data chunks of size _NL_ are fed into _L[â€²]_ , it is now round _r_ = _T_ 1 and player _QL_ will write down the final output _B_[Ë†] of _L[â€²]_ , which 

97 

we define as the output of the communication protocol _Ï€_ . Since the data fed into _L[â€²]_ follows the distribution _D_[order][is the same as that of] _[ L][â€²]_[.][In the following, we focus on this communication] ( _Î³j_ ) _[L] j_ =1[, the success probability of] _[ Ï€]_ protocol _Ï€_ (after fixing its internal randomness appropriately). 

We prove that this protocol _Ï€_ cannot make good progress on any of the individual problem instances. 

**Lemma E.33** (Hardness of each individual problem instance) **.** E _B_ [bias _Ï€_ ( _Î², B_ )] _â‰¤_ 2 _Î´, âˆ€Î² âˆˆ_ [ _L_ ] _._ 

_Proof of Theorem E.33._ We prove it by constructing a learning algorithm _L_ with space complexity _T_ 1 _LS_ and sample complexity _T_ 1 _N_ that can output _Î³Î² âˆˆ{_ 0 _,_ 1 _}_ with decent probability given data generated from _Dg,N[N]_[(] _[o]_[)] _[, o][ âˆ¼][p][Î³] Î²_[,][which][contradicts][our][assumption][in][Theorem][E.32][.] 

Suppose for the sake of contradiction that there is a _Î² âˆˆ_ [ _L_ ] such that E _B_ [bias _Ï€_ ( _Î², B_ )] _>_ 2 _Î´_ . Let 

**==> picture [330 x 14] intentionally omitted <==**

be the most probable solution of _Î³Î²_ after the protocol sees the final blackboard content _B[r]_ = _B_ . Then, by the definition of bias _Ï€_ ( _Î², B_ ), we have 

**==> picture [345 x 22] intentionally omitted <==**

We use _z[Î²]_ = ( _z_ 1 _[Î²][, . . . , z] T[Î²]_ 1 _N_[)][to][denote][that][data][samples][corresponding][the] _[Î²]_[-th][problem][instance.] By the averaging argument, we know that there is a way of fixing all the other random data samples _z_[1] _, . . . , z[Î²][âˆ’]_[1] _, z[Î²]_[+1] _, . . . , z[L]_ to some _z_[1] _[âˆ—] , . . . , z[Î²][âˆ’]_[1] _[âˆ—] , z[Î²]_[+1] _[âˆ—] , . . . , z[L][âˆ—]_ such that 

**==> picture [297 x 21] intentionally omitted <==**

where _B[âˆ—]_ = _B[âˆ—]_ ( _z_[1] _[âˆ—] , . . . , z[Î²][âˆ’]_[1] _[âˆ—] , z[Î²] , z[Î²]_[+1] _[âˆ—] , . . . , z[L][âˆ—]_ ) is the random variable of the final blackboard content when the data is _z_[1] _[âˆ—] , . . . , z[Î²][âˆ’]_[1] _[âˆ—] , z[Î²] , z[Î²]_[+1] _[âˆ—] , . . . , z[L][âˆ—]_ . Note that it is a random variable with randomness induced by _z[Î²]_ only, since the communication protocol is deterministic. 

We now construct the learning algorithm _L_ by hard-coding _z_[1] _[âˆ—] , . . . , z[Î²][âˆ’]_[1] _[âˆ—] , z[Î²]_[+1] _[âˆ—] , . . . , z[L][âˆ—]_ . Specifically, _L_ proceeds as follows. Let _z[Î²]_ be the input data sequence of _L_ . At the beginning, _L_ first feeds _z_ 1[1] _[âˆ—][, . . . , z] N_[1] _[âˆ—][, . . . , z]_ 1 _[Î²][âˆ’]_[1] _[âˆ—] , . . . , zN[Î²][âˆ’]_[1] _[âˆ—]_ into the communication protocol _Ï€_ (and thus _L[â€²]_ ), and calculate all the messages _M_[1] 1 _[,][ M]_[1] _Î²âˆ’_ 1[.][Recall][that][these][messages][are][the][memory][states][of] _[L][â€²]_[after][processing][corresponding][data] blocks of size _N_ . When the first data sample _z_ 1 _[Î²]_[arrives,] _[L]_[feeds][it][into] _[L][â€²]_[,][obtain][the][memory][state][of] _[L][â€²]_[.][Now] _L_ writes the memory state and all the previous messages _M_[1] 1 _[,][ M]_[1] _Î²âˆ’_ 1[into][its][memory,][which][uses][(1 + (] _[Î²][ âˆ’]_[1))] _[S]_ bits of memory. In a similar way, _L_ moves on and feeds _z_ 2 _[Î²][, . . . , z] N[Î²]_[sequentially][into] _[L][â€²]_[.] After processing _zN[Î²]_[,][it][computes] _[M]_[1] _Î²_[and][also][put][this][message][into][its][memory.][Then,][it][feeds][the][rest][of][the][first][data][chunk] _z_ 1 _[Î²]_[+1] _[âˆ—] , . . . , zN[Î²]_[+1] _[âˆ—] , . . . , z_ 1 _[L][âˆ—][, . . . , z] N[L][âˆ—]_[into] _[ L][â€²]_[, compute the messages] _[ M]_[1] _Î²_ +1 _[, . . . ,][ M] L_[1][and store them inside its mem-] ory. In other words, after processing this first data chunk of size _NL_ , the algorithm _L_ now stores in its memory all the messages of the first round _M_[1] 1 _[, . . . ,][ M]_[1] _L_[,][using] _[LS]_[bits][of][memory.][This][completes][the][processing][of][the] first _N_ samples from _z[Î²]_ . Now, _L_ moves on to the next _N_ samples of _z[Î²]_ and process them in a similar way. It never erases its memory and keeps storing more messages. At the end, _L_ holds all the messages in its memory, which is the final blackboard content _B[âˆ—]_ . It computes Ë† _Î¸_ ( _B[âˆ—]_ ) and output it as the outcome. This means that the success probability of _L_ is Pr _Î³Î²_ = _Î¸_[Ë†] ( _B[âˆ—]_ ) _>_ 1 _/_ 2 + _Î´_ . ï¿½ ï¿½ Since the only things _L_ writes into its memory are all the messages _M_[1] 1 _[, . . . ,][ M][T] L_[1][,][which][correspond][to] _[T]_[1] _[L]_ snapshots of the memory states of _L[â€²]_ , the space complexity of _L_ is _T_ 1 _LS_ . The number of samples _L_ uses is _T_ 1 _N_ . Also, since the data of different _Î²_ â€™s are generated independently, the input distribution is the same as _D[N][âˆ¼][p][Î³]_[As][a][result,] _[L]_[is][a][learning][algorithm][with][space][complexity] _[T]_[1] _[LS]_[and][sample][complexity] _g,N_[(] _[o]_[)] _[, o] Î²_[.] _T_ 1 _N_ , that given data generated from _Dg,N[N]_[(] _[o]_[)] _[, o][ âˆ¼][p][Î³] Î²_[,][outputs] _[Î³][Î²]_[with][success][probability][more][than][1] _[/]_[2 +] _[ Î´]_[,] violating the assumption of Theorem E.32. This proves Theorem E.33. 

Now that we have proved that _Ï€_ cannot make good progress on each individual problem instance, we move on to show that it cannot make good progress on the final XOR problem. To do this, we need to show that different _Î³Î²_ â€™s are independent even when conditioned on the final blackboard content _B[r]_ , which can be used by _Ï€_ to make predictions. 

We make use of the following fact from information theory. 

**Lemma E.34** ([99, Proposition A.4]) **.** _For any random variables A, B, C, D, if A and D are independent conditioned on both B and C, then_ 

**==> picture [299 x 11] intentionally omitted <==**

98 

_Proof._ Note that since _A_ and _D_ are independent conditioned on _B, C_ , we have 

**==> picture [484 x 28] intentionally omitted <==**

_I_ ( _A_ ; _B|CD_ ) = _H_ ( _A|CD_ ) _âˆ’ H_ ( _A|BCD_ ) = _H_ ( _A|CD_ ) _âˆ’ H_ ( _A|BC_ ) _â‰¤ H_ ( _A|C_ ) _âˆ’ H_ ( _A|BC_ ) = _I_ ( _A_ ; _B|C_ ) _,_ (E96) where we have used the fact that conditioning reduces entropy _H_ ( _A|CD_ ) _â‰¤ H_ ( _A|C_ ). 

We use this to prove the following lemma that shows the conditional independence of problem instances. This property resembles the rectangle property of usual communication protocols on independent inputs. **Lemma E.35** (Conditional independence of problem instances) **.** _For any Î² âˆˆ_ [ _L_ ] _, let z[âˆ’][Î²]_ = ( _z_[1] _, . . . , z[Î²][âˆ’]_[1] _, z[Î²]_[+1] _, . . . , z[L]_ ) _. Then, for any final blackboard content B, z[Î²] and z[âˆ’][Î²] are independent conditioned on B[r]_ = _B._ 

_Proof of Theorem E.35._ We prove this by induction. First note that at the beginning of the game, the blackboard is empty and we have that _z[Î²]_ and _z[âˆ’][Î²]_ are independent, because the input data are independent. Next, assume that for some 0 _â‰¤ k â‰¤ r âˆ’_ 1, _z[Î²]_ and _z[âˆ’][Î²]_ are independent conditioned on _B[k]_ = _B, âˆ€B_ . We will prove that _z[Î²]_ and _z[âˆ’][Î²]_ are independent conditioned on _B[k]_[+1] = _B, âˆ€B_ . 

To this end, we look at the conditional mutual information _I_ ( _z[Î²]_ ; _z[âˆ’][Î²] |B[k]_[+1] ). We know from the inductive hypothesis that _I_ ( _z[Î²]_ ; _z[âˆ’][Î²] |B[k]_ ) = 0 because _z[Î²]_ and _z[âˆ’][Î²]_ are independent conditioned on _B[k]_ . On the other hand, note that _B[k]_[+1] = _B[k] M[k]_ 1[+1] _. . . M[k] L_[+1] = _BÎ²[k]_[+1] +1 _[M][k] Î²_[+1] +1 _[. . .][ M] L[k]_[+1] , and _M[k] Î²_[+1] +1 _[, . . . ,][ M] L[k]_[+1] are deterministic functions of _BÎ²[k]_[+1] +1[and] _[z][âˆ’][Î²]_[because] _[Ï€]_[is][deterministic.][Hence,] _[M][k] Î²_[+1] +1 _[, . . . ,][ M] L[k]_[+1] are deterministic and thus independent from _z[Î²]_ , conditioned on _BÎ²[k]_[+1] +1[and] _[z][âˆ’][Î²]_[.][This][allows][us][to][invoke][Theorem][E.34][and][obtain] 

**==> picture [396 x 14] intentionally omitted <==**

Next, note that _BÎ²[k]_[+1] +1[=] _[B] Î²[k]_[+1] _M[k] Î²_[+1] , and _M[k] Î²_[+1] is a deterministic function of _BÎ²[k]_[+1] and _z[Î²]_ . Hence, _M[k] Î²_[+1] is deterministic and thus independent from _z[âˆ’][Î²]_ , conditioned on _BÎ²[k]_[+1] and _z[Î²]_ . We again invoke Theorem E.34 and obtain 

**==> picture [484 x 47] intentionally omitted <==**

**==> picture [448 x 14] intentionally omitted <==**

Due to the non-negativity of conditional mutual information, we have 

**==> picture [287 x 13] intentionally omitted <==**

and thus _z[Î²]_ and _z[âˆ’][Î²]_ are independent conditioned on _B[k]_[+1] . This completes the induction and proves Theorem E.35. 

Meanwhile, for independent random bits, the bias of their XOR is dampened exponentially. 

**Lemma E.36** (XOR of independent random bits, [99, Prop. A.9]) **.** _Let X_ 1 _, . . . , XL be independent random bits. We have_ 

**==> picture [310 x 37] intentionally omitted <==**

_Proof of Theorem E.36._ We only need to show the case of _L_ = 2, and the general case follows directly by recursively grouping random bits. Let _X_ 1 _, X_ 2 be two independent random bits. Let _Î²_ 1 = bias( _X_ 1) _, Î²_ 2 = bias( _X_ 2) and _b_ 1 = argmax _xâˆˆ{_ 0 _,_ 1 _}_ Pr[ _X_ 1 = _x_ ] _, b_ 2 = argmax _xâˆˆ{_ 0 _,_ 1 _}_ Pr[ _X_ 2 = _x_ ]. Then Pr[ _X_ 1 = _b_ 1] = (1 + _Î²_ 1) _/_ 2 _,_ Pr[ _X_ 2 = _b_ 2] = (1 + _Î²_ 2) _/_ 2. From the independence of _X_ 1 _, X_ 2, we have 

**==> picture [425 x 75] intentionally omitted <==**

Therefore, we have bias( _X_ 1 _âŠ• X_ 2) = _Î²_ 1 _Î²_ 2 = bias( _X_ 1)bias( _X_ 2). This completes the proof of Theorem E.36. 

99 

By combining Theorems E.33, E.35 and E.36, we prove the derandomized learning XOR lemma Theorem E.32. _Proof of Theorem E.32._ Recall that the success probability of the communication protocol _Ï€_ is the same as that Ë† of the learning algorithm _L[â€²]_ , which we use _p_ succ = Pr _B_ = _B_ =[1] 2[+] 2[1][E] _[B]_[[bias] _[Ï€]_[[] _[B]_[]]][to][denote.][Our][goal][is][to] ï¿½ ï¿½ prove an upper bound on E _B_ [bias _Ï€_ [ _B_ ]] and therefore _p_ succ. 

To this end, we fix any final blackboard content _B_ . Note that Theorem E.35 implies that the _Î³Î²_ â€™s are independent from each other even conditioned on _B[r]_ = _B_ , because any _Î³Î²_ is only correlated with _z[Î²]_ and not _z[âˆ’][Î²]_ . This allows us to invoke Theorem E.36 and obtain 

**==> picture [407 x 38] intentionally omitted <==**

On the other hand, Theorem E.33 asserts that E _B_ [bias _Ï€_ ( _Î², B_ )] _â‰¤_ 2 _Î´, âˆ€Î² âˆˆ_ [ _L_ ]. Therefore, 

**==> picture [391 x 37] intentionally omitted <==**

where we have used the independence of bias _Ï€_ ( _Î², B_ ) again by Theorem E.35. Hence, we arrive at 

**==> picture [334 x 21] intentionally omitted <==**

This completes the proof of Theorem E.32. 

## _e. Proof of Theorem E.30_ 

We are now ready to prove the original learning XOR lemma (Theorem E.30). Recall that the general proof idea is the following. We first use the learning algorithm _L[âŠ•]_ to construct an algorithm _L[â€²]_ with the same success probability but learns from the derandomized distribution _D_[order][in][Theorem][E.31][.] Then, we ( _Î³j_ ) _[L] j_ =1[as] invoke Theorem E.32 to upper bound the success probability of _L[â€²]_ , which implies an upper bound the success probability of _L[âŠ•]_ . 

_Proof of Theorem E.30._ Let _L[âŠ•]_ be any randomized classical learning algorithm with space complexity _S_ and sample complexity _T_ 1 _N_ , such that given data generated from ( _D_ ([1] _Î³j ,oj ,Y_[(0] _[,j]_[)] _,Y_[(1] _[,j]_[)] ) _[L] j_ =1 _[â†’][Ã—][T]_[1] _[D]_ ([2] _Î²,Î±,Y_[(] _[Î±,Î²]_[)] ) _[â†’][Ã—][N][z]_[)] as in dynamic NOPE, outputs _B_ =[ï¿½] _[L] j_ =1 _[Î³][j][âˆˆ{]_[0] _[,]_[ 1] _[}]_[with][success][probability] _[p]_[succ][.][Theorem][E.31][implies][that] there exists a randomized classical learning algorithm _L[â€²]_ with space complexity _S_ + _âŒˆ_ log _LâŒ‰_ and sample complexity _T_ 1 _NL_ that given data generated from _D_ ([order] _Î³j_ ) _[L] j_ =1[,][outputs] _[B]_[=][ï¿½] _[L] j_ =1 _[Î³][j][âˆˆ{]_[0] _[,]_[ 1] _[}]_[with][probability] _[p]_[succ][.][Now][we] invoke Theorem E.32, which shares the assumption of Theorem E.30, and asserts that the success probability of _L[â€²]_ is at most 1 _/_ 2+(2 _Î´_ ) _[L] /_ 2. Therefore, we have _p_ succ _â‰¤_ 1 _/_ 2+(2 _Î´_ ) _[L] /_ 2, concluding the proof of Theorem E.30. 

## _f. Low advantage leads to large sample complexity_ 

The learning XOR lemma (Theorem E.30) shows that the advantage of predicting _B_ within a single _Î³ âˆˆ{_ 0 _,_ 1 _}[L]_ instance decays exponentially with _L_ . In this section, we translate this exponentially decaying advantage into a blow up in sample complexity using a hybrid argument. 

**Lemma E.37** (Low advantage leads to large sample complexity) **.** _Let Ï„ be a positive integer and Z be a finite set. Let D_ 0 _, D_ 1 _be two distributions on Z[Ï„] . Suppose that any randomized classical learning algorithm with space complexity S, sample complexity Ï„ , and input form Z, given a sequence of IID data samples from DB, B âˆˆ{_ 0 _,_ 1 _}, cannot output B with probability more than_ 1 _/_ 2+ _Î´. Then, any randomized classical learning algorithm with space complexity S, sample complexity M , and input form Z, that given a sequence of IID data samples from DB, B âˆˆ{_ 0 _,_ 1 _}, outputs B with probability at least_ 2 _/_ 3 _, must satisfy_ 

**==> picture [266 x 25] intentionally omitted <==**

100 

_Proof of Theorem E.37._ We prove Theorem E.37 using a hybrid argument. Let _L_ be a randomized classical learning algorithm with space complexity _S_ , sample complexity _M_ , and input form _Z_ , that given a sequence of IID data samples from _DB, B âˆˆ{_ 0 _,_ 1 _}_ , outputs _B_[Ë†] = _B_ with probability at least 2 _/_ 3. Let _r_ = _âŒˆM/Ï„ âŒ‰_ and _M[â€²]_ = _rÏ„ âˆˆ_ [ _M, M_ + _Ï„_ ]. We define a new learning algorithm _L[â€²]_ with sample complexity _M[â€²]_ (now a multiple of _Ï„_ ) by executing _L_ on the first _M_ samples and discard the rest. Clearly, it has the same space complexity and success probability as _L_ . 

Now we define _r_ + 1 hybrid probability distributions 

**==> picture [327 x 12] intentionally omitted <==**

In particular, _M[â€²]_ = _rÏ„_ data samples drawn from _D_ 0 follows the distribution _H_ 0 = _D_ 0 _[âŠ—][r]_[,][while] _[M][ â€²]_[data][samples] drawn from _D_ 1 follows the distribution _Hr_ = _D_ 1 _[âŠ—][r]_[.][We][use] _[Z]_[=][(] _[Z]_[1] _[,][ Â· Â· Â·][, Z][r]_[)][to][denote][the][data][samples.] Note that here each _Zi âˆˆZ[Ï„]_ consists of _Ï„_ samples that may have correlation among them. Then, the learning guarantee of _L[â€²]_ reads 

**==> picture [339 x 25] intentionally omitted <==**

On the other hand, triangle inequality implies that 

**==> picture [406 x 93] intentionally omitted <==**

Let _i[âˆ—]_ = argmax _iâˆˆ_ [ _r_ ] ï¿½ï¿½ï¿½Pr _Zâˆ¼Hi_ [ Ë† _B_ = 1] _âˆ’_ Pr _Zâˆ¼Hiâˆ’_ 1[ Ë† _B_ = 1]ï¿½ï¿½ï¿½ be any _i âˆˆ_ [ _r_ ] that maximizes the value. Then, 

**==> picture [329 x 25] intentionally omitted <==**

Now we use the learning algorithm _L[â€²]_ to construct another learning algorithm _L_ 0 with space complexity _S_ , sample complexity _Ï„_ , and input form _Z_ , that given a sequence of IID data from _DB, B âˆˆ{_ 0 _,_ 1 _}_ , outputs _B_[Ë†] 0 = _B_ with probability at least 1 _/_ 2 + 1 _/_ (6 _r_ ). Note that if this is true, Theorem E.37 follows immediately. This is because the assumption implies that 

**==> picture [277 x 22] intentionally omitted <==**

and therefore 

**==> picture [299 x 25] intentionally omitted <==**

which yields the desired result 

**==> picture [280 x 25] intentionally omitted <==**

and completes the proof. 

To construct _L_ 0, we hard-code _i[â‹†]_ , _L[â€²]_ , and _D_ 0 _, D_ 1 into the construction as follows. _L_ 0 first draws _i[âˆ—] âˆ’_ 1 IID data blocks of size _Ï„_ from _D_ 1 and feeds them into _L[â€²]_ . Next, _L_ 0 reads in the actual input data of size _Ï„_ and feeds it into _L[â€²]_ . Then, it draws _r âˆ’ i[âˆ—]_ IID data blocks from _D_ 0 and feeds them into _L[â€²]_ . Finally, _L_ 0 collects the output of _L[â€²]_ and outputs it as the outcome. 

Note that if the input of _L_ 0 is drawn from _D_ 0, then the _M[â€²]_ = _rÏ„_ data samples fed into _L[â€²]_ follows the distribution _Hiâ‹†âˆ’_ 1. On the other hand, if the input of _L_ 0 is drawn from _D_ 1, then the data samples fed into _L[â€²]_ follows _Hiâ‹†_ . Hence, Equation (E110) implies that _L_ 0 has success probability at least 

**==> picture [359 x 30] intentionally omitted <==**

Moreover, by construction, _L_ 0 indeed has space complexity _S_ and sample complexity _Ï„_ . This concludes the proof of Theorem E.37. 

101 

## _g. Proof of Theorems E.27 and E.28_ 

We are now ready to prove the classical single-block hardness and sample complexity of dynamic NOPE (Theorems E.27 and E.28). We will make use of the distributional sample-space lower bound (Theorem E.29), the learning XOR lemma (Theorem E.30), and the sample complexity blow-up from low advantage (Theorem E.37). 

_Proof of Theorems E.27 and E.28._ Let _L_ be any randomized classical learning algorithm with space complexity _S_ , sample complexity _M_ , and input form _I_ = [ _N_ ] _Ã— {_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _} Ã—_ [ _L_ ] such that it solves dynamic NOPE with probability at least 2 _/_ 3. That is, for any _B âˆˆ{_ 0 _,_ 1 _}_ , given data generated from _Dg,f[N,T]_[1] ( _B_ ), _L_ outputs _B_ with probability at least 2 _/_ 3. Define _S_ 1 = _T_ 1 _L_ ( _S_ + _âŒˆ_ log _LâŒ‰_ ) and _M_ 1 = _T_ 1 _N_ as in the learning XOR lemma (Theorem E.30). Note that the assumption 

**==> picture [288 x 26] intentionally omitted <==**

implies that 

**==> picture [461 x 26] intentionally omitted <==**

where we have used _QC â‰¥_ â„¦( _T_ 1[2] _[L]_[ log log] _[ N]_[),] _[L]_[=] ï¿½log[2] ( _N_ )ï¿½, and _b_ = _âŒˆc_ log _N âŒ‰_ . Then the distributional sample-space lower bound (Theorem E.29) asserts that any randomized classical learning algorithm with space complexity _S_ 1, sample complexity _M_ 1, and input form _I_ 1 = [ _N_ ] _Ã— {_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}_ , given data generated from _D[N]_[cannot][output] _[Î³]_[with][probability][more][than] _g,N_[(] _[o]_[)] _[, o][ âˆ¼][p][Î³]_[,] 

**==> picture [370 x 21] intentionally omitted <==**

where we have used _QC_ being the (1 _/_ 3)-error query complexity and _b > c_ log _N â‰¥ c â‰¥_ 865 _/Î·_[2] _>_ 200 since _Î· âˆˆ_ (0 _._ 1 _,_ 2]. This gives us the assumption we need for invoking the learning XOR lemma (Theorem E.30) with _Î´_ = 1 _/_ 3, which implies that any randomized classical learning algorithm _L[âŠ•]_ with space complexity _S_ , sample complexity _T_ 1 _N_ = _Ï„D_ , and input form _I_ 1 _Ã—_ [ _L_ ] = [ _N_ ] _Ã— {_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _} Ã—_ [ _L_ ] = _I_ , given data generated from ( _D_ ([1] _Î³j ,oj ,Y_[(0] _[,j]_[)] _,Y_[(1] _[,j]_[)] ) _[L] j_ =1 _[â†’][Ã—][T]_[1] _[D]_ ([2] _Î²,Î±,Y_[(] _[Î±,Î²]_[)] ) _[â†’][Ã—][N][z]_[),][cannot][output] _[B]_[=][ï¿½] _[L] j_ =1 _[Î³][j][âˆˆ{]_[0] _[,]_[ 1] _[}]_[with][success] probability more than 

**==> picture [299 x 23] intentionally omitted <==**

This proves Theorem E.27. 

This is also exactly the assumption we need for invoking Theorem E.37 that shows low advantage leads to sample complexity blow up with _Ï„_ = _T_ 1 _N_ = _Ï„D, Î´_ = (2 _/_ 3) _[L] /_ 2 _, Z_ = _I_ . Applying Theorem E.37 to _L_ gives us 

**==> picture [443 x 25] intentionally omitted <==**

where we have used _L â‰¥_ 5 _>_ log3 _/_ 2(6) such that 1 _â‰¤_ 1 _/_ (6(3 _/_ 2) _[L]_ ). This concludes the proof of Theorem E.28. 

## **5. Connect to applications** 

In this section, we develop the necessary tools that connect dynamic NOPE to the various application tasks that we will explore in Section F, such as solving linear systems, binary classification, dimension reduction, etc. We begin by focusing on a specific oracle property called Forrelation [95, 96] and take the inner product function as the noisy encoding function. We design a distributional version of Forrelation, show that inner product is a good noisy encoding function, and prove some useful lemmas in Section E 5 a. 

In Section E 5 b, we construct an efficient quantum circuit that solves the dynamic NOPE task, which we then embed into various applications. In particular, in Sections E 5 c to E 5 e, we embed this circuit into the tasks of solving linear systems, binary classification, and dimension reduction. This shows that if we can solve the application tasks, we can solve dynamic NOPE, which is hard. Hence the application tasks must also be hard to solve. The full hardness proofs will be given in Section F for the various application tasks. 

102 

## _a. Forrelation and inner product_ 

We first introduce the oracle property function _f_ that we will use in dynamic NOPE. In particular, we consider the following oracle query problem called Forrelation. 

**Definition E.38** (( _Î´, K, n_ )-Forrelation, [95, 96]) **.** _Let n be a positive integer and N_ = 2 _[n] . Let K â‰¥_ 2 _be an integer and let Î´ âˆˆ_ (0 _,_ 1) _. We define the partial Boolean function_ forr _[n] Î´,K_[:] _[ {]_[0] _[,]_[ 1] _[}][KN][â†’{]_[0] _[,]_[ 1] _[}][as]_ 

**==> picture [326 x 31] intentionally omitted <==**

_where_ 

**==> picture [421 x 27] intentionally omitted <==**

**==> picture [400 x 25] intentionally omitted <==**

Forrelation has a _OÏµ_ (1) versus â„¦( _N_[1] _[âˆ’][Ïµ]_ ) quantum-classical query complexity separation for any arbitrarily small constant _Ïµ >_ 0. Specifically, [96] showed that there are two distributions _p[â€²]_ 0 _[, p]_ 1 _[â€²]_[over] _[{]_[0] _[,]_[ 1] _[}][KN]_[such][that] the following holds. Note that we are using the _{_ 0 _,_ 1 _}_ notation for oracles whereas [96] used _{Â±_ 1 _}_ . 

**Lemma E.39** (Oracle distributions for Forrelation, [96, Figure 1, Theorem 3.1, Section 5.4]) **.** _Let K â‰¥_ 2 _, n, N_ = 2 _[n] be positive integers and Î´_ = 2 _[âˆ’]_[5] _[K] . There are two distributions p[â€²]_ 0 _[, p]_ 1 _[â€²][supported][on][{]_[0] _[,]_[ 1] _[}][KN][such][that]_ 

**==> picture [319 x 13] intentionally omitted <==**

_2. Any classical query algorithm A that queries o âˆˆ{_ 0 _,_ 1 _}[KN] and outputs A_ ( _o_ ) _âˆˆ{_ 0 _,_ 1 _} such that_ 

**==> picture [301 x 22] intentionally omitted <==**

_must make at least_ 

**==> picture [294 x 31] intentionally omitted <==**

## _queries to o._ 

Recall that in dynamic NOPE, we need a property function that has a large distributional classical query complexity. But in Item 1 of Theorem E.39, the distribution _pÎ³, Î³ âˆˆ{_ 0 _,_ 1 _}_ does not always give an oracle _o_ with the corresponding property forr _[n] Î´,K_[(] _[o]_[)][=] _[Î³]_[.][This][means][that][an][algorithm][that][computes][Forrelation][may][not] be able to identify the underlying distribution _p[â€²] Î³_[,][which][is][required][to][solve][dynamic][NOPE.][To][fix][this][issue,] we regularize the distributions by truncating the support of _p[â€²] Î³[, Î³][âˆˆ{]_[0] _[,]_[ 1] _[}]_[to] 

**==> picture [335 x 14] intentionally omitted <==**

We use _pÎ³_ to denote the regularized distributions. More formally, we define _pÎ³_ to be the conditional distribution 

**==> picture [392 x 31] intentionally omitted <==**

In Theorem E.40, we will show that the classical distributional query complexity for identifying _pÎ³_ remains the same as in Theorem E.39 up to a factor of _K_ . 

On the other hand, the quantum algorithm for computing Forrelation [95, Proposition 6] is simple. It executes the circuit given in Theorem E.38 on log _N_ +1 qubits and identifies _pÎ³_ via a standard majority voting technique that boosts the 1 _/_ 2+Î˜( _Î´_ ) success probability to 1 _âˆ’ Î·_ with _O_ (log(1 _/Î·_ ) _/Î´_[2] ) repetitions and _O_ (logï¿½log(1 _/Î·_ ) _/Î´_[2][ï¿½] ) ancilla bits as the running counter for votes [96, Corrollary 1.4]. 

Together, we have the following distributional query complexity separation of Forrelation. 

103 

**Lemma E.40** (Distributional query complexity separation of Forrelation) **.** _Let n be a large integer and N_ = 2 _[n] . Let K â‰¥_ 2 _be an integer and let Î´_ = 2 _[âˆ’]_[5] _[K] . Let Î· âˆˆ_ (0 _,_ 1 _/_ 3] _. Then, there exists two distributions p_ 0 _, p_ 1 _supported on {_ 0 _,_ 1 _}[KN] and defined by_ forr _[n] Î´,K[such][that][given][o][âˆ¼][p][Î³][, Î³][âˆˆ{]_[0] _[,]_[ 1] _[}][,][there][exists][a][quantum] algorithm with_ log _N_ + _O_ (log log(1 _/Î·_ ) + _K_ ) _space complexity, O_ ( _K_ 2[10] _[K]_ log _N_ log(1 _/Î·_ )) _gate complexity, making O_ ( _K_ 2[10] _[K]_ log(1 _/Î·_ )) _queries that outputs Î³ with success probability at least_ 1 _âˆ’ Î·. Meanwhile, any randomized classical algorithm that can output Î³ with success probability at least_ 2 _/_ 3 _must make_ 

**==> picture [307 x 31] intentionally omitted <==**

## _queries._ 

_Proof of Theorem E.40._ We only need to show that the query complexity lower bound in Theorem E.39 for _p[â€²]_ 0 _[, p]_ 1 _[â€²]_ implies query complexity lower bound for _p_ 0 _, p_ 1. To this end, suppose we have a classical query algorithm _A_ that queries _o âˆˆ{_ 0 _,_ 1 _}[KN] , o âˆ¼ pÎ³, Î³ âˆˆ{_ 0 _,_ 1 _} Q_ times and outputs _A_ ( _o_ ) _âˆˆ{_ 0 _,_ 1 _}_ that is equal to _Î³_ with probability at least 2 _/_ 3. Then, we can amplify its success probability to 1 _âˆ’ Î´_ by making _Ï„_ = Î˜(log(1 _/Î´_ )) = Î˜( _K_ ) repetitions and taking majority vote. The resulting algorithm _A[â€²]_ has advantage 

**==> picture [353 x 12] intentionally omitted <==**

Now note that _pÎ³_ are defined as _p[â€²] Î³_[conditioned][on][forr] _[n] Î´,K_[(] _[o]_[) =] _[ Î³]_[.][This][means][that] 

**==> picture [473 x 88] intentionally omitted <==**

for some constant _N_ large, since _Î´_ = 2 _[âˆ’]_[5] _[K]_ with _K â‰¥_ 2 being a constant. Item 2 of Theorem E.39 then implies that 

**==> picture [320 x 31] intentionally omitted <==**

and therefore 

**==> picture [318 x 31] intentionally omitted <==**

as desired, because _Ï„_ = Î˜( _K_ ). This completes the proof of Theorem E.40. 

Next, we introduce the inner product function as our noisy encoding function. 

**Definition E.41** (Inner product noisy encoding function) **.** _Let b be a positive integer. We define the inner product noisy encoding function g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} as_ 

**==> picture [310 x 30] intentionally omitted <==**

The following standard proof shows that the inner product noisy encoding function _g_ has low discrepancy (defined in Theorem E.9) disc( _g_ ) _â‰¤_ 2 _[âˆ’][Î·b]_ with _Î·_ = 1 _/_ 2. 

**Lemma E.42** (Inner product has low discrepancy) **.** _Let b be a positive integer and g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be the inner product noisy encoding function. Then,_ 

**==> picture [277 x 13] intentionally omitted <==**

104 

_Proof of Theorem E.42._ Let _R_ = _S Ã— T_ be any rectangle where _S, T âˆˆ{_ 0 _,_ 1 _}[b]_ . Let _U, V âˆ¼_ Uniform( _{_ 0 _,_ 1 _}[b]_ ). From Theorem E.9, we have 

**==> picture [394 x 76] intentionally omitted <==**

where _s, t âˆˆ{_ 0 _,_ 1 _}_[2] _[b]_ are length-2 _[b]_ Boolean vectors such that _su_ = 1[ _u âˆˆ S_ ] and _tv_ = 1[ _v âˆˆ T_ ] for all _u, v âˆˆ{_ 0 _,_ 1 _}[b]_ , and _H âˆˆ{Â±_ 1 _}_[2] _[b][Ã—]_[2] _[b]_ such that _Huv_ = ( _âˆ’_ 1) _[g]_[(] _[u,v]_[)] _/_ 2 _[b/]_[2] . Note that there we are identifying length- _b_ bitstrings with elements from [2 _[b]_ ]. 

Next, we prove that _H_ is an orthogonal matrix. Indeed, the matrix element reads 

**==> picture [334 x 179] intentionally omitted <==**

Hence, _H[T] H_ = _I_ , and we arrive at 

**==> picture [417 x 21] intentionally omitted <==**

for any rectangle _R_ . Therefore, disc( _g_ ) _â‰¤_ 2 _[âˆ’][b/]_[2] . 

We will embed quantum circuits into application tasks, which naturally involve complex numbers. However, in most classical data processing applications, we work in real numbers. The following standard lemma provides a canonical way to realify complex matrices and vectors. 

**Lemma E.43** (Realification) **.** _For any complex vector âƒ—v âˆˆ_ C _[d] , we define its realification R_ [ _âƒ—v_ ] _âˆˆ_ R[2] _[d] as_ 

**==> picture [280 x 25] intentionally omitted <==**

_For any complex matrix A âˆˆ_ C _[d][Ã—][d] , we define its realification R_ [ _A_ ] _âˆˆ_ R[2] _[d][Ã—]_[2] _[d] as_ 

**==> picture [302 x 25] intentionally omitted <==**

_Then, the following properties hold_ 

_1. (Isometry): âˆ¥R_ [ _âƒ—v_ ] _âˆ¥_ 2 = _âˆ¥âƒ—vâˆ¥_ 2 _, âˆ€âƒ—v âˆˆ_ C _[d] ._ 

_2. (Inner product): R_ [ _âƒ—u_ ] _[T] R_ [ _âƒ—v_ ] = Re[ _âƒ—u[â€ ] âƒ—v_ ] _, âˆ€âƒ—u,âƒ—v âˆˆ_ C _[d] ._ 

_3. (Linearity): R_ [ _Aâƒ—v_ ] = _R_ [ _A_ ] _R_ [ _âƒ—v_ ] _, âˆ€A âˆˆ_ C _[d][Ã—][d] ,âƒ—v âˆˆ_ C _[d] ._ 

_4. (Matrix operations): for any A, B âˆˆ_ C _[d][Ã—][d] , R_ [ _AB_ ] = _R_ [ _A_ ] _R_ [ _B_ ] _, R_ [ _A[â€ ]_ ] = _R_ [ _A_ ] _[T] . If A is invertible, R_ [ _A_ ] _[âˆ’]_[1] = _R_ [ _A[âˆ’]_[1] ] _._ 

105 

_5. (Singular values): For any A âˆˆ_ C _[d][Ã—][d] , the singular values of R_ [ _A_ ] _are the same as those of A, with doubled multiplicity. Consequently, the norm and condition number of R_ [ _A_ ] _are the same as those of A._ 

_6. (Structured matrices): The realification of Hermitian matrices are symmetric. The realification of unitary matrices are orthogonal. The realification of s-sparse matrices are_ 2 _s-sparse._ 

_7. (Eigenvectors): For any Hermitian matrix A âˆˆ_ C _[d][Ã—][d] with the largest eigenvalue Î» and a unique corresponding eigenvector âƒ—v, its realification R_ [ _A_ ] _is symmetric with a two-fold degenerate largest eigenvalue Î» corresponding to two eigenvectors R_ [ _âƒ—v_ ] _, R_ [ _iâƒ—v_ ] _._ 

The above standard realification doubles the eigenvalue degeneracy of a matrix. To avoid that, we use the following realification of quantum circuits [179, 180]. 

**Lemma E.44** (Realification of quantum circuits) **.** _Let UT Â· Â· Â· U_ 1 _, Ui âˆˆ U_ (2 _[n]_ ) _be a sequence of T unitaries on n qubits. Let |ÏˆâŸ©âˆˆ_ C[2] _[n] be an n-qubit quantum state. Then, R_ [ _Ui_ ] _, i âˆˆ_ [ _T_ ] _are_ 2 _[n]_[+1] _-dimensional real, orthogonal matrices and therefore unitaries on n_ + 1 _qubits. Similarly, R_ [ _|ÏˆâŸ©_ ] _is a quantum state on n_ + 1 _qubits with real components. In particular, R_ [ _|xâŸ©_ ] = _|_ 0 _âŸ©|xâŸ© , âˆ€x âˆˆ{_ 0 _,_ 1 _}[n] ._ 

_Proof._ This follows directly from Items 1 and 6 of Theorem E.43. 

Theorem E.44 avoids the degeneracy problem because of the simple observation: the eigenspace of _R_ [ _|ÏˆâŸ©âŸ¨Ïˆ|_ ] with eigenvalue one is (doubly) degenerate, while that of _R_ [ _|ÏˆâŸ©_ ] _R_ [ _|ÏˆâŸ©_ ] _[T]_ is not. 

## _b. Quantum circuit for dynamic NOPE_ 

In this section, we construct a quantum circuit that efficiently solves the dynamic NOPE task in Section E 4 for the oracle property Forrelation with inner product noisy encoding. Then we embed this quantum circuit into various application tasks that will be used in Section F. 

The following lemma gives us the desired circuit. 

**Lemma E.45** (Quantum circuit for dynamic NOPE) **.** _Let n, N_ = 2 _[n] , T_ 1 _be large integers. Let K â‰¥_ 2 _be a constant integer. Let g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _} be the inner product noisy encoding function with encoding length b_ = _âŒˆ_ 40678 log( _KN_ ) _âŒ‰. Consider the oracle property function f_ = forr _[n]_ 2 _[âˆ’]_[5] _[K] ,K_[:] _[ {]_[0] _[,]_[ 1] _[}][KN][â†’{]_[0] _[,]_[ 1] _[}][.][Then,] there exists a_ (log _N_ + _O_ (log log _N_ )) _-qubit quantum circuit C consisting of O_ (log[3] _N_ log log _N_ ) _fixed two-qubit gates and O_ (log[2] _N_ log log _N_ ) _diagonal gates of the form_ 

**==> picture [380 x 27] intentionally omitted <==**

_or its controlled version cO_ 0 _, where Y_[(] _[Î±,Î²]_[)] _âˆˆ{_ 0 _,_ 1 _}[KN][Ã—][b] are any noisy encodings that can be generated in a single refreshing block of Dg,f[KN,T]_[1] ( _B_ ) _, such that the probability of measuring B in the first qubit of C |_ 0 _âŸ© is at least_ 0 _._ 9 _. Moreover, all the other qubits of C |_ 0 _âŸ© are in the |_ 0 _âŸ© state._ 

_Proof of Theorem E.45._ Recall that the data generation process, as defined in Section E 4, reads 

**==> picture [400 x 17] intentionally omitted <==**

where _Î³j âˆˆ{_ 0 _,_ 1 _}_ , _oj âˆˆ{_ 0 _,_ 1 _}[KN]_ , _Y_[(0] _[,j]_[)] _, Y_[(1] _[,j]_[)] _âˆˆ{_ 0 _,_ 1 _}[KN][Ã—][b]_ , _Î² âˆˆ_ [ _L_ ], _Î± âˆˆ{_ 0 _,_ 1 _}_ , and _zi_ = ( _xi, yi, Î±i, Î²i_ ) with _xi âˆˆ_ [ _KN_ ] and _yi âˆˆ{_ 0 _,_ 1 _}[b]_ . Here, _L_ = ï¿½log[2] ( _KN_ )ï¿½ _â‰¥_ 5. To prove Theorem E.45, we construct a quantum query algorithm that queries the unitary 

**==> picture [424 x 15] intentionally omitted <==**

and its controlled version _cO_ 0, and predicts _B_ with success probability at least 2 _/_ 3. Note that the number of qubits that _O_ 0 acts on is 

**==> picture [387 x 11] intentionally omitted <==**

because _L_ = ï¿½log[2] ( _KN_ )ï¿½ and _b_ = _âŒˆ_ 40678 log( _KN_ ) _âŒ‰_ . To construct the quantum query algorithm that predicts _B_ , we start by computing the oracle values _oÎ² âˆˆ {_ 0 _,_ 1 _}[KN] , Î² âˆˆ_ [ _L_ ] from _Y_[(] _[Î±,Î²]_[)] _âˆˆ{_ 0 _,_ 1 _}[KN][Ã—][b] , Î± âˆˆ{_ 0 _,_ 1 _}_ using the inner product noisy encoding map _g_ : _{_ 0 _,_ 1 _}[b] Ã— {_ 0 _,_ 1 _}[b] â†’{_ 0 _,_ 1 _}_ . In particular, we introduce an ancilla qubit _a_ and note that 

**==> picture [385 x 20] intentionally omitted <==**

106 

gives us the standard XOR oracle on _n_ 1 + 1 qubits using two Hadamard gates. Now, we introduce three ancilla qubits _a, a_ 1 _, a_ 2 and do the following steps. We start from 

**==> picture [296 x 12] intentionally omitted <==**

and apply _O_ 0 _[âŠ•]_[with][ancilla] _[a]_[1][,][yielding] 

**==> picture [318 x 21] intentionally omitted <==**

Then we apply a NOT gate on the _Î±_ register and apply _O_ 0 _[âŠ•]_[with][ancilla] _[a]_[2][,][obtaining] 

**==> picture [338 x 21] intentionally omitted <==**

Next, we apply an AND gate on _a_ 1 _, a_ 2 and store the result in _a_ 1. This gives us 

**==> picture [363 x 21] intentionally omitted <==**

Finally, we apply a CNOT gate on _a_ 1 _, a_ to copy out the result and uncompute everything. Note that the inverse unitaries used in uncomputation are the same as the original unitaries _O_ 0 _[â€ ]_[=] _[ O]_[0][.][This][constructs][the][unitary] 

**==> picture [377 x 20] intentionally omitted <==**

using only two ancilla qubits and _O_ (1) queries to _O_ 0 _[âŠ•]_[.][From] _[O]_ 0 _[âŠ•][,]_[prod] , we compute the inner product as follows. We start from _|x, Î²,_ 1 _âŸ©|Ï‡âŸ©a_ and apply _O_ 0 _[âŠ•][,]_[prod] , giving us 

**==> picture [324 x 20] intentionally omitted <==**

Then we add one to the _k_ register and apply _O_ 0 _[âŠ•][,]_[prod] . We repeat this until _k_ = _b_ and add another one to it to take _k_ back to 0. The final state is 

**==> picture [479 x 33] intentionally omitted <==**

In this way, we have constructed the unitary 

**==> picture [320 x 12] intentionally omitted <==**

using _O_ (1) ancilla and _O_ ( _b_ ) queries to _O_ 0 _[âŠ•]_[.][Lastly,][we][turn][this][into][the][phase][oracle] 

**==> picture [353 x 12] intentionally omitted <==**

with one more ancilla (e.g., in _|âˆ’âŸ©_ ). As a result, we have constructed the phase oracle for solving any _Î² âˆˆ_ [ _L_ ] instance of the Forrelation problem (see Theorem E.38) using _O_ (1) ancilla and _O_ ( _b_ ) queries to _O_ 0. Note that here we are computing the inner product bit by bit at the cost of an additional factor of _b_ in query complexity, as compared to use _O_ ( _b_ ) ancilla and compute the inner product directly. We choose this way of computing the inner product to keep the space complexity small: log _N_ + _O_ (log log _N_ ) rather than _O_ ( _b_ ) = _c_ log _N_ with a large constant _c_ . This will be crucial in determining the size of the linear system in Theorem E.46 and proving the final classical hardness result with the optimal exponent. 

Now, we invoke Theorem E.40, which gives us a quantum algorithm _A[O]_ with log _N_ + _O_ (log log(1 _/Î·_ )) space complexity, _O_ ( _K_ 2[10] _[K]_ log _N_ log(1 _/Î·_ )) = _O_ (log _N_ log(1 _/Î·_ )) gate complexity, making _O_ ( _K_ 2[10] _[K]_ log(1 _/Î·_ )) = _O_ (log(1 _/Î·_ )) queries to _O_ (with _Î²_ register set to _Î²_ ) that outputs _Î³Î²_ with success probability at least 1 _âˆ’ Î·_ , when _oÎ² âˆ¼ pÎ³Î²_ . Using _A[O]_ , we compute the parity _B_ =[ï¿½] _[L] Î²_ =1 _[Î³][Î²]_[as][follows.][We][introduce][an][ancilla][qubit] _a_ to record the result. We first initialize the _Î²_ register to _|_ 1 _âŸ©_ , execute _A[O]_ , and apply a CNOT gate to copy the output qubit to the ancilla _a_ . Then we run _A[O]_ in reverse to uncompute, add one to _Î²_ , execute _A[O]_ again (now for _Î²_ = 2), and copy out the result with a CNOT gate. We repeat the above procedure until _Î²_ = _L_ . Finally, we measure the ancilla qubit and output the measurement outcome. The union bound asserts that with probability at least 1 _âˆ’_ 2 _LÎ·_ , all 2 _L_ executions so _A[O]_ and its inverse are simultaneously correct and the output bit is equal to _B_ =[ï¿½] _[L] Î²_ =1 _[Î³][Î²]_[.][Note][that][here][we][are][reusing][the][ancilla][and][working][space][for][different] 

107 

executions of _A[O]_ by uncomputation to save space. We set _Î·_ = 1 _/_ (20 _L_ ). Then we have a quantum circuit _A_ such that when we measure the first qubit (the ancilla _a_ ), we obtain _B_ with success probability at least 0 _._ 9. It has space complexity _n_ 1 + _O_ (log log _L_ ) = log _N_ + _O_ (log log _N_ ) + _O_ (log log _L_ ) = log _N_ + _O_ (log log _N_ ), gate complexity _O_ ( _L_ log _N_ log(1 _/Î·_ )) = _O_ ( _L_ log _N_ log log _N_ ) = _O_ (log[3] _N_ log log _N_ ), and queries _O_ 0 

**==> picture [325 x 12] intentionally omitted <==**

times. Moreover, since we always uncompute every time we execute _A[O]_ , all the remaining qubits end up in the _|_ 0 _âŸ©_ state. This completes the proof of Theorem E.45. 

**==> picture [121 x 9] intentionally omitted <==**

Next, we embed this quantum circuit into a sparse and well-conditioned matrix following the idea of [118], such that solving the linear system given by this matrix is as hard as executing the quantum circuit. This will be used to prove the classical hardness of linear system in Section F 1. 

**Lemma E.46** (Embed a quantum circuit into a real linear system) **.** _Let n be a large integer and T, s be positive integers. Let UT Â· Â· Â· U_ 1 _be an n-qubit quantum circuit composed of T n-qubit unitaries Ui, i âˆˆ_ [ _T_ ] _that are all s-sparse. Define a_ 3 _T_ 2 _[n] dimensional unitary U as_ 

**==> picture [461 x 30] intentionally omitted <==**

_Let_ 

**==> picture [394 x 25] intentionally omitted <==**

_where the basis vectors in the first part of the factorization_ C[2] _[Ã—]_[2] _are labeled by {|_ 0 _aâŸ© , |_ 1 _aâŸ©}. Let P âˆˆ_ C[6] _[T]_[ 2] _[n][Ã—]_[6] _[T]_[ 2] _[n] be the basis permutation matrix that swaps |_ 0 _aâŸ© and |_ 1 _aâŸ© while keeping the rest unchanged. Similarly, define R âˆˆ_ C[6] _[T]_[ 2] _[n][Ã—]_[6] _[T]_[ 2] _[n] to be the basis permutation matrix that swaps the basis vectors |_ 1 _aâŸ©|tâŸ©|_ 0 _âŸ©|Ï‡âŸ© and |_ 0 _aâŸ©|tâŸ©|_ 0 _âŸ©|Ï‡âŸ© for all t âˆˆ_ [ _T_ + 1 _,_ 2 _T_ ] _, Ï‡ âˆˆ{_ 0 _,_ 1 _}[n][âˆ’]_[1] _and keeps the rest unchanged. Consider_ 

**==> picture [389 x 55] intentionally omitted <==**

_whose realification_ 

**==> picture [350 x 13] intentionally omitted <==**

_define a real linear system Aâƒ—x_ = _[âƒ—] b of dimension_ 24 _T_ 2 _[n] for âƒ—x âˆˆ_ R[24] _[T]_[ 2] _[n] ._ 

_Then, A is real, symmetric and O_ ( _s_ ) _-sparse with operator norm âˆ¥Aâˆ¥â‰¤_ 1 _and condition number Îº_ = _âˆ¥A[âˆ’]_[1] _âˆ¥âˆ¥Aâˆ¥â‰¤_ 4 _T . Moreover, let_ 

**==> picture [373 x 25] intentionally omitted <==**

_The solution vector âƒ—x satisfies_ 

**==> picture [336 x 25] intentionally omitted <==**

_where |ÏˆâŸ©_ = _UT Â· Â· Â· U_ 1 _|_ 0 _âŸ© is the n-qubit output state of the circuit and |_ 01 _âŸ© is the zero state on the first qubit of the circuit._ 

_Proof of Theorem E.46._ First note that _Ac_ is clearly Hermitian _A[â€ ] c_[=] _[A][c]_[by][construction.][Therefore,][its][reali-] fication _A_ is symmetric. Its sparsity depends on _U_ . Since for any basis state with some clock value _|tâŸ©_ , there is only one term in _U_ that acts on it, changes the clock value to _|t_ + 1 _âŸ©_ , and applies an _s_ -sparse unitary _Ut_ (or _I, UT[â€ ]_ +1 _âˆ’t_[),][thus][the][unitary] _[U]_[is][also] _[s]_[-sparse.][Therefore,] _[A][c]_[and][its][realification] _[A]_[=] _[R]_[[] _[A][c]_[]][are][both] _[O]_[(] _[s]_[)] 

108 

_P[â€ ] BcBc[â€ ][P]_ 0 sparse. To compute its condition number, note that _A[â€ ] c[A][c]_[=][1] 4 ï¿½ 0 _R[â€ ] Bc[â€ ][B][c][R]_ ï¿½. Since _P, R_ are basis permutation matrix, the singular values of _Ac_ are the same as those of _Bc/_ 2, and thus _A, Ac, Bc_ share the same condition number _Îº_ . _Bc_ is clearly invertible by construction. Moreover, _âˆ¥Bcâˆ¥â‰¤_ 1 + _e[âˆ’]_[1] _[/T] <_ 2 and 

**==> picture [322 x 23] intentionally omitted <==**

because 1 _âˆ’ e[âˆ’][w] â‰¥ w/_ 2 _, âˆ€w âˆˆ_ (0 _,_ 1]. Therefore, we have condition number _Îº_ = _âˆ¥Bcâˆ¥âˆ¥Bc[âˆ’]_[1] _[âˆ¥â‰¤]_[4] _[T]_[as][desired.] Next, we define the complex solution vector _âƒ—xc_ = _A[âˆ’] c_[1] _[âƒ—b][c]_[that][satisfies] 

**==> picture [340 x 13] intentionally omitted <==**

We calculate the complex solution vector 

**==> picture [459 x 55] intentionally omitted <==**

(E161) 

where the first equality can be verified by direct calculation _A[âˆ’]_[1] _A_ = _I_ and we are using _|_ 0 _bâŸ© , |_ 1 _âŸ©b_ to label the basis vectors corresponding to the two blocks in the block matrix _A_ . Now we plug in the expressions for _Bc, P_ and obtain 

**==> picture [442 x 46] intentionally omitted <==**

Note that _P_ is introduced here to transform the bias vector _[âƒ—] bc_ into the nontrivial subspace of _Bc_ . Using the formula for geometric series, we have 

**==> picture [419 x 94] intentionally omitted <==**

where we have used _U_[3] _[T]_ = _I_ and the shorthand _Ut_ = _I_ for _t âˆˆ_ [ _T_ +1 _,_ 2 _T_ ] and _Ut_ = _U_ 3 _[â€ ] T_ +1 _âˆ’t_[for] _[ t][ âˆˆ]_[[2] _[T]_[ +1] _[,]_[ 3] _[T]_[].] Recall that we use _|_ 01 _âŸ© , |_ 11 _âŸ©_ to denote the basis vector of the first qubit in the _n_ -qubit circuit. Therefore, the solution vector satisfies 

**==> picture [457 x 166] intentionally omitted <==**

109 

This implies that 

**==> picture [379 x 157] intentionally omitted <==**

where we have used the fact that _Uk Â· Â· Â· U_ 1 _|_ 0 _[n] âŸ©_ = _UT Â· Â· Â· U_ 1 _|_ 0 _[n] âŸ©_ = _|ÏˆâŸ©_ for _k âˆˆ_ [ _T,_ 2 _T âˆ’_ 1]. On the other hand, the norm of _âƒ—x_ reads 

This gives us 

**==> picture [404 x 81] intentionally omitted <==**

Taking the realification via Theorem E.43 and noting that _âˆ¥Mâˆ¥_ = _âˆ¥Mcâˆ¥_ = 1 completes the proof of Theorem E.46. 

## _d. Connect to binary classification_ 

Then, we move on to the application of binary classification. We consider binary classification with leastsquares SVM. In a least-squares SVM, we consider a binary-label training dataset of _N_ samples ( _âƒ—xi, yi_ ) _[N] i_ =1[,] each specified by a _D_ -dimensional feature vector _âƒ—xi âˆˆ_ R _[D]_ and a label _yi âˆˆ{Â±_ 1 _}_ . We use a matrix _X_ = ( _âƒ—x_ 1 _, . . . , âƒ—xN_ ) _[T] âˆˆ_ R _[N][Ã—][D]_ and a vector _âƒ—y_ = ( _y_ 1 _, . . . , yN_ ) _[T] âˆˆ{Â±_ 1 _}[N]_ to represent the training set. The goal is to Ë† use the training set to classify a new test point _âƒ—x âˆˆ_ R _[D]_ via _y_ = sgn( _âƒ—x[T]_ ( _X[T] X_ + _Î»ID_ ) _[âˆ’]_[1] _X[T] âƒ—y_ ), where _Î» â‰¥_ 0 is the _â„“_ 2 regularization strength. 

We show below that any quantum circuit _UT Â· Â· Â· U_ 1 of size _T_ can be embedded into a training dataset ( _X, âƒ—y_ ) Ë† with feature length _D_ = _N_ and a sparse test vector _âƒ—x_ such that calculating _y_ = sgn( _âƒ—x[T]_ ( _X[T] X_ ) _[âˆ’]_[1] _X[T] âƒ—y_ ) with no regularization suffices to determine sgn( _âŸ¨Ïˆ| Z_ 1 _|ÏˆâŸ©_ ), where _|ÏˆâŸ©_ = _UT Â· Â· Â· U_ 1 _|_ 0 _âŸ©_ is the output state of the circuit. One can interpret this result as proving the BQP hardness of binary classification. This will be used to prove classical hardness of binary classification in Section F 2. 

**Lemma E.47** (Embed a quantum circuit into an SVM) **.** _Let n be a large integer and T, s be positive integers. Let T[â€²]_ = 2 _T_ + _n_ +1 _. Let UT Â· Â· Â· U_ 1 _be an n-qubit quantum circuit composed of T n-qubit unitaries Ui, i âˆˆ_ [ _T_ ] _that are all s-sparse. Let Ac âˆˆ_ C[12] _[T][ â€²]_[2] _[n][Ã—]_[12] _[T][ â€²]_[2] _[n]_ = C[2] _âŠ—_ C[2] _âŠ—_ C[3] _[T][ â€²] âŠ—_ C[2] _[n] be the complex matrix specified by the unitary sequence U_ 1 _[â€ ][Â· Â· Â·][ U] T[ â€ ][Z]_[1] _[U][T][Â· Â· Â·][ U]_[1] _[H][n][ Â· Â· Â·][ H]_[1] _[in][Theorem][E.46][,][where][Z]_[1] _[is][the][Pauli][Z][gate][on][the][first][qubit][of][the] circuit and Hi is the Hadamard gate on the i-th qubit. We use b, a to label the two binary registers corresponding to the two layers of blocks inside Ac as defined in Theorem E.46. Let_ 

**==> picture [378 x 25] intentionally omitted <==**

_where_ 

**==> picture [409 x 74] intentionally omitted <==**

110 

_Let_ 

**==> picture [414 x 14] intentionally omitted <==**

_be a complex_ 2 _-sparse test vector, where we use c to label the binary register corresponding to the two blocks of Xc. Let the realification_ 

**==> picture [407 x 13] intentionally omitted <==**

_define a real training dataset of size_ 48 _T[â€²]_ 2 _[n] and feature dimension_ 48 _T[â€²]_ 2 _[n] and a_ 4 _-sparse test vector. Then, X is real, symmetric, and O_ ( _s_ ) _-sparse with norm âˆ¥Xâˆ¥â‰¤_ 1 _and condition number Îº_ = _âˆ¥X[âˆ’]_[1] _âˆ¥âˆ¥Xâˆ¥â‰¤_ 4 _T[â€²] , and_ 

**==> picture [328 x 25] intentionally omitted <==**

_where_ 

**==> picture [296 x 22] intentionally omitted <==**

_and |ÏˆâŸ©_ = _UT Â· Â· Â· U_ 1 _|_ 0 _âŸ© is the n-qubit output state of the circuit and Z_ 1 _is the Pauli Z observable on the first qubit of the circuit. In particular, we have_ 

**==> picture [332 x 12] intentionally omitted <==**

_Proof of Theorem E.47._ We use _VT â€² Â· Â· Â· V_ 1 = _U_ 1 _[â€ ][Â· Â· Â·][ U] T[ â€ ][Z]_[1] _[U][T][Â· Â· Â·][ U]_[1] _[H][n][ Â· Â· Â·][ H]_[1][to][denote][the][embedded][unitary] sequence that has length _T[â€²]_ = 2 _T_ + _n_ + 1. From Theorem E.46, we know that _Ac_ is Hermitian, _O_ ( _s_ ) sparse, and has norm _âˆ¥Acâˆ¥â‰¤_ 1 and condition number at most 4 _T[â€²]_ = 4(2 _T_ + _n_ + 1). This implies that both _Xc, X_ are _O_ ( _s_ ) sparse with norm _â‰¤_ 1 and condition number _Îº â‰¤_ 4 _T[â€²]_ = 4(2 _T_ + _n_ + 1). We also have 

**==> picture [375 x 25] intentionally omitted <==**

Let _âƒ—x_ 0 = _|_ 1 _bâŸ©|_ 0 _aâŸ©|T[â€²]_ + 1 _âŸ©|_ 0 _[n] âŸ©âˆˆ_ C[12] _[T][ â€²]_[2] _[n]_ such that 

**==> picture [269 x 25] intentionally omitted <==**

Let 

**==> picture [367 x 21] intentionally omitted <==**

Then we have 

_âƒ—x[â€ ] c_[(] _[X] c[â€ ][X][c]_[)] _[âˆ’]_[1] _[X] c[â€ ][âƒ—y][c]_[=] ï¿½ _âƒ—x[â€ ]_ 0 _[âƒ—x][â€ ]_ 0ï¿½[ï¿½] _AA[âˆ’] c[âˆ’] c_[1][1] _[âƒ—y][âƒ—y]_[1][2] ï¿½ = _âƒ—x[â€ ]_ 0 _[A] c[âˆ’]_[1][(] _[âƒ—y]_[1][+] _[ âƒ—y]_[2][) = 2] _[âƒ—x]_[0] _[A][âˆ’] c_[1] _[âƒ—b][c]_[= 2] _[ âŸ¨]_[1] _[b][| âŸ¨]_[0] _[a][| âŸ¨][T][ â€²]_[ + 1] _[| âŸ¨]_[0] _[n][|][ A][âˆ’] c_[1] _[âƒ—b][c][.]_[(E178)] 

The calculations in the proof of Theorem E.46 shows that 

**==> picture [448 x 97] intentionally omitted <==**

Plugging this in, we have 

**==> picture [409 x 107] intentionally omitted <==**

111 

where _|ÏˆâŸ©_ = _UT Â· Â· Â· U_ 1 _|_ 0 _[n] âŸ©_ is the output state of the _n_ -qubit circuit. This implies that _âƒ—x[â€ ] c_[(] _[X] c[â€ ][X][c]_[)] _[âˆ’]_[1] _[X] c[â€ ][âƒ—y][c]_[is][real] and 

**==> picture [474 x 55] intentionally omitted <==**

and 

**==> picture [415 x 25] intentionally omitted <==**

Therefore, we have 

**==> picture [327 x 27] intentionally omitted <==**

where 

**==> picture [396 x 31] intentionally omitted <==**

Taking the realification via Theorem E.43 completes the proof of Theorem E.47. 

## _e. Connect to dimension reduction_ 

Finally, we consider the application of dimension reduction. We focus on the task of performing principal component analysis (PCA) on a data matrix _X âˆˆ_ R _[N][Ã—][D]_ , which reduces the data to one dimension. That means finding the eigenvector _âƒ—w âˆˆ_ R _[D]_ of _X[T] X âˆˆ_ R _[D][Ã—][D]_ with the largest eigenvalue _Î»_ max and projecting the test vector _âƒ—x âˆˆ_ R _[D]_ to that direction as _âƒ—x Â· âƒ—w_ . This reduces the test vector _âƒ—x_ to a scalar _âƒ—x Â· âƒ—w_ , its 1D representation. 

In the following, we show that any quantum circuit _UT Â· Â· Â· U_ 1 of size _T_ can be embedded into a data matrix _X_ with feature length _D_ = _N_ and a sparse test vector _âƒ—x_ such that calculating the 1D representation _âƒ—x Â· âƒ—w_ to 1 _/_ poly( _T,_ log( _N_ )) error suffices to determine the output of that circuit. We also show that there is a sparse guiding vector that have good overlap with the principal component. One can interpret this result as proving the BQP hardness of dimension reduction given a good guiding vector. This will be used to prove the classical hardness of dimension reduction in Section F 3. 

**Lemma E.48** (Embed a quantum circuit into PCA) **.** _Let n be a large integer and T, s be positive integers. Let UT Â· Â· Â· U_ 1 _be an n-qubit quantum circuit composed of T n-qubit unitaries Ui, i âˆˆ_ [ _T_ ] _that are all s-sparse. Let_ 

**==> picture [455 x 64] intentionally omitted <==**

_where R_ [ _Â·_ ] _is the realification defined in Theorem E.44. Let_ 

**==> picture [352 x 24] intentionally omitted <==**

_define a real dataset of size_ ( _T_ + 1)2 _[n]_[+1] _and feature dimension_ ( _T_ + 1)2 _[n]_[+1] _. Consider the_ 1 _-sparse guiding vector âƒ—g and test vector âƒ—x defined as_ 

**==> picture [373 x 15] intentionally omitted <==**

_Then, the data matrix X is real, symmetric, and O_ ( _s_ ) _-sparse with norm âˆ¥Xâˆ¥â‰¤_ 1 _and gap_ 

**==> picture [338 x 24] intentionally omitted <==**

112 

_where Î»_ max( _X[T] X_ ) _, Î»_ min( _X[T] X_ ) _are the largest and second largest eigenvalues of X[T] X. Moreover, the guiding vector have overlap_ 

**==> picture [337 x 25] intentionally omitted <==**

_with the principal component âƒ—w of X, and the test vector âƒ—x has 1D representation_ 

**==> picture [339 x 24] intentionally omitted <==**

We note that if we do not require the guiding vector _âƒ—g_ to be sparse, we can pad the circuit with Î˜( _T_ ) identity gates in the beginning and choose _âƒ—g_ to be an equal superposition of all the clock time with identity gates tensor product with ï¿½ï¿½0 _n_ +1ï¿½. This will give a guiding vector with constant overlap _âƒ—g Â· âƒ—w_ = Î˜(1) but sparsity _O_ ( _T_ ). 

_Proof of Theorem E.48._ Since each _Ut_ is _O_ ( _s_ )-sparse, it is immediate by construction that _X_ is real, symmetric,and _O_ ( _s_ ) sparse. In addition, since the _Ut_ â€™s are unitary, we have that _âˆ¥H_ circ _âˆ¥â‰¤_ 1 + _T Â· O_ (1) = _O_ ( _T_ ) by triangle inequality. It is also straightforward to show that _H_ circ _â‰¥_ 0. Therefore, we have 0 _â‰¤ X â‰¤ I_ ( _T_ +1)2 _n_ +1. We prove the remaining properties by analyzing the spectrum of _H_ circ following [164, Section 14.4]. Consider the basis rotation unitary 

**==> picture [305 x 30] intentionally omitted <==**

We have that 

**==> picture [420 x 80] intentionally omitted <==**

Define 

**==> picture [444 x 80] intentionally omitted <==**

Elementary calculations show that _E_ 1 has minimal eigenvalue â„¦(1 _/T_[2] ) and _E_ 0 has minimal eigenvalue 0 with non-degenerate eigenvector 

**==> picture [295 x 23] intentionally omitted <==**

and second minimal eigenvalue â„¦(1 _/T_[2] ). Since _W[T] H_ circ _W_ is equal to _E_ 0 when the qubit register is ï¿½ï¿½0 _n_ +1ï¿½ and equal to _E_ 1 _âŠ— I_ 2 _n_ +1 when the qubit register is orthogonal to ï¿½ï¿½0 _n_ +1ï¿½, we know that _W[T] H_ circ _W_ has minimal eigenvalue 0 and second minimal eigenvalue â„¦(1 _/T_[2] ), and so does _H_ circ. The non-degenerate eigenvector with minimal eigenvalue 0 of _H_ circ is therefore 

**==> picture [364 x 30] intentionally omitted <==**

Since _X_ = _I_ ( _T_ +1)2 _n_ +1 _âˆ’ H_ circ _/âˆ¥H_ circ _âˆ¥_ , the vector _âƒ—w_ is indeed the principal component of _X_ , with eigenvalue _Î»_ max( _X_ ) = 1 _âˆ’_ 0 = 1. The gap of _X_ is 

**==> picture [441 x 25] intentionally omitted <==**

113 

because _âˆ¥H_ circ _âˆ¥â‰¤ O_ ( _T_ ). Moreover, the guiding vector _âƒ—g_ = _|_ 0 _âŸ©_ ï¿½ï¿½0 _n_ +1ï¿½ has overlap 

**==> picture [330 x 23] intentionally omitted <==**

The 1D representation of the test vector _âƒ—x_ = _|T âŸ©_ ï¿½ï¿½0 _n_ +1ï¿½ is 

**==> picture [404 x 24] intentionally omitted <==**

as desired. This completes the proof of Theorem E.48. 

**==> picture [469 x 221] intentionally omitted <==**

**----- Start of picture text -----**<br>
114<br>j<br>current<br>I 2 voltage i Aij<br>V 3 N A Ï‰x = Ï‰b<br>k bk<br>V 4<br>impedance current voltage<br>I 1 Quantum  Data: z = ( i, j, Aij, k, bk )<br>Advantage Task: estimate heat dissipation Ï‰x [T] MÏ‰x<br>impedance Z 4 machine size superpoly( N ) ?<br>Z 1 Ëœ O ( N [0] [.] [99] )<br>O ( N )<br>Linear system: power grid analysis poly(log  N ) time<br>**----- End of picture text -----**<br>


FIG. 8: **Overview of the linear system task.** We illustrate the linear system task with a particular real-world application scenario in power grid analysis. In power grid analysis, samples are obtained by performing measurements on a power grid to read off the impedance values and the voltage values of random locations that are changing dynamically. We may want to estimate the heat dissipation of some critical junctions, given by a quadratic form of the current. This reduces to solving a high-dimensional linear system _Aâƒ—x_ = _[âƒ—] b_ . Our results show that a small quantum machine with size poly(log _N_ ) can solve this task with _O_[Ëœ] ( _N_ ) samples, whereas any classical machine with exponentially larger size _O_ ( _N_[0] _[.]_[99] ) cannot solve the task unless it uses a sample size at least super-polynomial in _N_ . 

## **Appendix F: Applications** 

In this section, we apply quantum oracle sketching to various applications, including solving linear systems (Section F 1 and Figure 8), binary classification (Section F 2 and Figure 9), and dimension reduction (Section F 3). We show that we can solve these useful classical data processing tasks in an end-to-end fashion with a small quantum computer. Then, we use techniques developed in Section E to rigorously prove the classical hardness of solving these tasks. In particular, we prove that, using the same number of samples, any classical machine needs exponentially larger size to solve these tasks. Moreover, in a dynamic setting, if the classical machine does not have enough size, it would need super-polynomially more samples. Throughout this section, we use _|xâŸ©_ =[ï¿½] _j[x][j][ |][j][âŸ©][/][âˆ¥][âƒ—x][âˆ¥]_[2][to denote the real quantum state corresponding to any vector] _[ âƒ—x]_[ = (] _[x]_[1] _[, . . . , x][N]_[)] _[T][âˆˆ]_[R] _[N]_[.] 

## **1. Linear system** 

We begin with the fundamental primitive of solving linear systems, summarized in Figure 8. The solution of large linear systems serves as the computational bottleneck in a vast array of scientific and engineering disciplines. It is a key subroutine in many problems including regression, optimization, and solving differential equations that governs chemicals, materials, biological systems, fluid, and mechanical systems, etc. As we increase the dataset size, sampling rate, or precision, the dimension _N_ of these systems grows rapidly. Consequently, storing the data for processing becomes a bottleneck. In this section, we show that a small quantum machine can solve linear systems better than exponentially larger classical machines. 

Formally, we consider _N_ -dimensional linear systems of the form 

**==> picture [319 x 14] intentionally omitted <==**

where _A_ is a symmetric, sparse and well-conditioned matrix with operator norm _âˆ¥Aâˆ¥â‰¤_ 1 after appropriate rescaling. The assumption that _A_ is symmetric incurs no loss of generality; any general linear system can 0 _A_ always be embedded into a symmetric formulation _A_ sym _âƒ—x_ sym = _[âƒ—] b_ sym, where _A_ sym = _A[T]_ 0 _âˆˆ_ R[2] _[N][Ã—]_[2] _[N]_ and ï¿½ ï¿½ _âƒ— âƒ—b_ sym = ( _âƒ—b,âƒ—_ 0) _[T] âˆˆ_ R[2] _[N]_ with the solution _âƒ—x_ sym = (0 _, âƒ—x_ ) _[T]_ . This embedding preserves the sparsity and condition number. We characterize the tractability of the linear system with two parameters: the sparsity _s_ (the maximal number of nonzero elements per row or column) and condition number _Îº_ = _âˆ¥A[âˆ’]_[1] _âˆ¥âˆ¥Aâˆ¥_ . We focus on the regime where 

115 

the dimension _N_ is very large, and yet it remains sparse and well-conditioned: 

**==> picture [283 x 11] intentionally omitted <==**

**==> picture [101 x 9] intentionally omitted <==**

Now we formally define our data processing task of solving linear systems, summarized in Theorems F.1 and F.2. In particular, we specify the data generation process and the goal of the task. We consider a data generation process where we randomly get a non-zero matrix element of coefficient matrix _A_ and a random component of the bias vector _[âƒ—] b_ = ( _b_ 1 _, . . . , bN_ ) _[T]_ . 

Recall that in Section D 5, we define the matrix data generation process of the matrix _A_ as a hierarchical data generation process that generates random non-zero matrix elements as data 

**==> picture [374 x 15] intentionally omitted <==**

We assume that the linear system is properly normalized such that _âˆ¥Aâˆ¥â‰¤_ 1. The vector data generation process of _[âƒ—] b_ is a hierarchical data generation process that generates random components of the vector as data 

**==> picture [331 x 14] intentionally omitted <==**

The matrix elements _Aij_ and vector components _bk_ are specified by bitstrings of length _b_ = poly(log _N_ ) to sufficient accuracy. For simplicity, we assume that these binary representations are exact and use _Aij, bk_ to stand for the corresponding values. 

In the task of solving linear systems, we consider any hierarchical data generation process _D_ LS( _A,[âƒ—] b_ ) with bounded repetition number _R_ that generates data samples of the form 

**==> picture [280 x 13] intentionally omitted <==**

## where 

**==> picture [476 x 15] intentionally omitted <==**

gives us random non-zero matrix elements of the coefficient matrix _A_ and random components of the bias vector _âƒ—b_ . Recall that the repetition number _R_ characterizes the correlation in the data, and is defined as 

**==> picture [316 x 14] intentionally omitted <==**

where _Nz_ =[ï¿½] _[Ï„] i_ =1 _[Î´][z] i[,z]_[is][the][number][of][repeating] _[z]_[â€™s][in][a][refreshing][block][of][data][and] _[Ï„]_[is][refreshing][time][that] bounds the correlation time scale. The specific way of sampling these data can be arbitrary as long as it satisfies the above form. Our discussion generalizes straightforwardly to the alternative scenario where each time we can choose to get either _z_[coeff] or _z_[bias] . 

Next, we specify the goal of solving a high-dimensional linear system. The standard task of calculating the whole solution vector _âƒ—x_ = _A[âˆ’]_[1] _[âƒ—] b_ is undesirable when the dimension is very large, since writing down the solution vector already takes _O_ ( _N_ ) memory. Instead, in many cases, our goal is to estimate some property of the solution vector. In particular, we consider the prototypical task of estimating the normalized quadratic form value 

**==> picture [270 x 25] intentionally omitted <==**

to _Ïµ_ additive error for some symmetric matrix _M âˆˆ_ R _[N][Ã—][N]_ with known norm _âˆ¥Mâˆ¥_ . We assume that _M_ can be efficiently measured on a quantum machine. That means the space and time complexity of measuring _M_ are both poly(log _N_ ). This assumption can be relaxed if we allow the quantum machine to run longer. This motivates our definition of the linear system task as follows. 

116 

**Task F.1** (Linear system task) **.** _Let N, R be integers and Ïµ âˆˆ_ (0 _,_ 1] _. Consider any symmetric matrix M âˆˆ_ R _[N][Ã—][N] that specifies a quadratic form of our interest and can be efficiently measured. The linear system task is to estimate the normalized quadratic form value_ 

**==> picture [254 x 25] intentionally omitted <==**

_to Ïµ additive error using data samples from any data generation process D_ LS( _A,[âƒ—] b_ ) _defined above with repetition number at most R that corresponds to a linear system Aâƒ—x_ = _[âƒ—] b, A âˆˆ_ R _[N][Ã—][N] ,[âƒ—] b âˆˆ_ R _[N] , where the coefficient matrix A has_ poly(log _N_ ) _sparsity and_ poly(log _N_ ) _condition number._ 

Our quantum algorithm is flexible enough to handle correlated data with time-varying features. This allows us to further consider a dynamic scenario, where the linear system changes over time, but the property we want to estimate remains approximately fixed. This resembles the batch processing strategy common in modern large-scale data analysis, where we keep processing batches of data that share a common underlying property that we want to learn. We use _Î¸ âˆˆ_ R to denote that underlying property value. In particular, we consider any hierarchical data generation process _D_ DLS( _Î¸, Ïµ_ ) with bounded repetition number _R_ and refreshing time _Ï„_ of the form 

**==> picture [330 x 14] intentionally omitted <==**

In other words, the linear system _Aâƒ—x_ = _[âƒ—] b_ changes every _Ï„_ time steps and we keep getting random non-zero matrix elements of _A_ and random components of _[âƒ—] b_ of the current linear system as the data. We require all linear systems sampled from _DÎ¸,Ïµ_[0][to][have][poly(log] _[ N]_[)][sparsity,][poly(log] _[ N]_[)][condition][number,][and][the][desired] property: 

**==> picture [321 x 26] intentionally omitted <==**

The specific way that _DÎ¸_[0][samples the linear system can be arbitrary as long as it satisfies the above requirements.] Formally, we define the dynamic linear system task as follows. 

**Task F.2** (Dynamic linear system task) **.** _Let N, R, Ï„ be integers and Ïµ âˆˆ_ (0 _,_ 1] _. Consider any symmetric matrix M âˆˆ_ R _[N][Ã—][N] that specifies a quadratic form of our interest and can be efficiently measured. The dynamic linear system task is to estimate the underlying normalized quadratic form value Î¸ to_ 2 _Ïµ additive error using data samples from any D_ DLS( _Î¸, Ïµ_ ) _defined above with repetition number at most R and refreshing time Ï„ ._ 

In the following, we first state our main results on quantum advantage in solving linear systems. Then we prove the quantum easiness and classical hardness in subsequent sections. 

_b. Main results_ 

Our first result shows that given the same amount of samples, a small quantum machine can solve the linear system task better than an exponentially larger classical machine. Note that the scaling _N_[1] _[âˆ’][Î¶]_ is effectively _N_ since it holds for any constant _Î¶ >_ 0. 

**Theorem F.3** (Quantum advantage in solving linear systems) **.** _Consider the linear system task with dimension N and repetition number R defined in Theorem F.1. Using O_[Ëœ] ( _RN_ ) _samples, a quantum machine with_ poly(log _N_ ) _size can solve it with_ 1 _/_ poly(log _N_ ) _error and high success probability, while any classical machine with o_ ( _N_[1] _[âˆ’][Î¶]_ ) _size for any constant Î¶ >_ 0 _cannot solve it with constant error and success probability more than_ 1 _/_ 2 + 1 _/N[Ï‰]_[(1)] _. Moreover, the data processing time per sample of the quantum machine is_ poly(log _N_ ) _._ 

The second result shows that if the size of the classical machine is slightly smaller than _o_ ( _N_ ), it would need super-polynomially more samples than a small quantum machine to solve the dynamic linear system task. In the context of batch processing, this means that quantum machines can solve the task with a few batches of data, whereas sub-exponential size classical machines require super-polynomially many batches. 

117 

**Theorem F.4** (Quantum advantage in solving dynamic linear systems) **.** _Consider the dynamic linear system task with dimension N , repetition number R, and sufficient refreshing time Ï„_ = _O_[Ëœ] ( _RN_ ) _defined in Theorem F.2. A quantum machine with_ poly(log _N_ ) _size can use O_[Ëœ] ( _RN_ ) _samples to solve it with_ 1 _/_ poly(log _N_ ) _error and high success probability, while any classical machine with o_ ( _N_[1] _[âˆ’][Î¶]_ ) _size for any constant Î¶ >_ 0 _that solves it with constant error and probability at least_ 2 _/_ 3 _must collect at least RN[Ï‰]_[(1)] _samples. Moreover, the data processing time per sample of the quantum machine is_ poly(log _N_ ) _._ 

Together, Theorems F.3 and F.4 establish unconditional and exponential quantum advantages in the foundational task of solving linear systems that appears in almost every aspect of science and engineering. 

## _c. Quantum algorithm_ 

Here, we prove the quantum algorithm parts of Theorems F.3 and F.4. We construct an algorithm that solves a high-dimensional linear system on a small quantum computer. We do so by combining quantum oracle sketching (Theorem D.16), quantum state sketching (Theorem D.24), and standard quantum linear system solvers. We use the Heisenberg-scaling quantum amplitude estimation to measure _M_ , which gives us the optimal 1 _/Ïµ_[2] sample complexity after the quadratic slowdown. One may also use standard quantum limit measurements that will lead to a 1 _/Ïµ_[4] dependence on the error _Ïµ_ . 

**Theorem F.5** (Solving linear systems with quantum oracle sketching) **.** _Let Ïµ, Î´ âˆˆ_ (0 _,_ 1) _. Let N be a large integer and Aâƒ—x_ = _[âƒ—] b be an N -dimensional linear system. Here, A âˆˆ_ R _[N][Ã—][N] is an s-sparse matrix with norm âˆ¥Aâˆ¥â‰¤_ 1 _and condition number at most Îº. âƒ—x,[âƒ—] b âˆˆ_ R _[N] are N -dimensional vectors. Consider any symmetric matrix M âˆˆ_ R _[N][Ã—][N] that specifies a quadratic form of our interest and can be efficiently measured using SM qubits. Then, there exists a quantum algorithm that produces an estimate Î¸_[Ë†] _âˆˆ_ [ _âˆ’_ 1 _,_ 1] _satisfying_ 

**==> picture [323 x 143] intentionally omitted <==**

_with probability at least_ 1 _âˆ’ Î´, using_ 

_qubits and_ 

_samples from the data generation process D_ LS( _A,[âƒ—] b_ ) _with repetition number R. In particular, we have_ 

**==> picture [299 x 13] intentionally omitted <==**

**==> picture [407 x 12] intentionally omitted <==**

We note that Theorem F.5 immediately implies the quantum algorithm part of Theorem F.3 by definition of the linear system task. It also proves the quantum algorithm part of Theorem F.4 by taking _Ï„_ = _O_[Ëœ] ( _RN_ ) larger than _M_ = _O_[Ëœ] ( _RN_ ) and noting that 

**==> picture [270 x 25] intentionally omitted <==**

with probability at least 1 _âˆ’ Î´_ , as required. 

We use the following quantum linear system solver as the backbone of our quantum algorithm and instantiate the oracle queries with quantum oracle sketching. We refer interested readers to a recent survey [181] for an overview on alternative quantum linear system solvers. 

118 

**Lemma F.6** (Quantum linear system solver [82]) **.** _Let n be an integer and N_ = 2 _[n] . Let Aâƒ—x_ = _[âƒ—] b be a linear system, where A âˆˆ_ C _[N][Ã—][N] , âƒ—x,[âƒ—] b âˆˆ_ C _[N] with âˆ¥Aâˆ¥â‰¤_ 1 _and condition number at most Îº. There exists a quantum algorithm that produces a state Ï satisfying_ 

**==> picture [324 x 25] intentionally omitted <==**

_using O_ ( _n_ ) _qubits, O_ ( _Îº_ log(1 _/Ïµ_ )) _gates, and O_ ( _Îº_ log(1 _/Ïµ_ )) _queries to the block encoding of A and the state preparation unitary of |bâŸ© and their inverse and controlled versions._ 

Recall that in Theorem D.23, we have shown that _O_[Ëœ] ( _RNs_[5] ) samples suffice to implement the block encoding of an _s_ -sparse matrix _A_ . In addition, Theorem D.24 shows that we can use _O_[Ëœ] ( _RN_ ) samples to prepare the quantum state _|bâŸ©_ =[ï¿½] _[N] j_ =1 _[b][j][ |][j][âŸ©][/][âˆ¥][âƒ—b][âˆ¥]_[of][the][vector] _[ âƒ—b]_[=][(] _[b]_[1] _[, . . . , b][N]_[)] _[T]_[ .][Together,][these][primitives][allow][us][to] implement all the necessary subroutines that we need in quantum linear system solvers. In particular, we combine Theorem F.6 with Theorem D.23 and Theorem D.24 to prove Theorem F.5. 

_Proof of Theorem F.5._ Let _n_ = _âŒˆ_ log2( _N_ ) _âŒ‰_ and embed _A,[âƒ—] b_ into 2 _[n] âˆˆ_ [ _N,_ 2 _N_ ] dimension to apply quantum oracle and state sketching. Theorem F.6 states that there is a quantum linear system solver that produces a state _Ï_ satisfying 

**==> picture [285 x 11] intentionally omitted <==**

using _O_ ( _n_ ) qubits and 

**==> picture [285 x 11] intentionally omitted <==**

queries to the block encoding of _A_ and the state preparation unitary of _|bâŸ©_ and their inverse and controlled versions. 

Our proof proceeds in two steps. We first use this quantum linear system solver to construct a query algorithm that estimates the quadratic form value to _Ïµ_ error with probability at least 1 _âˆ’ Î´/_ 2. Then, we instantiate the queries with quantum oracle and state sketching. The instantiation error is chosen to be _Î´/_ 2 such that the total variation distance error on the final estimate is _Î´/_ 2. This immediately implies that the final estimate is accurate up to _Ïµ_ error with probability at least 1 _âˆ’ Î´/_ 2 _âˆ’ Î´/_ 2 = 1 _âˆ’ Î´_ . 

As the first step, we construct the query algorithm that estimates the quadratic form value. The quantum linear system solver produces a state _Ï_ that is _Ïµ/_ 2 close to _|xâŸ©_ using _O_ ( _n_ ) qubits and _Q_ 0 = _O_ ( _Îº_ log(1 _/Ïµ_ )) queries to _A_ and _|bâŸ©_ . Note that we can also execute the inverse of the quantum linear system solver with the same query complexity. This allows us to use standard quantum amplitude estimation [127, 182] to measure _M/âˆ¥Mâˆ¥_ on _Ï_ and get a classical estimate _Î¸_[Ë†] 0 satisfying 

**==> picture [300 x 19] intentionally omitted <==**

with probability at least 1 _âˆ’ Î´/_ 2 using _O_ (log(1 _/Î´_ ) _/Ïµ_ ) queries to the quantum linear system solver and its inverse, along with additional _SM_ qubits and _O_ ( _TM_ log(1 _/Î´_ ) _/Ïµ_[2] ) time, where _TM_ = poly(log _N_ ) is the time complexity of measuring _M_ . The resulting estimation error of the quadratic form value is 

**==> picture [419 x 90] intentionally omitted <==**

The total number of queries to _A_ and _|bâŸ©_ amounts to 

**==> picture [350 x 11] intentionally omitted <==**

We view this whole quantum algorithm as a query algorithm that produces a classical random variable _Î¸_[Ë†] 0 which is _Ïµ_ close to the quadratic form value with probability at least 1 _âˆ’ Î´/_ 2. 

The second step is to instantiate the queries to _A_ and _|bâŸ©_ in the query algorithm using quantum oracle and state sketching. We first replace all queries to the block encoding of _A_ and its inverse and controlled versions 

119 

to their _Ïµ_ 1-approximate versions in Theorem D.23. This incurs an error of _E_ 1 = _QÏµ_ 1 = _Î´/_ 6, where we set _Ïµ_ 1 = _Î´/_ (6 _Q_ ) = Î˜( _ÏµÎ´/_ ( _Îº_ log(1 _/Ïµ_ ) log(1 _/Î´_ ))). 

Next, we replace the queries to _Ïµ_ 1-approximate versions of block encoding of _A_ and its inverse and controlled versions by the random unitary channel that we build from samples in Theorem D.23. This incurs an additional error of _E_ 2 = _QÏµ_ 1 = _Î´/_ 6, and uses _O_ ( _n_ + _b_ + log[2] _[.]_[5] (1 _/Ïµ_ 1)) = _O_ ( _n_ + _b_ + log[2] _[.]_[5] ( _ÏµÎ´[Îº]_[))][qubits][and] 

**==> picture [388 x 31] intentionally omitted <==**

samples from the data generation process. Note that here we only use the coefficient data and throw away the bias data in each sample. 

Finally, we replace the queries to the state preparation unitary of _|bâŸ©_ and its inverse by the _Ïµ_ 1-error random unitary that we build from samples according to Theorem D.24. This incurs an additional error of _E_ 3 = _QÏµ_ 1 = _Î´/_ 6, and uses _O_ ( _n_ log( _N/Ïµ_ 1)) _â‰¤ O_ ( _n_[2] logï¿½ _ÏµÎ´Îº_ ï¿½) qubits and 

**==> picture [372 x 31] intentionally omitted <==**

samples from the data generation process. Here we only use the bias data and throw away the coefficient data in each sample. 

According to Theorem D.17, the total error in instantiating the query algorithm is bounded by 

**==> picture [308 x 11] intentionally omitted <==**

This _Î¸_ Ë†, has a distribution that ismeans that the output _Î´/_ of2 close tothe query-instantiated _Î¸_ Ë†0 in total variation distance.quantum algorithm,In particular, this implies that the successwhich is a classical random variable probability 

**==> picture [452 x 25] intentionally omitted <==**

as desired. The total number of qubits used is 

**==> picture [451 x 19] intentionally omitted <==**

The total number of samples is 

**==> picture [344 x 31] intentionally omitted <==**

This completes the proof of Theorem F.5. 

## _d. Classical hardness_ 

In this section, we prove the two classical hardness results in Theorems F.3 and F.4. We prove them by constructing a specific linear system using Theorem E.46. Solving it amounts to solving the (dynamic) Noisy Oracle Property Estimation (NOPE) task defined in Section E (Theorems E.1 and E.26), whose classical hardness we have already proved in Theorems E.27 and E.28. 

This gives us two classical hardness results. The first result follows from Theorem E.27 and shows that any classical learning algorithm that wants to perform better than random guessing in solving a linear system with the same number of samples quantum algorithms need must have â„¦( _N_[1] _[âˆ’][Î¶]_ ) size for any constant _Î¶ >_ 0. The second result follows from Theorem E.28 and shows that when the linear system is dynamic, any classical learning algorithm will need a number of samples super-polynomial in _N_ if it has size _o_ ( _N_[1] _[âˆ’][Î¶]_ ) for any constant _Î¶ >_ 0. 

The general idea of proving these results is to embed the quantum circuit that solves dynamic NOPE from _âƒ—x[T] Mâƒ—x_ Theorem E.45 into a linear system via Theorem E.46. The normalized quadratic form value _âˆ¥âƒ—xâˆ¥âˆ¥Mâˆ¥âˆ¥âƒ—xâˆ¥_[encodes] the oracle property _B âˆˆ{_ 0 _,_ 1 _}_ that we want to estimate in (dynamic) NOPE. Then we show that given any classical algorithm that solves the linear system task of this specific linear system, we can use it to construct a classical algorithm that solves (dynamic) NOPE. In the (dynamic) NOPE task, we take the oracle property 

120 

function _f_ to be _K_ -Forrelation (Theorem E.38) and the noisy encoding function _g_ to be the inner product (Theorem E.41). 

In the following, we construct the data generation process _D_ LS _[N,K,R]_ ( _B_ ) _, B âˆˆ{_ 0 _,_ 1 _}_ for linear systems, where _N_ is the dimension of the linear system, _K_ = Î˜(1) is the constant in the Forrelation that we will embed, _R_ is an integer that specifies the repetition number, and _B_ indicates whether the quadratic form of the solution vector has a large or small value (see Equation (E158)). The goal is to solve for _B_ . It helps to compare this construction to the dynamic NOPE data generation process defined in Section E 4. 

Given _N_ , we define another large integer _N[â€²]_ as follows. Let _T_ = Î˜(log[3] _N[â€²]_ log log _N[â€²]_ ) be the total number of two-qubit gates and diagonal gates in the quantum circuit from Theorem E.45. Let _n[â€²]_ = log _N[â€²]_ + _O_ (log log _N[â€²]_ ) be the number of qubits in that circuit from Theorem E.45. To properly embed that circuit into the _N_ - dimensional linear system, we define _N[â€²]_ such that _N_ = 24 _T_ 2 _[n][â€²]_ = _N[â€²] Â·_ polylog _N[â€²]_ as in Theorem E.46. This implies _N[â€²]_ = _N/_ polylog _N_ . The resulting linear systems have sparsity _s_ = _O_ (1) and condition number _Îº_ = _O_ ( _T_ ) = _O_ (log[3] _N_ log log _N_ ) from Theorem E.46. Let _L_ = ï¿½log[2] ( _KN[â€²]_ )ï¿½ _â‰¥_ 5 be the number of independent oracle instances that we have in dynamic NOPE. 

We define the data generation process as 

**==> picture [401 x 15] intentionally omitted <==**

where _T_ 3 = _R_ , _T_ 2 = _KN[â€²]_ , _T_ 1 = _âŒˆMQ/_ ( _T_ 2 _T_ 3) _âŒ‰_ = polylog( _KN[â€²]_ ), _MQ_ = _RN_ polylog( _N_ ) is the number of samples quantum machines need in Theorem F.5, _A âˆˆ_ R _[N][Ã—][N]_ is an _N_ -dimensional, symmetric, _O_ (1)-sparse matrix with condition number _Îº_ = _O_ ( _T_ ) = _O_ (log[3] _N_ log log _N_ ), _Î± âˆˆ{_ 0 _,_ 1 _}, Î² âˆˆ_ [ _L_ ] label which part of the matrix _A_ that we are currently collecting matrix element data from, _i, j âˆˆ_ [ _N_ ] labels the row/column of the matrix elements _Aij_ , and _l âˆˆ_ [ _N_ ] _, bl_ is a random component of a fixed bias vector _[âƒ—] b_ . 

The data are sampled in the following way that resembles dynamic NOPE in Section E 4. _DB_[0][samples][a] length- _L_ bitstring _Î³_ with parity 

**==> picture [267 x 31] intentionally omitted <==**

uniformly random. For each _j âˆˆ_ [ _L_ ], we sample a random oracle _oj âˆ¼ pÎ³j_ , where _p_ 0 _, p_ 1 are the distributions of Forrelation defined in Theorem E.39. Then we sample a noisy encoding pair ( _Y_[(0] _[,j]_[)] _, Y_[(1] _[,j]_[)] ) _âˆ¼_ Uniform(( _g[N]_ ) _[âˆ’]_[1] ( _oj_ )) using the inner product noisy encoding function _g_ defined in Theorem E.41. Next, note that ( _Y_[(0] _[,j]_[)] _, Y_[(1] _[,j]_[)] ) _[L] j_ =1[specifies][an] _[n][â€²]_[-qubit][quantum][circuit] _[C]_[with] _[T]_[=] _[O]_[(log][3] _[ N][ â€²]_[ log log] _[ N][ â€²]_[)] gates via Theorem E.45, and the quantum circuit _C_ gives a linear system _Aâƒ—x_ = _[âƒ—] b_ with dimension 24 _T_ 2 _[n][â€²]_ = _N_ via Theorem E.46. Here, _A_ is indeed symmetric and _O_ (1)-sparse with condition number _Îº_ = _O_ ( _T_ ) = _O_ (log[3] _N_ log log _N_ ). Now we define _DA_[1][.][We][first][sample][a][uniformly][random][coordinate] _[Î²][âˆ¼]_[Uniform([] _[L]_[])][and] a random bit _Î± âˆ¼_ Bern(1 _/_ 2) as in dynamic NOPE. Then we pick out _Y_[(] _[Î±,Î²]_[)] and use it to generate the data samples. 

In particular, we define _D_ ([2] _Î±,Î²_ )[in][the][following][way.] We first sample a random row of the matrix _A_ as follows. We note that after uniformly sampling the realification blocks given in Theorem E.43, the linear space corresponding to the matrix _A_ has a particular factorization given by Theorem E.46. We sample the blocks of _A_ in Equation (E155) and the blocks of _Bc_ in Equation (E154) uniformly randomly. Then we are left with the subspace _|tâŸ©|ÏˆâŸ©_ where _|tâŸ©_ is the clock register and _|ÏˆâŸ©_ is the _n[â€²]_ -qubit register that the quantum circuit runs on. We sample a clock time _t âˆ¼_ Uniform([ _T_ ]) and the matrix is reduced to a specific gate in the _n[â€²]_ -qubit subspace (either a fixed two qubit gate or a diagonal gate that depends on _Y_[(] _[Î±,Î²]_[)] ). The remaining subspace further factorizes into _|x, Î±, Î², kâŸ©_ and the rest of the working qubits. We sample a random basis of this _n[â€²]_ -qubit subspace by plug in the specific ( _Î±, Î²_ ) that we have already sampled, sample _x âˆ¼_ Uniform([ _KN[â€²]_ ]) _, k âˆ¼_ Uniform([ _b_ ]), and sample a computational basis of the rest of the working qubits uniformly random. This together specifies and thus samples a row _i_ of the matrix _A_ . Note that the marginal distribution of _i_ is uniform over [ _N_ ] (because _Î±, Î²_ are sampled uniformly), though there are correlations between consecutive samples of _i_ since they share the same set of ( _Î±, Î²_ ). 

Now we uniformly randomly select a non-zero column _j_ that corresponds to the row _i_ and picks out the matrix element _Aij_ . Note that by construction of the matrix _A_ as in Theorem E.46, the picked out matrix element is the real or imaginary part of either 1, from the identity matrices in Equations (E154) and (E155), or a matrix element of a fixed two qubit gates, or 1 _âˆ’_ ( _âˆ’_ 1)[(] _[Y] x_[(] _[Î±,Î²]_[)] ) _k eâˆ’_ 1 _/T_ (see Equation (E154)) which is solely specified by _Y_[(] _[Î±,Î²]_[)] . This gives us the sample ( _i, j, Aij_ ). We randomly sample a bias vector component ( _l âˆ¼_ Uniform([ _N_ ]) _, bl_ ) and obtain the full data sample _z_ = ( _i, j, Aij, l, bl_ ). We repeat this sample _T_ 3 times, completing the data generation process. 

121 

This data generation process _D_ LS _[N,K,R]_ is a valid data generation process of dynamic linear systems. It produces matrix element data uniformly distributed over the non-zero elements of the matrix _A_ . The underlying value is given by Theorem E.46 as 

**==> picture [290 x 24] intentionally omitted <==**

where _qB_ is the probability of measuring 0 on the embedded circuit given by Theorem E.45 when the underlying oracle property is _B_ . Theorem E.45 ensures that _q_ 1 _â‰¤_ 0 _._ 1 _, q_ 0 _â‰¥_ 0 _._ 9. The repetition number of the data generation process is upper bounded by _T_ 2 _T_ 3 _/_ ( _KN[â€²]_ ) = _R_ , because the sampling step of _DA_[1] _[â†’][Ã—][T]_[1] _[D]_ ([2] _Î±,Î²_ )[is][independent.] The refreshing time is _Ï„_ = _T_ 1 _T_ 2 _T_ 3 = _O_ ( _MQ_ ) = _O_[Ëœ] ( _RN_ ), satisfying the requirements in Theorems F.3 and F.4. This data generation process for linear systems _D_ LS _[N,K,R]_ ( _B_ ) is designed to reduce to the dynamic NOPE data _Dg,f[KN][â€²][,T]_[1] ( _B_ ) in Section E 4 via Theorems E.45 and E.46. Using this data generation process, we prove the following two results. 

**Theorem F.7** (Classical hardness of solving linear systems) **.** _Let Î¶ >_ 0 _be any constant. Let N be the dimension of a linear system task and R be its repetition number. Using O_[Ëœ] ( _RN_ ) _samples, any randomized classical learning algorithm with space complexity_ 

**==> picture [255 x 12] intentionally omitted <==**

_cannot solve the linear system task with Ïµ_ = 0 _._ 03 _error and success probability more than_ 1 _/_ 2 + 1 _/N[Ï‰]_[(1)] _._ 

**Theorem F.8** (Classical hardness of solving dynamic linear systems) **.** _Let Î¶ >_ 0 _be any constant. Let N be the dimension of a dynamic linear system task and R, Ï„_ = _O_[Ëœ] ( _RN_ ) _be its repetition number and refreshing time. Any randomized classical learning algorithm that solves the task with Ïµ_ = 0 _._ 03 _error and success probability at least_ 2 _/_ 3 _must have sample complexity_ 

**==> picture [255 x 13] intentionally omitted <==**

**==> picture [96 x 10] intentionally omitted <==**

**==> picture [256 x 13] intentionally omitted <==**

Theorem F.7 immediately implies the classical hardness part of Theorem F.3 because the first _O_[Ëœ] ( _RN_ ) samples from the constructed dynamic linear system data belongs to the same linear system and therefore is a valid sequence of non-dynamic linear system data. Theorem F.8 directly implies the classical hardness part of Theorem F.4. Together with Theorem F.5, this completes the proof of the quantum advantage claims in Theorems F.3 and F.4. 

_Proof of Theorems F.7 and F.8._ We prove Theorems F.7 and F.8 by showing that given any classical learning algorithm that can estimate the normalized quadratic form value to _Ïµ_ = 0 _._ 03 error in the constructed linear system task, we can use it to construct an algorithm that decides the oracle property _B âˆˆ{_ 0 _,_ 1 _}_ in dynamic NOPE, which we have proved to be hard in Theorems E.27 and E.28. 

First note that from Theorem E.46, we have that the normalized quadratic form value of the linear systems in _D_ LS _[N,K,R]_ is 

**==> picture [315 x 26] intentionally omitted <==**

where _qB_ is the probability of measuring 0 on the embedded circuit when the underlying oracle property is _B_ . Theorem E.45 ensures that _q_ 1 _â‰¤_ 0 _._ 1 _, q_ 0 _â‰¥_ 0 _._ 9. That means, if we can estimate the normalized quadratic form value to _Ïµ_ = 0 _._ 03 error, we can decide the value of _B âˆˆ{_ 0 _,_ 1 _}_ because 

**==> picture [374 x 23] intentionally omitted <==**

We choose _K_ = _âŒˆ_ 1 _._ 001 _/Î¶âŒ‰_ such that 

**==> picture [327 x 26] intentionally omitted <==**

122 

For the sake of contradiction, we suppose we have a randomized classical learning algorithm _L_ with space complexity 

**==> picture [311 x 26] intentionally omitted <==**

and sample complexity _M_ that given a sequence of data samples drawn from _D_ LS _[N,K,R]_ ( _B_ ), estimates to _Ïµ_ error and hence decides _B_ with probability _p_ succ. In the following, we design a classical learning algorithm _L[â€²]_ that decides _B_ in dynamic NOPE using data from _Dg,f[KN][â€²][,T]_[1] ( _B_ ). 

The first step of _L[â€²]_ is to generate data samples that look like _D_ LS _[N,K,R]_ ( _B_ ) from _Dg,f[KN][â€²][,T]_[1] ( _B_ ). Sampling a random component of the bias vector ( _l, bl_ ) is straightforward, since _[âƒ—] b_ is simply (1 _,_ 0 _, . . . ,_ 0) _[T]_ . To sample a matrix element data ( _i, j, Aij_ ), we sample a random row _i âˆˆ_ [ _N_ ] using the same sampling procedure as in the definition of _D_ LS _[N,K,R]_ ( _B_ ). Specifically, we sample a block of the realification, a block of _A_ in Equation (E155) and a block of _Bc_ in Equation (E154) uniformly random and sample a clock time _t âˆ¼_ Uniform([ _T_ ]). Now we split into two cases: (1) the sampled clock time _t_ corresponds to a fixed two qubit gate; and (2) _t_ corresponds to a diagonal gate (the oracle). In case (1), we sample a random row of the corresponding gate matrix, which specifies the row _i_ of the matrix _A_ . We then randomly sample a non-zero column _j_ of _A_ and the corresponding matrix element _Aij_ is a fixed number given by the matrix element of that fixed two-qubit gate. This generates a sample _z_ LS = ( _i, j, Aij, l, bl_ ) that we will feed into the linear system solver _L_ . In case (2), we draw a sample _z_ = ( _x, Yx_[(] _[Î±,Î²]_[)] _, Î±, Î²_ ) from _Dg,f[KN][â€²][,T]_[1] ( _B_ ). Then we sample a random row of the oracle with given ( _x, Î±, Î²_ ) (i.e., sample _k âˆ¼_ Uniform([ _b_ ]) and output the row _|x, Î±, Î², kâŸ©_ ) and a random basis of the rest of the working qubits. This specifies the row _i_ of the matrix _A_ . We then randomly sample a non-zero column _j_ of _A_ and calculate the corresponding matrix element _Aij_ = 1 _âˆ’_ ( _âˆ’_ 1)[(] _[Y] x_[(] _[Î±,Î²]_[)] ) _k_ using that data sample from _Dg,f[KN][â€²][,T]_ 1( _B_ ). This generates a sample _z_ LS = ( _i, j, Aij, l, bl_ ) that we will feed into the linear system solver _L_ . In both cases, we repeat the same _z_ LS _T_ 3 times. This procedure generates data samples that exactly matches _D_ LS _[N,K,R]_ ( _B_ ) by construction. After sampling a linear system data point _z_ LS = ( _i, j, Aij, l, bl_ ), we feed it into the learning algorithm _L_ for linear systems. We repeat this _M_ times so that _L_ receives _M_ samples whose distribution matches that of _D_ LS _[N,K,R]_ ( _B_ ), produces an estimate of the normalized quadratic form value, and based on that estimate the value of the underlying bit _B_ . We use the estimated bit of _L_ as the final output of _L[â€²]_ . 

Note that since the data generation does not require knowledge of the previous data samples from _Dg,f[KN][â€²][,T]_[1] ( _B_ ), it can be performed online and thus the space complexity of _L[â€²]_ is _S[â€²]_ = _S_ , the same as that of _L_ . Moreover, the sample complexity of _L[â€²]_ is _M[â€²] â‰¤ M/T_ 3 because we only draw a data sample from _Dg,f[KN][â€²][,T]_[1] ( _B_ ) when case (2) happens and we repeat each data sample _T_ 3 times. The success probability of _L[â€²]_ is _p_ succ, the same as that of _L_ . Finally, we invoke Theorems E.27 and E.28. Note that for the inner product _g_ , we have _Î·_ = 1 _/_ 2, _c_ = (865 _/Î·_[2] ) logï¿½865 _/Î·_[2][ï¿½] = (865 _Ã—_ 4) log(865 _Ã—_ 4) _â‰ˆ_ 40677 _._ 68, and therefore the choice of _b_ = _âŒˆ_ 40678 log( _KN[â€²]_ ) _âŒ‰_ satisfies the requirement. For the Forrelation _f_ we use, Theorem E.40 implies that the (1 _/_ 3)-error classical distributional query complexity is (using _K_ = Î˜(1)) 

**==> picture [294 x 26] intentionally omitted <==**

Therefore, we have 

**==> picture [328 x 26] intentionally omitted <==**

satisfying the condition of Theorems E.27 and E.28. Therefore, if the _M_ = _T_ 1 _T_ 2 _T_ 3 = _O_[Ëœ] ( _RN_ ) samples are drawn from the first refreshing block only, then _M[â€²] â‰¤ M/T_ 3 = _T_ 1 _KN[â€²]_ and Theorem E.27 implies that 

**==> picture [324 x 23] intentionally omitted <==**

proving Theorem F.7. Similarly, Theorem E.28 implies that 

**==> picture [324 x 13] intentionally omitted <==**

proving Theorem F.8. This completes the proof of Theorems F.7 and F.8 and, together with the quantum algorithm result Theorem F.5, proves Theorems F.3 and F.4. 

123 

**==> picture [465 x 183] intentionally omitted <==**

**----- Start of picture text -----**<br>
D<br>movie i Ï‰xi yi<br>feature vector label<br>N<br>X Ï‰y<br>One of the best movies. Ï‰w<br>Fantastic movie. Quantum  Data: z = ( i, Ï‰xi, yi )<br>Advantage Task: predict labels of new samples y Ë†<br>Story makes no sense. machine size superpoly( N ) ?<br>Ëœ O ( D [0] [.] [99] )<br>O ( N )<br>Binary classification: sentiment analysis poly(log  D )<br>time<br>**----- End of picture text -----**<br>


FIG. 9: **Overview of the binary classification task.** We illustrate the binary classification task with a particular real-world application scenario in sentiment analysis of movie reviews. We collect positive and negative reviews of movies from users, encode them into feature vectors _âƒ—xi âˆˆ_ R _[D]_ , and use them to predict labels of new samples. A sample is the feature vector of a review _âƒ—xi_ and its label _yi_ (positive or negative). A canonical way of binary classification is the support vector machine (SVM), which is trained on the high-dimensional data matrix _X âˆˆ_ R _[N][Ã—][D]_ and label vector _âƒ—y_ and produces a decision boundary represented by a weight vector _âƒ—w âˆˆ_ R _[D]_ that classifies new samples. Our results show that a small quantum machine with size poly(log _D_ ) can solve this task with _O_[Ëœ] ( _N_ ) samples, whereas any classical machine with exponentially larger size _O_ ( _D_[0] _[.]_[99] ) cannot solve the task unless it uses a sample size at least super-polynomial in _N_ . 

## **2. Binary classification** 

In this section, we consider the fundamental task of classification in data science and machine learning. We focus on the prototypical example of binary classification. In a binary classification task, we are given _N_ data samples of the form 

**==> picture [340 x 12] intentionally omitted <==**

where _âƒ—xi_ is a vector of _D_ features and _yi âˆˆ{Â±_ 1 _}_ is its binary label. This forms a training dataset of size _N_ , represented by 

**==> picture [390 x 43] intentionally omitted <==**

where _X_ is the feature matrix and _âƒ—y_ is the label vector. Here, we adopt the convention used in data science, where each row represents a data sample and each column is a feature. The goal of binary classification is to use this training dataset to predict the labels of future unseen test data samples _âƒ—x[â€²]_ . 

A standard method for performing binary classification is support vector machine (SVM). The most basic version of SVM is the least-squares SVM (LS-SVM), where we aim to find a weight vector _âƒ—w âˆˆ_ R _[D]_ that explains the dataset by minimizing the quadratic loss function 

**==> picture [299 x 17] intentionally omitted <==**

with _â„“_ 2 regularization strength _Î» â‰¥_ 0. This method is also known as ridge classifier. Generalizations to other regularization methods such as _â„“_ 1 (lasso) are straightforward. We assume that the data matrix has been properly normalized such that _âˆ¥Xâˆ¥â‰¤_ 1 and all matrix elements _|Xij| â‰¤_ 1. The closed form solution of the weight vector reads 

**==> picture [301 x 13] intentionally omitted <==**

**==> picture [441 x 10] intentionally omitted <==**

**==> picture [347 x 12] intentionally omitted <==**

124 

We assume that the test vector is also properly normalized such that all its components have magnitude less than one: _âˆ¥âƒ—x[â€²] âˆ¥âˆž â‰¤_ 1. The classifiability of a test vector _âƒ—x[â€²]_ can be characterized by the margin _Î³_ ( _âƒ—x[â€²]_ ), defined as 

**==> picture [277 x 25] intentionally omitted <==**

which is the magnitude of the projection of _âƒ—x[â€²]_ on to the vector _âƒ—w_ , indicating how far the test point is from the decision boundary. A classifiable test vector should have a margin that is not too small (e.g., _Î³_ ( _âƒ—x[â€²]_ ) _â‰¥_ 1 _/_ poly(log _N,_ log _D_ )). 

We characterize the tractability of the binary classification task by three parameters: the sparsity _s_ , the regularized condition number _Îº_ reg, and the classifiability of the test vector _Î³_ ( _âƒ—x[â€²]_ ). The sparsity _s_ is the maximal number of non-zero elements in _X_ per row or column, which bounds the number of non-zero features per sample and the number of samples each feature is presented in. Such sparsity appears in many natural datasets (e.g., natural language data with common words trimmed off.) The regularized condition number is the condition number of the matrix that we invert in LS-SVM, _X[T] X_ + _Î»ID_ , which is equal to 

**==> picture [341 x 31] intentionally omitted <==**

where _Ïƒ_ max( _X_ ) _, Ïƒ_ min( _X_ ) are the maximal and minimal singular value of _X_ and _Îº_ = _Ïƒ_ max( _X_ ) _/Ïƒ_ min( _X_ ) is the condition number of _X_ . When no regularization is imposed ( _Î»_ = 0), the regularized condition number _Îº_ reg is the same as the condition number _Îº_ . In natural dataset, often only the largest few singular values matter for classification, but they are buried in a long tail of small singular values that are not important. Choosing a regularization strength _Î»_ that effectively truncates the long tail provides a balance between good regularized condition number _Îº_ reg and good classification performance. We focus on the regime where the number of samples _N_ and feature dimension _D_ are very large, and yet the binary classification task remains sparse, well-conditioned, and classifiable: 

**==> picture [368 x 24] intentionally omitted <==**

for every test vector _âƒ—x[â€²] j[, j]_[=][1] _[, . . . m]_[.][We][call][such][test][vectors][classifiable][vectors.][Note][that][we][always][have] _D_ = Î˜([Ëœ] _N_ ) when the sparsity _s â‰¤_ poly(log _N,_ log _D_ ). 

## _a. Problem formulation_ 

Now we formally define our data processing task of binary classification, summarized in Theorems F.9 and F.10. In particular, we specify the data generation process and the goal of the task. We consider a data generation process where we randomly get a sparse feature vector ( _i, âƒ—xi_ ) from the sparse feature matrix _X_ and its corresponding label _yi_ . The components of _âƒ—xi_ are specified by bitstrings of length _b_ = poly(log _N,_ log _D_ ) to sufficient accuracy. For simplicity, we assume that this binary representation is exact and use _âƒ—xi_ to stand for the corresponding values. 

Specifically, we consider any hierarchical data generation process _D_ BC( _X, âƒ—y_ ) with bounded repetition number _R_ that generates data samples of the form 

**==> picture [328 x 14] intentionally omitted <==**

where _âƒ—xi_ is a random entry of feature vector in the feature matrix _X_ and _yi_ is the label of that training data point. Recall that the repetition number _R_ characterize the correlation in the data, and is defined as 

**==> picture [316 x 15] intentionally omitted <==**

where _Nz_ =[ï¿½] _[Ï„] i_ =1 _[Î´][z] i[,z]_[is][the][number][of][repeating] _[z]_[â€™s][in][a][refreshing][block][of][data][and] _[Ï„]_[is][refreshing][time][that] bounds the correlation time scale. The specific way of sampling these data can be arbitrary as long as it satisfies the above form. Our results generalize straightforwardly to the more demanding scenario, where we only get a random non-zero subset of the feature vector _âƒ—xi_ , or a random and possibly unmatched label ( _j, yj_ ). Next, we specify the goal of the binary classification task. We aim to classify all possible sparse and classifiable test vectors _âƒ—x[â€²]_[= 1] _[, . . . , m]_[that][are][properly][normalized] _[âˆ¥][âƒ—x][â€²]_[In][other][words,][we][want][to][calculate][the] _j[, j] j[âˆ¥][âˆž][â‰¤]_[1.] prediction 

**==> picture [343 x 13] intentionally omitted <==**

125 

for any _s_ -sparse test vector _âƒ—x[â€²] j_[that][is][classifiable.][That][is,] 

**==> picture [351 x 25] intentionally omitted <==**

This motivates our definition of the binary classification task as follows. 

**Task F.9** (Binary classification task) **.** _Let N, D, R be integers and Î» â‰¥_ 0 _be any â„“_ 2 _regularization strength. The binary classification task is to predict the label y_ Ë† _j of any_ poly(log _N,_ log _D_ ) _-sparse and classifiable test vector âƒ—x[â€²] j[in][a][test][set][{][âƒ—x][â€²] j[}] j[m]_ =1 _[of][any][size][m][,][according][to][the][LS-SVM][rule]_ 

**==> picture [327 x 13] intentionally omitted <==**

_using data samples from any data generation process D_ BC( _X, âƒ—y_ ) _defined above with repetition number at most R that corresponds to the normalized feature matrix X âˆˆ_ R _[N][Ã—][D] , âˆ¥Xâˆ¥â‰¤_ 1 _with label vector âƒ—y âˆˆ_ R _[N] , where the feature matrix X has_ poly(log _N,_ log _D_ ) _sparsity and_ poly(log _N,_ log _D_ ) _regularized condition number._ 

Our quantum algorithm is flexible enough to handle correlated data with time-varying features. This allow us to further consider a dynamic scenario, where the training data ( _X, âƒ—y_ ) changes over time, but the labels of the test vectors remain fixed. This resembles the batch training strategy common in modern large-scale machine learning, where we train our model on batches of data that are different but the desired labels of the test vectors are fixed. We use _{y_ Ë† _j}[m] j_ =1[to][denote][that][fixed][set][of][labels][of][the][test][vectors] _[âƒ—x][â€²] j_[.][We][consider][any][hierarchical] data generation process _D_ DBC( _{_ ( _âƒ—x[â€²] j[,]_[ Ë†] _[y][j]_[)] _[}][m] j_ =1[)][with][bounded][repetition][number] _[R]_[and][refreshing][time] _[Ï„]_[of][the] form 

**==> picture [372 x 15] intentionally omitted <==**

In other words, the training set ( _X, âƒ—y_ ) changes every _Ï„_ time steps, and we keep getting random feature vectors and corresponding labels of the current training dataset. We require all training set ( _X, âƒ—y_ ) sampled from _D{_[0] ( _âƒ—x[â€²] j[,][y]_[Ë†] _[j]_[)] _[}] j[m]_ =1 to have poly(log _N,_ log _D_ ) sparsity, poly(log _N,_ log _D_ ) regularized condition number, and fixed classification rule: _y_ Ë† _j_ = sgn( _âƒ—x[â€²] j[T]_[(] _[X][T][ X]_[+] _[ Î»I][D]_[)] _[âˆ’]_[1] _[X][T][âƒ—y]_[)] _[.]_ (F56) 

The specific way that _D{_[0] ( _âƒ—x[â€²] j[,][y]_[Ë†] _[j]_[)] _[}] j[m]_ =1[samples][the][training][set][can][be][arbitrary][as][long][as][it][satisfies][the][above] requirements. Formally, we define the dynamic binary classification task as follows. 

**Task F.10** (Dynamic binary classification task) **.** _Let N, D, R, Ï„ be integers and Î» â‰¥_ 0 _be any â„“_ 2 _regular-_ Ë† _ization strength. The dynamic binary classification task is to predict the label yj of any_ poly(log _N,_ log _D_ ) _- sparse and classifiable test vector âƒ—x[â€²] j[in][a][test][set][{][âƒ—x][â€²] j[}][m] j_ =1 _[of][any][size][m][using][data][samples][from][any] D_ DBC( _{_ ( _âƒ—x[â€²] j[,]_[ Ë†] _[y][j]_[)] _[}][m] j_ =1[)] _[defined][above][with][repetition][number][at][most][R][and][refreshing][time][Ï„][.]_ 

In the following, we first state our main results on quantum advantage in binary classification. Then we prove the quantum easiness and classical hardness in subsequent sections. 

_b. Main results_ 

Our first result shows that given the same amount of samples, a small quantum machine can solve the binary classification task better than an exponentially larger classical machine. This means that using a quantum machine, we can build a better model with exponentially smaller size. Note that the scaling _D_[1] _[âˆ’][Î¶]_ is effectively _D_ since it holds for any constant _Î¶ >_ 0. 

**Theorem F.11** (Quantum advantage in binary classification) **.** _Consider the binary classification task withO_ Ëœ( _RNsample_ ) _samples,dimensiona quantum machine withN , feature dimension_ poly(log _D and Drepetition_ ) _size can solve it with high success probability, whilenumber R defined in Theorem F.9. Using any classical machine with o_ ( _D_[1] _[âˆ’][Î¶]_ ) _size for any constant Î¶ >_ 0 _cannot solve it with success probability more than_ 1 _/_ 2 + 1 _/N[Ï‰]_[(1)] _. Moreover, the data processing time per sample of the quantum machine is_ poly(log _D_ ) _._ 

126 

The second result shows that if the size of the classical machine is slightly smaller than _o_ ( _D_ ), it would need super-polynomially more samples than a small quantum machine to solve the dynamic binary classification task. In the context of batch training, this means that quantum machines can solve the task with a few batches of training data, whereas sub-exponential size classical machines require super-polynomially many batches. 

**Theorem F.12** (Quantum advantage in dynamic binary classification) **.** _Consider the dynamic binary classification task with sample dimension N , feature dimension D, repetition number R, and sufficient refreshingO_ Ëœ( _RN_ ) _samplestime Ï„ to_ = _solveO_[Ëœ] ( _RNit_ ) _withdefinedhighinsuccessTheoremprobability,F.10. A quantumwhile anymachineclassicalwithmachine_ poly(log _with D_ ) _osize_ ( _D_[1] _[âˆ’] can[Î¶]_ ) _sizeuse for any constant Î¶ >_ 0 _that solves it with probability at least_ 2 _/_ 3 _must collect at least RN[Ï‰]_[(1)] _samples. Moreover, the data processing time per sample of the quantum machine is_ poly(log _D_ ) _._ 

Together, Theorems F.11 and F.12 establish unconditional and exponential quantum advantages in the foundational task of binary classification. 

## _c. Quantum algorithm_ 

Here, we prove the quantum algorithm parts of Theorems F.11 and F.12. We construct an algorithm that runs high-dimensional SVM on a small quantum computer. We do so by combining quantum oracle sketching (Theorem D.16), quantum state sketching (Theorem D.24), and standard quantum ridge regression solver that prepares the weight vector _|wâŸ©_ of the LS-SVM. We use a variant of Clifford classical shadow [74], which we call interferometric classical shadow (Theorem F.16), to readout the weight vector _|wâŸ©_ into a classical representation, which is used for predicting the labels of all possible test vectors. 

**Theorem F.13** (Binary classification with quantum oracle sketching) **.** _Let N, D be large integers, Î´ âˆˆ_ (0 _,_ 1) _, and Î» â‰¥_ 0 _be the â„“_ 2 _regularization strength. Let X_ = ( _âƒ—x_ 1 _, . . . , âƒ—xN_ ) _[T] âˆˆ_ R _[N][Ã—][D] , âƒ—y_ = ( _y_ 1 _, . . . , yN_ ) _[T] âˆˆ_ R _[N] be a training dataset where X is s-sparse with norm âˆ¥Xâˆ¥â‰¤_ 1 _and regularized condition number Îº_ reg = ï¿½( _Ïƒ_ max[2] ( _X_ ) + _Î»_ ) _/_ ( _Ïƒ_ min[2][(] _[X]_[) +] _[ Î»]_[)] _[.][Consider][a][set][of][s][-sparse][test][vectors][{][âƒ—x][â€²] j[}][m] j_ =1 _[,][ âˆ¥][âƒ—x][â€²] j[âˆ¥][âˆž][â‰¤]_[1] _[,][of] any size m that all have margin Î³_ ( _âƒ—x[â€²] j_[)] _[â‰¥][Î³]_[test] _[,][ âˆ€][j][âˆˆ]_[[] _[m]_[]] _[.][There][exists][a][quantum][algorithm][that][can] output the prediction y_ Ë† _j_ = sgn( _âƒ—x[â€²] j[Â·][âƒ—w]_[)] _[,] âƒ—w_ = ( _X[T] X_ + _Î»ID_ ) _[âˆ’]_[1] _X[T] âƒ—y,_ (F57) 

_for any j âˆˆ_ [ _m_ ] _with probability at least_ 1 _âˆ’ Î´ using_ 

**==> picture [444 x 87] intentionally omitted <==**

_qubits and_ 

_samples from the data generation process D_ BC( _X, âƒ—y_ ) _with repetition number R. In particular, we have_ 

**==> picture [453 x 35] intentionally omitted <==**

We note that Theorem F.13 immediately implies the quantum algorithm part of Theorem F.11 by definition of the binary classification task. It also proves the quantum algorithm part of Theorem F.12 by taking _Ï„_ = _O_[Ëœ] ( _RN_ ) larger than _M_ = _O_[Ëœ] ( _RN_ ). 

We use the following quantum ridge regression solver as the backbone of our quantum algorithm and instantiate the oracle queries with quantum oracle sketching. We note that for coherent usage, the failure probability originally stated in [83] is absorbed into the error parameter _Ïµ_ by replacing standard amplitude amplification with fixed-point amplitude amplification. We bound the error in 2-norm to avoid ambiguity in the global phase. The complexity scaling with _Îº_ reg may be further improved by applying Theorem F.6 to the augmented matrix 

127 

**==> picture [36 x 24] intentionally omitted <==**

**Lemma F.14** (Quantum ridge regression solver [83, Theorem 32]) **.** _Let N, D be large integers. Let Î» â‰¥_ 0 _be the normalized â„“_ 2 _regularization strength. Let X âˆˆ_ R _[N][Ã—][D] , âƒ—y âˆˆ_ R _[N] be the training dataset with norm âˆ¥Xâˆ¥â‰¤_ 1 _and regularized condition number Îº_ reg = ~~ï¿½~~ ( _Ïƒ_ max[2] ( _X_ ) + _Î»_ ) _/_ ( _Ïƒ_ min[2][(] _[X]_[) +] _[ Î»]_[)] _[.][There][exists][a][quantum][algorithm][that] applies a unitary V such that_ 

**==> picture [385 x 25] intentionally omitted <==**

_using S_ = _O_ (log(max _{N, D}_ ) + log( _Îº_ reg)) _qubits, O_ ( _Îº_ reg log( _Îº_ reg) log( _Îº_ reg _/Ïµ_ )) _gates, and O_ ( _Îº_ reg log( _Îº_ reg) log( _Îº_ reg _/Ïµ_ )) _queries to the block encoding of X and the state preparation unitary of |yâŸ©_ =[ï¿½] _i[y][i][ |][i][âŸ©][/][âˆ¥][âƒ—y][âˆ¥][and][their][inverse][and][controlled][versions.]_ 

We use Clifford classical shadow tomography to readout the weight vector and make predictions. 

**Lemma F.15** (Clifford classical shadow, [74]) **.** _Let Ï be any D-dimensional quantum state and O_ 1 _, . . . , Om âˆˆ_ Ë† C _[D][Ã—][D] be observables. Let Ïµ, Î´ âˆˆ_ (0 _,_ 1) _. Then, there is a quantum algorithm that can predict oi such that_ 

**==> picture [307 x 11] intentionally omitted <==**

_with probability at least_ 1 _âˆ’ Î´, using_ 

**==> picture [305 x 25] intentionally omitted <==**

Ë† _copies of Ï. Moreover, the time complexity of predicting any oi is_ poly( _D_ ) _if the expectation value of Oi on any stabilizer state can be calculated in_ polylog( _D_ ) _time._ 

To make predictions on the labels, we need to estimate the sign of _âŸ¨x|wâŸ©_ . Measuring the observable _|xâŸ©âŸ¨x|_ on _|wâŸ©_ only gives us the magnitude _| âŸ¨x|wâŸ©|_[2] . The standard way of keeping the sign information is via Hadamard test, in which we introduce an ancilla, prepare the state ~~_âˆš_~~ 12[(] _[|]_[0] _[âŸ©|][x][âŸ©]_[+] _[ |]_[1] _[âŸ©|][w][âŸ©]_[),][and measure the ancilla.][However,] this contradicts our goal of classical shadow, where we want to collect a universal set of data from _|wâŸ©_ that can be used to predict many different _|xâŸ©_ afterwards. To address this issue, we develop the following technique that we call interferometric classical shadow. 

**Lemma F.16** (Interferometric classical shadow) **.** _Let |wâŸ© , |x_ 1 _âŸ© , . . . , |xmâŸ©âˆˆ_ C _[D] be D-dimensional pure states. Assume that we have complete classical descriptions of |x_ 1 _âŸ© , . . . , |xmâŸ©. Let Ïµ, Î´ âˆˆ_ (0 _,_ 1) _. Then, there is a quantum algorithm that can predict o_ Ë† _i such that_ 

**==> picture [297 x 67] intentionally omitted <==**

_with probability at least_ 1 _âˆ’ Î´, using_ 

_queries of the controlled state preparation unitary of |wâŸ©. Moreover, the time complexity of predicting any o_ Ë† _i is_ polylog( _D_ ) _if the overlap between |xiâŸ© and any stabilizer state can be calculated in_ polylog( _D_ ) _time._ 

_Proof of Theorem F.16._ We apply Clifford classical shadow (Theorem F.15) on the state 

**==> picture [302 x 24] intentionally omitted <==**

which can be prepared with a single query of the controlled state preparation of _|wâŸ©_ on ~~_âˆš_~~ 12[(] _[|]_[0] _[âŸ©]_[+] _[|]_[1] _[âŸ©]_[)] _[ |]_[0] _[âŸ©]_[.][Consider] the observables _Oi_ = _|xi_ + _âŸ©âŸ¨xi_ + _| âˆ’|xiâˆ’âŸ©âŸ¨xiâˆ’|_ , where 

**==> picture [306 x 24] intentionally omitted <==**

128 

satisfy _âŸ¨xi_ + _|xiâˆ’âŸ©_ = 0. Note that trï¿½ _Oi_[2] ï¿½ = 2 and we have 

**==> picture [340 x 58] intentionally omitted <==**

Moreover, evaluating the expectation value of _Oi_ on any stabilizer state reduces to evaluating the overlap between _|xiâŸ©_ and any stabilizer state. Theorem F.16 then follows directly from Theorem F.15. 

Recall that in Theorem D.23, we have shown that _O_[Ëœ] ( _RNs_[5] ) samples suffice to implement the block encoding of an _s_ -sparse matrix. In addition, Theorem D.24 shows that we can use _O_[Ëœ] ( _RN_ ) samples to prepare the quantum state of any vector. We combine Theorem F.14 with Theorem D.23 and Theorem D.24 to prove Theorem F.13. 

_Proof of Theorem F.13._ Let _n_ = _âŒˆ_ log2(max( _N, D_ )) _âŒ‰â‰¤_ min _{O_ (log( _sD_ )) _, O_ (log( _sN_ )) _}_ and embed _X, âƒ—y_ into 2 _[n]_ dimension to apply quantum oracle and state sketching. Theorem F.14 states that there is a quantum ridge regression solver, which is a unitary _V_ that prepares the state _|wâŸ©_ with _Ïµ/_ 2 error using _O_ ( _n_ + log( _Îº_ reg)) qubits and 

**==> picture [316 x 11] intentionally omitted <==**

queries to the block encoding of _X_ and the state preparation unitary of _|yâŸ©_ and their inverse and controlled versions. By replacing all gates and queries in _V_ with their controlled versions, we obtain a controlled state preparation unitary _cV_ that prepares _|wâŸ©_ with error _Ïµ/_ 2. 

Similar to the proof of Theorem F.5, our proof of Theorem F.13 proceeds in two steps. We first use this quantum ridge regression solver to construct a query algorithm that can predict _y_ Ë† _j_ correctly for any _j âˆˆ_ [ _m_ ] with probability at least 1 _âˆ’ Î´/_ 2. Then, we instantiate the queries with quantum oracle and state sketching. The instantiation error is chosen to be _Î´/_ 2 such that the total variation distance error on the final prediction is _Î´/_ 2. This immediately implies that the final prediction is correct with probability at least 1 _âˆ’ Î´/_ 2 _âˆ’ Î´/_ 2 = 1 _âˆ’ Î´_ . 

As the first step, we construct the query algorithm that makes correct predictions. The quantum ridge regression solver gives us a controlled state preparation unitary _cV_ that prepares _|wâŸ©_ to _Ïµ/_ 2 using _O_ ( _n_ +log( _Îº_ reg)) qubits and _Q_ 0 = _O_ ( _Îº_ reg log( _Îº_ reg) log( _Îº_ reg _/Ïµ_ )) queries to _X_ and _|yâŸ©_ . To readout the weight vector well enough that we can predict any _s_ -sparse test vector _âƒ—x[â€²] j_[,][we][imagine][that][we][have][an] _[Ïµ]_[0][-covering][net] _[N]_[over][the][set] 

**==> picture [332 x 12] intentionally omitted <==**

in _âˆ¥Â· âˆ¥_ 2. Note that this covering net is only a analysis tool and it is not used in the algorithm. The covering net has size 

**==> picture [326 x 28] intentionally omitted <==**

We run interferometric classical shadow (Theorem F.16) using the controlled state preparation unitary _cV_ with the test states _|x[â€²] âŸ©_ , _âƒ—x[â€²] âˆˆN_ , error _Ïµ_ 0, and success probability _Î´/_ 2. This consumes 

**==> picture [347 x 25] intentionally omitted <==**

queries to _cV_ and guarantees that the prediction of the overlap is _Ïµ_ 0 accurate on the _Ïµ_ 0-covering net _N_ of _X_ test. By continuity, this implies that the prediction of the overlap is _E_ 0 = _O_ ( _Ïµ_ 0) accurate on the whole set _X_ test (see e.g., [175, Exercise 4.4.3]). We choose _Ïµ_ 0 such that _Ïµ/_ 2 = _E_ 0 = _O_ ( _Ïµ_ 0). Combining the error of the state preparation unitary, we know that the produced estimator is an _E_ 0 + _Ïµ/_ 2 = _Ïµ_ accurate estimate of _âŸ¨x[â€²] |wâŸ©_ for all _âƒ—x[â€²] âˆˆX_ test. Meanwhile, if the size of test vectors _m_ is small, then _O_ (log( _m/Î´_ ) _/Ïµ_[2] ) queries suffice. Hence the number of queries to _cV_ that we need is 

**==> picture [337 x 25] intentionally omitted <==**

From the assumption, we know that the margin of each test vector _âƒ—x[â€²] j_[satisfies] 

**==> picture [333 x 25] intentionally omitted <==**

129 

This implies that 

**==> picture [300 x 21] intentionally omitted <==**

because _âƒ—x[â€²] j_[is] _[s]_[-sparse][and][hence] _[âˆ¥][âƒ—x][â€²] j[âˆ¥]_[2] _[â‰¤]_ ï¿½ _sâˆ¥âƒ—x[â€²] j[âˆ¥][âˆž][â‰¤âˆš] s_ . Therefore, estimating ï¿½ _x[â€²] j[|][w]_ ï¿½ to _Î³_ test _/_ (3 _[âˆš] s_ ) suffices to determine 

**==> picture [314 x 13] intentionally omitted <==**

We therefore set 

**==> picture [263 x 21] intentionally omitted <==**

This gives us a quantum query algorithm that makes 

**==> picture [415 x 94] intentionally omitted <==**

queries to _X, |yâŸ©_ and can output the prediction _y_ Ë† _j, âˆ€j âˆˆ_ [ _m_ ] (a classical random variable) with probability at least 1 _âˆ’ Î´/_ 2. Moreover, the space complexity is 

**==> picture [468 x 53] intentionally omitted <==**

where the first term comes from the ridge regression solver, the second comes from the classical shadow data, and the third one comes from classical simulation of Clifford circuits. 

The second step is to instantiate the queries to _X_ and _|yâŸ©_ in the query algorithm using quantum oracle and state sketching. We first replace all queries to the block encoding of _X_ and its inverse and controlled versions to their _Ïµ_ 1-approximate versions in Theorem D.23. This incurs an error of _E_ 1 = _QÏµ_ 1 = _Î´/_ 6, where we set _Ïµ_ 1 = _Î´/_ (6 _Q_ ). 

Next, we replace the queries to _Ïµ_ 1-approximate versions of block encoding of _X_ and its inverse and controlled versions by the random unitary channel that we build from samples in Theorem D.23. This incurs an additional error of _E_ 2 = _QÏµ_ 1 = _Î´/_ 6, and uses _O_ ( _n_ + _b_ + log[2] _[.]_[5] (1 _/Ïµ_ 1)) = _O_ ( _n_ + _b_ + log[2] _[.]_[5] ( _Q/Î´_ )) qubits and 

**==> picture [391 x 30] intentionally omitted <==**

samples from the data generation process. Note that here we only use the feature data and throw away the label data in each sample. 

Finally, we replace the queries to the state preparation unitary of _|yâŸ©_ and its inverse and controlled versions by the _Ïµ_ 1-error random unitaries that we build from samples according to Theorem D.24. This incurs an additional error of _E_ 3 = _QÏµ_ 1 = _Î´/_ 6, and uses _O_ ( _n_ log( _N/Ïµ_ 1)) _â‰¤ O_ ( _n_ logï¿½ _NÎ´Q_ ï¿½) qubits and 

**==> picture [373 x 31] intentionally omitted <==**

samples from the data generation process. Here we only use the label data and throw away the feature data in each sample. 

According to Theorem D.17, the total error in instantiating the query algorithm is bounded by 

**==> picture [308 x 11] intentionally omitted <==**

130 

This means that the output of the query-instantiated quantum algorithm, which is a classical random variable must be correct with probability at least 1 _âˆ’ Î´/_ 2 _âˆ’ Î´/_ 2 = 1 _âˆ’ Î´_ . The total number of qubits used is 

**==> picture [457 x 96] intentionally omitted <==**

The total number of samples is 

This completes the proof of Theorem F.13. 

## _d. Classical hardness_ 

In this section, we prove the two classical hardness results in Theorems F.11 and F.12. We fix the _â„“_ 2 regularization strength _Î»_ = 0 throughout the proof so that the regularized condition number is the same as the condition number of _X_ : _Îº_ reg = _Îº_ . We will construct a (dynamic) binary classification task with _N_ = _D_ . Hence, for simplicity, we will use _N_ alone throughout this section. We prove the classical hardness results by constructing a specific binary classification task using Theorem E.47. Solving it amounts to solving the (dynamic) Noisy Oracle Property Estimation (NOPE) task defined in Section E (Theorems E.1 and E.26), whose classical hardness we have already proved in Theorems E.27 and E.28. 

This gives us two classical hardness results. The first result follows from Theorem E.27 and shows that any classical learning algorithm that wants to perform better than random guessing in binary classification with the same number of samples quantum algorithms need must have â„¦( _D_[1] _[âˆ’][Î¶]_ ) size for any constant _Î¶ >_ 0. The second result follows from Theorem E.28 and shows that when the binary classification task is dynamic, any classical learning algorithm will need a number of samples super-polynomial in _N_ if it has size _o_ ( _D_[1] _[âˆ’][Î¶]_ ) for any constant _Î¶ >_ 0. 

The general idea of proving these results is to embed the quantum circuit that solves dynamic NOPE from Ë† Theorem E.45 into a binary classification task via Theorem E.47. The label _y_ of a fixed, sparse test vector _âƒ—x_ encodes the oracle property _B âˆˆ{_ 0 _,_ 1 _}_ that we want to estimate in (dynamic) NOPE. Then we show that given any classical algorithm that predicts the label _y_ Ë†, we can use it to construct a classical algorithm that solves (dynamic) NOPE. In the (dynamic) NOPE task, we take the oracle property function _f_ to be _K_ -Forrelation (Theorem E.38) and the noisy encoding function _g_ to be the inner product (Theorem E.41). 

In the following, we construct the data generation process _D_ BC _[N,K,R]_ ( _B_ ) _, B âˆˆ{_ 0 _,_ 1 _}_ for binary classification, where _N_ is both the sample dimension and the feature dimension (i.e., _D_ = _N_ ), _K_ = Î˜(1) is the constant in the Forrelation that we will embed, _R_ is an integer that specifies the repetition number, and _B_ indicates whether the label of that fixed test vector is +1 or _âˆ’_ 1 (see Theorem E.47). The goal is to solve for _B_ . It helps to compare this construction to the dynamic NOPE data generation process defined in Section E 4. 

Given _N_ , we define another large integer _N[â€²]_ as follows. Let _T_ = Î˜(log[3] _N[â€²]_ log log _N[â€²]_ ) be the total number of two-qubit gates and diagonal gates given in Theorem E.45 and let _n[â€²]_ = log _N[â€²]_ + _O_ (log log _N[â€²]_ ) be the number of qubits in Theorem E.45. To properly embed that circuit into the _N_ -dimensional training dataset, we define _N[â€²]_ such that _N_ = 48 _T_ 2 _[n][â€²]_ = _N[â€²] Â·_ polylog _N[â€²]_ as in Theorem E.47. This implies _N[â€²]_ = _N/_ polylog _N_ . The resulting feature matrix _X_ have sparsity _s_ = _O_ (1) and condition number _Îº_ = _O_ ( _T_ ) = _O_ (log[3] _N_ log log _N_ ) from Theorem E.47. We fix the label vector to be the _âƒ—y_ in Theorem E.47. Let _L_ = ï¿½log[2] ( _KN[â€²]_ )ï¿½ _â‰¥_ 5 be the number of independent oracle instances that we have in dynamic NOPE. 

Now we define the data generation process 

**==> picture [392 x 15] intentionally omitted <==**

where _T_ 3 = _R_ , _T_ 2 = _KN[â€²]_ , _T_ 1 = _âŒˆMQ/_ ( _T_ 2 _T_ 3) _âŒ‰_ = polylog( _KN[â€²]_ ), _MQ_ = _RN_ polylog( _N_ ) is the number of samples quantum machines need in Theorem F.13, _X âˆˆ_ R _[N][Ã—][N]_ is an _N_ -dimensional, symmetric, _O_ (1)-sparse feature matrix with condition number _Îº_ = _O_ ( _T_ ) = _O_ (log[3] _N_ log log _N_ ), _Î± âˆˆ{_ 0 _,_ 1 _}, Î² âˆˆ_ [ _L_ ] label which part of the matrix _X_ that we are currently collecting matrix element data from, _i âˆˆ_ [ _N_ ] labels the _i_ -th training data point _âƒ—xi_ (the _i_ -th row of the matrix _X_ ), and _yi_ is the corresponding label in _âƒ—y_ . 

The data are sampled in the following way that resembles dynamic NOPE in Section E 4. _DB_[0][samples][a] length- _L_ bitstring _Î³_ with parity 

**==> picture [267 x 31] intentionally omitted <==**

131 

uniformly random. For each _j âˆˆ_ [ _L_ ], we sample a random oracle _oj âˆ¼ pÎ³j_ , where _p_ 0 _, p_ 1 are the distributions of Forrelation defined in Theorem E.39. Then we sample a noisy encoding pair ( _Y_[(0] _[,j]_[)] _, Y_[(1] _[,j]_[)] ) _âˆ¼_ Uniform(( _g[N]_ ) _[âˆ’]_[1] ( _oj_ )) using the inner product noisy encoding function _g_ defined in Theorem E.41. Next, note that ( _Y_[(0] _[,j]_[)] _, Y_[(1] _[,j]_[)] ) _[L] j_ =1[specifies][an] _[n][â€²]_[-qubit][quantum][circuit] _[C]_[with] _[T]_[=] _[O]_[(log][3] _[ N][ â€²]_[ log log] _[ N][ â€²]_[)] gates via Theorem E.45, and the quantum circuit _C_ gives a training dataset ( _X, âƒ—y_ ) with dimension 48 _T[â€²]_ 2 _[n][â€²]_ = _N_ via Theorem E.47. Here, _X_ is indeed _O_ (1)-sparse with condition number _Îº_ = _O_ ( _T_ ) = _O_ (log[3] _N_ log log _N_ ). Now we define _DX_[1][.][We][first][sample][a][uniformly][coordinate] _[Î²][âˆ¼]_[Uniform([] _[L]_[])][and][a][random][bit] _[Î±][ âˆ¼]_[Bern(1] _[/]_[2)][as][in] dynamic NOPE. Then we pick out _Y_[(] _[Î±,Î²]_[)] and use it to generate the data samples. 

In particular, we define _D_ ([2] _Î±,Î²_ )[in][the][following][way.] We first sample a random row of the matrix _X_ as follows. We note that after uniformly sampling the realification blocks given in Theorem E.43, the linear space corresponding to the matrix _X_ has a particular factorization given by Theorem E.47. We sample the nested blocks of _X_ uniformly randomly. Then we are left with the subspace _|tâŸ©|ÏˆâŸ©_ where _|tâŸ©_ is the clock register and _|ÏˆâŸ©_ is the _n[â€²]_ -qubit register that the quantum circuit runs on. We sample a clock time _t âˆ¼_ Uniform([ _T_ ]) and the matrix is reduced to a specific gate in the _n[â€²]_ -qubit subspace (either a fixed two qubit gate or a diagonal gate that depends on _Y_[(] _[Î±,Î²]_[)] ). The remaining subspace further factorizes into _|x, Î±, Î², kâŸ©_ and the rest of the working qubits. We sample a random basis of this _n[â€²]_ -qubit subspace by plug in the specific ( _Î±, Î²_ ) that we have already sampled, sample _x âˆ¼_ Uniform([ _KN[â€²]_ ]) _, k âˆ¼_ Uniform([ _b_ ]), and sample a computational basis of the rest of the working qubits uniformly random. This together specifies and thus samples a row _i_ of the matrix _X_ . Note that the marginal distribution of _i_ is uniform over [ _N_ ] (because _Î±, Î²_ are sampled uniformly), though there are correlations between consecutive samples of _i_ since they share the same set of ( _Î±, Î²_ ). 

Note that by construction of the matrix _X_ as in Theorem E.47, the picked out row vector _âƒ—xi_ is _O_ (1) sparse, and has components that is the real or imaginary part of either 1, from the identity matrices in Equations (E154) and (E155), or a matrix element of a fixed two qubit gates, or 1 _âˆ’_ ( _âˆ’_ 1)[(] _[Y] x_[(] _[Î±,Î²]_[)] ) _k eâˆ’_ 1 _/T_ (see Equation (E154)) which is solely specified by _Y_[(] _[Î±,Î²]_[)] . This gives us the sample _z_ = ( _i, âƒ—xi, yi_ ) and we repeat this sample _T_ 3 times, completing the data generation process. 

This data generation process _D_ BC _[N,K,R]_ is a valid data generation process of dynamic binary classification. It produces a random row sample uniformly distributed over the rows of _X_ . The test vector is a single fixed _O_ (1)-sparse vector _âƒ—x[â€²]_ specified in Theorem E.47, which satisfies 

**==> picture [431 x 25] intentionally omitted <==**

where _qB_ is the probability of measuring 0 on the embedded circuit given by Theorem E.45 when the underlying oracle property is _B_ . Theorem E.45 ensures that _q_ 1 _â‰¤_ 0 _._ 1 _, q_ 0 _â‰¥_ 0 _._ 9. Therefore, we have the label 

**==> picture [295 x 12] intentionally omitted <==**

and the margin 

**==> picture [328 x 12] intentionally omitted <==**

as required. The repetition number of the data generation process is upper bounded by _T_ 2 _T_ 3 _/_ ( _KN[â€²]_ ) = _R_ , _O_ becauseËœ( _RN_ ), thesatisfyingsamplingthesteprequirementsof _DX_[1] _[â†’][Ã—]_ in _[T]_[1] Theorems _[D]_ ([2] _Î±,Î²_ )[is][independent.] F.11 and F.12[The] .[refreshing][time][is] _[Ï„]_[=] _[ T]_[1] _[T]_[2] _[T]_[3][=] _[ O]_[(] _[M][Q]_[) =] 

This data generation process for binary classification _D_ BC _[N,K,R]_ ( _B_ ) is designed to reduce to the dynamic NOPE data _Dg,f[KN][â€²][,T]_[1] ( _B_ ) in Section E 4 via Theorems E.45 and E.47. Using this data generation process, we prove the following two results. 

**Theorem F.17** (Classical hardness of binary classification) **.** _Let Î¶ >_ 0 _be any constant. Let N, D be theO_ Ëœ( _RNsample_ ) _samples,and featureany randomizeddimensionclassicalof a binarylearningclassificationalgorithmtaskwithandspaceR becomplexityits repetition number. Using_ 

**==> picture [255 x 12] intentionally omitted <==**

_cannot solve the binary classification task with success probability more than_ 1 _/_ 2 + 1 _/N[Ï‰]_[(1)] _._ 

132 

**Theorem F.18** (Classical hardness of dynamic binary classification) **.** _Let Î¶ >_ 0 _be any constant. Let N, D be the sample and feature dimension of a dynamic binary classification task and R, Ï„_ = _O_[Ëœ] ( _RN_ ) _be its repetition number and refreshing time. Any randomized classical learning algorithm that solves the task with success probability at least_ 2 _/_ 3 _must have sample complexity_ 

**==> picture [96 x 10] intentionally omitted <==**

**==> picture [256 x 56] intentionally omitted <==**

Theorem F.17 immediately implies the classical hardness part of Theorem F.11 because the first _O_[Ëœ] ( _RN_ ) samples from the constructed binary classification data belongs to the same training dataset and therefore is a valid sequence of non-dynamic binary classification data. Theorem F.18 directly implies the classical hardness part of Theorem F.12. Together with the quantum algorithm result Theorem F.13, this completes the proof of the quantum advantage claims in Theorems F.11 and F.12. 

_Proof of Theorems F.17 and F.18._ Recall that _N_ = _D_ in the task that we construct. For simplicity, we will use _N_ throughout the proof. We prove Theorems F.17 and F.18 by showing that given any classical learning algorithm that can predict the label _y_ Ë† of the test vector _âƒ—x[â€²]_ , we can use it to construct an algorithm that decides _B_ from _Dg,f[KN][â€²][,T]_[1] ( _B_ ), which we have proved to be hard in Theorems E.27 and E.28. First note that, since 

**==> picture [267 x 13] intentionally omitted <==**

if we can predict the label _y_ Ë†, we can indeed decide _B_ . We choose _K_ = _âŒˆ_ 1 _._ 001 _/Î¶âŒ‰_ such that 

**==> picture [327 x 26] intentionally omitted <==**

For the sake of contradiction, suppose we have a randomized classical learning algorithm _L_ with space complexity 

**==> picture [311 x 26] intentionally omitted <==**

and sample complexity _M_ that given a sequence of data samples drawn from _D_ BC _[N,K,R]_ ( _B_ ), predicts _y_ Ë† and hence decides _B_ with probability _p_ succ. In the following, we design a classical learning algorithm _L[â€²]_ that decides _B_ using data from _Dg,f[KN][â€²][,T]_[1] ( _B_ ). 

The first step of _L[â€²]_ is to generate data samples that look like _D_ BC _[N,K,R]_ ( _B_ ) from _Dg,f[KN][â€²][,T]_[1] ( _B_ ). We sample a random row _i âˆˆ_ [ _N_ ] of _X_ using the same sampling procedure as in the definition of _D_ BC _[N,K,R]_ ( _B_ ). To this end, we sample a block of the realification, a block of _X_ , a block of _A_ in Equation (E155) and a block of _B_ in Equation (E154) uniformly random and sample a clock time _t âˆ¼_ Uniform([ _T_ ]). Now we split into two cases: (1) the sampled clock time _t_ corresponds to a fixed two qubit gate; and (2) _t_ corresponds to a diagonal gate (the oracle). In case (1), we sample a random row of the corresponding gate matrix, which specifies the row _i_ of the matrix _X_ . The corresponding training data vector _âƒ—xi_ is completed determined by the matrix elements of that fixed two-qubit gate, and therefore can be calculated. This generates a sample _z_ BC = ( _i, âƒ—xi, yi_ ) that we will feed into the binary classifier _L_ . In case (2), we draw a sample _z_ = ( _x, Yx_[(] _[Î±,Î²]_[)] _, Î±, Î²_ ) from _Dg,f[KN][â€²][,T]_[1] ( _B_ ). Then we sample a random row of the oracle with given ( _x, Î±, Î²_ ) (i.e., sample _k âˆ¼_ Uniform([ _b_ ]) and output the row _|x, Î±, Î², kâŸ©_ ) and a random basis of the rest of the working qubits. This specifies the row _i_ of the matrix _X_ . We then calculate the corresponding training data vector _âƒ—xi_ , which is completely determined by the row of the diagonal gate with the diagonal element 1 _âˆ’_ ( _âˆ’_ 1)[(] _[Y] x_[(] _[Î±,Î²]_[)] ) _k_ , using that data sample from _Dg,f[KN][â€²][,T]_ 1( _B_ ). This generates a sample _z_ BC = ( _i, âƒ—xi, yi_ ) that we will feed into the binary classifier _L_ . In both cases, we repeat the same _z_ BC _T_ 3 times. Note that this procedure generates data samples that exactly matches _D_ BC _[N,K,R]_ ( _B_ ) by construction. 

After sampling a training data point _z_ BC = ( _i, âƒ—xi, yi_ ), we feed it into the learning algorithm for binary classification _L_ . We repeat this _M_ times so that _L_ receives _M_ samples whose distribution matches that of _D_ BC _[N,K,R]_ ( _B_ ) and produces a prediction of the label _y_ Ë† that provides a prediction of _B_ . We use this predicted bit of _L_ as the final output of _L[â€²]_ . 

133 

Note that since the data generation does not require knowledge of the previous data samples from _Dg,f[KN][â€²][,T]_[1] ( _B_ ), it can be performed online and thus the space complexity of _L[â€²]_ is _S[â€²]_ = _S_ . Moreover, the sample complexity of _L[â€²]_ is _M[â€²] â‰¤ M/T_ 3 because we only draw a data sample from _Dg,f[KN][â€²][,T]_[1] ( _B_ ) when case (2) happens and we repeat each data sample _T_ 3 times. The success probability of _L[â€²]_ is _p_ succ, the same as that of _L_ . 

Finally, we invoke Theorems E.27 and E.28. Note that for the inner product _g_ , we have _Î·_ = 1 _/_ 2, _c_ = (865 _/Î·_[2] ) logï¿½865 _/Î·_[2][ï¿½] = (865 _Ã—_ 4) log(865 _Ã—_ 4) _â‰ˆ_ 40677 _._ 68, and therefore the choice of _b_ = _âŒˆ_ 40678 log( _KN[â€²]_ ) _âŒ‰_ satisfies the requirement. For the Forrelation _f_ we use, Theorem E.40 implies that the (1 _/_ 3)-error classical distributional query complexity is (using _K_ = Î˜(1)) 

**==> picture [292 x 26] intentionally omitted <==**

and therefore 

**==> picture [325 x 27] intentionally omitted <==**

satisfying the condition of Theorems E.27 and E.28. Therefore, if the _M_ = _T_ 1 _T_ 2 _T_ 3 = _O_[Ëœ] ( _RN_ ) samples are drawn from the first refreshing block only, then _M[â€²] â‰¤ M/T_ 3 = _T_ 1 _KN[â€²]_ and Theorem E.27 implies that 

**==> picture [324 x 24] intentionally omitted <==**

proving Theorem F.17. On the other hand, Theorem E.28 implies that 

**==> picture [324 x 13] intentionally omitted <==**

proving Theorem F.18. This completes the proof of Theorems F.17 and F.18 and, together with the quantum algorithm result Theorem F.13, proves Theorems F.11 and F.12. 

134 

**==> picture [462 x 330] intentionally omitted <==**

**----- Start of picture text -----**<br>
D<br>A A low dimensional rep.<br>A<br>U G A i Ï‰xi<br>U<br>G C feature vector<br>A<br>C A N<br>U<br>U U X<br>U U<br>C A A<br>G<br>G U A C A A Quantum  Data: z = ( i, Ï‰xi )<br>U A Advantage Task: estimate low dimensional rep. Ï‰ ( Îµx )<br>A<br>U G machine size<br>C U A superpoly( N ) ?<br>A<br>ne<br>O Ëœ( N ) O ( D [0] [.] [99] )<br>Dimension reduction: RNA sequencing poly(log  D ) time<br>10: Overview of the dimension reduction task. We illustrate the dimension reduction task with a<br>application scenario in single cell RNA sequencing (scRNA-seq). We conduct RNA sequencing experiments<br>obtain gene sequences in cell samples, which are represented as feature vectors âƒ—xii âˆˆ R [[D]] (e.g., via frequency<br>-mer representations). A sample is the feature vector âƒ—xii of a single RNA sequence. A canonical way of dimension<br>is principal component analysis (PCA), which is performed on the high-dimensional data matrix X âˆˆ R [[N]]<br>produces a principal component vector âƒ—w âˆˆ R [[D]] that represents the most important feature combination. We<br>low dimension representation Î¾ ( âƒ—x ) of a sample âƒ—x by projecting it onto the principal component âƒ—w . Our results<br>that a small quantum machine with size poly(log  D ) can solve this task with O [[Ëœ]] ( N ) samples, whereas any classical machine<br>exponentially larger size O ( D [[0]] [[.]] [[99]] ) cannot solve the task unless it uses a sample size at least super-polynomial in<br>3. Dimension reduction<br>**----- End of picture text -----**<br>


FIG. 10: **Overview of the dimension reduction task.** We illustrate the dimension reduction task with a particular real-world application scenario in single cell RNA sequencing (scRNA-seq). We conduct RNA sequencing experiments to obtain gene sequences in cell samples, which are represented as feature vectors _âƒ—xii âˆˆ_ R _[[D]]_ (e.g., via frequency counting of _k_ -mer representations). A sample is the feature vector _âƒ—xii_ of a single RNA sequence. A canonical way of dimension reduction is principal component analysis (PCA), which is performed on the high-dimensional data matrix _X âˆˆ_ R _[[N]][Ã—][D]_ and produces a principal component vector _âƒ—w âˆˆ_ R _[[D]]_ that represents the most important feature combination. We obtain the low dimension representation _Î¾_ ( _âƒ—x_ ) of a sample _âƒ—x_ by projecting it onto the principal component _âƒ—w_ . Our results show that a small quantum machine with size poly(log _D_ ) can solve this task with _O_[[Ëœ]] ( _N_ ) samples, whereas any classical machine with exponentially larger size _O_ ( _D_[[0]] _[[.]]_[[99]] ) cannot solve the task unless it uses a sample size at least super-polynomial in _N_ . 

In this section, we consider the fundamental task of dimension reduction in data science and machine learning. We focus on principal component analysis (PCA), the standard method for dimension reduction. For simplicity, we consider the task of reducing the dimension to one. It is straightforward to generalize this to more dimensions. In PCA, we are given a dataset _X_ = ( _âƒ—x_ 1 _, . . . , âƒ—xN_ ) _[T]_ of size _N_ , where each data sample _âƒ—xi âˆˆ_ R _[D]_ is a _D_ - dimensional feature vector and is properly normalized such that _âˆ¥Xâˆ¥â‰¤_ 1. The principal component of this dataset _X_ is a unit vector _âƒ—w âˆˆ_ R _[D]_ , the direction of which explains the most variance of the data. It is the top eigenvector of the covariance matrix _X[T] X âˆˆ_ R _[D][Ã—][D]_ with the largest eigenvalue _Î»_ max = _Ïƒ_ max[2][,][where] _[Ïƒ]_[max] is the largest singular value of _X_ . The principal component _âƒ—w_ provides us with a way to perform dimension reduction on any set of test vector _{âƒ—x[â€²] j[}][m] j_ =1[.][We][reduce][each][test][vector] _[âƒ—x][â€²] j_[to][one][dimension][by][projecting][it][to] the direction of _âƒ—w_ : 

**==> picture [332 x 21] intentionally omitted <==**

We call _Î¾_ ( _âƒ—x[â€²] j_[)][the][one-dimensional][(1] _[D]_[)][representation][of][the][test][vector] _[ âƒ—x][â€²] j_[.][The][goal][of][dimension][reduction][is] to find the 1D representation _Î¾_ ( _âƒ—x[â€²] j_[)][of][any][test][vector] _[âƒ—x][â€²] j_[,][given][the][dataset] _[X]_[.] It is often the case that we can obtain a good initial guess _âƒ—g âˆˆ_ R _[D] , âˆ¥âƒ—gâˆ¥_ 2 = 1 _,_ of the principal component. We call this initial guess _âƒ—g_ the guiding vector. The quality of a guiding vector _âƒ—g_ is given by the overlap between _âƒ—g_ and the true principal component _âƒ—w_ : 

**==> picture [255 x 11] intentionally omitted <==**

and a good guiding vector should have a large overlap with the principal component, as compared to a random vector that has overlap _âˆ¼_ 1 _/âˆšD_ . For example, when there is a prominent feature in the dataset, the corresponding basis vector is usually a good guiding vector. Another way to obtain a good guiding vector, is to first conduct a small-scale PCA on a sub-sampled dataset, and use the resulting principal component as the guiding vector for the full PCA. 

We characterize the tractability of the dimension reduction task by three parameters: the sparsity _s_ , the spectral gap âˆ†, and the quality _Ï‡_ of the guiding vector _âƒ—g_ defined below. The sparsity _s_ is the maximal number of non-zero elements in _X_ per row or column, which bounds the number of non-zero features per sample and the number of samples each feature is presented in. Such sparsity appears in many natural datasets (e.g., natural 

135 

language data with common words trimmed off.) The spectral gap âˆ†is the gap between the largest eigenvalue _Î»_ max( _X[T] X_ ) of _X[T] X_ and the second largest eigenvalue _Î»_ sec( _X[T] X_ ) 

**==> picture [360 x 13] intentionally omitted <==**

where _Ïƒ_ max( _X_ ) _, Ïƒ_ sec( _X_ ) are the largest and second largest singular values of _X_ . âˆ†captures the gap between the signal (the principal component) and the noise (the other singular vectors) in the data. A large gap means a distinguishable signal in the data. This corresponds to the spike in the spiked covariance model, a standard model for the covariance structure of high-dimensional data [183]. Under the power law distribution of eigenvalues usually seen in realistic datasets [81], with the normalization _âˆ¥Xâˆ¥_ = 1, the gap is a constant 1 _âˆ’_ 2 _[âˆ’][Î±]_ = _O_ (1), where _Î±_ is the exponent in the power law. Even when the spectrum is indeed continuous, the parameter âˆ† serves as a cutoff scale at which we wish to distinguish the principal component from competing modes. Our algorithm will return a vector _âƒ—w_ that is a linear combination of all singular vectors that have singular values close to the principal component within âˆ†. These singular vectors are roughly equally well up to precision âˆ†. Hence this is sufficient for the purpose of dimension reduction. The quality of the guiding vector _Ï‡_ represents how good our initial guess is. We define the quality parameter _Ï‡_ by 

**==> picture [294 x 25] intentionally omitted <==**

where _Ï‡_ = 0 means that the guiding vector is no better than a random guess, and _Ï‡_ = 1 means that the guiding vector already has constant overlap with the principal component. We assume that _Ï‡_ = Î˜(1) is a constant. 

We focus on the regime where the number of samples _N_ and feature dimension _D_ are very large, and yet the dimension reduction task remains sparse, gapped, and well-guided: 

**==> picture [406 x 25] intentionally omitted <==**

Note that we always have _D_ = Î˜([Ëœ] _N_ ) when the sparsity _s â‰¤_ poly(log _N,_ log _D_ ). 

## _a. Problem formulation_ 

Now we formally define our data processing task of dimension reduction, summarized in Theorems F.19 and F.20. In particular, we specify the data generation process and the goal of the task. We assume that a guiding vector _âƒ—g_ with quality _Ï‡_ is known to us and the state _|gâŸ©_ can be prepared in poly(log _D_ ) time (e.g., say it is sparse and we can directly prepare the state _|gâŸ©_ ). We consider a data generation process where we randomly get a sparse feature vector ( _i, âƒ—xi_ ) from the sparse feature matrix _X_ . The components of _âƒ—xi_ are specified by bitstrings of length _b_ = poly(log _N,_ log _D_ ) to sufficient accuracy. For simplicity, we assume that this binary representation is exact and use _âƒ—xi_ to stand for the corresponding values. 

Specifically, we consider any hierarchical data generation process _D_ DR( _X_ ) with bounded repetition number _R_ that generates data samples of the form 

**==> picture [322 x 15] intentionally omitted <==**

where _âƒ—xi_ is a random entry of feature vector in the feature matrix _X_ . Recall that the repetition number _R_ characterize the correlation in the data, and is defined as 

**==> picture [316 x 15] intentionally omitted <==**

where _Nz_ =[ï¿½] _[Ï„] i_ =1 _[Î´][z] i[,z]_[is][the][number][of][repeating] _[z]_[â€™s][in][a][refreshing][block][of][data][and] _[Ï„]_[is][refreshing][time][that] bounds the correlation time scale. The specific way of sampling these data can be arbitrary as long as it satisfies the above form. Our results generalize straightforwardly to the more demanding scenario, where we only get a random non-zero subset of the feature vector _âƒ—xi_ . 

Next, we specify the goal of the dimension reduction task. We aim to estimate the 1D representation _Î¾_ ( _âƒ—x[â€²] j_[)] of all possible sparse test vectors _âƒ—x[â€²] j[, j]_[= 1] _[, . . . , m]_[that][are][properly][normalized] _[âˆ¥][âƒ—x][â€²] j[âˆ¥][âˆž][â‰¤]_[1.][In][other][words,][we] want to estimate the 1D representation 

**==> picture [332 x 20] intentionally omitted <==**

for any _s_ -sparse test vector _âƒ—x[â€²] j_[.] 

136 

This motivates our following definition of the dimension reduction task. 

**Task F.19** (Dimension reduction task) **.** _Let N, D, R be integers and Ïµ âˆˆ_ (0 _,_ 1] _. The dimension reduction task is to estimate the 1D representation_ 

**==> picture [317 x 21] intentionally omitted <==**

_of any_ poly(log _N,_ log _D_ ) _-sparse test vector âƒ—x[â€²] j[in a test set][ {][âƒ—x][â€²] j[}][m] j_ =1 _[of any size][ m][ to][ Ïµ][ additive error, using] data samples from any data generation process D_ DR( _X_ ) _defined above with repetition number at most R that corresponds to the normalized data matrix X âˆˆ_ R _[N][Ã—][D] , âˆ¥Xâˆ¥â‰¤_ 1 _, which has_ poly(log _N,_ log _D_ ) _sparsity and_ 1 _/_ poly(log _N,_ log _D_ ) _gap, given a guiding vector âƒ—g with quality Ï‡ âˆˆ_ [0 _,_ 1] _._ 

We also consider the dynamic scenario where we have correlated data with time-varying features. That means the data matrix _X_ changes over time, but the 1D representations _Î¾_ ( _âƒ—x[â€²] j_[)][of][the][test][vectors] _[âƒ—x][â€²] j_[remain] approximately the same. One can also think of this as having a time-varying data matrix _X_ with its principal component roughly fixed. This resembles the batch processing strategy common in modern large-scale data mining, where we analyze the data on batches of data that are different but the desired 1D representations are fixed. We use _{Î¾j}[m] j_ =1[to][denote][that][fixed][set][of][1D][representations][of][the][test][vectors] _[âƒ—x][â€²] j_[.][We][consider] any hierarchical data generation process _D_ DDR( _{_ ( _âƒ—x[â€²] j[, Î¾][j]_[)] _[}] j[m]_ =1[) with bounded repetition number] _[ R]_[ and refreshing] time _Ï„_ of the form 

**==> picture [375 x 16] intentionally omitted <==**

In other words, the data matrix _X_ changes every _Ï„_ time steps, and we keep getting random feature vectors of the current training dataset. We require all data matrices _X_ sampled from _D{_[0] ( _âƒ—x[â€²] j[,Î¾][j]_[)] _[}] j[m]_ =1 _[,Ïµ]_[to][have][poly(log] _[ N,]_[ log] _[ D]_[)] sparsity, at least 1 _/_ poly(log _N,_ log _D_ ) gap, and give roughly the same 1D representations: 

**==> picture [336 x 20] intentionally omitted <==**

We also assume that the guiding vector _âƒ—g_ has quality at least _Ï‡_ with respect to all data matrices _X_ . The specific way that _D{_[0] ( _âƒ—x[â€²] j[,Î¾][j]_[)] _[}][m] j_ =1 _[,Ïµ]_[samples][the][data][matrix] _[X]_[can][be][arbitrary][as][long][as][it][satisfies][the][above] requirements. Formally, we define the dynamic dimension reduction task as follows. 

**Task F.20** (Dynamic dimension reduction task) **.** _Let N, D, R, Ï„ be integers and Ïµ âˆˆ_ (0 _,_ 1] _. The dynamic dimension reduction task is to estimate the underlying 1D representation Î¾j of any_ poly(log _N,_ log _D_ ) _- sparse test vector âƒ—x[â€²] j[in][a][test][set][{][âƒ—x][â€²] j[}][m] j_ =1 _[of][any][size][m][to]_[2] _[Ïµ][error][using][data][samples][from][any] D_ DDR( _{_ ( _âƒ—x[â€²] j[, Î¾][j]_[)] _[}][m] j_ =1 _[, Ïµ]_[)] _[defined][above][with][repetition][number][at][most][R][and][refreshing][time][Ï„][,][given][a] guiding vector âƒ—g with quality at least Ï‡ âˆˆ_ [0 _,_ 1] _._ 

In the following, we first state our main results on quantum advantage in dimension reduction. Then we prove the quantum easiness and classical hardness in subsequent sections. 

## _b. Main results_ 

Our first result shows that given the same amount of samples, a small quantum machine can solve the dimension reduction task better than an exponentially larger classical machine. Moreover, the better the quality of the guiding vector is, the larger the quantum advantage is. This means that using a quantum machine, we can build a better model with exponentially smaller size, as long as there is a guiding vector slightly better than random guessing. Note that the scaling _D_[(1] _[âˆ’][Î¶]_[)] _[Ï‡]_ is effectively _D[Ï‡]_ since it holds for any constant _Î¶ >_ 0. 

**Theorem F.21** (Quantum advantage in dimension reduction) **.** _Consider the dimension reduction task with sample dimension N , feature dimension D, repetition number R, and guiding vector quality Ï‡ âˆˆ_ (0 _,_ 1] _defined in Theorem F.19. Using O_[Ëœ] ( _RND_[1] _[âˆ’][Ï‡]_ ) _samples, a quantum machine with_ poly(log _D_ ) _size can solve it with_ 1 _/_ poly(log( _D_ )) _error and high success probability, while any classical machine with o_ ( _D_[(1] _[âˆ’][Î¶]_[)] _[Ï‡]_ ) _size for any constant Î¶ >_ 0 _cannot solve it with_ 1 _/_ poly(log( _D_ )) _error and success probability more than_ 0 _._ 67 _. Moreover, the data processing time per sample of the quantum machine is_ poly(log _D_ ) _._ 

137 

The second result shows that if the size of the classical machine is slightly smaller than _o_ ( _D_[2] _[Ï‡][âˆ’]_[1] ), it would need super-polynomially more samples than a small quantum machine to solve the dynamic dimension reduction task. This separation starts as soon as we have a guiding state of quality _Ï‡ >_ 1 _/_ 2 (i.e., _âƒ—g Â· âƒ—w â‰¥_ â„¦(1[Ëœ] _/D_[1] _[/]_[4] )). In the context of batch processing, this means that quantum machines can solve the task with a few batches of training data, whereas sub-exponential size classical machines require super-polynomially many batches. 

**Theorem F.22** (Quantum advantage in dynamic dimension reduction) **.** _Consider the dynamic dimension reduction task with sample dimension N , feature dimension D, repetition number R, guiding vector quality Ï‡ âˆˆ_ (1 _/_ 2 _,_ 1] _, and sufficient refreshing time Ï„_ = _O_[Ëœ] ( _RND_[1] _[âˆ’][Ï‡]_ ) _defined in Theorem F.20. A quantum machine with_ poly(log _D_ ) _size can use O_[Ëœ] ( _RND_[1] _[âˆ’][Ï‡]_ ) _samples to solve it with_ 1 _/_ poly(log( _D_ )) _error and high success probability, while any classical machine with o_ ( _D_[(1] _[âˆ’][Î¶]_[)(2] _[Ï‡][âˆ’]_[1)] ) _size for any constant Î¶ >_ 0 _that solves it with_ 1 _/_ poly(log( _D_ )) _error and probability at least_ 2 _/_ 3 _must collect at least RN[Ï‰]_[(1)] _samples. Moreover, the data processing time per sample of the quantum machine is_ poly(log _D_ ) _._ 

Together, Theorems F.21 and F.22 establish unconditional and exponential quantum advantages in the foundational task of dimension reduction. 

## _c. Quantum algorithm_ 

Here, we prove the quantum algorithm parts of Theorems F.21 and F.22. We construct an algorithm that performs high-dimensional PCA on a small quantum computer. We do so by combining quantum oracle sketching (Theorem D.16), quantum state sketching (Theorem D.24), and a ground state preparation algorithm [84]. We again use the interferometric classical shadow developed in the last section (Theorem F.16) to readout the principal component _|wâŸ©_ into a classical representation, which is used for predicting the 1D representations of all possible test vectors. 

**Theorem F.23** (Dimension reduction with quantum oracle sketching) **.** _Let N, D be large integers, Ïµ, Î´ âˆˆ_ (0 _,_ 1) _, and Ï‡ âˆˆ_ [0 _,_ 1] _be the quality parameter. Let X_ = ( _âƒ—x_ 1 _, . . . , âƒ—xN_ ) _âˆˆ_ R _[N][Ã—][D] be a dataset matrix that is s-sparse with norm âˆ¥Xâˆ¥â‰¤_ 1 _and gap_ âˆ†= _Î»_ max( _X[T] X_ ) _âˆ’ Î»_ sec( _X[T] X_ ) _. Consider a set of s-sparse test vectors {âƒ—x[â€²] j[}][m] j_ =1 _[,][ âˆ¥][âƒ—x][â€²] j[âˆ¥][âˆž][â‰¤]_[1] _[,][of][any][size][m][.][There][exists][a][quantum][algorithm][that][can] output an Ïµ-approximate estimate Î¾_[Ë†] _j of the 1D representation_ 

**==> picture [453 x 92] intentionally omitted <==**

**==> picture [453 x 59] intentionally omitted <==**

**==> picture [311 x 13] intentionally omitted <==**

**==> picture [442 x 13] intentionally omitted <==**

We note that Theorem F.23 immediately implies the quantum algorithm part of Theorem F.21 by definition ofËœ the dimension reduction task.Ëœ It also proves the quantum algorithm part of Theorem F.22 by taking _Ï„_ = _O_ ( _RND_[1] _[âˆ’][Ï‡]_ ) larger than _M_ = _O_ ( _RND_[1] _[âˆ’][Ï‡]_ ) and noting that 

**==> picture [215 x 14] intentionally omitted <==**

with probability at least 1 _âˆ’ Î´_ , as required. 

138 

We use the following quantum ground state preparation algorithm as the backbone of our quantum algorithm and instantiate the oracle queries with quantum oracle sketching. We note that for coherent usage, the failure probability originally stated in [84] is absorbed into the error parameter _Ïµ_ by replacing standard amplitude amplification with fixed-point amplitude amplification. We bound the error in 2-norm to avoid ambiguity in the global phase. 

**Lemma F.24** (Quantum ground state preparation [84, Corollary 9]) **.** _Let D be a large integer. Let H âˆˆ_ R _[D][Ã—][D] be a real, symmetric matrix with the smallest eigenvalue Î»_ 1 _and corresponding unit eigenvector âƒ—w âˆˆ_ R _[D] and second smallest eigenvalue Î»_ 2 _such that Î»_ 2 _âˆ’ Î»_ 1 _â‰¥_ âˆ† _. Let âƒ—g âˆˆ_ R _[D] be a unit vector such that âƒ—g Â· âƒ—w â‰¥ q. There exists a quantum algorithm that applies a unitary V such that_ 

**==> picture [311 x 13] intentionally omitted <==**

_using S_ = _O_ (log( _D_ )+log(1 _/q_ )) _qubits, O_[Ëœ] ï¿½ _q_ 1âˆ†[log(1] _[/Ïµ]_[)] ï¿½ _gates, and O_[Ëœ] ï¿½ _q_ 1âˆ†[log(1] _[/Ïµ]_[)] ï¿½ _queries to the block encoding of H and the state preparation unitary of |gâŸ© and their inverse and controlled versions._ 

Recall that in Theorem D.23, we have shown that _O_[Ëœ] ( _RNs_[5] ) samples suffice to implement the block encoding of an _s_ -sparse matrix. In addition, Theorem D.24 shows that we can use _O_[Ëœ] ( _RN_ ) samples to prepare the quantum state of any vector. We combine Theorem F.24 with Theorem D.23, Theorem D.24, and interferometric classical shadow (Theorem F.16) to prove Theorem F.23. 

_Proof of Theorem F.23._ Let _n_ = _âŒˆ_ log2(max( _N, D_ )) _âŒ‰â‰¤_ min _{O_ (log( _sD_ )) _, O_ (log( _sN_ )) _}_ and embed _X_ into 2 _[n]_ dimension to apply quantum oracle and state sketching. We define _H_ = _âˆ’X[T] X âˆˆ_ R _[D][Ã—][D]_ , which is real and symmetric. The smallest eigenvalue of _H_ corresponds to the largest singular value of _X_ , and therefore the ground state of _H_ is indeed the principal component _âƒ—w_ of _X_ . The gap between the smallest and second smallest eigenvalues of _H_ is âˆ†by definition. The block encoding of _H_ can be implemented with two queries to the block encoding of _X_ and its inverse. We use _q_ = _âƒ—g Â· âƒ—w â‰¥_ â„¦(1[Ëœ] _/D_[(1] _[âˆ’][Ï‡]_[)] _[/]_[2] ) to denote the overlap between the guiding state _âƒ—g_ and the principal component _âƒ—w_ . 

Theorem F.24 states that there is a quantum ground state preparation algorithm, which is a unitary _V_ that prepares the state _|wâŸ©_ with _Ïµ[â€²] /_ 2 error using _O_ ( _n_ + log(1 _/q_ )) = _O_ ( _n_ + (1 _âˆ’ Ï‡_ ) log( _D_ )) qubits and 

**==> picture [354 x 26] intentionally omitted <==**

queries to the block encoding of _X_ and the state preparation unitary of _|gâŸ©_ and their inverse and controlled versions. By replacing all gates and queries in _V_ with their controlled versions, we obtain a controlled state preparation unitary _cV_ that prepares _|wâŸ©_ with error _Ïµ[â€²] /_ 2. 

Similar to the proof of Theorems F.5 and F.13, our proof of Theorem F.23 proceeds in two steps. We first use this quantum ground state preparation algorithm to construct a query algorithm that can estimate the 1D representation _Î¾_ ( _âƒ—x[â€²] j_[)][to] _[Ïµ]_[error][for][any] _[j][âˆˆ]_[[] _[m]_[]][with][probability][at][least][1] _[ âˆ’][Î´/]_[2.][Then,][we][instantiate][the] queries with quantum oracle and state sketching. The instantiation error is chosen to be _Î´/_ 2 such that the total variation distance error on the final estimate is _Î´/_ 2. This immediately implies that the final prediction is _Ïµ_ -accurate with probability at least 1 _âˆ’ Î´/_ 2 _âˆ’ Î´/_ 2 = 1 _âˆ’ Î´_ . 

As the first step, we construct the query algorithm that estimates the 1D representation. The quantum ground state preparation algorithm gives us a controlled state preparation unitary _cV_ that prepares _|wâŸ©_ to _Ïµ[â€²] /_ 2 using _O_ ( _n_ + (1 _âˆ’ Ï‡_ ) log( _D_ )) qubits and _Q_ 0 queries to _X_ and _|gâŸ©_ . To readout the weight vector well enough that we can predict any _s_ -sparse test vector _âƒ—x[â€²] j_[,][we][imagine][that][we][have][an] _[Ïµ]_[0][-covering][net] _[N]_[over][the][set] 

**==> picture [332 x 12] intentionally omitted <==**

in _âˆ¥Â· âˆ¥_ 2. Note that this covering net is only a analysis tool and it is not used in the algorithm. The covering net has size 

**==> picture [326 x 27] intentionally omitted <==**

We run interferometric classical shadow (Theorem F.16) using the controlled state preparation unitary _cV_ with the test states _|x[â€²] âŸ©_ , _âƒ—x[â€²] âˆˆN_ , error _Ïµ_ 0, and success probability _Î´/_ 2. This consumes 

**==> picture [347 x 25] intentionally omitted <==**

139 

queries to _cV_ and guarantees that the prediction of the overlap is _Ïµ_ 0 accurate on the _Ïµ_ 0-covering net _N_ of _X_ test. By continuity, this implies that the prediction of the overlap is _E_ 0 = _O_ ( _Ïµ_ 0) accurate on the whole set _X_ test (see e.g., [175, Exercise 4.4.3]). We choose _Ïµ_ 0 such that _Ïµ[â€²] /_ 2 = _E_ 0 = _O_ ( _Ïµ_ 0). Combining the error of the state preparation unitary, we know that the produced estimator _o_ Ë†( _âƒ—x[â€²]_ ) is an _E_ 0 + _Ïµ[â€²] /_ 2 = _Ïµ[â€²]_ accurate estimate of _âŸ¨x[â€²] |wâŸ©_ for all _âƒ—x[â€²] âˆˆX_ test. Meanwhile, if the size of test vectors _m_ is small, then _O_ (log( _m/Î´_ ) _/Ïµ[â€²]_[2] ) queries suffice. Hence, with 

**==> picture [336 x 25] intentionally omitted <==**

queries to _cV_ , we can produce an estimator _o_ Ë†( _âƒ—x[â€²] j_[)][satisfying] 

**==> picture [289 x 13] intentionally omitted <==**

for any _j âˆˆ_ [ _m_ ] with probability at least 1 _âˆ’ Î´/_ 2. Furthermore, the 1D representation is given by 

**==> picture [312 x 14] intentionally omitted <==**

Therefore, we calculate and output the final estimator 

**==> picture [282 x 15] intentionally omitted <==**

which satisfies 

**==> picture [372 x 15] intentionally omitted <==**

where we have chosen _Ïµ[â€²]_ = _Ïµ/[âˆš] s_ and used the fact that _âƒ—x[â€²] j_[is] _[s]_[-sparse][and][hence] _[âˆ¥][âƒ—x][â€²] j[âˆ¥]_[2] _[â‰¤]_ ï¿½ _sâˆ¥âƒ—x[â€²] j[âˆ¥][âˆž][â‰¤âˆš] s_ . This gives us the desired quantum query algorithm that makes 

**==> picture [364 x 54] intentionally omitted <==**

queries to _X_ and can output the _Ïµ_ -error prediction _Î¾_[Ë†] _j, âˆ€j âˆˆ_ [ _m_ ] (a classical random variable) with probability at least 1 _âˆ’ Î´/_ 2. Moreover, the space complexity is 

**==> picture [469 x 48] intentionally omitted <==**

where the first term comes from the ground state preparation algorithm, the second comes from the classical shadow data, and the third one comes from classical simulation of Clifford circuits. 

The second step is to instantiate the queries to _X_ in the query algorithm using quantum oracle sketching. We first replace all queries to the block encoding of _X_ and its inverse and controlled versions to their _Ïµ_ 1-approximate versions in Theorem D.23. This incurs an error of _E_ 1 = _QÏµ_ 1 = _Î´/_ 4, where we set _Ïµ_ 1 = _Î´/_ (4 _Q_ ). 

Next, we replace the queries to _Ïµ_ 1-approximate versions of block encoding of _X_ and its inverse and controlled versions by the random unitary channel that we build from samples in Theorem D.23. This incurs an additional error of _E_ 2 = _QÏµ_ 1 = _Î´/_ 4, and uses _O_ ( _n_ + _b_ + log[2] _[.]_[5] (1 _/Ïµ_ 1)) = _O_ ( _n_ + _b_ + log[2] _[.]_[5] ( _Q/Î´_ )) qubits and 

**==> picture [388 x 60] intentionally omitted <==**

samples from the data generation process. 

According to Theorem D.17, the total error in instantiating the query algorithm is bounded by 

**==> picture [296 x 11] intentionally omitted <==**

140 

This means that the output of the query-instantiated quantum algorithm, which is a classical random variable must be correct with probability at least 1 _âˆ’ Î´/_ 2 _âˆ’ Î´/_ 2 = 1 _âˆ’ Î´_ . The total number of qubits used is 

**==> picture [409 x 36] intentionally omitted <==**

The total number of samples is 

**==> picture [354 x 26] intentionally omitted <==**

This completes the proof of Theorem F.23. 

## _d. Classical hardness_ 

In this section, we prove the two classical hardness results in Theorems F.21 and F.22. We will construct a (dynamic) dimension reduction task with _N_ = _D_ . Hence, for simplicity, we will use _N_ alone throughout this section. We prove the classical hardness results by constructing a specific dimension reduction task using Theorem E.48. Solving it amounts to solving the (dynamic) Noisy Oracle Property Estimation (NOPE) task defined in Section E (Theorems E.1 and E.26), whose classical hardness we have already proved in Theorem E.29 and Theorem E.28. 

This gives us two classical hardness results. The first result (Theorem F.26) follows from the distributional sample-space lower bound of NOPE (Theorem E.29) and shows that any classical learning algorithm that wants to achieve success probability 0 _._ 67 in dimension reduction with the same number of samples quantum algorithms need must have â„¦( _D_[(1] _[âˆ’][Î¶]_[)] _[Ï‡]_ ) size for any constant _Î¶ >_ 0. The second result (Theorem F.25) follows from Theorem E.28 and shows that when the dimension reduction task is dynamic, any classical learning algorithm will need a number of samples super-polynomial in _N_ if it has size _o_ ( _D_[(1] _[âˆ’][Î¶]_[)(2] _[Ï‡][âˆ’]_[1)] ) for any constant _Î¶ >_ 0. The dynamic result follows a similar reasoning as the linear system and binary classification case. We therefore prove it first. The non-dynamic result requires a slight modification, which we will detail at the end of this section. 

The general idea of proving these results is to embed the quantum circuit that solves dynamic NOPE from Theorem E.45 into a dimension reduction task via Theorem E.48. The 1D representation _Î¾_ ( _âƒ—x_ ) of a fixed, sparse test vector _âƒ—x_ encodes the oracle property _B âˆˆ{_ 0 _,_ 1 _}_ that we want to estimate in (dynamic) NOPE. Then we show that given any classical algorithm that solves the dimension reduction task, we can use it to construct a classical algorithm that solves (dynamic) NOPE. In the (dynamic) NOPE task, we take the oracle property function _f_ to be _K_ -Forrelation (Theorem E.38) and the noisy encoding function _g_ to be the inner product (Theorem E.41). 

In the following, we construct the data generation process _D_ DR _[N,K,R]_ ( _B_ ) _, B âˆˆ{_ 0 _,_ 1 _}_ for dimension reduction, where _N_ is both the sample dimension and the feature dimension (i.e., _D_ = _N_ ), _K_ = Î˜(1) is the constant in the Forrelation that we will embed, _R_ is an integer that specifies the repetition number, and _B_ indicates whether the 1D representation of that fixed test vector has a large or small value (see Theorem E.48). The goal is to solve for _B_ . It helps to compare this construction to the dynamic NOPE data generation process defined in Section E 4. 

Given _N_ , we define another large integer _N[â€²]_ as follows. Let _T_ = Î˜(log[3] _N[â€²]_ log log _N[â€²]_ ) be the total number of two-qubit gates and diagonal gates given in Theorem E.45 and let _n[â€²]_ = log _N[â€²]_ + _O_ (log log _N[â€²]_ ) be the number of qubits in Theorem E.45. To properly embed that circuit into the _N_ -dimensional training dataset, we define _N[â€²]_ such that _N_ = ( _T_ + 1)2 _[n][â€²]_[+1] = _N[â€²] Â·_ polylog _N[â€²]_ as in Theorem E.48. This implies _N[â€²]_ = _N/_ polylog _N_ . The resulting data matrix _X_ have sparsity _s_ = _O_ (1) and gap âˆ† _â‰¥_ â„¦(1 _/T_[3] ) = â„¦(1[Ëœ] _/_ log[9] _N[â€²]_ ) from Theorem E.48. We fix the guiding vector to be the _âƒ—g_ in Theorem E.48 that has overlap _âƒ—g Â· âƒ—w_ = 1 _/âˆšT_ + 1 = â„¦(1 _/_ polylog( _N_ )), which means that it already has maximal quality _Ï‡_ = 1. Hence this guiding vector has quality at least _Ï‡_ for any _Ï‡ âˆˆ_ [0 _,_ 1]. Let _L_ = ï¿½log[2] ( _KN[â€²]_ )ï¿½ _â‰¥_ 5 be the number of independent oracle instances that we have in dynamic NOPE. 

Now we define the data generation process 

**==> picture [385 x 15] intentionally omitted <==**

where _T_ 3 = _R_ , _T_ 2 = _KN[â€²]_ , _T_ 1 = _âŒˆMQ/_ ( _T_ 2 _T_ 3) _âŒ‰_ = ( _KN[â€²]_ )[1] _[âˆ’][Ï‡]_ polylog( _KN[â€²]_ ), _MQ_ = _RND_[1] _[âˆ’][Ï‡]_ polylog( _N_ ) is the number of samples quantum machines need in Theorem F.23, _X âˆˆ_ R _[N][Ã—][N]_ is an _N_ -dimensional, symmetric, _O_ (1)-sparse feature matrix with gap âˆ† _â‰¥_ â„¦(1[Ëœ] _/_ log[9] _N_ ), _Î± âˆˆ{_ 0 _,_ 1 _}, Î² âˆˆ_ [ _L_ ] label which part of the matrix _X_ 

141 

that we are currently collecting data from, and _i âˆˆ_ [ _N_ ] labels the _i_ -th training data point _âƒ—xi_ (the _i_ -th row of the matrix _X_ ). 

The data are sampled in the following way that resembles dynamic NOPE in Section E 4. _DB_[0][samples][a] length- _L_ bitstring _Î³_ with parity 

**==> picture [267 x 31] intentionally omitted <==**

uniformly random. For each _j âˆˆ_ [ _L_ ], we sample a random oracle _oj âˆ¼ pÎ³j_ , where _p_ 0 _, p_ 1 are the distributions of Forrelation defined in Theorem E.39. Then we sample a noisy encoding pair ( _Y_[(0] _[,j]_[)] _, Y_[(1] _[,j]_[)] ) _âˆ¼_ Uniform(( _g[N]_ ) _[âˆ’]_[1] ( _oj_ )) using the inner product noisy encoding function _g_ defined in Theorem E.41. Next, note that ( _Y_[(0] _[,j]_[)] _, Y_[(1] _[,j]_[)] ) _[L] j_ =1[specifies][an] _[n][â€²]_[-qubit][quantum][circuit] _[C]_[with] _[T]_[=] _[O]_[(log][3] _[ N][ â€²]_[ log log] _[ N][ â€²]_[)] gates via Theorem E.45, and the quantum circuit _C_ gives a data matrix _X_ with dimension ( _T_ + 1)2 _[n][â€²]_[+1] = _N_ via Theorem E.48. Here, _X_ is indeed _O_ (1)-sparse with gap âˆ† _â‰¥_ â„¦(1[Ëœ] _/_ log[9] _N_ ). Now we define _DX_[1][.][We][first] sample a uniformly coordinate _Î² âˆ¼_ Uniform([ _L_ ]) and a random bit _Î± âˆ¼_ Bern(1 _/_ 2) as in dynamic NOPE. Then we pick out _Y_[(] _[Î±,Î²]_[)] and use it to generate the data samples. 

In particular, we define _D_ ([2] _Î±,Î²_ )[in the following way.][We first sample a random row of the matrix] _[ X]_[as follows.] Note that the linear space in which the matrix _X_ lives factorizes as _|tâŸ©|ÏˆâŸ©_ where _|tâŸ©_ is the clock register and _|ÏˆâŸ©_ is the ( _n[â€²]_ +1)-qubit register that the realified quantum circuit runs on. We sample a clock time _t âˆ¼_ Uniform([ _T_ ]) and the matrix is reduced to a specific gate in the ( _n[â€²]_ + 1)-qubit subspace (either a fixed two qubit gate or a diagonal gate that depends on _Y_[(] _[Î±,Î²]_[)] ). The remaining subspace further factorizes into _|x, Î±, Î², kâŸ©_ and the rest of the working qubits. We sample a random basis of this ( _n[â€²]_ + 1)-qubit subspace by plug in the specific ( _Î±, Î²_ ) that we have already sampled, sample _x âˆ¼_ Uniform([ _KN[â€²]_ ]) _, k âˆ¼_ Uniform([ _b_ ]), and sample a computational basis of the rest of the working qubits uniformly random. This together specifies and thus samples a row _i_ of the matrix _X_ . Note that the marginal distribution of _i_ is uniform over [ _N_ ] (because _Î±, Î²_ are sampled uniformly), though there are correlations between consecutive samples of _i_ since they share the same set of ( _Î±, Î²_ ). 

Note that by construction of the matrix _X_ as in Theorem E.48, the picked out row vector _âƒ—xi_ is _O_ (1) sparse, and has components that is the real or imaginary part of either 1, from the identity matrices in Theorem E.48, or a matrix element of a fixed two qubit gates, or ( _âˆ’_ 1)[(] _[Y] x_[(] _[Î±,Î²]_[)] ) _k_ which is solely specified by _Y_ ( _Î±,Î²_ ). This gives us the sample _z_ = ( _i, âƒ—xi_ ) and we repeat this sample _T_ 3 times, completing the data generation process. 

This data generation process _D_ DR _[N,K,R]_ is a valid data generation process of dynamic dimension reduction. It produces a random row sample uniformly distributed over the rows of _X_ . The test vector is a single fixed _O_ (1)-sparse vector _âƒ—x[â€²]_ specified in Theorem E.48, which satisfies 

**==> picture [361 x 25] intentionally omitted <==**

where _qB_ is the probability of measuring 0 on the embedded circuit given by Theorem E.45 when the underlying oracle property is _B_ . Theorem E.45 ensures that the other qubits in the circuit are indeed in _|_ 0 _âŸ©_ at the end and that _q_ 1 _â‰¤_ 0 _._ 1 _, q_ 0 _â‰¥_ 0 _._ 9. The quality of the guiding vector _âƒ—g_ given in Theorem E.48 is maximal ( _Ï‡_ = 1) and hence is indeed at least _Ï‡_ for any _Ï‡ âˆˆ_ [0 _,_ 1]. The repetition number of the data generation process is upper bounded by _T_ 2 _T_ 3 _/_ ( _KN[â€²]_ ) = _R_ , because the sampling step of _DX_[1] _[â†’][Ã—][T]_[1] _[D]_ ([2] _Î±,Î²_ )[is][independent.][The][refreshing] time is _Ï„_ = _T_ 1 _T_ 2 _T_ 3 = _O_ ( _MQ_ ) = _O_[Ëœ] ( _RND_[1] _[âˆ’][Ï‡]_ ), satisfying the requirements in Theorems F.21 and F.22. 

This data generation process for dimension reduction _D_ DR _[N,K,R]_ ( _B_ ) is designed to reduce to the dynamic NOPE data _Dg,f[KN][â€²][,T]_[1] ( _B_ ) in Section E 4 via Theorems E.45 and E.48. Using this data generation process, we prove the following result. 

**Theorem F.25** (Classical hardness of dynamic dimension reduction) **.** _Let Î¶ >_ 0 _be any constant. Let N, D be the sample and feature dimension of a dimension reduction task and R, Ï„_ = _O_[Ëœ] ( _RND_[1] _[âˆ’][Ï‡]_ ) _be its repetition number and refreshing time. Given a guiding vector of constant quality at least Ï‡ >_ 1 _/_ 2 _, any randomized classical learning algorithm that solves the task with error Ïµ_ = Î˜(1 _/_ log[2] ( _N_ )) _and success probability at least_ 2 _/_ 3 _must have sample complexity_ 

**==> picture [453 x 56] intentionally omitted <==**

142 

Theorem F.25 directly implies the classical hardness part of Theorem F.22. Together with the quantum algorithm result Theorem F.13, this completes the proof of the quantum advantage claim in Theorem F.12. However, to obtain the claim in Theorem F.21 where 2 _Ï‡ âˆ’_ 1 is improved to _Ï‡_ , we need to design a different data generation process based on the distributional sample-space lower bound (Theorem E.29) that we will detail later. 

_Proof of Theorem F.25._ Recall that _N_ = _D_ in the task that we construct. For simplicity, we will use _N_ throughout the proof. We prove Theorem F.25 by showing that given any classical learning algorithm that can estimate the 1D representation _Î¾_ ( _âƒ—x[â€²]_ ) of the test vector _âƒ—x[â€²]_ , we can use it to construct an algorithm that decides _B_ from _Dg,f[KN][â€²][,T]_[1] ( _B_ ), which we have proved to be hard in Theorem E.28. First note that from Theorem E.48, we have that the 1D representation is 

**==> picture [361 x 25] intentionally omitted <==**

where _qB_ is the probability of measuring 0 on the embedded circuit when the underlying oracle property is _B_ . Theorem E.45 ensures that _q_ 1 _â‰¤_ 0 _._ 1 _, q_ 0 _â‰¥_ 0 _._ 9. That means, if we can estimate the 1D representation to _Ïµ_ = Î˜(1 _/_ log[2] ( _N_ )) _â‰¤_ 0 _._ 3 _/âˆšT_ + 1 = Î˜(1[Ëœ] _/_ log[1] _[.]_[5] ( _N_ )) error, we can decide the value of _B âˆˆ{_ 0 _,_ 1 _}_ because 

**==> picture [320 x 24] intentionally omitted <==**

We choose _K_ = ï¿½ _Î¶_ (21 _.Ï‡_ 001 _âˆ’_ 1) ï¿½ such that 

**==> picture [365 x 26] intentionally omitted <==**

For the sake of contradiction, suppose we have a randomized classical learning algorithm _L_ with space complexity 

**==> picture [458 x 26] intentionally omitted <==**

and sample complexity _M_ that given a sequence of data samples drawn from _D_ DR _[N,K,R]_ ( _B_ ), estimates the 1D representation to _Ïµ_ error and hence decides _B_ with probability _p_ succ. In the following, we design a classical learning algorithm _L[â€²]_ that decides _B_ using data from _Dg,f[KN][â€²][,T]_[1] ( _B_ ). 

The first step of _L[â€²]_ is to generate data samples that look like _D_ DR _[N,K,R]_ ( _B_ ) from _Dg,f[KN][â€²][,T]_[1] ( _B_ ). We sample a random row _i âˆˆ_ [ _N_ ] of _X_ using the same sampling procedure as in the definition of _D_ DR _[N,K,R]_ ( _B_ ). To this end, we first sample a clock time _t âˆ¼_ Uniform([ _T_ ]). Now we split into two cases: (1) the sampled clock time _t_ corresponds to a fixed two qubit gate; and (2) _t_ corresponds to a diagonal gate (the oracle). In case (1), we sample a random row of the corresponding gate matrix, which specifies the row _i_ of the matrix _X_ . The corresponding training data vector _âƒ—xi_ is completed determined by the matrix elements of that fixed two-qubit gate, and therefore can be calculated. This generates a sample _z_ DR = ( _i, âƒ—xi_ ) that we will feed into the dimension reduction solver _L_ . In case (2), we draw a sample _z_ = ( _x, Yx_[(] _[Î±,Î²]_[)] _, Î±, Î²_ ) from _Dg,f[KN][â€²][,T]_[1] ( _B_ ). Then we sample a random row of the oracle with given ( _x, Î±, Î²_ ) (i.e., sample _k âˆ¼_ Uniform([ _b_ ]) and output the row _|x, Î±, Î², kâŸ©_ ) and a random basis of the rest of the working qubits. This specifies the row _i_ of the matrix _X_ . We then calculate the corresponding data vector _âƒ—xi_ , which is completely determined by the row of the diagonal gate with the diagonal element ( _âˆ’_ 1)[(] _[Y] x_[(] _[Î±,Î²]_[)] ) _k_ , using that data sample from _Dg,f[KN][â€²][,T]_ 1( _B_ ). This generates a sample _z_ DR = ( _i, âƒ—xi_ ) that we will feed into the dimension reduction solver _L_ . In both cases, we repeat the same _z_ DR _T_ 3 times. Note that this procedure generates data samples that exactly matches _D_ DR _[N,K,R]_ ( _B_ ) by construction. After sampling a training data point _z_ DR = ( _i, âƒ—xi_ ), we feed it into dimension reduction solver _L_ . We repeat this _M_ times so that _L_ receives _M_ samples whose distribution matches that of _D_ DR _[N,K,R]_ ( _B_ ) and produces an estimate of the 1D representation that provides a prediction of _B_ . We use this predicted bit of _L_ as the final output of _L[â€²]_ . 

Note that since the data generation does not require knowledge of the previous data samples from _Dg,f[KN][â€²][,T]_[1] ( _B_ ), it can be performed online and thus the space complexity of _L[â€²]_ is _S[â€²]_ = _S_ . Moreover, the sample complexity of _L[â€²]_ is _M[â€²] â‰¤ M/T_ 3 because we only draw a data sample from _Dg,f[KN][â€²][,T]_[1] ( _B_ ) when case (2) happens and we repeat each data sample _T_ 3 times. The success probability of _L[â€²]_ is _p_ succ, the same as that of _L_ . 

Finally, we invoke Theorem E.28. Note that for the inner product _g_ , we have _Î·_ = 1 _/_ 2, _c_ = (865 _/Î·_[2] ) logï¿½865 _/Î·_[2][ï¿½] = (865 _Ã—_ 4) log(865 _Ã—_ 4) _â‰ˆ_ 40677 _._ 68, and therefore the choice of _b_ = _âŒˆ_ 40678 log( _KN[â€²]_ ) _âŒ‰_ 

143 

satisfies the requirement. For the Forrelation _f_ we use, Theorem E.40 implies that the (1 _/_ 3)-error classical distributional query complexity is (using _K_ = Î˜(1)) 

**==> picture [294 x 26] intentionally omitted <==**

Together with _T_ 1 = _N[â€²]_[1] _[âˆ’][Ï‡]_ polylog( _KN[â€²]_ ), we have 

**==> picture [330 x 26] intentionally omitted <==**

satisfying the condition of Theorem E.28. Therefore, Theorem E.28 implies that 

**==> picture [324 x 13] intentionally omitted <==**

proving Theorem F.25. Together with the quantum algorithm result Theorem F.23, this proves the quantum advantage claim in dynamic dimension reduction (Theorem F.22). 

Finally, we prove the following result that implies the classical hardness part of Theorem F.21. 

**Theorem F.26** (Classical hardness of dimension reduction) **.** _Let Î¶ >_ 0 _be any constant. Let N, D be the sample and feature dimension of a dimension reduction task and R be its repetition number. Given a guiding vector of constant quality Ï‡ âˆˆ_ (0 _,_ 1] _, using O_[Ëœ] ( _RND_[1] _[âˆ’][Ï‡]_ ) _samples, any randomized classical learning algorithm with space complexity_ 

**==> picture [260 x 12] intentionally omitted <==**

_cannot solve the dimension reduction task with error Ïµ_ = Î˜(1 _/_ log[2] ( _N_ )) _and success probability more than_ 0 _._ 67 _._ 

The origin of the difference between the _D[Ï‡]_ exponent and the _D_[2] _[Ï‡][âˆ’]_[1] exponent is as follows. The ground state preparation algorithm has query complexity _Q âˆ¼_ 1 _/_ ( _âƒ—g Â· âƒ—w_ ) _âˆ¼ D_[(1] _[âˆ’][Ï‡]_[)] _[/]_[2] . Due to the quadratic slowdown of quantum oracle sketching (caused by the incoherent random sampling of classical data), we have sample complexity _M âˆ¼ NQ_[2] _âˆ¼ ND_[1] _[âˆ’][Ï‡]_ . The classical sample-space lower bound in Theorem E.29 then provides the classical space lower bound _S_ â‰³ _DQC/M âˆ¼ D Â· N/_ ( _ND_[1] _[âˆ’][Ï‡]_ ) _âˆ¼ D[Ï‡]_ as claimed. This is the intuition behind Theorem F.26. As for the dynamic version (Theorem F.25), the learning XOR lemma (Theorem E.30) incurs an additional _T_ 1 _âˆ¼ M/N âˆ¼ D_[1] _[âˆ’][Ï‡]_ factor in the space lower bound due to interleaving problem instances. This leads to a final space lower bound of _S_ â‰³ _D[Ï‡] /T_ 1 _âˆ¼ D[Ï‡][âˆ’]_[(1] _[âˆ’][Ï‡]_[)] = _D_[2] _[Ï‡][âˆ’]_[1] as in Theorem F.25. 

_Proof of Theorem F.26._ We modify the dynamic data generation process for dimension reduction _D_ DR _[N,K,R]_ ( _B_ ) such that (1) all the _L_ problem instances are the same (i.e., _Î³_ 1 = _Â· Â· Â·_ = _Î³L_ = _Î³_ 0 _âˆˆ{_ 0 _,_ 1 _}_ and _oÎ², Y_[(] _[Î±,Î²]_[)] are the same for different _Î² âˆˆ_ [ _L_ ]) and (2) _L_ is rounded to the smallest odd number. This means that the decision bit 

**==> picture [279 x 31] intentionally omitted <==**

With this modification, the data generation process of the dimension reduction task is reduced to mimic that of the non-dynamic NOPE _Dg,KN[KN][â€²][â€²]_[(] _[o]_[)] _[, o][âˆ¼][p][Î³]_ 0[from][Section][E 1][with][the][Forrelation][property] _[f]_[and][each][sample] repeated _R_ times. We call this new data generation process _D_[Ëœ] DR _[N,K,R]_ ( _B_ ). 

Now we consider the same reduction as in the proof of Theorem F.25. We have that estimating the 1D representation to _Ïµ_ = Î˜(1 _/_ log[2] ( _N_ )) error suffice to determine the value of _B âˆˆ{_ 0 _,_ 1 _}_ and hence _Î³_ 0. We choose _K_ = 1 _._ 001 such that ï¿½ _Î¶Ï‡_ ï¿½ 

**==> picture [335 x 26] intentionally omitted <==**

For the sake of contradiction, suppose we have a randomized classical learning algorithm _L_ with space complexity 

**==> picture [411 x 26] intentionally omitted <==**

144 

and sample complexity _M_ that given a sequence of data samples drawn from the modified _D_[Ëœ] DR _[N,K,R]_ ( _B_ ), estimates the 1D representation to _Ïµ_ error and hence decides _Î³_ 0 _âˆˆ{_ 0 _,_ 1 _}_ with probability _p_ succ _â‰¥_ 0 _._ 67. With the same data reduction detailed in the proof of Theorem F.25, _L_ can be used to construct a classical learning algorithm _L[â€²]_ that decides _Î³_ 0 with probability _p_ succ _â‰¥_ 0 _._ 67 using the same space complexity _S_ and _M[â€²]_ = _M/T_ 3 = _M/R_ data from _Dg,KN[KN][â€²][â€²]_[(] _[o]_[)] _[, o][ âˆ¼][p][Î³]_ 0[.] 

Finally, we invoke Theorem E.29. Note that for the inner product _g_ , we have _Î·_ = 1 _/_ 2, _c_ = (865 _/Î·_[2] ) logï¿½865 _/Î·_[2][ï¿½] = (865 _Ã—_ 4) log(865 _Ã—_ 4) _â‰ˆ_ 40677 _._ 68, and therefore the choice of _b_ = _âŒˆ_ 40678 log( _KN[â€²]_ ) _âŒ‰_ satisfies the requirement. For the Forrelation _f_ we use, Theorem E.40 implies that the (1 _/_ 3)-error classical distributional query complexity is (using _K_ = Î˜(1)) 

**==> picture [294 x 26] intentionally omitted <==**

Meanwhile, the success probability satisfies 

**==> picture [345 x 13] intentionally omitted <==**

for large enough _N[â€²]_ , satisfying the conditions in Theorem E.29. Therefore, Theorem E.29 implies that 

**==> picture [380 x 55] intentionally omitted <==**

where we have used _M_ = _O_[Ëœ] ( _RND_[1] _[âˆ’][Ï‡]_ ) = _O_[Ëœ] ( _RN_[2] _[âˆ’][Ï‡]_ ). This contradicts _S â‰¤ o_ ï¿½ polylog( _N[â€²][Ï‡][âˆ’]_[1] _[/K] N[â€²]_ ) ï¿½. Therefore, no such classical learning algorithm exists. This completes the proof of Theorem F.26. Together with the quantum algorithm result Theorem F.23, this proves the quantum advantage claim in non-dynamic dimension reduction (Theorem F.21). 
