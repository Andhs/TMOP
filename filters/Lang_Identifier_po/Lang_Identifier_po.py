# sys.path.append(os.getcwd() + '/..') # Uncomment for standalone running
from abstract_filter import *
from polyglot.detect import Detector


class Lang_Identifier_po(AbstractFilter):
	def __init__(self):
		self.num_of_scans = 0
		self.src_language = ""
		self.trg_language = ""

	def initialize(self, source_language, target_language, extra_args):
		self.num_of_scans = 0
		self.src_language = extra_args['source language extended']
		self.trg_language = extra_args['target language extended']
		self.normalize = extra_args['normalize scores']

		if extra_args['emit scores'] == True:
			self.num_of_scans = 1
		return

	def finalize(self):
		pass

	def process_tu(self, tu, num_of_finished_scans):
		src_lang = Detector(tu.src_phrase, quiet=True).language.code
		trg_lang = Detector(tu.trg_phrase, quiet=True).language.code

		if src_lang != self.src_language and src_lang not in self.src_language:
			return [0]
		if trg_lang != self.trg_language and trg_lang not in self.trg_language:
			return [0]
		return [1]

	def do_after_a_full_scan(self, num_of_finished_scans):
		pass

	def decide(self, tu):
		src_lang = Detector(tu.src_phrase, quiet=True).language.code
		trg_lang = Detector(tu.trg_phrase, quiet=True).language.code
#		print("PO: ", src_lang + " to " + trg_lang)

		if src_lang != self.src_language and src_lang not in self.src_language:
			return 'reject'
		if trg_lang != self.trg_language and trg_lang not in self.trg_language:
			return 'reject'

		return 'accept'
