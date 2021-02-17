import ProgressBar from "./ProgressBar";

interface Assignment {
    name: String,
    progressBar: ProgressBar,
    wordList: [SimpleContentObject],
    characterList: [SimpleContentObject],
    radicalList: [SimpleContentObject],
}

interface SimpleContentObject {
    type: String,
    qid: String,
    status: 'mastered'|'familiar'|'remaining',
    chinese: String,
    pinyin: String,
}


export default Assignment;