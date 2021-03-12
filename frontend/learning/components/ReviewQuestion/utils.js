export function getTextAudio(obj) {
    let text = 'error';
    let audio = null;
    if (typeof obj == 'string')
        text = obj;
    else if (typeof obj == 'object') {
        text = obj.text;
        audio = obj.audio;
    }
    return [text, audio];
}
