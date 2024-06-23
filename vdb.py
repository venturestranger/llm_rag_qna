from annoy import AnnoyIndex
from sentence_transformers import SentenceTransformer, util
from config import Config
import numpy as np


# intialize vector database
class VDB:
	def __init__(self):
		self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
		self.vocab_file = Config.VOCAB_FILE
		self.index_file = Config.INDEX_FILE
		self.index = AnnoyIndex(self.model.encode('hello world').shape[-1], Config.METRIC)

		try:
			self.index.load(self.index_file)

			with open(self.vocab_file, 'rb') as file:
				self.vocab = pickle.load(file)
		except:
			self.vocab = []
	
	# fetch similar word-units
	def fetch(self, word: str):
		ids = self.index.get_nns_by_vector(self.model.encode(word), Config.NEIGHBORS)

		return [self.vocab[i] for i in ids]
	
	# intialize a new index from the given word-units
	def intialize(self, words: list[str]):
		index = self.AnnoyIndex(self.model.encode('hello world').shape[-1], Config.METRIC) 

		for id, word in enumerate(words):
			self.index.add_item(id, word)

		self.vocab = words
		self.index.build(Config.INDEX_TREES)
		self.index.save(Config.INDEX_FILE)

		with open(Config.VOCAB_FILE, 'wb') as file:
			pickle.dump(self.vocab, file)
