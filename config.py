class Config:
	EMBEDDING_MODEL = 'distiluse-base-multilingual-cased-v1'
	INDEX_FILE = './storage/database.idx'
	VOCAB_FILE = './storage/database.voc'
	METRIC = 'angular'
	INDEX_TREES = 10
	NEIGHBORS = 1
	HOST = '0.0.0.0'
	PORT = 6785
	LLM_PROMPT_SYSTEM = 'You can answer only question related to provided sightsees'
	LLM_PROMPT_PREFIX = 'Regarding this information:\n'
	LLM_PROMPT_SUFFIX = 'Give a short answer for the question:\n'
	OPENAI_KEY = ''

