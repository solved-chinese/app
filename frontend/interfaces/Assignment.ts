import { ProgressBarData } from '@interfaces/CoreLearning';
import { ItemType } from '@interfaces/CoreItem';

export interface Assignment {
    name: string,
    progressBar: ProgressBarData,
    wordList: SimpleContentObject[],
    characterList: SimpleContentObject[],
    radicalList: SimpleContentObject[],
}

export interface SimpleContentObject {
    type: ItemType,
    qid: number,
    status: 'mastered' | 'familiar' | 'remaining',
    chinese: string,
    pinyin: string,
    definition: string
}