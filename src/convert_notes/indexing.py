from pathlib import Path
from datetime import datetime


def update_research_index():
    researchdir = Path('_research')
    entries = [e for e in researchdir.rglob('*.md')]
    unique_dates = list({str(e).split('\\')[1] for e in entries})
    unique_dates.sort()
    dated_entry_dict = {date: [str(e) for e in entries if date in str(e)] for date in unique_dates}

    header = '---\ntitle: Research Updates\n' + f"date: {datetime.now().strftime('%Y-%m-%d')}" + '\n---\n\n'
    header = header + '[Back to main Readme](../README.md)\n\n'
    index = ''
    for date, entries in dated_entry_dict.items():
        index += f'## {date} \n\n'
        for idx, entry in enumerate(entries):
            entry_path = '\\'.join(str(entry).split('\\')[1:])
            entry_path = entry_path.replace(' ', '%20')
            if len(entries) > 1:
                index += f'{idx + 1}. '
            index += '[' + Path(entry).stem + ']' + '(' + entry_path + ')\n\n'

    index = header + index

    with open('_research/research_index.md', 'w') as f:
        f.write(index)

if __name__ == "__main__":
    update()
