# Metabo-Figureflow

**Metabo-Figureflow** is a lightweight Python workflow for generating reproducible metabolomics figures and summary tables from curated LC-MS feature tables.

This repository was developed for a *Rafflesia*–*Tetrastigma* untargeted LC-MS metabolomics dataset, but the scripts may be adapted for similar feature-table-based metabolomics studies. The workflow focuses on downstream visualization and summary export, not raw LC-MS preprocessing, peak picking, alignment, or metabolite annotation.

## Purpose

The goal of this repository is to provide transparent and reusable scripts for:

- PCA visualization of LC-MS sample groups
- stacked-bar visualization of metabolite abundance patterns
- export of PCA scores, PCA loadings, and normalized abundance tables
- reproducible figure generation from curated feature tables

This workflow assumes that the input feature table has already undergone upstream LC-MS processing, blank handling, feature annotation, and curation.

## Current status

This repository is currently an early-stage reproducible figure workflow. At this stage, the first working script generates a 3D PCA plot from the curated LC-MS feature table and exports PCA scores and loadings.

## Repository structure

```text
metabo-figureflow/
├── README.md
├── requirements.txt
├── data/
│   └── rafflesia_lcms_feature_table.xlsx
├── scripts/
│   └── pca_3d_sample_groups.py
└── outputs/
```

## Input data

The PCA script expects an Excel file named:

```text
rafflesia_lcms_feature_table.xlsx
```

The workbook should contain a sheet named:

```text
Sheet1
```

The table should include:

- `Feature_Label`, used as the feature identifier when available
- sample intensity columns containing group names such as:
  - `sapbud`
  - `Raffbudspec`
  - `Raffbudlag`
  - `infectedTHAI`
  - `infectedCAM`
  - `infectedILO`
  - `UNinfectedTHAI`
  - `UNinfectedCAM`
  - `UNinfectedILO`
  - `uninfecraffspec-stemleaf`
  - `nonhostILO`
  - `NonhostCAM`
  - `raffseed`
  - `Ampelopsis`

Average columns beginning with `ave` are excluded from the PCA.

## Installation

Install the required Python packages:

```bash
pip install pandas numpy scikit-learn matplotlib openpyxl
```

Optional: save these dependencies in a `requirements.txt` file:

```text
pandas
numpy
scikit-learn
matplotlib
openpyxl
```

## Script 1: 3D PCA of sample groups

### Script

```text
scripts/pca_3d_sample_groups.py
```

### Description

This script performs PCA on LC-MS feature intensities across sample groups.

The script:

1. loads the curated Excel feature table
2. uses `Feature_Label` as the feature identifier when available
3. removes average columns beginning with `ave`
4. assigns sample columns to predefined biological groups
5. transposes the matrix so rows represent samples and columns represent features
6. converts all intensity values to numeric format
7. applies autoscaling using mean-centering and unit-variance scaling
8. performs PCA with three components
9. generates a 3D PCA plot
10. exports PCA scores and loadings as CSV files

### Run

From the repository folder, run:

```bash
python scripts/pca_3d_sample_groups.py
```

If the script is in the same folder as the Excel file, run:

```bash
python pca_3d_sample_groups.py
```

On Windows, if `python` does not work, try:

```cmd
py scripts\pca_3d_sample_groups.py
```

or, if the script is in the same folder as the Excel file:

```cmd
py pca_3d_sample_groups.py
```

### Expected outputs

```text
PCA_scores_autoscaled_main-data.csv
PCA_loadings_autoscaled_main-data.csv
```

`PCA_scores_autoscaled_main-data.csv` contains sample coordinates for PC1, PC2, and PC3, plus group labels.

`PCA_loadings_autoscaled_main-data.csv` contains feature-level PCA loadings for PC1, PC2, and PC3.

## Note on file paths

During early testing, the simplest setup is to keep the Python script and Excel file in the same folder:

```text
pca_3d_sample_groups.py
rafflesia_lcms_feature_table.xlsx
```

If the repository later uses separate `scripts/` and `data/` folders, the input path inside the script should be updated from:

```python
file_path = "rafflesia_lcms_feature_table.xlsx"
```

to:

```python
file_path = "data/rafflesia_lcms_feature_table.xlsx"
```

## Scope

Metabo-Figureflow is not intended to replace full metabolomics platforms or raw LC-MS processing pipelines. It is designed as a transparent downstream figure-generation workflow for curated feature tables.
