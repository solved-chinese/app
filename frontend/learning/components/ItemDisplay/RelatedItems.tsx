import React, { CSSProperties } from "react";
import styled from "styled-components";
import "@learning.styles/ItemDisplay.css";
import { CharacterShort, ItemType, WordShort } from "@interfaces/CoreItem";

const Heading = styled.h2`
  color: var(--teritary-text);
  margin-top: 10px;
  font-size: 0.9em;
  font-weight: 400;
`;

const RelatedItemsList = styled.ul`
  line-height: 1.5em;
`;

type RelatedItemsProps = {
  /**
   * The character used to look up related items
   * a user has viewed so far. Not
   * @deprecated
   */
  item: string;

  /**
   * A list of items to be displayed in the related
   * items view.
   */
  items: CharacterShort[] | WordShort[];

  /**
   * The type of the related items to be displayed
   * (word or character)
   */
  itemType: Extract<ItemType, "word" | "character">;
};

/** Display related words that a user has seen. */
export default class RelatedItems extends React.Component<RelatedItemsProps> {
  render(): JSX.Element {
    const items = this.props.items;
    if (items.length == 0) {
      return <></>;
    } else {
      return (
        <>
          <Heading>{`Related ${this.props.itemType}s you've seen`}</Heading>
          <RelatedItemsList>
            {items.map((v, i) => {
              return (
                <RelatedItemEntry
                  style={i % 2 ? {} : {}} // changed to single color
                  key={v.chinese}
                  item={v}
                />
              );
            })}
          </RelatedItemsList>
        </>
      );
    }
  }
}

const RelatedWordItemDisplay = styled.li`
  display: flex;
  justify-content: flex-start;
  padding: 3px 3px 3px 6px;
`;

const ItemComp = styled.p`
  display: inline-block;
  font-size: 1em;
  color: var(--secondary-text);
  padding-right: 15px;
  margin-bottom: 0;
  white-space: nowrap;
`;

const ItemCompWord = styled(ItemComp)`
  font-size: 1.2em;
`;

const ItemCompPhonetic = styled(ItemComp)`
  font-size: 0.9em;
`;

const ItemCompDef = styled(ItemComp)`
  flex-grow: 3;
  max-width: 90%; // aligning approach, 60% is good for breakdown view, 90% is good for character display
  margin-left: auto; // aligning approach
  text-overflow: ellipsis;
  overflow: hidden;
`;

type RelatedItemEntryProps = {
  /**
   * The css style object to be used for this entry.
   */
  style: CSSProperties;

  /**
   * The word or character short-form descriptor.
   */
  item: CharacterShort | WordShort;
};

class RelatedItemEntry extends React.Component<RelatedItemEntryProps> {
  render(): JSX.Element {
    const { chinese, pinyin, fullDefinition } = this.props.item;

    // TODO: The curly font for part of speech
    return (
      <RelatedWordItemDisplay style={this.props.style}>
        <ItemCompWord className="use-chinese">{chinese}</ItemCompWord>
        <ItemCompPhonetic className="use-chinese">
          {`/${pinyin}/`}
        </ItemCompPhonetic>
        <ItemCompDef className="use-serifs divider">
          {fullDefinition}
        </ItemCompDef>
      </RelatedWordItemDisplay>
    );
  }
}
