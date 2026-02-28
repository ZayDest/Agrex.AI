"""
enhanced_transistor_detection.py
--------------------------------

This script provides a simple command‑line interface for detecting
transistor‑shaped contours within an image.  It is based on the
original Jupyter notebook in the `Agrex.AI` repository but has been
refactored to be reusable from the command line and improved in a
number of ways:

* **Modular functions**: The detection logic is encapsulated in
  functions so that it can be imported and reused.
* **Automatic thresholding**: If no threshold is specified the script
  uses Otsu’s method to determine a suitable binary threshold
  automatically.  A manual threshold can still be provided via
  `--threshold`.
* **Configurable cropping**: Some images may contain large borders
  around the region of interest.  The `--crop` argument lets you
  specify a rectangle (x1 y1 x2 y2) to crop the image before
  processing.
* **Command‑line interface**: Run the script from a terminal and
  specify the input image, output path and optional parameters.
* **Visualisation**: Rectangles are drawn around each detected
  transistor.  The result can either be displayed in a window or
  written to disk.

Example usage::

    python enhanced_transistor_detection.py path/to/image.jpg --crop 100 200 800 1200 --save result.jpg

The script prints the number of detected transistors and saves the
annotated image to ``result.jpg``.  If ``--save`` is omitted the
image will be displayed on screen.

"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import List, Tuple, Optional

import cv2
import numpy as np


@dataclass
class DetectionResult:
    """Data structure to hold detection results."""

    boxes: List[Tuple[int, int, int, int]]  # List of bounding boxes (x, y, w, h)
    annotated_image: np.ndarray              # Image with rectangles drawn


def detect_transistors(
    image: np.ndarray,
    threshold: Optional[int] = None,
    crop: Optional[Tuple[int, int, int, int]] = None,
    kernel_size: int = 3,
    morph_iterations: int = 2,
) -> DetectionResult:
    """Detect transistor‑like contours in an image.

    Args:
        image: Input image (as a NumPy array, BGR format).
        threshold: Optional fixed threshold for binarisation.  If
            ``None`` (default) the threshold will be computed using
            Otsu’s method.
        crop: Optional cropping rectangle given as ``(x1, y1, x2, y2)``.
        kernel_size: Size of the structuring element used for
            morphological opening.
        morph_iterations: Number of times to apply morphological
            opening.

    Returns:
        DetectionResult containing bounding boxes and annotated image.
    """
    # Crop image if coordinates provided
    if crop is not None:
        x1, y1, x2, y2 = crop
        image = image[y1:y2, x1:x2].copy()

    # Convert to grayscale and blur to reduce noise
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding (Otsu’s method if threshold not provided)
    if threshold is None:
        _, thresh = cv2.threshold(
            blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
        )
    else:
        _, thresh = cv2.threshold(blurred, threshold, 255, cv2.THRESH_BINARY)

    # Morphological opening to remove small noise
    kernel = np.ones((kernel_size, kernel_size), np.uint8)
    morph = cv2.morphologyEx(
        thresh, cv2.MORPH_OPEN, kernel, iterations=morph_iterations
    )

    # Find contours
    contours, _ = cv2.findContours(
        morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    # Compute bounding boxes
    boxes: List[Tuple[int, int, int, int]] = []
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        boxes.append((x, y, w, h))

    # Draw boxes on a copy of the image
    annotated = image.copy()
    for x, y, w, h in boxes:
        cv2.rectangle(annotated, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return DetectionResult(boxes=boxes, annotated_image=annotated)


def parse_crop_arg(crop_str: Optional[List[int]]) -> Optional[Tuple[int, int, int, int]]:
    """Parse crop argument from CLI into a tuple.

    Expects a list of four integers representing x1 y1 x2 y2.
    """
    if crop_str is None:
        return None
    if len(crop_str) != 4:
        raise ValueError(
            "--crop must be four integers: x1 y1 x2 y2"
        )
    x1, y1, x2, y2 = map(int, crop_str)
    if x2 <= x1 or y2 <= y1:
        raise ValueError("Invalid crop coordinates: ensure x2 > x1 and y2 > y1")
    return (x1, y1, x2, y2)


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Detect transistor‑shaped contours in an image and optionally "
            "save the annotated output."
        )
    )
    parser.add_argument(
        "image",
        help="Path to the input image",
    )
    parser.add_argument(
        "--threshold",
        type=int,
        default=None,
        help=(
            "Manual threshold for binary segmentation (0–255). "
            "If omitted, Otsu’s method is used."
        ),
    )
    parser.add_argument(
        "--crop",
        nargs=4,
        type=int,
        metavar=("x1", "y1", "x2", "y2"),
        help="Optional crop rectangle to limit the region of interest",
    )
    parser.add_argument(
        "--save",
        metavar="OUTPUT",
        help="Path to save the annotated image. If omitted, a window will show the result",
    )
    args = parser.parse_args()

    # Read image
    image = cv2.imread(args.image)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {args.image}")

    crop_rect = parse_crop_arg(args.crop)

    result = detect_transistors(
        image=image,
        threshold=args.threshold,
        crop=crop_rect,
    )

    print(f"Detected {len(result.boxes)} potential transistors")

    if args.save:
        cv2.imwrite(args.save, result.annotated_image)
        print(f"Annotated image saved to {args.save}")
    else:
        # Display result in a window
        cv2.imshow("Transistor Detection", result.annotated_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()