# AUDIO FEATURE EXTRACTION

- [Description](#Description)
- [Install](#Install)

- ## Description

This program leverages the powerful audio feature extraction capabilities of [Praat](https://www.fon.hum.uva.nl/praat), enhanced with configurations made by [Shahabks](https://github.com/Shahabks/my-voice-analysis). The primary goal of this tool is to extract detailed audio features from datasets such as:
* syllables mean
* average syllable duration
* F2 range
* speech rate mean
* pauses mean
* speaking duration mean
* pause duration mean
* original duration mean
* speaking balance mean
* speaking duration percentage
* pausing duration percentage
* articulation rate mean
* F0 mean mean
* local jitter average
* local absolute jitter average
* local shimmer average
* local db shimmer average
* mean harmonics to noise - mean HNR
* F1 average
* F2 average
* F3 average
* F4 average
* amplitude difference H1-A3
* pitch average
* mean intensity

- ## Install

It is highly recommended to install [conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation) to avoid potential issues with missing C libraries.
* Clone an existing base environment:
  ```bash
  conda create --name new-env-name --clone base
* Clone repository
  ```bash
  git clone https://github.com/Matic-M/Audio-feature-extraction
* Install parselmouth
  ```bash
  pip install praat-parselmouth
* Ensure build tools and dependencies are installed
  ```bash
  pip install -r requirements.txt

* if building wheels fails, try [prebuilt wheels](https://pypi.org/project/praat-parselmouth/#files)
* For more information visit [readthedocs.io](https://parselmouth.readthedocs.io/en/stable/installation.html) and maintained [Parselmouth](https://github.com/YannickJadoul/Parselmouth)
