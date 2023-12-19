# A One-Size-Fits-All Approach to Improving Randomness in Paper Assignment

## Table of Contents

- [General Information](#general-information)
- [Technologies Used](#technologies-used)
- [File Structure](#file-structure)
- [Reproducing the Experiments](#reproducing-the-experiments)

## General Information

This repository contains the source code for the experiments in the NeurIPS 2023 paper: [A One-Size-Fits-All Approach to Improving Randomness in Paper Assignment](https://arxiv.org/abs/2310.05995). We implemented **Perturbed Maximization**, a peer review paper assignment algorithm aiming to improve the randomness of assignment, and tested its performance under several configurations.

## Technologies Used

- Gurobi Version 10.0

## File Structure

The repository contains the following directories:
- `cpp`: the C++ implementation network flow based approximation.
- `datasets`: the datasets used in the experiments.
- `figures`: the figures used in the paper.
- `logs`: the log files of the experiments.
- `plot`: the scripts used to plot the figures.
- `python`: the Python implementation of PM.

## Reproducing the Experiments

We have written a set of scripts so that the experiments are easily reproduced. Although the source code of algorithms is cross-platform, the scripts use `bash` and `make`, so they only work under Linux-like systems (including Windows Subsystem for Linux).

Before running the scripts, please make sure that you have installed Gurobi, obtained a license and set up the environment variables. For more information, please refer to [Gurobi Documentation](https://www.gurobi.com/documentation/).

- To reproduce the experiments in Section 6, run the following command in root directory:
	```bash
	make main
	```
- To reproduce the experiments in Appendix A.1, run the following commands in root directory:
	```bash
	make speedcpp
	make speedpython
	```
- To reproduce the experiments in Appendix A.2, run the following command in root directory:
	```bash
	make hypertune
	```
- To reproduce the experiments in Appendix A.3, run the following command in root directory:
	```bash
	make additional
	```
- To generate the figures in the paper, run the following command in root directory:
	```bash
	make plots
	```