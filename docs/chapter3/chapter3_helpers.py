"""第三章《PyTorch 与资源核算》配套工具：正文片段依赖的辅助函数与 FLOPs 统计。"""

from __future__ import annotations

import time
import torch


def get_device() -> torch.device:
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def same_storage(a: torch.Tensor, b: torch.Tensor) -> bool:
    try:
        return a.untyped_storage().data_ptr() == b.untyped_storage().data_ptr()
    except Exception:
        return a.storage().data_ptr() == b.storage().data_ptr()


def time_matmul(x: torch.Tensor, w: torch.Tensor, repeats: int = 30, warmup: int = 5) -> float:
    """返回单次 matmul 的平均耗时（秒）。"""
    for _ in range(warmup):
        y = x @ w
    del y
    if x.is_cuda:
        torch.cuda.synchronize()
    t0 = time.perf_counter()
    for _ in range(repeats):
        y = x @ w
    del y
    if x.is_cuda:
        torch.cuda.synchronize()
    return (time.perf_counter() - t0) / repeats


def matmul_flop_count(x: torch.Tensor, w: torch.Tensor) -> int:
    """GEMM (B, D) @ (D, K) 的经典估算：2 * B * D * K FLOPs。"""
    b, d = x.shape
    d2, k = w.shape
    if d != d2:
        raise ValueError(f"内维不匹配: x.shape={x.shape}, w.shape={w.shape}")
    return 2 * b * d * k


def get_promised_flop_per_sec(device: torch.device, dtype: torch.dtype) -> float:
    """教学用粗粒度理论峰值（FLOP/s）；真实硬件请以厂商数据与实测为准。"""
    if device.type != "cuda":
        return 5e11
    if dtype in (torch.float16, torch.bfloat16):
        return 990e12
    if dtype == torch.float32:
        return 60e12
    return 50e12


def print_matmul_flops(x: torch.Tensor, w: torch.Tensor) -> int:
    """在 y = x @ w 之后调用：打印并返回 FLOPs。"""
    n = matmul_flop_count(x, w)
    print(f"GEMM FLOPs ≈ {n:,}  ({n / 1e9:.4f} GFLOPs)")
    return n


def print_mfu_summary(
    actual_flop_per_sec: float,
    promised_flop_per_sec: float,
    label: str = "",
) -> None:
    mfu = actual_flop_per_sec / promised_flop_per_sec
    prefix = f"{label} " if label else ""
    print(f"{prefix}实际 FLOP/s ≈ {actual_flop_per_sec:.3e}")
    print(f"{prefix}理论峰值 FLOP/s ≈ {promised_flop_per_sec:.3e}")
    print(f"{prefix}MFU ≈ {mfu:.2%}")
