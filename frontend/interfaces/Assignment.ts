import ProgressBar from './ProgressBar';

export interface Assignment {
    name: string,
    progressBar: ProgressBar,
    wordList: [SimpleContentObject],
    characterList: [SimpleContentObject],
    radicalList: [SimpleContentObject],
}

interface SimpleContentObject {
    type: string,
    qid: string,
    status: 'mastered'|'familiar'|'remaining',
    chinese: string,
    pinyin: string,
}