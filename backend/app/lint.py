import subprocess


"""Script to run pre-commit hooks on all files using poetry."""


def main() -> None:
    """Execute pre-commit hooks on all files using poetry.

    Raises:
        subprocess.CalledProcessError: If the pre-commit command fails
    """
    try:
        result = subprocess.run(
            ["poetry", "run", "pre-commit", "run", "--all-files"],
            check=False,
            text=True,
        )
        if result.returncode != 0:
            print(f"Pre-commit checks failed with exit code {result.returncode}")
            exit(result.returncode)
    except Exception as e:
        print(f"An error occurred while running pre-commit: {e}")
        exit(1)


if __name__ == "__main__":
    main()
