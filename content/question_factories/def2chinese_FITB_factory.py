import logging

from .question_factory_registry import QuestionFactoryRegistry
from .general_factory import GeneralFactory, WordFactoryMixin, \
    FITBFactoryMixin


@QuestionFactoryRegistry.register
class Def2ChineseFITBFactory(WordFactoryMixin,
                             FITBFactoryMixin,
                             GeneralFactory):
    question_type = "Def2ChineseFITB"
    question_order = 10
    logger = logging.getLogger(__name__)
