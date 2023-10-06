// Speed test program of the network flow based approximation
#include<bits/stdc++.h>
#include "lib/PerturbedMaximization.hpp"
using namespace std;
typedef long long ll;

const ll M = 1e8;							// a large integer
const int Precision = 10;					// parameter w in the paper

int paper_requirement;					  	// number of reviewers required for each paper
int reviewer_loadlimit;						// maximum number of papers for each reviewer
Matrix<ll> similarity;						// similarity matrix

PerturbedMaximization<ll> algorithm;		// the network flow based algorithm
PerturbedMaximizationInput<ll> Input;		// input of the algorithm
PerturbedMaximizationOutput<ll> Output;		// output of the algorithm

// Shrinking factor of PM-E
Array<double> FactorExp(int precision, double alpha, double q) {
	Array<double> ans; ans.init(precision);
	for (int i = 0; i < precision; i++){
		double pred = 1.0 * i / precision;
		double succ = 1.0 * (i + 1) / precision;
		if (succ - 1e-6 < q) ans[i] = expl(-alpha * pred) - expl(-alpha * succ);
	}
	return ans;
}

// Shrinking factor of PM-Q
Array<double> FactorQuad(int precision, double beta, double q) {
	Array<double> ans; ans.init(precision);
	for (int i = 0; i < precision; i++) {
		double pred = 1.0 * i / precision;
		double succ = 1.0 * (i + 1) / precision;
		if (succ - 1e-6 < q) ans[i] = (succ - succ * succ * beta) - (pred - pred * pred * beta);
	}
	return ans;
}

// Load dataset from file
void LoadDataset(string filename) {
	for (auto &x : filename) x = tolower(x);
	freopen(("datasets/" + filename + ".in").c_str(), "r", stdin);
	scanf("%d%d", &Input.num_papers, &Input.num_reviewers);
	paper_requirement = 3;
	reviewer_loadlimit = 6 + 6 * (filename == "aamas2015");
	Input.paper_requirement.init(Input.num_papers);
	for (int i = 0; i < Input.num_papers; i++)
		Input.paper_requirement[i] = paper_requirement;
	Input.reviewer_loadlimit.init(Input.num_reviewers);
	for (int i = 0; i < Input.num_reviewers; i++)
		Input.reviewer_loadlimit[i] = reviewer_loadlimit;
	similarity.init(Input.num_papers, Input.num_reviewers);
	for (int i = 0; i < Input.num_papers; i++)
	for (int j = 0; j < Input.num_reviewers; j++) {
		double tmp; scanf("%lf", &tmp);
		similarity[i][j] = tmp * M;
	}
	Input.discretize_precision = Precision;
	Input.similarity = similarity;
}

// Main function. Usage: ./speed [dataset] [algorithm] [maxprob] [beta] [alpha] [offset]
int main(int argc, char *argv[]) {
	srand(time(0));
	LoadDataset(string(argv[1]));
	string name = string(argv[2]);
	double maxprob = atof(argv[3]);
	double beta    = atof(argv[4]);
	double alpha   = atof(argv[5]);
	double offset  = atof(argv[6]);
	if (name == "PM-Q") Input.shrink_factor = FactorQuad(Input.discretize_precision, beta, maxprob + offset);
	else Input.shrink_factor = FactorExp(Input.discretize_precision, alpha, maxprob + offset);
	Output = algorithm.solve(Input);
	printf("Quality: %.2lf\n", 1.0 * Output.quality / M);
	printf("PQuality: %.2lf\n", Output.pquality / M);
	printf("Maxprob: %.2lf\n", Output.maxprob);
	printf("AvgMax: %.2lf\n", Output.avgmaxprob);
	printf("Support: %d\n", Output.support);
	printf("Entropy: %.2lf\n", Output.entropy);
	printf("L2 Norm: %.2lf\n", Output.ltwonorm);
	return 0;
}