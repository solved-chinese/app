import React, {useState, useRef} from 'react';
import Radio from '@material-ui/core/Radio';
import RadioGroup from '@material-ui/core/RadioGroup';
import FormControlLabel from '@material-ui/core/FormControlLabel';
import FormControl from '@material-ui/core/FormControl';
import FormLabel from '@material-ui/core/FormLabel';
import styled from 'styled-components';
import '@assignment.styles/SearchPage.css';
import getSearchResults from '@learning.services/getSearchResults'
import { ContentObject } from "@interfaces/Search";

// Containers
const ContentContainer = styled.div`
    max-width: 900px;
    margin: 20px auto;
    
    @media only screen and (max-width: 480px) {
    margin: 20px 0;
    }
`;
const SearchButton = styled.button`
    width: 100px;
    height: 20px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 10px;
    background-color: red;
    font-size: 1.5rem;
    text-align: center;
    color: white;
    outline: none;
    box-shadow: none;
`;

const ChoiceButton = styled.button`
    width: 100px;
    height: 20px;
    margin-left: auto;
    margin-right: auto;
    border-radius: 10px;
    border: none;
    font-size: 1.5rem;
    text-align: center;
    color: black;
    outline: none;
    box-shadow:none;
`;


type SearchProps = {};



const SearchPage = (prop: SearchProps): JSX.Element => {
    const [queryType, setQueryType] = useState<'auto'|'chinese'|'pinyin'|'definition'>('auto');
    const [keyword, setKeyword] = useState<string>('');
    const [resultList, setResultList] = useState<ContentObject[]>(Array<ContentObject>(0));

    const handleQueryTypeChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setQueryType((event.target as HTMLInputElement).value);
    };

    const onSubmit = () => {
        getSearchResults({
            keyword: keyword,
            queryType: queryType
        }).then((searchResult) => {
            setResultList(searchResult.results);
        })
    };

    const renderSearchResult = () => {
        return resultList.map((contentObject, index) => (
            <div key={index}>
                 {contentObject.chinese}
            </div>
        ));
    };

    return (
        <ContentContainer>
            <FormControl component="fieldset">
                <FormLabel component="legend">Search By</FormLabel>
                <RadioGroup row value={queryType} onChange={handleQueryTypeChange}>
                    <FormControlLabel value="auto" control={<Radio />} label="Auto" />
                    <FormControlLabel value="chinese" control={<Radio />} label="Chinese" />
                    <FormControlLabel value="pinyin" control={<Radio />} label="Pinyin" />
                    <FormControlLabel value="definition" control={<Radio />} label="English Definition" />
                </RadioGroup>
            </FormControl>
            <br/>
            <input
                autoFocus
                value={keyword}
                onChange={ e => setKeyword(e.target.value) }
            />
            <button onClick={onSubmit}>
                Search
            </button>
            { renderSearchResult() }
        </ContentContainer>
    );
};

export default SearchPage;
