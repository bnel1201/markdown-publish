# Note Converter: a simple package for publishing linked markdown into html

all files in a directory are converted and markdown links updated to html links similar to org-mode publish

## converting all files in a directory using pandoc


`for f in *.org; do pandoc "$f" -s -o "${f%.org}.md"; done`

The issue is that this does not update the link extensions

## TODO

add a sample make file to show how to only update files that have been changed rather than re-run everything