import os
import sys

project = 'HuaBook'
author = 'You'
release = '1.0'

extensions = [
    'myst_parser',
]

source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

master_doc = 'index'

html_theme = 'sphinx_rtd_theme'

latex_engine = 'xelatex'

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',
    'fontpkg': r'''
\usepackage{fontspec}
\setmainfont{CMU Serif}
\setsansfont{CMU Sans Serif}
''',
}

latex_documents = [
    ('index', 'huabook.tex', 'Huawei SUN2000 Book', 'You', 'manual'),
]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
