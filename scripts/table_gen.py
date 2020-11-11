import os

from pathlib import Path

def parse_one_line(line):
    if 'SUCC' in line:
        tags = line.strip().split()[2]
        parts = tags.strip().split('-')
        version = '-'.join(parts[:-3])
        target, subtarget, ty = parts[-3], parts[-2], parts[-1]
        return (version, target, subtarget, ty), True
    elif 'FAIL' in line:
        tags = line.strip().split(',')[0].strip().split()[2]
        parts = tags.strip().split('-')
        version = '-'.join(parts[:-3])
        target, subtarget, ty = parts[-3], parts[-2], parts[-1]
        return (version, target, subtarget, ty), False
    else:
        return None

def main():
    batch_rslts = {}

    log_dir = Path('../batch_log')
    log_files = log_dir.rglob('*.log')

    for log_file in log_files:
        with open(str(log_file.absolute()), 'r') as f:
            for line in f.readlines():
                rslt = parse_one_line(line)
                if rslt != None:
                    k, v = rslt
                    if batch_rslts.get(k, None) == None:
                        batch_rslts[k] = v
                    else:
                        batch_rslts[k] = batch_rslts[k] | v

    outputs = []
    succ, whole = 0, 0
    for k, v in batch_rslts.items():
        version, target, subtarget, ty = k
        progress = 'SUCC' if v else 'FAIL'
        outputs.append("|%s|%s|%s|%s|%s|" % (target, subtarget, version, ty, progress))
        succ = succ + (1 if v else 0)
        whole = whole + 1
    outputs.sort()
    outputs.append("|%s|%s|%s|%s|%s/%s|" % ('-', '-', '-', '-', succ, whole))

    with open('../detailed_progress.md', 'w') as f:
        f.write('''\
|   target   |   subtarget   |   openwrt version   |   type   |   progress   |
|:----------:|:-------------:|:-------------------:|:--------:|:------------:|
'''
)
        f.write('\n'.join(outputs))


if __name__ == '__main__':
    main()