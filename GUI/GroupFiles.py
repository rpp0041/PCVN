from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase
from GroupFilesUtils import *
import bibtexparser

def group_files(pbar):

	# Load BibTex files extract from Google Scholar, Scopus and WOS
	# in order to remove duplicate publications and to group them in just one file
	# so it will make easier to work with.


	# Load BibTex files extract from the websites

	# Load Google Scholar BibTex File
	with open('bibtexScopus.bib', encoding='utf-8') as bibfile:
	    Scopus = bibtexparser.load(bibfile)
	# Load Scopus BibTex File
	with open('bibtexScholar.bib', encoding='utf-8') as bibfile:
	    Scholar = bibtexparser.load(bibfile)
	# Load WOS BibTex File
	with open('savedrecs.bib', encoding='utf-8') as bibfile:
	    WOS = bibtexparser.load(bibfile)

	try:
	    with open('savedrecs(1).bib', encoding='utf-8') as bibfile:
	        WOS2 = bibtexparser.load(bibfile)
	    for x in WOS2.entries:
	        WOS.entries.append(x)
	except:
	    pass
	""" update progress bar GUI"""
	pbar['value'] =20
	pbar.update()

	""" Parse WOS db in order to get same format for every bibTex db 
	this will help us in the future comparison (otherwise it will be impossible)"""
	ImpactIndexList = list()
	JournalList = list()
	ParseWOS(WOS.entries, ImpactIndexList, JournalList)

	""" update progress bar GUI"""
	pbar['value'] =80
	pbar.update()

	#####################################################################

	""" Remove Duplicates from the BibTex Files"""
	WOS.entries, Scopus.entries = RemoveDupliates(WOS.entries, Scopus.entries)
	WOS.entries, Scholar.entries = RemoveDupliates(WOS.entries, Scholar.entries)
	Scopus.entries, Scholar.entries = RemoveDupliates(
	    Scopus.entries, Scholar.entries)


	""" Write the dictionaries modified in a new BibTex file 
	 at this point we will not have duplicate publications,
	 also modify some field´s name to fit BibTex Standard (cites)
	 and parse volume field becouse in same cases we get 
	 extra information that prouces errors in ACADEMIA
	"""
	writer = BibTexWriter()
	db = BibDatabase()
	for i in Scopus.entries:
	    """ Rename cites"""
	    i['cites'] = i['citation_count']
	    i.pop('citation_count')
	    """ Parse Volume """
	    i = ParseVolume(i)
	    """ Add pub to write BibTex db """
	    db.entries.append(i)
	for i in Scholar.entries:
	    """ Parse Volume """
	    i = ParseVolume(i)
	    """ Add pub to write BibTex db """
	    db.entries.append(i)
	for i in WOS.entries:
	    """ Rename cites """
	    i['cites'] = i['number-of-cited-references']
	    i.pop('number-of-cited-references')
	    """ Parse Volume """
	    i = ParseVolume(i)
	    """ Parse ImpactIndex"""
	    i = ParseImpacIndex(i)
	    """ Add pub to write BibTex db """
	    db.entries.append(i)
	""" Write db to BibTex file """
	with open('BibFINAL.bib', 'w', encoding='utf-8') as bibfile:
	    bibfile.write(writer.write(db))

	""" update progress bar GUI"""
	pbar['value'] =100
	pbar.update()
