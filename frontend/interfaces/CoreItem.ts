interface CoreItem {
    /** Resource url. */
    url: string,

    /** Audio file url. */
    audioUrl: string,

    /** Integrated chinese level. */
    ICLevel: number | null,

    /** Identify whether the item has been finished. */
    isDone: boolean,

    /** The chinese character(s). */
    chinese: string,

    /**
     * A short description used to identify the same words or characters that have
     * different meanings, such as 花(to spend)费 and 花(flower)草.
     */
    identifier: string,

    /**
     * A string with display friendly pinyin. If there are multiple characters,
     * each character's pinyin is separated with a single space.
     */
    pinyin: string,

    /**
     * The item's pinyin without tone notation and spaces (if there was any). Used
     * mainly for searching.
     */
    searchablePinyin: string
}

export interface Radical extends CoreItem {
    /** Image URL for the radical. */
    image: string,

    /** A 2-3 words definition of the radical. */
    definition: string,

    /** A more detailed, one-sentence explanation of the radical. */
    explanation: string,

    isLearnable: boolean,

    /** A list of characters related to the radical. */
    relatedCharacters: CharacterShort[]
}

/**
 * Represent a single definition of the object, including the
 * definition string and the corresponding part of speech (optional).
 */
export interface ItemDefinition {
    definition: string,
    partOfSpeech?: string
}

export interface Character extends CoreItem {
    /** A list of definitions of the character. */
    definitions: ItemDefinition[],

    /** A list of composing radicals in their URL. */
    radicals: string[],

    characterType: string,

    /** A single sentence that helps with memorizing the character. */
    memoryAid: string,

    /** A list of words related to the character. */
    relatedWords: WordShort[]
}

export interface CharacterShort {
    /** The chinese character(s). */
    chinese: string,

    /**
     * A string with display friendly pinyin. If there are multiple characters,
     * each character's pinyin is separated with a single space.
     */
    pinyin: string,

    /**
     * Definitions composed into a string. Each definition is separated by a semicolon.
     * Part of speech identifiers are also included in the beginning of each definition
     * if they are available.
     * @example mv. definition; conj. 2nd definition; pn. 3rd definition
     */
    fullDefinition: string
}

export interface Word extends CoreItem {

    /** A list of definitions of the word. */
    definitions: ItemDefinition[],

    /** A list of sentence objects */
    sentences: HighlightedSentence[],

    /**
     * A list of characters within the word, represented with their URL.
     * If the word only has a single character, the only item becomes the
     * radical urls joined together with a semicolon.
     */
    characters: string[],

    /** A single sentence that helps with memorizing the word. */
    memoryAid: string
}

export type WordShort = CharacterShort

export interface HighlightedSentence {

    /**
     * The sentence's pinyin, with inline-highlighting encoded.
     * @example <ni hao> wo men
     */
    pinyinHighlight: string,

    /**
     * The sentence in Chinese, with inline-highlighting encoded.
     * @example <你好>, 他是?
     */
    chineseHighlight: string,

    /**
     * Sentence translation with inline-highlighting encoded.
     * @example <Hello>, and you are?
     */
    translationHighlight: string,

    /** The audio url for the sentence. */
    audioUrl: string
}

export type ItemType = 'word' | 'character' | 'radical'
