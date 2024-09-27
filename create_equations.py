import latextools
from latextools import LatexCommand
import yaml
import os
from termcolor import colored
import subprocess
from pathlib import Path
import pickle

vcsfile = Path("vcs")

if vcsfile.is_file():
    with open(vcsfile, "rb") as f:
        vcs = pickle.load(f)

    print(f"{colored('vcs', 'yellow')}\tloaded")
else:
    vcs = {}

def shortcut(short, long):
    cmd = r"\newcommand{\%s}{%s}" % (short, long)
    return LatexCommand(None, cmd, packages=[latextools.pkg.amsmath])

commands = [
    latextools.cmd.all_math,
    LatexCommand(None, r"\newcommand{\bs}[1]{\boldsymbol{#1}}", packages=[latextools.pkg.amsmath]),
    LatexCommand(None, r"\renewcommand{\b}[1]{\boldsymbol{#1}}", packages=[latextools.pkg.amsmath]),
]

with open("equations.yaml") as f:
    equations = yaml.safe_load(f)

forced_render = equations.get('force_render', [])

def render(filename, code):
    rendered = latextools.render_snippet(
        content="$" + code + "$", 
        commands=commands,
    )
    rendered.as_svg().save(filename)

for name, code in equations['shortcuts'].items():
    commands.append(shortcut(name, code))
    print(f"{colored("cmd", "yellow")}\t{name}")

for name, code in equations.items():
    filename = f"equations/{name}.svg"
    if name in ['shortcuts', 'force_render']:
        continue
    elif name in forced_render:
        print(f"{colored("force", "red")}\t{name}\t==>\t{filename}")
    elif os.path.exists(filename):
        if name in vcs:
            if vcs[name] == code and os.path.exists(filename):
                print(f"{colored("skip", "green")}\t{name} (unchanged)")
                continue
            else:
                print(f"{colored("render", "red")}\t{name}\t==>\t{filename} (code changed)")
        else:
            print(f"{colored("render", "red")}\t{name}\t==>\t{filename} (no record)")
    else:
            print(f"{colored("render", "red")}\t{name}\t==>\t{filename} (new)")
    render(filename, code)
    vcs[name] = code
    print(f"{colored("rasterize", "yellow")}\t{filename}")
    cmd = ['inkscape', '--export-type=PNG', '--export-dpi=600', filename]
    subprocess.run(cmd)

with open("vcs", "wb") as f:
    pickle.dump(vcs, f)
    print(f"{colored('vcs', 'yellow')}\toveridden")