#!/usr/bin/env python
"""Compare two files and produce a well formatted diff in an HTML file.

A command line wrapper for Python's difftool.
"""

import argparse
from difflib import HtmlDiff
from pathlib import Path
import re
from typing import Optional


class DiffDoc:
    """A container to keep HTML bric-a-brac tidy. Provides a single
    class methods convert a diff to an HTML page.
    """
    # Create an additional explanation of the webpage:
    BACKBUTTON = '<br><button onclick="history.back()">Go Back</button><br>'
    HEAD1 = '<h1>{}</h1>'
    HEAD3 = '<h3>{}</h3>'
    HEAD = """
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

    <html>

    <head>
        <meta http-equiv="Content-Type"
            content="text/html; charset=utf-8" />
        <title></title>
        <style type="text/css">
            h1, h2, h3 {
                font-family: Consolas, Sans, sans-serif
            }
            #code {
                font-family: 'Jetbrains Mono', consolas, 'Courier New', monospace;
            }
            table {
                font-family: 'Jetbrains Mono', consolas, 'Courier New', monospace;
                border-style: solid;
                border-width: 2px;
                margin-top: 5px;
            }
            .legend,
            .legend th,
            .legend td {
                border-style: none;
            }
            td.diff_header {
                text-align:right;
            }
            .diff_next {
                border-left-style: solid;
                border-left-color: black;
                border-left-width: 3px;
            }
            .diff_add {background-color:#aaffaa}
            .diff_chg {background-color:#ffff77}
            .diff_sub {background-color:#ffaaaa}
        </style>
    </head>
    """

    KEYTABLE = """
        <table class="diff" summary="Legends" id="legend">
            <tr> <th colspan="2"> Legends </th> </tr>
            <tr> <td> <table border="" summary="Colors">
                        <tr><th> Colors </th> </tr>
                        <tr><td class="diff_add">&nbsp;Added&nbsp;</td></tr>
                        <tr><td class="diff_chg">Changed</td> </tr>
                        <tr><td class="diff_sub">Deleted</td> </tr>
                    </table></td>
                <td> <table border="" summary="Links">
                        <tr><th colspan="2"> Links </th> </tr>
                        <tr><td>(f)irst change</td> </tr>
                        <tr><td>(n)ext change</td> </tr>
                        <tr><td>(t)op</td> </tr>
                    </table></td> </tr>
        </table>
    """

    TAIL = """
            </body>
        </html>
    """

    @classmethod
    def diff_to_html(
        cls, left, right, title, left_title, right_title, subtitle
    ):
        # Carry out comparison:
        htmldiff = HtmlDiff()
        html_data = htmldiff.make_table(
            left,
            right,
            fromdesc=left_title,
            todesc=right_title
        )

        output = (
            cls.HEAD
            + cls.BACKBUTTON
            + cls.HEAD1.format(title)
            + f'{cls.HEAD3.format(subtitle) if subtitle else ""}'
            + html_data
            + cls.BACKBUTTON
            + cls.KEYTABLE
            + cls.TAIL
        )
        return output


def parse_args():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument('left', help='The first file to compare.')
    parser.add_argument('right', help='The second file to compare.')
    parser.add_argument(
        '-l', '--left-strip',
        help='Regex expression acting on the left hand side of the diff',
        dest='strip_left'
    )
    parser.add_argument(
        '-r', '--right-strip',
        help='Regex expression acting on the right hand side of the diff',
        dest='strip_right'
    )
    parser.add_argument(
        '-t', '--title',
        help=(
            'Add a title to the page, other than the names of the files'
            ' being compared. If set the names of the files being compared'
            ' will be added as a subtitle.'
        )
    )
    parser.add_argument(
        '-n', '--notes',
        help='Additional notes to be added below the title and subtitle.'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output file path. If unset output will be printed to stdout.',
        dest='output'
    )
    return parser.parse_args()


def read_file(filepath: Path, sub: Optional[str] = None) -> list[str]:
    """Read file and carry out substutions on lines.

    Returns a list of strings.
    """
    lines = Path(filepath).read_text().split('\n')
    if sub:
        lines = [re.sub(sub, '', line) for line in lines]
    return lines


def main():
    # Parse command line args and environment variables:
    opts = parse_args()

    parsed_html = DiffDoc.diff_to_html(
        read_file(opts.left, opts.strip_left),
        read_file(opts.right, opts.strip_right),
        opts.title or f'{opts.left} vs {opts.right}',
        opts.left,
        opts.right,
        f'{opts.left} vs {opts.right}' if opts.title else None
    )

    if opts.output:
        # Write html file
        Path(opts.output).write_text(parsed_html)
    else:
        print(parsed_html)


if __name__ == '__main__':
    main()
