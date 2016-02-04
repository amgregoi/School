1)
To start, we build our index.  We start the job that reads in our initial corpus "cranfield.txt". the mapper will grab the relevant text from the document, clean it up and send it to the reducer where we finish building the inverted index.  After we have our inverted index we start our next job to get the total number of documents that will be used to calculate IDF.  Next we can read in our inverted index that we created from step one and use the newly acquired document count to calculate document lengths.  I used one more job to update the inverted index with tf-idf values.  This finishes my pre processing for our query system.

I used a variety of hasmaps, and borrowed structures from cloud9(Histogram, PairOfxxxx).

2)
Mapper1: takes the document id as the key and the contents of the document as its value.
Reducer1: takes the output of mapper1.  The Key is a word from the document, and the value is a PairOfStringInt(doc_num, term count).
	This job is used to get/build our inverted index
	
Mapper2: takes the inverted index we outputted from our first job, reads it back in. (key = doc_id of inverted index file, value = contents of inverted index file)
Reducer2: takes the output from the mapper. (key = empty string, value = invertedindexobject)
	The key was empty so that we can reduce everything together to get a total count of documents in the corpus
	invertedindexobject is an object that holds a word, doc freq of word, list of documents and its term freq for said documents
	This job is used to get document count

Mapper3: takes the inverted index as its input ( same as previosu job), and we pass in the new founded document length through the job configuration. (key = doc_id of inverted index file, value doc_contents of inverted index file)
Reducer3: takes in the output of the mapper. (key = document_id, value = document_length)
	After calculating tf-idf for the terms in the mapper, we calculate document length in the reducer by document
	and output a file with the setup |doc_num	doc_length|
	
Mapper4: takes in the inverted index like before and updates the tf for the documents in the list with tf-idf.
reuses reducer1 to output a new inverted index


3)
To use the program, export to jar, and run it with with the arguments <corpus_path> <output_path> <stopword_list_path>
After you run the the file and it does its preprocessing the query answer class will be called and you can make queries
based on what was built with the corpus and stopword list provided.


4)
Ex
Enter query (-1 to exit): what is the basic mechanism of the transonic aileron buzz
	cranfield0496	 score: 0.59505945	 P = 0.00202	 R = 0.10000
	cranfield0903	 score: 0.2893704	 P = 0.00221	 R = 0.20000
	cranfield0643	 score: 0.26918155	 P = 0.00467	 R = 0.30000
	cranfield0199	 score: 0.23090063	 P = 0.02010	 R = 0.40000
	cranfield0335	 score: 0.18220045	 P = 0.01493	 R = 0.50000
	cranfield0313	 score: 0.15690392	 P = 0.01917	 R = 0.60000
	cranfield0660	 score: 0.15545985	 P = 0.01061	 R = 0.70000
	cranfield1099	 score: 0.153071	 P = 0.00728	 R = 0.80000
	cranfield0503	 score: 0.1516494	 P = 0.01789	 R = 0.90000
	cranfield1364	 score: 0.14961836	 P = 0.00733	 R = 1.00000


Ex
Enter query (-1 to exit): papers on shock-sound wave interaction
	cranfield0462	 score: 0.6441662	 P = 0.00216	 R = 0.10000
	cranfield0170	 score: 0.40817642	 P = 0.01176	 R = 0.20000
	cranfield0256	 score: 0.31371805	 P = 0.01172	 R = 0.30000
	cranfield0798	 score: 0.31225175	 P = 0.00501	 R = 0.40000
	cranfield1364	 score: 0.30837232	 P = 0.00367	 R = 0.50000
	cranfield0345	 score: 0.28200197	 P = 0.01739	 R = 0.60000
	cranfield0335	 score: 0.27942637	 P = 0.02090	 R = 0.70000
	cranfield0064	 score: 0.25617224	 P = 0.12500	 R = 0.80000
	cranfield1097	 score: 0.25420058	 P = 0.00820	 R = 0.90000
	cranfield0291	 score: 0.24708852	 P = 0.03436	 R = 1.00000


Ex
Enter query (-1 to exit): material properties of photoelastic materials  
	cranfield0462	 score: 0.2908065	 P = 0.00216	 R = 0.10000
	cranfield0463	 score: 0.113223515	 P = 0.00432	 R = 0.20000
	cranfield1097	 score: 0.112711966	 P = 0.00273	 R = 0.30000
	cranfield0761	 score: 0.109761596	 P = 0.00526	 R = 0.40000
	cranfield1025	 score: 0.10287271	 P = 0.00488	 R = 0.50000
	cranfield1043	 score: 0.097377755	 P = 0.00575	 R = 0.60000
	cranfield1099	 score: 0.09450302	 P = 0.00637	 R = 0.70000
	cranfield0866	 score: 0.094395064	 P = 0.00924	 R = 0.80000
	cranfield1117	 score: 0.09102574	 P = 0.00806	 R = 0.90000
	cranfield0542	 score: 0.08539655	 P = 0.01845	 R = 1.00000


5)
As mentioned earlier, I borrowed a few structures from cloud9 to aid in the implmentation of this project.
I also used the stemmer library you directed us to



=======================

All the map reduce jobs mentioned above are in VSRSystem.java
InvertedIndexObject.java was also talked about above, it is a row in the inverted index
Stemmer is a library used to stem words for the inverted index
lookup and queryAnswer.java are used for the query response after we build our system.

