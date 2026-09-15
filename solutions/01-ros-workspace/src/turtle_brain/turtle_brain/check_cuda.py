"""Run a real CUDA operation without ROS or a graphical display."""

import torch

if not torch.cuda.is_available():
    raise RuntimeError(
        "PyTorch cannot access CUDA. Use an NVIDIA GPU with a compatible driver "
        "and the CUDA platform from Exercise 1, or follow the workshop's Brev setup."
    )

print("GPU:", torch.cuda.get_device_name(0))
print("Compute capability:", torch.cuda.get_device_capability(0))
print("Architectures in this build:", torch.cuda.get_arch_list())

values = torch.ones(4, device="cuda")
result = (values * 2).sum()
print("GPU result:", result.item())  # Expected: 8.0; waits for the CUDA work to finish.
