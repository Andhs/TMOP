# sys.path.append(os.getcwd() + '/..') # Uncomment for standalone running
from abstract_filter import *
import langid


class Lang_Identifier(AbstractFilter):
	def __init__(self):
		self.num_of_scans = 0
		self.src_language = ""
		self.trg_language = ""

	def initialize(self, source_language, target_language):
		self.num_of_scans = 0
		self.src_language = source_language.lower()
		self.trg_language = target_language.lower()

		langid.load_model()
		return

	def finalize(self):
		pass

	def process_tu(self, tu, num_of_finished_scans):
		pass

	def do_after_a_full_scan(self, num_of_finished_scans):
		pass

	def decide(self, tu):
		src_lang = langid.classify(tu.src_phrase)[0]
		trg_lang = langid.classify(tu.trg_phrase)[0]

		if src_lang != self.src_language and src_lang not in self.src_language:
			return 'reject'
		if trg_lang != self.trg_language and trg_lang not in self.trg_language:
			return 'reject'

		return 'accept'