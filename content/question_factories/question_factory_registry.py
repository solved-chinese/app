class QuestionFactoryRegistry:
    _type2factories = {}
    _model2factories = {}

    @classmethod
    def register(cls, factory):
        assert factory.question_type not in cls._type2factories, \
            "factory with same type already exists"
        cls._type2factories[factory.question_type] = factory
        cls._model2factories.setdefault(factory.question_model, []).append(factory)
        return factory

    @classmethod
    def get_factory_by_type(cls, question_type):
        return cls._type2factories[question_type]

    @classmethod
    def get_factories_by_model(cls, model):
        return cls._model2factories.get(model, [])
