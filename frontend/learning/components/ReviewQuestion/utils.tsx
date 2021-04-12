import {AudioTextProvider} from '@interfaces/ReviewQuestion';

export const getTextAudio = (obj: AudioTextProvider | string): [string, string | null] => {
    let text = 'error';
    let audio = null;
    if (typeof obj == 'string')
        text = obj;
    else if (typeof obj == 'object') {
        text = obj.text;
        audio = obj.audio;
    }
    return [text, audio];
};
