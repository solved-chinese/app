interface CoreItem {
    url: String,
    definitions: [Definition],
    pinyin: String,
    audioUrl: String,
    chinese: String,
    identifier: String,
    isDone: String
}

interface Definition {
    partOfSpeech: String,
    definition: String
}

export interface Character extends CoreItem {
    relatedWords: [WordShort],
    radicals: [String],
    characterType: String,
    memoryAid: String
}

export interface CharacterShort {
    chinese: String,
    pinyin: String,
    fullDefinition: String
}

export interface Radical extends CoreItem {
    image: String,
    explanation: String,
    note: String,
    relatedCharacters: [CharacterShort]
}

export interface Word extends CoreItem {
    sentences: [Sentence]
}

interface Sentence {
    pinyinHighlight: String,
    chineseHighlight: String,
    translationHighlight: String,
    audioUrl: String
}

export interface WordShort {
    chinese: String,
    pinyin: String,
    fullDefinition: String
}

export interface ItemDescriptor {
    qid: Number,
    type: String,
    hasNext: Boolean,
    onActionNext: Function,
    displayRef: any
}