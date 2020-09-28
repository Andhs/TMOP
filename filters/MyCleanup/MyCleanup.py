# sys.path.append(os.getcwd() + '/..') # Uncomment for standalone running
from abstract_filter import *


class MyCleanup(AbstractFilter):
	def __init__(self):
		self.num_of_scans = 0
		self.src_language = ""
		self.trg_language = ""

		return

#
	def initialize(self, source_language, target_language, extra_args):
		self.num_of_scans = 0
		self.src_language = extra_args['source language']
		self.trg_language = extra_args['target language']
		if extra_args['emit scores'] == True:
			self.num_of_scans = 1

		return

	def finalize(self):
		pass

	def process_tu(self, tu, num_of_finished_scans):
		nonlocal status

		find_bad(self, tu)

		if status == "Deleted":
			return [0]
		return [1]

	def do_after_a_full_scan(self, num_of_finished_scans):
		pass

	def decide(self, tu):
		nonlocal status

		find_bad(self, tu)

		if status == "Deleted":
			return 'reject'
		return 'accept'

	def find_bad(self, tu):
		nonlocal status
		status = "OK"

		garbage = bad_symbol_number(tu.src_phrase)
		cleaning(tu.src_phrase, garbage)

		garbage = bad_symbol_number(tu.trg_phrase)
		cleaning(tu.trg_phrase, garbage)

		cleaning_diff(tu.src_phrase, tu.trg_phrase)

		return status

	# Подсчитываем число не самых нужных символов
	def bad_symbol_number(segment):
	# Список символов, которых не должно быть много, иначе это слишком мусорный сегмент
		badsymbols = "«»\'!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~01234567890 "
		garbage = 0
		for c in segment:
			if c in badsymbols:
				garbage += 1
		return(garbage)

	# Собственно чистка - убираем сегмент, если в нем слишком большая доля не самых нужных символов. Меняем статус (для правого сегмента - если уже не была удалена строка по левому сегменту)
	def cleaning_garbage(segment, garbage):
		nonlocal status
		if garbage/len(segment.strip('\n')) > 0.45:
			status = "Deleted"

	# Убираем сегменты слишком длинные (по числу слов, а число слов - количество пробелов + 1)
	def cleaning_long(segment):
		nonlocal status
		words = 1
		for c in segment:
			if c == " ":
				words += 1
		if words > 50:
			status = "Deleted"

	# Убираем сегменты, которые слишком различаются по длине (по словам)
	def cleaning_diff(segment_one, segment_two):
		nonlocal status
		if status != "Deleted":
			words_one = 1
			words_two = 1
			for c in segment_one:
				if c == " ":
					words_one += 1
			for c in segment_two:
				if c == " ":
					words_two += 1
			if (words_one/words_two > 1.5 or words_two/words_one > 1.5) and words_one > 10 and words_two > 10: 
				status = "Deleted"

	# Собираем все случаи чистки (реализуемые по одному из параллельных сегментов) в одну функцию
	def cleaning(segment, garbage):
		nonlocal status
		# Имеет смысл проверять, если еще не удален параллельный сегмент за счет левого сегмента
		if status != "Deleted":
			cleaning_garbage(segment, garbage)
		if status != "Deleted":        
			cleaning_long(segment)


