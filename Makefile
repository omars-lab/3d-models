# https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_OpenSCAD_in_a_command_line_environment
# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html

.PHONY: cookie-cutters

openscad := /Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD

%.png: %.scad
	${openscad} -o $*.png $*.scad

cookie-cutters:
	make -f ./Makefile CookieCutter-Arabesque.png
	make -f ./Makefile CookieCutter-Mosque.png
