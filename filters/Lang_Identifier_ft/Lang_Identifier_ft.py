# sys.path.append(os.getcwd() + '/..') # Uncomment for standalone running
from abstract_filter import *
import fasttext


class Lang_Identifier_ft(AbstractFilter):
	def __init__(self):
		self.num_of_scans = 0
		self.src_language = ""
		self.trg_language = ""


	def initialize(self, source_language, target_language, extra_args):
		self.num_of_scans = 0
		self.src_language = extra_args['source language']
		self.trg_language = extra_args['target language']
		self.normalize = extra_args['normalize scores']

		if extra_args['emit scores'] == True:
			self.num_of_scans = 1
		pretrained_lang_model = "lid.176.ftz"
		self.model = fasttext.load_model(pretrained_lang_model)
		return

	def finalize(self):
		pass

	def process_tu(self, tu, num_of_finished_scans):
		src_lang = model.predict(tu.src_phrase, k=1)[0][0][-2:]
		trg_lang = model.predict(tu.trg_phrase, k=1)[0][0][-2:]

		if src_lang != self.src_language and src_lang not in self.src_language:
			return [0]
		if trg_lang != self.trg_language and trg_lang not in self.trg_language:
			return [0]
		return [1]

	def do_after_a_full_scan(self, num_of_finished_scans):
		pass

	def decide(self, tu):
		src_lang = model.predict(tu.src_phrase, k=1)[0][0][-2:]
		trg_lang = model.predict(tu.trg_phrase, k=1)[0][0][-2:]
		print(src_lang + " to " + trg_lang)

		if src_lang != self.src_language and src_lang not in self.src_language:
			return 'reject'
		if trg_lang != self.trg_language and trg_lang not in self.trg_language:
			return 'reject'

		return 'accept'
