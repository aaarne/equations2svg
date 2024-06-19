import latextools
from latextools import LatexCommand
import yaml
import os
from termcolor import colored

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
        print(f"{colored("skip", "green")}\t{name} (found {filename})")
        continue
    else:
        print(f"{colored("render", "red")}\t{name}\t==>\t{filename}")
    render(filename, code)
