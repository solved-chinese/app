import { ItemType } from '@interfaces/CoreItem';
import { ReviewQuestionData } from '@interfaces/ReviewQuestion';

export interface ProgressBarData {
    mastered: number,
    familiar: number,
    remaining: number,
    bonus: number,
}

export type LearningAction = 'review' | 'display' | 'assignment' | 'done'

export interface DisplayObjectContent {
    qid: number,
    type: ItemType
}

export type LearningObjectContent = DisplayObjectContent | ReviewQuestionData

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