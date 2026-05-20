# Diff2HTML

Python's difflib is a great standard library feature.

But I wanted a command line version.

## Installation

```
pip install diff2html
```

## Usage

```
diff2html fileA fileB --output diff.html
firefox diff.html
```

## Full help

```
usage: Compare two files and produce a well formatted diff in an HTML file.

A command line wrapper for Python's difftool.

       [-h] [-l STRIP_LEFT] [-r STRIP_RIGHT] [-t TITLE] [-n NOTES] [-o OUTPUT]
       left right

positional arguments:
  left                  The first file to compare.
  right                 The second file to compare.

options:
  -h, --help            show this help message and exit
  -l, --left-strip STRIP_LEFT
                        Regex expression acting on the left hand side of the
                        diff
  -r, --right-strip STRIP_RIGHT
                        Regex expression acting on the right hand side of the
                        diff
  -t, --title TITLE     Add a title to the page, other than the names of the
                        files being compared. If set the names of the files
                        being compared will be added as a subtitle.
  -n, --notes NOTES     Additional notes to be added below the title and
                        subtitle.
  -o, --output OUTPUT   Output file path. If unset output will be printed to
                        stdout.
```
