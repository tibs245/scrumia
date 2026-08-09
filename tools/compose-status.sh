#!/bin/bash
# Output the composition from .scrumia/config.yaml in a readable format.
# Used as a fixture in tools/validate.py to detect drift.

set -e

REPO_ROOT="$(git rev-parse --show-toplevel)"
CONFIG="$REPO_ROOT/.scrumia/config.yaml"

if [[ ! -f "$CONFIG" ]]; then
  echo "Error: .scrumia/config.yaml not found" >&2
  exit 1
fi

# Use Python for precise parsing
python3 << PYTHON
config_file = "$CONFIG"
with open(config_file) as f:
    content = f.read()

# Extract just composition section
comp_start = content.find('composition:')
if comp_start == -1:
    exit(1)

comp_end = content.find('\n\n', comp_start)
if comp_end == -1:
    # Find the next section marker instead
    for marker in ['apps:', 'settings:']:
        pos = content.find(marker, comp_start)
        if pos > comp_start and (comp_end == -1 or pos < comp_end):
            comp_end = pos - 1

if comp_end == -1:
    comp_end = len(content)

comp_section = content[comp_start:comp_end].rstrip()

# Extract just apps section
apps_start = content.find('apps:')
if apps_start == -1:
    exit(1)

# Find where apps section ends (next top-level key)
apps_end = len(content)
for marker in ['settings:']:
    pos = content.find('\n' + marker, apps_start)
    if pos > apps_start:
        apps_end = pos + 1
        break

apps_section = content[apps_start:apps_end].rstrip()

# Clean up and output
print("# Which module fills which slot.")
print("# An empty slot = capability absent, owned.")
print()
print(comp_section)
print()
print(apps_section)
PYTHON
