import argparse
from pathlib import Path
from typing import List, Optional, Tuple

from ryans_cpp_transpiler.complainers import ALL_COMPLAINERS, Complaint
from ryans_cpp_transpiler.converters import ALL_CONVERTERS
from ryans_cpp_transpiler.utils.string_replace import (
    batch_string_replace,
    make_inline_record_index,
)
from ryans_cpp_transpiler.utils.types import (
    ConvertedPartialTxt,
    FormattedSlice2,
    OriginalSlice2,
    OriginalTxt,
)


def askyn(question: str, default: Optional[bool] = None) -> bool:
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
        file_txt: OriginalTxt = f.read()
        file_idxs, file_squished = make_inline_record_index(file_txt)

    # Run all Converters
    replacements: List[Tuple[OriginalSlice2, ConvertedPartialTxt]] = []
    for converter in ALL_CONVERTERS:
        replacements_new: List[
            Tuple[FormattedSlice2, ConvertedPartialTxt]
        ] = converter.from_cpp(file_squished)
        replacements += [
            ((file_idxs[sl[0]], file_idxs[sl[1]]), t) for sl, t in replacements_new
        ]

    # Make the replacements
    new_txt = batch_string_replace(file_txt, replacements=replacements)

    # Save the new file
    if renamed.is_file():
        if askyn(f"Are you sure you want to overwrite {renamed}"):
            with renamed.open("w") as f:
                f.write(new_txt)
        else:
            print(f"Skipping {file}")
    else:
        with renamed.open("w") as f:
            f.write(new_txt)


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
        file_txt: OriginalTxt = f.read()
        file_idxs, file_squished = make_inline_record_index(file_txt)

    # Run all Complainers
    complaints: List[Complaint] = []
    for complainer in ALL_COMPLAINERS:
        complaints += complainer.check(file_squished, converter=file_idxs)

    # Run all Converters
    replacements: List[Tuple[OriginalSlice2, ConvertedPartialTxt]] = []
    for converter in ALL_CONVERTERS:
        replacements_new: List[
            Tuple[FormattedSlice2, ConvertedPartialTxt]
        ] = converter.to_cpp(file_squished)
        replacements += [
            ((file_idxs[sl[0]], file_idxs[sl[1]]), t) for sl, t in replacements_new
        ]

    # Make the replacements
    new_txt = batch_string_replace(file_txt, replacements=replacements)

    # Save the new file
    if renamed.is_file():
        if askyn(f"Are you sure you want to overwrite {renamed}"):
            with renamed.open("w") as f:
                f.write(new_txt)
        else:
            print(f"Skipping {file}")
    else:
        with renamed.open("w") as f:
            f.write(new_txt)


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
