import {DisplayObjectContent} from '@interfaces/CoreItem';
import {ReviewQuestionAnswer, ReviewQuestionData} from '@interfaces/ReviewQuestion';

/**
 * Data for rendering the progress bar in CoreLearning
 */
export interface ProgressBarData {
    /** The number of mastered items. */
    mastered: number,

    /** The number of familiar items. */
    familiar: number,

    /** The number of remaining items. */
    remaining: number,

    /** The number of bonus items. */
    bonus: number,
}

/**
 * There are four action kinds for a learning step. The specific learning
 * instructions are returned by server upon calling service/getLearningNext.
 * If *action = review*, it means react should render a review question.
 * A *display* means displaying an word/character/radical object, and
 * *assignment* is for viewing the active assignment.
 */
export type LearningAction = 'review' | 'display' | 'assignment' | 'done'


export type LearningObjectContent = DisplayObjectContent | ReviewQuestionData

export interface LearningObjectDescriptor {
    action: LearningAction,
    content: LearningObjectContent
}

export interface LearningNextResponse extends LearningObjectDescriptor {
    progressBar: ProgressBarData,
    state: string,
}

export interface AnswerSubmitResponse extends LearningNextResponse {
    isCorrect: boolean,
    answer: ReviewQuestionAnswer
}