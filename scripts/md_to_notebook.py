#!/usr/bin/env python3
"""
将 Markdown 教程转为 Jupyter Notebook（.ipynb）。
- 围栏代码块 -> 代码单元或说明单元（按语言与内容启发式分类）
- 第 3 章自动插入 FLOPs / MFU 等「运行结果」单元，并修正 get_batch 缺 return
用法：
  python scripts/md_to_notebook.py              # 默认处理 docs/ 下教程 md
  python scripts/md_to_notebook.py path/to/a.md # 单文件
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


NBFORMAT_MAJOR = 4
NBFORMAT_MINOR = 5


def _src_to_lines(text: str) -> list[str]:
    if not text:
        return []
    lines = text.splitlines(keepends=True)
    if lines and not lines[-1].endswith("\n"):
        lines[-1] = lines[-1] + "\n"
    return lines


def _markdown_cell(text: str) -> dict:
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": _src_to_lines(text),
    }


def _code_cell(text: str) -> dict:
    return {
        "cell_type": "code",
        "metadata": {},
        "source": _src_to_lines(text),
        "outputs": [],
        "execution_count": None,
    }


def _iter_fence_chunks(text: str):
    lines = text.splitlines(keepends=True)
    md_buf: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.lstrip(" ")
        if stripped.startswith("```"):
            if md_buf:
                yield "markdown", "".join(md_buf)
                md_buf = []
            lang = stripped[3:].strip()
            if lang.endswith("\n"):
                lang = lang[:-1]
            lang = lang.strip()
            i += 1
            code_lines: list[str] = []
            while i < len(lines):
                cl = lines[i]
                cs = cl.lstrip(" ")
                if cs.startswith("```"):
                    i += 1
                    break
                code_lines.append(cl)
                i += 1
            code = "".join(code_lines).rstrip("\n")
            yield "fence", (lang, code)
        else:
            md_buf.append(line)
            i += 1
    if md_buf:
        yield "markdown", "".join(md_buf)


_PSEUDO_PATTERNS = (
    "Model:",
    "y[i, k] =",
    "合并维度",
    "$$",
    "\\frac{",
)


def _is_pseudocode_block(code: str) -> bool:
    s = code.strip()
    if not s:
        return True
    for p in _PSEUDO_PATTERNS:
        if p in s:
            return True
    if s.startswith("y[i, k]"):
        return True
    return False


def _is_probably_python(code: str, lang: str) -> bool:
    lang_l = (lang or "").lower().strip()
    if lang_l in ("python", "py"):
        return not _is_pseudocode_block(code)
    if lang_l:
        return False
    if _is_pseudocode_block(code):
        return False
    keys = (
        "import ",
        "from ",
        "torch.",
        "def ",
        "class ",
        "assert ",
        "nn.",
        "np.",
        "F.",
        "return ",
        "if __name__",
        "@torch",
        "cuda.",
        "self.",
    )
    if any(k in code for k in keys):
        return True
    if re.search(r"\w+\s*=\s*torch\.", code):
        return True
    if re.search(r"\w+\s*@\s*\w+", code):
        return True
    return False


def _fence_to_notebook_cells(lang: str, code: str) -> list[dict]:
    lang_l = (lang or "").lower().strip()
    if lang_l in ("bash", "sh", "shell", "zsh"):
        body = code.strip("\n")
        src = f"%%bash\n{body}" if body else "%%bash\n"
        return [_code_cell(src)]
    if lang_l in ("c", "cpp", "cuda"):
        return [_code_cell(f"// 语言: {lang or 'c'}\n/*\n{code}\n*/")]
    if lang_l in ("text", "txt", "json", "markdown", "md", "yaml", "yml", "toml"):
        fence = lang_l if lang_l != "txt" else ""
        inner = fence + "\n" + code if fence else code
        return [_markdown_cell("```" + inner + "\n```\n")]
    if lang_l in ("python", "py") or _is_probably_python(code, lang):
        fixed = _fix_common_snippet(code)
        return [_code_cell(fixed)]
    return [_markdown_cell("```" + (lang + "\n" if lang else "") + code + "\n```\n")]


def _fix_common_snippet(code: str) -> str:
    if "def get_batch" in code and not re.search(r"\breturn\b", code):
        return code.rstrip() + "\n    return x\n"
    return code


def md_to_cells(md_text: str) -> list[dict]:
    cells: list[dict] = []
    for kind, payload in _iter_fence_chunks(md_text):
        if kind == "markdown":
            if payload.strip():
                cells.append(_markdown_cell(payload))
        else:
            lang, code = payload
            cells.extend(_fence_to_notebook_cells(lang, code))
    return cells


def _chapter3_preamble() -> dict:
    src = r'''from pathlib import Path
import sys

from typing import Iterable

import numpy as np
import torch
import torch.nn as nn

# 导入第三章配套工具（与本 ipynb 同目录下的 chapter3_helpers.py）
_here = Path.cwd().resolve()
for p in (_here, _here / "docs" / "chapter3"):
    hp = p / "chapter3_helpers.py"
    if hp.is_file() and str(p) not in sys.path:
        sys.path.insert(0, str(p))
        break

from chapter3_helpers import (
    get_device,
    same_storage,
    time_matmul,
    matmul_flop_count,
    get_promised_flop_per_sec,
    print_matmul_flops,
    print_mfu_summary,
)
'''
    return _code_cell(src)


def enrich_chapter3_notebook(cells: list[dict]) -> list[dict]:
    """在 GEMM 示例与 MFU 示例后插入打印 FLOPs / MFU 的单元。"""
    out: list[dict] = []
    i = 0
    while i < len(cells):
        c = cells[i]
        out.append(c)
        if c.get("cell_type") != "code":
            i += 1
            continue
        src = "".join(c.get("source", []))
        # 第一次大规模 matmul 演示后输出 FLOPs 并设置 actual_num_flops
        if (
            "y = x @ w" in src
            and "get_device()" in src
            and "if torch.cuda.is_available():" in src
            and "matmul_flop_count" not in src
        ):
            out.append(
                _code_cell(
                    "# —— 运行结果：本段矩阵乘法的 FLOPs（与正文 2*B*D*K 一致）——\n"
                    "actual_num_flops = matmul_flop_count(x, w)\n"
                    "print_matmul_flops(x, w)\n"
                )
            )
        if "bf16_mfu = bf16_actual_flop_per_sec / bf16_promised_flop_per_sec" in src:
            out.append(
                _code_cell(
                    "# —— 运行结果：MFU ——\n"
                    'print_mfu_summary(bf16_actual_flop_per_sec, bf16_promised_flop_per_sec, label="bfloat16")\n'
                )
            )
        if (
            "actual_flop_per_sec = actual_num_flops / actual_time" in src
            and "print(" not in src
        ):
            out.append(
                _code_cell(
                    "# —— 运行结果：实测 FLOP/s ——\n"
                    "print(f\"实测 FLOP/s ≈ {actual_num_flops / actual_time:.3e}\")\n"
                )
            )
        if (
            "promised_flop_per_sec = get_promised_flop_per_sec(device, x.dtype)" in src
            and "print(" not in src
        ):
            out.append(
                _code_cell(
                    "# —— 运行结果：理论峰值 FLOP/s ——\n"
                    "print(f\"理论峰值 FLOP/s ≈ {promised_flop_per_sec:.3e}\")\n"
                )
            )
        i += 1
    return out


def build_notebook(md_path: Path, cells: list[dict]) -> dict:
    body = cells
    if "chapter3" in md_path.name and "pytorch" in md_path.name:
        body = enrich_chapter3_notebook(body)
    final_cells = []
    if "chapter3" in md_path.name and "pytorch" in md_path.name:
        final_cells.append(_markdown_cell("## 环境准备\n运行下方单元以加载第三章辅助函数。\n"))
        final_cells.append(_chapter3_preamble())
    final_cells.extend(body)
    return {
        "cells": final_cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {"name": "python", "pygments_lexer": "ipython3"},
        },
        "nbformat": NBFORMAT_MAJOR,
        "nbformat_minor": NBFORMAT_MINOR,
    }


def convert_file(md_path: Path, out_path: Path | None = None) -> Path:
    md_text = md_path.read_text(encoding="utf-8")
    cells = md_to_cells(md_text)
    nb = build_notebook(md_path, cells)
    if out_path is None:
        out_path = md_path.with_suffix(".ipynb")
    out_path.write_text(json.dumps(nb, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return out_path


def default_doc_md_files(repo_root: Path) -> list[Path]:
    docs = repo_root / "docs"
    paths: list[Path] = []
    for p in sorted(docs.rglob("*.md")):
        if ".history" in str(p):
            continue
        if p.name == "_sidebar.md":
            continue
        paths.append(p)
    return paths


def default_coursework_md_files(repo_root: Path) -> list[Path]:
    """作业目录下的说明/导读类 Markdown（排除纯变更日志）。"""
    cw = repo_root / "coursework"
    if not cw.is_dir():
        return []
    out: list[Path] = []
    for p in sorted(cw.rglob("*.md")):
        if p.name == "CHANGELOG.md":
            continue
        out.append(p)
    return out


def default_all_targets(repo_root: Path) -> list[Path]:
    return default_doc_md_files(repo_root) + default_coursework_md_files(repo_root)


def main(argv: list[str]) -> int:
    repo = Path(__file__).resolve().parents[1]
    if len(argv) > 1:
        targets = [Path(a).resolve() for a in argv[1:]]
    else:
        targets = default_all_targets(repo)
    for md in targets:
        if not md.is_file():
            print(f"skip (not found): {md}", file=sys.stderr)
            continue
        out = convert_file(md)
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
