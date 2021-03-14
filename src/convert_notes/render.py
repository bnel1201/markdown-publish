from pathlib import Path
import os
import subprocess
import sys
from shutil import copy2
from multiprocessing import Pool

style_sheet = Path(__file__).parent / 'pandoc.css'


def convert_file(infile, output_ext='.html', update_links=True, f='markdown', t='html5', extra_args=None):
    """
    convert_file
    ---
    parameters:
        required:
        - infile: file to be converted

        optional:
        - output_ext: the desired output file extension e.g. '.html' or '.docx'
        - update_links: convert file hyperlinks to `output_ext`, useful if converting multiple documents using `convert_all`
        - f: from format, the input format (same as Pandoc)
        - t: to from format, the output format (same as Pandoc)
        - extra_args: filters, flags, or other arguments to pass to Pandoc e.g. `--citeproc` or `--mathjax`, see <https://pandoc.org/MANUAL.html> for more info
    """
    outfile = infile.parent / f'{infile.stem}{output_ext}'
    print(infile, '->', outfile)
    with open(infile) as file:
        try:
            input_string = file.read()
        except:
            Warning(f"Issue reading: {infile}")
            return None

    if update_links:
        input_string = input_string.replace(infile.suffix, output_ext)

    tempfile = infile.parent / f'{infile.stem}_temp{infile.suffix}'
    with open(tempfile, 'w') as file:
        file.write(input_string)
    nparents = len(outfile.parents)
    style_loc = f'../'*(nparents-1) + f'{style_sheet.stem}{style_sheet.suffix}'
    cmd = f'pandoc -s "{tempfile}" -f {f} -t {t} -c {style_loc} -o "{outfile}" --mathjax'
    if extra_args:
        cmd += ' '+extra_args
    subprocess.call(cmd)
    os.remove(tempfile)    
    return outfile


def convert_all(root_dir='.', ext='.md', pool=False, ignore=[], **kwargs):
    """
    convert_all
    ---
    parameters:
        optional:
        - root_dir: directory containing files to be converted, defaults to current path
        - ext: filter for only files ending in this extension, e.g.: '.md' for all markdown files notes.md, outline.md, ...
        - pool: True to enable multiprocessing
        - output_ext: the desired output file extension e.g. '.html' or '.docx'
        - update_links: convert file hyperlinks to `output_ext`, useful if converting multiple documents using `convert_all`
        - f: from format, the input format (same as Pandoc)
        - t: to from format, the output format (same as Pandoc)
        - extra_args: filters, flags, or other arguments to pass to Pandoc e.g. `--citeproc` or `--mathjax`, see <https://pandoc.org/MANUAL.html> for more info
    """
    copy2(style_sheet, root_dir)
    ignore = list(map(Path, ignore))
    all_files = [file for file in Path(root_dir).rglob(f'*{ext}') if file not in ignore]
    if pool:
        all_files = list(all_files)
        with Pool(5) as p:
            p.map(convert_file, all_files, **kwargs)
    else:
        return [convert_file(file, **kwargs) for file in all_files]


if __name__ == '__main__':
    path = Path('.')
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    convert_all(path)