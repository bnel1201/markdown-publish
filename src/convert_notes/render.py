from pathlib import Path
import os
import subprocess
import sys
from shutil import copy2
from multiprocessing import Pool

style_sheet = Path(__file__).parent / 'pandoc.css'


def convert_file(infile, output_ext='.html', update_links=True):
    outfile = infile.parent / f'{infile.stem}{output_ext}'
    print(infile, '->', outfile)
    with open(infile) as file:
        try:
            input_string = file.read()
        except:
            Warning(f"Issue reading: {infile}")
            return

    if update_links:
        input_string = input_string.replace(infile.suffix, output_ext)

    tempfile = infile.parent / f'{infile.stem}_temp{infile.suffix}'
    with open(tempfile, 'w') as file:
        file.write(input_string)
    nparents = len(outfile.parents)
    style_loc = f'../'*(nparents-1) + f'{style_sheet.stem}{style_sheet.suffix}'
    cmd = f'pandoc -s "{tempfile}" -f markdown -t html5 -c {style_loc} -o "{outfile}"'
    subprocess.call(cmd)
    os.remove(tempfile)    
    return outfile


def convert_all(root_dir='.', ext='.md'):
    copy2(style_sheet, root_dir)
    all_files = Path(root_dir).rglob(f'*{ext}')
    for file in all_files:
        print(file, '->', convert_file(file))

def convert_all(root_dir='.', ext='.md', pool=False):
    copy2(style_sheet, root_dir)
    all_files = Path(root_dir).rglob(f'*{ext}')
    if pool:
        all_files = list(all_files)
        with Pool(5) as p:
            p.map(convert_file, all_files)
    else:
        list(map(convert_file, all_files))


if __name__ == '__main__':
    path = Path('.')
    if len(sys.argv) > 1:
        path = Path(sys.argv[1])
    convert_all(path)