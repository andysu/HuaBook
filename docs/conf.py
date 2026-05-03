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

# --- PDF SETTINGS (rinohtype) ---
extensions.append('rinoh.frontend.sphinx')

rinoh_documents = [('index', 'huabook', 'Huawei SUN2000 Book', 'You', 'manual')]

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
