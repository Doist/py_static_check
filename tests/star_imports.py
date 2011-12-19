"""
You can define a file that resolves star imports.
Pyflakes will ignore files that have star imports!
"""
import os
STAR_IMPORTS = {
    'os': os.__all__,
}
