# Reproduction README

## Model summary

> Anagnostou, A. Groen, D. Taylor, S. Suleimenova, D. Abubakar, N. Saha, A. Mintram, K. Ghorbani, M. Daroge, H. Islam, T. Xue, Y. Okine, E. Anokye, N. **FACS-CHARM: A Hybrid Agent-Based and Discrete-Event Simulation Approach for Covid-19 Management at Regional Level**. 2022 Winter Simulation Conference (WSC), Singapore, pp. 1223-1234. (2022). <https://doi.org/10.1109/WSC57314.2022.10015462>.

This paper includes two models - we have focussed just on the dynamiC Hospital wARd Management (CHARM) model. CHARM is a discrete-event simulation modelling intensive care units (ICU) in the COVID-19 pandemic (as well as subsequent stays in a recovery bed). It includes three types of admission to the ICU (emergency, elective or COVID-19). COVID-19 patients are kept seperate, and if they run out of capacity due to a surge in COVID-19 admissions, additional capacity can be pooled from the elective and emergency capacity.

## Scope of the reproduction

In this assessment, we attempted to reproduce 1 item: a figure.

## Reproducing these results

### Repository overview

```{bash}
├── docker
│   └──  ...
├── input
│   └──  ...
├── output
│   └──  ...
├── scripts
│   └──  ...
├── tests
│   └──  ...
├── environment.yml
└── README.md
```

* `docker/` - Instructions for creation of Docker container.
* `input/` - Input files for the model
* `output/` - Output files from the model and reproduction.
* `scripts/` - Code for the model and for reproducing the figure in the scope.
* `tests/` - Test to check that model produces consistent results with our reproduction.
* `environment.yml` - Instructions for creation of python environment.
* `README.md` - This file!

### Step 1. Set up environment

#### Option A: Conda/mamba environment

A `conda`/`mamba` environment has been provided. To create this environment on your machine, you should run this command in your terminal:

```
conda env create -f environment.yaml
```

You can then use this environment in your preferred IDE, such as VSCode (where you will be asked to select the kernel/interpreter). You can activate it in the terminal by running:

```
conda activate anagnostou2022
```

You can run either of these commands also using `mamba` instead (e.g. `mamba activate anagnostou2022`).

#### Option B: Build local docker image

A `Dockerfile` is provided, which you can use to build the Docker image. The docker image will include the correct version of Python and the packages, and an installation of jupyterlab which you can run from your browser. It will also include the scripts and outputs from this directory.

For this option (and option C), you'll need to ensure that `docker` is installed on your machine.

To create the docker image and then open jupyter lab:

1. In the terminal, navigate to parent directory of the `reproduction/` folder
2. Build the image:

```
sudo docker build --tag anagnostou2022 . -f ./reproduction/docker/Dockerfile
```

3. Create a docker container from that image and open jupyter lab:

```
(sleep 2 && xdg-open http://localhost:8080) & sudo docker run -it -p 8080:80 --name anagnostou2022_docker anagnostou2022
```

#### Option C: Pull pre-built docker image

A pre-built image is available on the GitHub container registry. To use it:

1. Create a Personal Access Token (Classic) for your GitHub account with `write:packages` and `delete:packages` access
2. On terminal, run the following command and enter your sudo password (if prompted), followed by the token just generated (which acts as your GitHub password)

```
sudo docker login ghcr.io -u githubusername
```

3. Download the image:

```
sudo docker pull ghcr.io/pythonhealthdatascience/anagnostou2022
```

4. Create container and open Jupyter Lab:

```
(sleep 2 && xdg-open http://localhost:8080) & sudo docker run -it -p 8080:80 --name anagnostou2022_docker ghcr.io/pythonhealthdatascience/anagnostou2022:latest
```

### Step 2. Running the model

#### Option A: From the command line

You can run the model from the command line (although this will not produce the figure). Assuming you are in the `reproduction/` folder, run the command:

```
python3 main.py -z input/ZONES.csv -p input/ICU_INPUT_PARAMS.csv -c input/DAILY_ARRIVALS.csv -o output/OUT_STATS.csv 
```

#### Option B: Execute the notebook

You can execute the `reproduction.ipynb` file to run the model. This will also produce the **figure** from the article.

#### Option C: Pytest

The model has been set up as a test, so you can check whether your output matches the expected output, when run with the provided input parameters. You can run this from the terminal. Ensure that the `anagnostou2022` environment is active and that you are in the `reproduction/` folder. Then simply run:

```
pytest
```

## Reproduction specs and runtime

This reproduction was conducted on an Intel Core i7-12700H with 32GB RAM running Ubuntu 22.04.4 Linux.

The run time for `reproduction.ipynb` or the tests is only a couple of seconds.

## Citation

To cite the original study, please refer to the reference above. To cite this reproduction, please refer to the CITATION.cff file in the parent folder.

## License

This repository is licensed under the BSD 3-Clause license.