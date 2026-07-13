from io import StringIO

import pytest

from darija_tools.cli import main


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["normalize", "طريق ٧", "--normalize-digits"], "طريق 7\n"),
        (["normalize", "  دار\t دار  ", "--collapse-whitespace"], "دار دار\n"),
        (["translit", "bghit taxi", "--keep-loanwords"], "بغيت taxi\n"),
    ],
)
def test_cli_exposes_library_options(argv, expected, capsys):
    assert main(argv) == 0
    assert capsys.readouterr().out == expected


def test_cli_combines_normalization_options(capsys):
    assert (
        main(
            [
                "normalize",
                "  طريق\t٧  ",
                "--normalize-digits",
                "--collapse-whitespace",
            ]
        )
        == 0
    )
    assert capsys.readouterr().out == "طريق 7\n"


def test_cli_options_remain_opt_in(capsys):
    assert main(["normalize", "طريق ٧"]) == 0
    assert capsys.readouterr().out == "طريق ٧\n"

    assert main(["translit", "taxi"]) == 0
    assert capsys.readouterr().out == "تاكسي\n"


def test_cli_options_work_with_stdin(monkeypatch, capsys):
    monkeypatch.setattr("sys.stdin", StringIO("bghit taxi\n"))
    assert main(["translit", "--keep-loanwords"]) == 0
    assert capsys.readouterr().out == "بغيت taxi\n"
