# https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_OpenSCAD_in_a_command_line_environment
# https://www.gnu.org/software/make/manual/html_node/Automatic-Variables.html

SHELL := /bin/bash
ROOT_DIR := $(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))

# Default openscad lib path: https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Libraries
DEP := ${HOME}/Documents/OpenSCAD/libraries/dotSCAD
# Resolve the OpenSCAD binary across install variants (versioned app, plain app, PATH).
openscad := $(shell \
	for c in \
		/Applications/OpenSCAD-*.app/Contents/MacOS/OpenSCAD \
		/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD \
		$$(command -v openscad); do \
		[ -x "$$c" ] && echo "$$c" && break; \
	done)

# gh-pages deploy
PAGES_BRANCH := gh-pages
PAGES_WORKTREE := $(ROOT_DIR)/.gh-pages
DEPLOY_PATHS := index.html build/images build/stls src LICENSE README.md

.PHONY: cookie-cutters web-images deploy

%.png: %.scad
	@echo Generating $*.png from $@
	${openscad} -o ${ROOT_DIR}/build/images/$$(basename $*.png) $*.scad

%.stl: %.scad
	@echo Generating $*.stl from $@
	${openscad} -o ${ROOT_DIR}/build/stls/$$(basename $*.stl) $*.scad

cookie-cutters:
	ls ${ROOT_DIR}/src/CookieCutters/*.scad | sed 's/.scad//g' | grep -v Common \
		| xargs -n 1 basename \
		| xargs -n 1 bash -c ' \
			cd ${ROOT_DIR}/src/CookieCutters && make -f ${ROOT_DIR}/Makefile $${0}.png $${0}.stl \
		'
clean:
	rm -rf ${ROOT_DIR}/build/images/*.png
	rm -rf ${ROOT_DIR}/build/stls/*.stl

${DEP}:
	mkdir -f $$( dirname ${DEP} )
	git clone git@github.com:JustinSDK/dotSCAD.git ${DEP}

start: ${DEP}
	open -a "OpenSCAD"

open:
	open -a "Google Chrome" ${ROOT_DIR}/index.html

index_images:
	cat <(echo -n 'var data = ' ) <(ls -1 build/images/*.png | grep -v Common | jq -R '.' | jq -s ) > data.js

# Post-process raw renders into transparent, autocropped web images
# (build/images/web/) that the gallery uses. Requires pillow.
web-images:
	@command -v python3 >/dev/null || { echo "python3 required"; exit 1; }
	@python3 -c "import PIL" 2>/dev/null || { echo "Pillow required: pip install pillow"; exit 1; }
	cd ${ROOT_DIR} && python3 build/process_images.py

# Publish the static gallery to the gh-pages branch via a dedicated worktree,
# so master's working tree is never disturbed. gh-pages has a history that is
# intentionally separate from master; we sync the built site onto it.
deploy: web-images
	@set -euo pipefail; \
	cd ${ROOT_DIR}; \
	git show-ref --verify --quiet refs/heads/${PAGES_BRANCH} \
		|| { echo "branch ${PAGES_BRANCH} not found"; exit 1; }; \
	git worktree add -f ${PAGES_WORKTREE} ${PAGES_BRANCH}; \
	trap 'git worktree remove --force ${PAGES_WORKTREE} 2>/dev/null || true' EXIT; \
	for p in ${DEPLOY_PATHS}; do \
		rm -rf "${PAGES_WORKTREE}/$$p"; \
		mkdir -p "$$(dirname "${PAGES_WORKTREE}/$$p")"; \
		cp -R "$$p" "${PAGES_WORKTREE}/$$p"; \
	done; \
	cd ${PAGES_WORKTREE}; \
	git add -A; \
	if git diff --cached --quiet; then \
		echo "gh-pages already up to date"; \
	else \
		git commit -m "Deploy gallery from master ($$(git -C ${ROOT_DIR} rev-parse --short HEAD))"; \
		git push origin ${PAGES_BRANCH}; \
		echo "Deployed to ${PAGES_BRANCH}."; \
	fi
