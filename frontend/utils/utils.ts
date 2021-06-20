import { AudioTextProvider } from "@interfaces/ReviewQuestion";

/**
 * Generate a random id containing lower-cased letters and numbers.
 * @param length
 */
export function makeID(length: number): string {
  let result = "";
  const characters = "abcdefghijklmnopqrstuvwxyz0123456789";
  const charactersLength = characters.length;
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return result;
}

/**
 * Retrieve the text audio strings if the object is a AudioTextProvider.
 * @param obj
 */
export const getTextAudio = (
  obj: AudioTextProvider | string
): [string, string | null] => {
  let text = "error";
  let audio = null;
  if (typeof obj == "string") text = obj;
  else if (typeof obj == "object") {
    text = obj.text;
    audio = obj.audio;
  }
  return [text, audio];
};
