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

html_theme = 'sphinx_rtd_theme'

# --- PDF SETTINGS ---
latex_engine = 'xelatex'

latex_documents = [
    ('index', 'huabook.tex', 'Huawei SUN2000 Book', 'You', 'manual'),
]

latex_elements = {
    'papersize': 'a4paper',
    'pointsize': '11pt',

    # Підтримка кирилиці
    'fontpkg': r'''
\usepackage{fontspec}
\setmainfont{DejaVu Serif}
''',

    # Обкладинка як титульна сторінка
    'maketitle': r'''
\begin{titlepage}
\centering
\includegraphics[width=\textwidth]{cover.png}
\vfill
{\Huge HuaBook \par}
\vspace{1cm}
{\Large Huawei SUN2000 Documentation\par}
\end{titlepage}
''',
}

# щоб Sphinx бачив картинки
html_static_path = ['.']
