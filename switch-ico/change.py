"""Convert an SVG file to a multi-size Windows ICO file.

Dependencies:
    pip install pillow resvg-py

Examples:
    py change.py svg1.svg
    py change.py input.svg -o output.ico
    py change.py input.svg --sizes 16 32 48 64 128 256
"""

from __future__ import annotations

import argparse
import io
import sys
from pathlib import Path
from typing import Sequence


DEFAULT_SIZES = (16, 24, 32, 48, 64, 128, 256)


def _load_dependencies():
    """Import optional dependencies and show an actionable error if absent."""
    try:
        from PIL import Image
        from resvg_py import svg_to_bytes
    except ImportError as exc:
        raise RuntimeError(
            "缺少依赖，请先运行：pip install pillow resvg-py"
        ) from exc

    return Image, svg_to_bytes


def _validate_sizes(sizes: Sequence[int]) -> tuple[int, ...]:
    """Return sorted unique ICO sizes after validating Windows ICO limits."""
    normalized = tuple(sorted(set(sizes)))
    if not normalized:
        raise ValueError("至少需要指定一个图标尺寸")
    if any(size < 1 or size > 256 for size in normalized):
        raise ValueError("图标尺寸必须在 1 到 256 像素之间")
    return normalized


def convert_svg_to_ico(
    svg_path: Path,
    output_path: Path | None = None,
    sizes: Sequence[int] = DEFAULT_SIZES,
) -> Path:
    """Convert *svg_path* to a transparent, multi-size ICO and return its path."""
    svg_path = svg_path.expanduser().resolve()
    if not svg_path.is_file():
        raise FileNotFoundError(f"找不到 SVG 文件：{svg_path}")
    if svg_path.suffix.lower() != ".svg":
        raise ValueError(f"输入文件必须是 .svg：{svg_path}")

    output_path = (
        output_path.expanduser().resolve()
        if output_path is not None
        else svg_path.with_suffix(".ico")
    )
    if output_path.suffix.lower() != ".ico":
        raise ValueError(f"输出文件必须使用 .ico 扩展名：{output_path}")
    if not output_path.parent.is_dir():
        raise FileNotFoundError(f"输出目录不存在：{output_path.parent}")

    icon_sizes = _validate_sizes(sizes)
    Image, svg_to_bytes = _load_dependencies()

    svg_text = svg_path.read_text(encoding="utf-8")
    largest_size = max(icon_sizes)
    png_data = svg_to_bytes(
        svg_string=svg_text,
        width=largest_size,
        height=largest_size,
    )

    with Image.open(io.BytesIO(png_data)) as rendered:
        image = rendered.convert("RGBA")

    # ICO supports several embedded resolutions; Pillow produces each one from
    # this high-resolution RGBA source while retaining SVG transparency.
    image.save(output_path, format="ICO", sizes=[(size, size) for size in icon_sizes])
    return output_path


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="将 SVG 转换为包含多个尺寸的 Windows ICO 图标。"
    )
    parser.add_argument(
        "svg",
        nargs="?",
        type=Path,
        default=Path("svg1.svg"),
        help="输入的 SVG 文件（默认：svg1.svg）",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="输出的 ICO 文件（默认：与输入文件同名）",
    )
    parser.add_argument(
        "--sizes",
        nargs="+",
        type=int,
        default=DEFAULT_SIZES,
        metavar="PX",
        help="写入 ICO 的尺寸列表，范围 1-256",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    try:
        output_path = convert_svg_to_ico(args.svg, args.output, args.sizes)
    except (FileNotFoundError, OSError, RuntimeError, ValueError) as exc:
        print(f"转换失败：{exc}", file=sys.stderr)
        return 1

    print(f"转换成功：{output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
