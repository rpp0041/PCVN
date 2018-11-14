from pyscopus import Scopus # Import library that will help us in the search

key ='a3ddc2b8df64bc16774266fb842c0365' # Key gived by Elsevier to acces their api 
scopus = Scopus(key)

author_id= input('ID del Autor: ')   # We ask the user to enter the author´s ID

author_pub= scopus.search_author_publication(author_id,10000) # int number indicates the number of publications to be retrieved (set by default in 10000)
															  # (pending of improve)


titles = author_pub['title']	# list with all the author´s publications
citation = author_pub['citation_count'] # list with number of citations for each publication

## Write data to txt File
file = open('testfileScopus.txt','w') 
for i in range(0,len(titles)):
    file.write(titles[i]+' , '+str(citation[i])+'\n')
file.close()