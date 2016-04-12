"""Utils to generate encounter menus

This package contains utils to build API for generating "menus". The menu
(represented by AdvancedMenu object) contains list of options and each of them
can have it's own requirements and outcomes. It is possible to create separate
menu object for each menu you generate or use single instance and clear it with
.start method.

option module contains several Option classes which you can combine & inherit to
make your own custom Option.
"""
