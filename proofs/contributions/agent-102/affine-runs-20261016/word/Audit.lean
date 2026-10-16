import Agent102RunWord

/- Agent #102 的区间词子代理：对本模块全部 27 个导出声明逐项审计。 -/
#print axioms Agent102.word_nil
#print axioms Agent102.word_cons
#print axioms Agent102.word_append
#print axioms Agent102.word_length
#print axioms Agent102.word_reverse
#print axioms Agent102.Span.shift
#print axioms Agent102.Span.shift_covers
#print axioms Agent102.Span.shift_overlaps
#print axioms Agent102.spansFrom_shift
#print axioms Agent102.spansFrom_eq_map_spans
#print axioms Agent102.spansFrom_append
#print axioms Agent102.length_spansFrom
#print axioms Agent102.length_spans
#print axioms Agent102.mem_spansFrom_bounds
#print axioms Agent102.exists_mem_spansFrom_covers
#print axioms Agent102.exists_mem_spansFrom_covers_iff
#print axioms Agent102.mem_spans_bounds
#print axioms Agent102.exists_mem_spans_covers
#print axioms Agent102.exists_mem_spans_covers_iff
#print axioms Agent102.eq_of_mem_spansFrom_covers
#print axioms Agent102.eq_of_mem_spans_covers
#print axioms Agent102.getElem?_word_of_mem_spansFrom
#print axioms Agent102.getElem?_word_of_covers
#print axioms Agent102.Span.overlaps_iff_exists_covers
#print axioms Agent102.Span.overlaps_of_covers
#print axioms Agent102.word_eq_iff_length_and_overlap_digits
#print axioms Agent102.word_eq_iff_count_sum_and_overlap_digits
