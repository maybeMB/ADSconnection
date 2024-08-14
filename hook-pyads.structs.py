# -*- coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

# 收集 pyads.structs 包下的所有子模块
hiddenimports = collect_submodules('pyads.structs')
