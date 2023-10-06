// Network flow based approximation of perturbed maximization
#include<assert.h>
#include "Matrix.hpp"
#include "Array.hpp"
using namespace std;

template <class T>
class PerturbedMaximizationInput {
private:
public:
	int discretize_precision;		// parameter w in the paper
	Array<double> shrink_factor;	// calculated from perturbation function f
	int num_papers, num_reviewers;  // number of papers and reviewers
	Array<int> paper_requirement;	// number of reviewers required for each paper
	Array<int> reviewer_loadlimit;  // maximum number of papers for each reviewer
	Matrix<T> similarity;			// similarity matrix
};

template <class T>
class PerturbedMaximizationOutput {
private:
public:
	string message;					// error message
	Matrix<double> matching;		// matching matrix
	T quality; int support;			// quality and support of the matching
	double pquality, entropy, maxprob, avgmaxprob, ltwonorm;  // other measures of the matching
};

template <class T>
class PerturbedMaximization {
private:
	int num_papers, num_reviewers;			// number of papers and reviewers
	int precision;							// parameter w in the paper
	int expected_flow;						// sum of paper requirements
	Array <double> factor;					// calculated from perturbation function f
	Matrix <T> cost; 						// cost matrix of maxcost flow
	Matrix <int> flow;						// flow matrix of maxcost flow
	Array <int> cap_paper, cap_reviewer;    // remaining capacity of papers and reviewers
	
	// Auxiliary function for maxcost flow: weight of an edge
	T weight(int paper, int reviewer, bool forward) {
		if (forward) return T(factor[flow[paper][reviewer]] * cost[paper][reviewer]);
		else return -T(factor[flow[paper][reviewer] - 1] * cost[paper][reviewer]);
	}

	// Auxiliary function for maxcost flow: initialize the algorithm
	void init(PerturbedMaximizationInput<T> instance) {
		num_papers = instance.num_papers;
		num_reviewers = instance.num_reviewers;
		precision = instance.discretize_precision;
		cost = instance.similarity; factor = instance.shrink_factor;
		flow.init(num_papers, num_reviewers);
		
		expected_flow = 0;
		cap_paper.init(num_papers);
		for (int i = 0; i < num_papers; i++) {
			cap_paper[i] = instance.paper_requirement[i] * precision;
			expected_flow += cap_paper[i];
		}
		cap_reviewer.init(num_reviewers);
		for (int i = 0; i < num_reviewers; i++) {
			cap_reviewer[i] = instance.reviewer_loadlimit[i] * precision;
		}
	}

	// Auxiliary variables for the shortest path in maxcost flow
	T distINF; bool setINF;
	Array <T> dist_paper, dist_reviewer; T distT;
	Array <T> auxh_paper, auxh_reviewer; T auxhT;
	Array <int> home_paper, home_reviewer; int homeT;
	Array <bool> vis_paper, vis_reviewer;

	// Auxiliary function for maxcost flow: initialize shortest path 
	void initShortestPath() {
		if (is_same<T, int>::value) distINF = INT_MAX;
		else if (is_same<T, long long>::value) distINF = LLONG_MAX;
		else assert(setINF);
		auxhT = 0;
		vis_paper.init(num_papers);
		dist_paper.init(num_papers);
		auxh_paper.init(num_papers);
		home_paper.init(num_papers);
		vis_reviewer.init(num_reviewers);
		dist_reviewer.init(num_reviewers);
		auxh_reviewer.init(num_reviewers);
		home_reviewer.init(num_reviewers);

		for (int i = 0; i < num_papers; i++)
		for (int j = 0; j < num_reviewers; j++)
			auxh_reviewer[j] = max(auxh_reviewer[j], weight(i, j, true));
		for (int i = 0; i < num_reviewers; i++)
			auxhT = max(auxhT, auxh_reviewer[i]);
	}

