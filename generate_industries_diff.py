import subprocess
import os
import re


def get_git_diff(branch1, branch2, folder):
    cmd = ["git", "diff", "--name-only", branch1, branch2, "--", folder]
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        raise Exception(f"Git command failed with message: {result.stderr}")

    file_paths = result.stdout.strip().split('\n')
    return file_paths


def trim_paths(file_paths): 
    trimmed_paths = []

    for path in file_paths:
        parts = path.split('/')
        if len(parts) >= 3:
            trimmed_path = '/'.join(parts[:3])
            trimmed_paths.append(trimmed_path)

    return trimmed_paths


def remove_duplicates(paths):
    unique_paths = list(set(paths))
    return unique_paths


def save_to_file(paths, filename):
    with open(filename, 'w') as f:
        for path in paths:
            f.write(path + '\n')


def update_yml_file(paths, yml_file, folder):
    content = ""
    if os.path.exists(yml_file):
        with open(yml_file, 'r') as f:
            content = f.read()

    content = re.sub(r'manifestOnly:\s*false', 'manifestOnly: true', content)

    lines = content.split('\n')
    processed_lines = []
    skip_line = False
    manifest_found = False

    for i, line in enumerate(lines):
        if re.match(r'^manifest:\s*$', line):
            manifest_found = True
            skip_line = True
            continue

        if skip_line and (line.startswith(' ') or line.startswith('\t')):
            continue

        if skip_line and line and not (line.startswith(' ') or line.startswith('\t')):
            skip_line = False

        if not skip_line:
            processed_lines.append(line)

    content = '\n'.join(processed_lines)

    if content and not content.endswith('\n'):
        content += '\n'

    content += 'manifest:\n'

    # Remove folder name from paths if present
    trimmed_paths = []
    for path in paths:
        if path.startswith(folder + '/'):
            trimmed_paths.append(path[len(folder) + 1:])
        else:
            trimmed_paths.append(path)

    with open(yml_file, 'w') as f:
        f.write(content)
        for path in trimmed_paths:
            f.write(f'  - {path}\n')

    print(f"Updated {yml_file} with manifest entries")


def main(source_branch, target_branch, folder, yml_file=None):
    # Get the diff file paths
    file_paths = get_git_diff(target_branch, source_branch, folder)

    # Trim the paths
    trimmed_paths = trim_paths(file_paths)

    # Remove duplicates
    unique_paths = remove_duplicates(trimmed_paths)
    unique_paths.sort(reverse=False)

    if yml_file:
        update_yml_file(unique_paths, yml_file, folder)
    else:
        output_file = folder + ".txt"
        save_to_file(unique_paths, output_file)
        print(f"Unique trimmed paths saved to {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate a diff between two branches for a specific folder.')
    parser.add_argument('--source-branch', metavar='path', required=True, help='Source branch name')
    parser.add_argument('--target-branch', metavar='path', required=True, help='Target branch name.')
    parser.add_argument('--folder', metavar='path', required=True, help='Name of the folder to take diff from.')
    parser.add_argument('--yml-file', metavar='path', help='Path to the .yml file to update. If provided, will update the file instead of creating a new .txt file.')
    args = parser.parse_args()
    main(source_branch=args.source_branch, target_branch=args.target_branch, folder=args.folder, yml_file=args.yml_file)
