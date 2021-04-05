from pathlib import Path
import os
import subprocess
import re
import sys
from shutil import copy2
from multiprocessing import Pool
import fire

style_sheet = Path(__file__).parent / 'pandoc.css'


def append_relative_path(input_string, file_dir='.', figure_dir='.'):
        pat = f'({figure_dir}\/.*?\.[\w:]+)'
        image_filenames = re.findall(pat, input_string)
        for im_file in image_filenames:
            new_path = str(file_dir / im_file)
            input_string = input_string.replace(im_file, new_path)
        return input_string


def replace_equation_refs(data):
    """
    equation references from <https://github.com/tomduck/pandoc-eqnos> damage docx word files
    This function removes equation references and replaces them with equation numbers
    """
    eqs = re.findall('\{\#eq:.+\}', data)
    refs = {eq.replace('#', '@'): str(idx+1) for idx,eq in enumerate(eqs)}
    data_doc = data

    # replace references with numbers
    for old_eq, new_eq in refs.items():
        data_doc = data_doc.replace(old_eq, new_eq)

    # remove equation labels which damage the docx file
    for idx, eq in enumerate(eqs):
        data_doc = data_doc.replace(eq, f'({idx+1})')
    return data_doc

def file_to_str(infile):
    with open(infile) as file:
        try:
            return file.read()
        except:
            Warning(f"Issue reading: {infile}")
            return None


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
    infile = Path(infile)
    outfile = infile.parent / f'{infile.stem}{output_ext}'

    print(infile, '->', outfile)
    input_string = file_to_str(infile)

    if update_links:
        input_string = input_string.replace(infile.suffix, output_ext)

    if output_ext=='.docx':
        # Currently this assumes that there is a folder next to the file called figures containing all of the figures
        # this is only relevant when converting to .docx files to tell them where to find the figures relative 
        # to the working directory where pandoc was called from
        input_string = append_relative_path(input_string, infile.parent, 'figures')
        input_string = replace_equation_refs(input_string)

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


if __name__ == '__main__': fire.Fire(convert_all)
