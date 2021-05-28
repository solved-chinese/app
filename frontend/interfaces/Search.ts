export interface SearchParams {
    keyword: string,
    queryType: 'auto' | 'chinese' | 'pinyin' | 'definition',
}

export interface ContentObject {
    chinese: string
}

export interface SearchResult {
    results: ContentObject[],
    queryType: 'pinyin' | 'definition' | 'chinese',
}
