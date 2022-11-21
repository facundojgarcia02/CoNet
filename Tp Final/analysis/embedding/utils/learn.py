from gensim.models import Word2Vec

def learn_embeddings(walks, dimensions = 128, window_size = 10, workers = 4, epochs = 1, output = "output.emb") -> None:
	'''
	Learn embeddings by optimizing the Skipgram objective using SGD.
	'''

	walks = [map(str, walk) for walk in walks]
	model = Word2Vec(walks, vector_size=dimensions, window=window_size, min_count=4, sg=1, workers=workers, epochs=epochs)
	model.save(output)
	
	return None