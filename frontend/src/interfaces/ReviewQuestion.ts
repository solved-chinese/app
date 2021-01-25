interface ReviewQuestion {
    id: String,
    form: String,
    content: ReviewQuestionContent
}

interface ReviewQuestionContent {
    question: TextProvider,
}

export interface MCQuestionContent extends ReviewQuestionContent {
    context: TextProvider,
    choices: [TextProvider]
}

export interface FITBQuestionContent extends ReviewQuestionContent {
    title: TextProvider
}

interface TextProvider {
    text: String,
    audio: String
}

export default ReviewQuestion;