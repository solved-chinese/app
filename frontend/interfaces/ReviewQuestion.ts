interface ReviewQuestion {
    id: string,
    form: string,
    content: ReviewQuestionContent
}

interface ReviewQuestionContent {
    question: TextProvider,
}

export interface MCQuestionContent extends ReviewQuestionContent {
    context: TextProvider,
    choices: [TextProvider]
}

export interface CNDQuestionContent extends ReviewQuestionContent {
    title: TextProvider,
    answer_length: TextProvider,
    choices: [TextProvider]
}

export interface FITBQuestionContent extends ReviewQuestionContent {
    title: TextProvider
}

interface TextProvider {
    text: string,
    audio: string
}

export default ReviewQuestion;