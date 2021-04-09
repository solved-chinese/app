export interface ReviewQuestionData {
    id: string,
    form: string,
    content: ReviewQuestionContent
}

export type ReviewQuestionContent = MCQuestionContent | CNDQuestionContent | FITBQuestionContent

export interface AudioTextProvider {
    text: string,
    audio: string
}

export interface MCQuestionContent {
    question: AudioTextProvider
    context: string,
    choices: AudioTextProvider[]
}

export interface CNDQuestionContent {
    question: string,
    title: string,
    description: string,
    answerLength: number,
    choices: string[]
}

export interface FITBQuestionContent {
    question: string,
    title: string
}

export type MCAnswer = string

export type CNDAnswer = string[]

export type FITBAnswer = string

export type ReviewQuestionAnswer = MCAnswer | CNDAnswer | FITBAnswer

export interface AnswerVerificationResponse {
    isCorrect: boolean,
    answer: ReviewQuestionAnswer
}