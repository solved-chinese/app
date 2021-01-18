# @QuestionFactoryRegistry.register
# class Chinese2PinyinMCFactory:
#     question_type = "Chinese2Pinyin"
#     question_model = Word
#
#     @classmethod
#     def generate(cls, ro):
#         """
#         incorrect answers should have the same number of chinese characters
#         """
#         word = ro.word
#         assert word is not None
#
#         # select words that have overlapping characters
#         len_chinese = len(re.findall(CHINESE_CHAR_REGEX, word.chinese))
#         related_character_queryset = filter_num_chinese(
#             Word.objects.filter(characters__in=word.characters.distinct()),
#             len_chinese
#         )[:MAX_RANDOM_CHOICE_NUM]
#         # select words that are in the same set
#         same_word_set_queryset = filter_num_chinese(
#             Word.objects.filter(word_set__in=word.word_sets.distinct()),
#             len_chinese
#         )[:MAX_RANDOM_CHOICE_NUM]
#         queryset = related_character_queryset | same_word_set_queryset
#         queryset = queryset.exclude(pk=word.pk).distinct()
#         # make sure there are enough choices
#         if queryset.count() < MAX_MC_CHOICE_NUM:
#             raise CannotAutomaticallyGenerateException(
#                 "Too few elements in queryset")
#         queryset = queryset.order_by('?')[:MAX_MC_CHOICE_NUM]
#         reviwable = word.get_reviewable_object()
#         # add context if possible
#         context_link = None
#         if word.sentences.exists():
#             sentence = word.sentences.first()
#             context_link = LinkedField.of(sentence, 'chinese')
#         MC = MCQuestion.objects.create(
#             question_type=cls.question_type,
#             context_link=context_link,
#             question=f"How do you say {word.chinese}",
#         )
#         # add choices
#         for candidate_word in itertools.chain(queryset, [word]):
#             linked_value = LinkedField.of(candidate_word, 'pinyin')
#             MCChoice.objects.create(
#                 linked_value=linked_value,
#                 weight=MCChoice.WeightType.CORRECT
#                     if candidate_word.pk == word.pk
#                     else MCChoice.WeightType.AUTO_COMMON_WRONG,
#                 question=MC
#             )
#         return GeneralQuestion.objects.create(MC=MC, reviewable=reviwable)
#
#
# def filter_num_chinese(qs, len_chinese):
#     return qs.filter(
#         chinese__regex=f"^{CHINESE_CHAR_REGEX}{{{len_chinese}}}$"
#     ).exclude(
#         chinese__regex=f"^{CHINESE_CHAR_REGEX}{{{len_chinese+1}}}$"
#     )
