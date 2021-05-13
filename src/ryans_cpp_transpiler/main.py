import argparse
from collections import defaultdict
from pathlib import Path
from typing import DefaultDict, List, Optional, Tuple, TypeVar

from iregex import Regex

from ryans_cpp_transpiler.complainers import ALL_COMPLAINERS
from ryans_cpp_transpiler.converters import ALL_CONVERTERS
from ryans_cpp_transpiler.utils.string_replace import batch_string_replace
from ryans_cpp_transpiler.utils.types import (
    Complaint,
    ConvertedPartialTxt,
    ConvertedTxt,
    HasContext,
    OriginalIdx,
    OriginalSlice,
    OriginalTxt,
    PartialIdx,
    PartialSlice,
    PartialTxt,
)

# ================= Utilities ===============


def _askyn(question: str, default: Optional[bool] = None) -> bool:
    """
    Asks a yes or no question and returns a bool.
    REF: https://gist.github.com/garrettdreyfus/8153571
    """
    # Modify the question with the default value capitalized
    if default is not None:
        if default:
            question += " [Y/n]: "
        else:
            question += " [y/N]: "
    else:
        question += " [y/n]: "

    # Iterate until an answer is determined
    while True:
        reply = str(input(question).lower().strip())
        if reply == "" and default is not None:
            return default
        elif reply in ("y", "yes"):
            return True
        if reply in ("n", "no"):
            return False
        else:
            print(f"Unrecognized answer: '{reply}'")


def _optional_overwrite(file_path: Path, new_txt: ConvertedTxt) -> None:
    """Writes `new_txt` to `renamed`, but asks the user if their is already a file it would otherwise overwrite."""
    if file_path.is_file():
        if _askyn(f"Are you sure you want to overwrite {file_path}?"):
            with file_path.open("w") as f:
                f.write(new_txt)
        else:
            print(f"Skipping {file_path}")
    else:
        with file_path.open("w") as f:
            f.write(new_txt)


def _partial_idx_to_original(idx: PartialIdx, start_idx: OriginalIdx) -> OriginalIdx:
    """
    Converts a PartialIdx to an OriginalIdx using the start_idx.

    Very simple function I know but it avoids type and variable ambiguity.
    """
    return OriginalIdx(idx + start_idx)


# ============== Converters / Complainers ==============

T = TypeVar("T", bound=HasContext)


def _get_all_contexts(all: List[T]) -> DefaultDict[Regex, List[T]]:
    """
    Gets all contexts from the list of HasContext objects, and returns a dictionary mapping between context and all
    objects using that context.
    """
    by_context: DefaultDict[Regex, List[T]] = defaultdict(list)
    for c in all:
        by_context[c.context].append(c)
    return by_context


def _handle_converters(
    file_txt: OriginalTxt, to_cpp: bool
) -> List[Tuple[OriginalSlice, ConvertedPartialTxt]]:
    """Handles all converters and returns the replacements made by those converters."""
    # First we will get all contexts of all the converters
    converters_by_context = _get_all_contexts(ALL_CONVERTERS)
    # This will get all replacements via the converters
    replacements: List[Tuple[OriginalSlice, ConvertedPartialTxt]] = []
    for context, converters in converters_by_context.items():
        for match in context.compile().finditer(file_txt):
            for converter in converters:
                # Pick the converter function based on the boolean variable
                f = converter.to_cpp if to_cpp else converter.from_cpp

                # Get the replacements from the converter
                replacements_new: List[Tuple[PartialSlice, ConvertedPartialTxt]] = f(
                    PartialTxt(file_txt[match.start() : match.end()])
                )

                # Add replacements converted to original idx format
                replacements += [
                    (
                        (
                            _partial_idx_to_original(
                                beginning, start_idx=OriginalIdx(match.start())
                            ),
                            _partial_idx_to_original(
                                end, start_idx=OriginalIdx(match.start())
                            )
                            + 1,
                        ),
                        t,
                    )
                    for (beginning, end), t in replacements_new
                ]

    return replacements


