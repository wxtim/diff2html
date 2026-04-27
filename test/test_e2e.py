from pathlib import Path
from shlex import split
from subprocess import run


REPO = Path(__file__).parent.parent
KGO = REPO / 'test/example/example.html'

COMMAND = split("""./diff_to_html \
                test/example/foo1 \
                test/example/foo2 \
                --left-strip /some/very/long/path/to/a/ \
                --right-strip /another/very/long/path/to/a/ \
                --title "My Diff"
""")


def test_example():
    f"""Test example output against KGO

    Runs, from home of repo:

    {COMMAND}

    To update test, copy and add:

    --output test/example/example.html \

    """
    result = run(COMMAND, capture_output=True, cwd=str(REPO))

    assert result.returncode == 0

    for res, kgo in zip(
        result.stdout.decode().split('\n'),
        (KGO).read_text().split('\n')
    ):
        assert res == kgo, f'{res} != {kgo}'
