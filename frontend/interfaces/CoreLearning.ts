import {ItemType} from '@interfaces/CoreItem';

export interface ProgressBarData {
    mastered: number,
    familiar: number,
    remaining: number,
    bonus: number,
}

export type LearningAction = 'review' | 'display' | 'assignment' | 'done'

export interface LearningObjectContent {
    qid: number,
    type?: ItemType
}

export interface LearningObjectDescriptor {
    action: LearningAction,
    content: LearningObjectContent
}

export interface LearningNextResponse extends LearningObjectDescriptor {
    progressBar: ProgressBarData,
    state: string
}

export interface AnswerSubmitResponse extends LearningNextResponse {
    isCorrect: boolean,
    answer: number
}