def _handle_complaints(file_txt: OriginalTxt) -> List[Complaint]:
    """Handles all complainers and returns the complaints made by those complainers."""
    # First we will get all contexts of all the converters
    complainers_by_context = _get_all_contexts(ALL_COMPLAINERS)

    # This will get all replacements via the converters
    complaints: List[Complaint] = []
    for context, complainers in complainers_by_context.items():
        if context is None:
            context = Regex().anything()
        for match in context.compile().finditer(file_txt):
            for complainer in complainers:
                complaints += complainer.check_rcpp(
                    original_txt=file_txt,
                    context_range=(match.start(), match.end() + 1),
                )

    return complaints


# =============== From / To CPP ==============


def _from_cpp(file: Path) -> None:
    """from_cpp but for one file at a time."""
    # Some impossible assertions
    assert file.is_file(), f"{str(file)} does not exist."

    # Create the replacement file name
    if file.suffix == ".cpp":
        renamed: Path = file.with_suffix(".rcpp")
    elif file.suffix == ".hpp":
        renamed = file.with_suffix(".rhpp")
    else:
        raise TypeError(f"Extension not in (.cpp, .hpp), found {file.suffix}")

    # Read the file
    with file.open("r") as f:
        file_txt: OriginalTxt = OriginalTxt(f.read())

    # ====== Run all Converters ======
    replacements = _handle_converters(file_txt, to_cpp=False)

    # Make the replacements
    new_txt = batch_string_replace(file_txt, replacements=replacements)

    # Save the new file
    _optional_overwrite(renamed, new_txt)


def from_cpp(args: argparse.Namespace) -> None:
    """Converts all the files found via args.filepath into rcpp/rhpp from cpp/hpp."""
    filepath = Path(args.filepath)
    if filepath.is_file():
        files: List[Path] = [filepath]
    elif filepath.is_dir():
        files = list(filepath.glob("*.cpp")) + list(filepath.glob("*.hpp"))
        if not files:
            raise FileNotFoundError(f"No files exist matching {args.filepath}")
    else:
        files = list(Path().glob(args.filepath))
        if not files:
            raise FileNotFoundError(f"No files exist matching {args.filepath}")
    for f in files:
        _from_cpp(f)


def _to_cpp(file: Path) -> None:
    """to_cpp but for one file at a time."""
    # Some impossible assertions
    assert file.is_file(), f"{str(file)} does not exist."

    # Create the replacement file name
    if file.suffix == ".rcpp":
        renamed: Path = file.with_suffix(".cpp")
    elif file.suffix == ".rhpp":
        renamed = file.with_suffix(".hpp")
    else:
        raise TypeError(f"Extension not in (.rcpp, .rhpp), found {file.suffix}")

    # Read the file
    with file.open("r") as f:
        file_txt: OriginalTxt = OriginalTxt(f.read())

    # ====== Run all Complainers ======
    complaints = _handle_complaints(file_txt)

    if complaints:
        print("Complaints Found:")
        print()
        for c in complaints:
            print(str(c))
            print()
        exit(1)

    # ====== Run all Converters ======
    replacements = _handle_converters(file_txt, to_cpp=False)

    # Make the replacements
    new_txt = batch_string_replace(file_txt, replacements=replacements)

    # Save the new file
    _optional_overwrite(renamed, new_txt)


def to_cpp(args: argparse.Namespace) -> None:
    """Converts all the files found via args.filepath into cpp/hpp from rcpp/rhpp."""
    filepath = Path(args.filepath)
    if filepath.is_file():
        files: List[Path] = [filepath]
    elif filepath.is_dir():
        files = list(filepath.glob("*.rcpp")) + list(filepath.glob("*.rhpp"))
        if not files:
            raise FileNotFoundError(f"No files exist matching {args.filepath}")
    else:
        files = list(Path().glob(args.filepath))
        if not files:
            raise FileNotFoundError(f"No files exist matching {args.filepath}")
    for f in files:
        _to_cpp(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    to_parser = subparsers.add_parser(
        "to_cpp", help="Converts from rcpp/rhpp to cpp/hpp."
    )
    to_parser.add_argument("filepath")
    to_parser.set_defaults(func=to_cpp)

    from_parser = subparsers.add_parser(
        "from_cpp", help="Converts from cpp/hpp to rcpp/rhpp."
    )
    from_parser.add_argument("filepath")
    from_parser.set_defaults(func=from_cpp)

    args = parser.parse_args()
    try:
        args.func(args)
    except AttributeError:
        parser.parse_args(["-h"])
