.PHONY: install all targets target mediakit print crm crm-rank crm-validate crm-brief events log clean

install:
	pip install -r requirements.txt

all:            ## dossiers génériques + media kit
	python -m kit --all
	python -m kit mediakit

targets:        ## PDF + one-pager + e-mail pour toutes les cibles
	python -m kit --targets

target:         ## make target T=triplaco
	python -m kit --target $(T)

mediakit:
	python -m kit mediakit

print:          ## qualité impression (300 dpi)
	PRESS_DPI=300 PRESS_JPEG_QUALITY=92 python -m kit --all

crm:            ## pipeline, scores, relances dues
	python -m kit --crm

crm-rank:       ## le classement : à qui donner son mois
	python -m kit --crm-rank

crm-validate:   ## refuse toute adresse e-mail non sourcée
	python -m kit --crm-validate

crm-deadlines:  ## les dates de dépôt des subsides — rater une date coûte un an
	python -m kit --crm-deadlines

crm-brief:      ## make crm-brief T=triplaco
	python -m kit --crm-brief $(T)

events:         ## base événements
	python -m kit --events

clean:
	rm -rf output/* .cache
