# Blades and Dragons Makefile

#CHROME := "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
CHROME := "chromium-browser"

TABS := abilities classes
TABLES := $(foreach T,${TABS},src/rule/${T}.tsv)

RULES := ${TABLES}

CLASSES := Cleric Fighter Rogue Wizard
# CLASSES := Fighter
CHAR_PDFS := $(foreach C,${CLASSES},build/character/${C}.pdf)


# General

build/ build/character/ build/template/ site/:
	mkdir -p $@

build/character/asset/: | build/character/
	ln -s asset/ $|

.PHONY: clean
clean:
	rm -rf build/

# Rules

src/rule/abilities.tsv:
	curl -L -o $@ "${GOOGLE_SHEET}0"

src/rule/classes.tsv:
	curl -L -o $@ "${GOOGLE_SHEET}794716610"

.PHONY: fetch
fetch:
    ifeq ($(GOOGLE_SHEET),)
        $(error GOOGLE_SHEET must be set)
    endif
	rm -rf ${TABLES}
	make ${TABLES}

# Characters

build/template/character.html: src/template/character.html | build/template/
	cp $< $@

build/character/%.json: src/script/character.py src/rule/abilities.tsv src/rule/classes.tsv | build/character/
	python3 $^ $* > $@

build/character/%.html: build/template/character.html build/character/%.json
	sed s/data.json/$*.json/ < $< > $@

build/character/%.pdf: build/character/%.html asset/ | build/character/asset/
	${CHROME} --headless \
	--disable-gpu \
	--ignore-certificate-errors \
	--print-to-pdf-no-header \
	--print-to-pdf=$@ $<

build/characters.pdf: ${CHAR_PDFS}
	pdfunite $^ $@

site/characters.pdf: build/characters.pdf
	cp $< $@

.PHONY: all
all: site/characters.pdf

.PHONY: watch
watch:
	ls -d src/rule/* src/template/* src/script/* asset/*.js asset/*.css | entr make clean all
