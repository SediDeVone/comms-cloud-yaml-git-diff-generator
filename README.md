# comms-cloud-yaml-git-diff-generator

A Python utility that generates YAML manifest files for Communication Cloud Salesforce, including only changed elements between Git branches. This tool helps streamline the deployment process by identifying and including only the components that have changed.

## Description

This tool analyzes the differences between two Git branches for a specified folder and generates either:
1. A text file containing the unique trimmed paths of changed files
2. An updated YAML file with manifest entries for the changed files

The script is particularly useful for Salesforce Communication Cloud deployments where you need to create manifest files that include only the changed components.

## Features

- Compare files between two Git branches
- Trim file paths to a specified depth
- Remove duplicate entries
- Generate a text file with changed paths
- Update an existing YAML file with manifest entries
- Automatically set `manifestOnly: true` in YAML files

## Installation

No installation is required. Simply clone the repository and ensure you have Python 3.x installed.

```bash
git clone https://github.com/yourusername/comms-cloud-yaml-git-diff-generator.git
cd comms-cloud-yaml-git-diff-generator
```

## Usage

```bash
python generate_industries_diff.py --source-branch <source_branch> --target-branch <target_branch> --folder <folder_path> [--yml-file <yaml_file_path>]
```

### Arguments

- `--source-branch`: The source branch name (required)
- `--target-branch`: The target branch name (required)
- `--folder`: The name of the folder to take diff from (required)
- `--yml-file`: Path to the .yml file to update (optional). If provided, will update the file instead of creating a new .txt file.

### Examples

Generate a text file with changed paths:
```bash
python generate_industries_diff.py --source-branch feature-branch --target-branch main --folder force-app
```

Update an existing YAML file with manifest entries:
```bash
python generate_industries_diff.py --source-branch feature-branch --target-branch main --folder force-app --yml-file deployment.yml
```

## How It Works

1. The script gets the file differences between two Git branches for a specific folder
2. It trims the file paths to include only the first 3 parts of each path
3. Duplicate paths are removed
4. Depending on the options:
   - If a YAML file is specified, it updates the file with manifest entries
   - Otherwise, it creates a text file with the unique trimmed paths

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Sedi De'Vone
