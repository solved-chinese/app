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

export type LearningAction = 'review' | 'display' | 'assignment' | 'done'

export type LearningObjectContent = DisplayObjectContent | ReviewQuestionData

/**
 * An instance that describes a learning step.
 */
export interface LearningStepDescriptor {

    /**
     * The **action type** for a learning step.
     *
     * There are four action kinds for a learning step. The specific learning
     * instructions are returned by server upon calling service/getLearningNext.
     * If `action = review`, it means react should render a review question.
     * A `display` instruction means displaying an word/character/radical object, and
     * `assignment` is for viewing the active assignment.
     */
    action: LearningAction,

    /**
     * The **content payload** of the learning action.
     *
     * If `action = review`, the content
     * will be of type `ReviewQuestionData`, else if `action = display`, the content
     * would have type `DisplayObjectContent`. Content is undefined for assignment and
     * done instructions.
     */
    content: LearningObjectContent
}

/**
 * The server response when calling getLearningNext.
 */
export interface LearningNextResponse extends LearningStepDescriptor {
    /**
     * Data for rendering the progress bar in CoreLearning
     */
    progressBar: ProgressBarData,

    /**
     * State identifier in a learning step, used for server
     * status verification.
     */
    state: string,
}

/**
 * The server response when submitting an answer.
 */
export interface AnswerSubmitResponse extends LearningNextResponse {
    isCorrect: boolean,
    answer: ReviewQuestionAnswer
}