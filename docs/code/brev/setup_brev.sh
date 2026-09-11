#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/prefix-dev/roscon-2026-declarative-ros-workspaces-with-pixi.git}"
REPO_DIR="${REPO_DIR:-${HOME}/roscon-2026-declarative-ros-workspaces-with-pixi}"

# Install Pixi for the default Brev user.
if ! command -v pixi >/dev/null 2>&1; then
    curl -fsSL https://pixi.sh/install.sh | bash
fi

PIXI="${HOME}/.pixi/bin/pixi"
if [ ! -x "${PIXI}" ]; then
    PIXI="$(command -v pixi)"
fi

# Make Pixi available in future shells and add completions.
grep -q '.pixi/bin' "${HOME}/.bashrc" 2>/dev/null || echo 'export PATH="${HOME}/.pixi/bin:${PATH}"' >> "${HOME}/.bashrc"
grep -q 'pixi completion --shell bash' "${HOME}/.bashrc" 2>/dev/null || echo 'eval "$(pixi completion --shell bash)"' >> "${HOME}/.bashrc"

# A small toolbox for editing and inspecting the workshop repository on the instance.
"${PIXI}" global install bat curl git gh nvim tree

# Clone or update the workshop material.
if [ -d "${REPO_DIR}/.git" ]; then
    git -C "${REPO_DIR}" pull --ff-only
else
    git clone "${REPO_URL}" "${REPO_DIR}"
fi

cd "${REPO_DIR}"

# Pre-download both ROS environments and PyTorch while the instance starts.
# Compatible NVIDIA hosts select the preferred CUDA platform; CPU hosts stay on CPU.
"${PIXI}" install --all --manifest-path solutions/01-ros-workspace/pixi.toml

cat <<EOF

Brev setup complete.
Repository: ${REPO_DIR}
Try:
  cd ${REPO_DIR}
  pixi run --manifest-path solutions/01-ros-workspace/pixi.toml topics
For the CUDA exercise (requires an NVIDIA GPU and compatible driver):
  nvidia-smi
  pixi run --manifest-path solutions/01-ros-workspace/pixi.toml --platform cuda-linux-64 cuda-check
Instructions: https://prefix-dev.github.io/roscon-2026-declarative-ros-workspaces-with-pixi/exercises/01-ros-workspace/#19-run-it-on-a-real-gpu
EOF