	// Auxiliary function for maxcost flow: calculate shortest path in maxcost flow
	bool Dijkstra() {
		// Initialize dists and vises.
		for (int i = 0; i < num_papers; i++) {
			dist_paper[i] = -distINF;
			vis_paper[i] = false;
		}
		for (int i = 0; i < num_reviewers; i++) {
			dist_reviewer[i] = -distINF;
			vis_reviewer[i] = false;
		}
		distT = -distINF;
		// Go from S
		for (int i = 0; i < num_papers; i++)
			if (cap_paper[i] > 0) {
				home_paper[i] = -1;
				dist_paper[i] = -auxh_paper[i];
			}
		// Go from other vertices
		while (true) {
			T longest = -distINF;
			bool paper = false; int from = -1;
			for (int i = 0; i < num_papers; i++)
				if (!vis_paper[i] && dist_paper[i] > longest) {
					longest = dist_paper[i];
					from = i; paper = true;
				}
			for (int i = 0; i < num_reviewers; i++)
				if (!vis_reviewer[i] && dist_reviewer[i] > longest) {
					longest = dist_reviewer[i];
					from = i; paper = false;
				}
			if (from == -1) break;
			if (paper) {
				vis_paper[from] = true;
				for (int i = 0; i < num_reviewers; i++)
					if (flow[from][i] < precision && dist_paper[from] + auxh_paper[from] + weight(from, i, true) - auxh_reviewer[i] > dist_reviewer[i]) {
						assert(auxh_paper[from] + weight(from, i, true) - auxh_reviewer[i] <= 0);
						dist_reviewer[i] = dist_paper[from] + auxh_paper[from] + weight(from, i, true) - auxh_reviewer[i];
						home_reviewer[i] = from;
					}
			} else {
				vis_reviewer[from] = true;
				if (cap_reviewer[from] > 0 && dist_reviewer[from] + auxh_reviewer[from] - auxhT > distT) {
					distT = dist_reviewer[from] + auxh_reviewer[from] - auxhT;
					homeT = from;
				}
				for (int i = 0; i < num_papers; i++)
					if (flow[i][from] > 0 && dist_reviewer[from] + auxh_reviewer[from] + weight(i, from, false) - auxh_paper[i] > dist_paper[i]) {
						assert(auxh_reviewer[from] + weight(i, from, false) - auxh_paper[i] <= 0);
						dist_paper[i] = dist_reviewer[from] + auxh_reviewer[from] + weight(i, from, false) - auxh_paper[i];
						home_paper[i] = from;
					}
			}
		}
		// Update auxhs
		for (int i = 0; i < num_papers; i++)
			if (vis_paper[i]) auxh_paper[i] += dist_paper[i];
		for (int i = 0; i < num_reviewers; i++)
			if (vis_reviewer[i]) auxh_reviewer[i] += dist_reviewer[i];
		if (distT != distINF) auxhT += distT;
		return distT != -distINF;
	}

	// Auxiliary function for maxcost flow: confirm a flow path
	void Flowpath() {
		expected_flow -= 1;
		bool paper = false; int pos = homeT;
		cap_reviewer[pos]--;
		while (true) {
			if (paper) {
				if (home_paper[pos] == -1) {
					cap_paper[pos]--;
					return;
				} else {
					int nxt = home_paper[pos];
					flow[pos][nxt]--;
					pos = nxt; paper = false;
				}
			} else {
				int nxt = home_reviewer[pos];
				flow[nxt][pos]++;
				pos = nxt; paper = true;
			}
		}
	}
public:

	// Public function: set infinity
	void setMaxT(T Max) {
		distINF = Max;
		setINF = true;
	}

	// Main function: solve perturbed maximization 
	PerturbedMaximizationOutput<T> solve(PerturbedMaximizationInput<T> instance) {
		init(instance);
		initShortestPath();
		while (Dijkstra()) Flowpath();
		PerturbedMaximizationOutput<T> ans;
		if (expected_flow == 0) ans.message = "Feasible. Matching calculated.";
		else ans.message = "Infeasible. Not enough reviewers. Matching is best-effort.";
		ans.matching.init(num_papers, num_reviewers);
		ans.entropy = 0;
		ans.maxprob = 0;
		ans.quality = 0;
		ans.support = 0;
		ans.pquality = 0;
		ans.ltwonorm = 0;
		ans.avgmaxprob = 0;
		for (int i = 0; i < num_papers; i++) {
			double Max = 0;
			for (int j = 0; j < num_reviewers; j++) {
				for (int k = 0; k < flow[i][j]; k++)
					ans.pquality += cost[i][j] * instance.shrink_factor[k];
				ans.matching[i][j] = 1.0 * flow[i][j] / precision;
				ans.quality += cost[i][j] * ans.matching[i][j];
				ans.support += ans.matching[i][j] != 0;
				ans.ltwonorm += ans.matching[i][j] * ans.matching[i][j];
				ans.maxprob = max(ans.maxprob, ans.matching[i][j]);
				Max = max(Max, ans.matching[i][j]);
				if (ans.matching[i][j] != 0) ans.entropy -= ans.matching[i][j] * log(ans.matching[i][j]);
			}
			ans.avgmaxprob += Max;
		}
		ans.ltwonorm = sqrt(ans.ltwonorm);
		ans.avgmaxprob /= num_papers;
		return ans;
	}
};