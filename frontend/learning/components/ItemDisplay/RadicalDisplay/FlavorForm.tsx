import React, { Component } from "react";
import styled from "styled-components";

import "@learning.styles/Menus.css";

const ExplanationSignal = styled.img`
  position: relative;
  margin-top: 27px; // according to the position of text of definition
  margin-left: 3px;
  font-weight: 100;
  // width = 100%;
  cursor: pointer;
  transform: scale(0.6);
  filter: invert(12%) sepia(69%) saturate(6868%) hue-rotate(7deg) brightness(92%) contrast(109%); 
  &:hover {
    transform: scale (0.8);
    transition : 200ms ease-in-out
  }
`;

interface Props {
  explanation: string;
}

interface IState {
  modalIsOpen: string;
  atUserItems: boolean;
}

const Explanation = styled.div`
  color: var(--secondary-text);
  font-size: 1em;
  text-align: left;
`;

export default class FlavorForm extends React.Component<Props, IState> {
  constructor(props: Props) {
    super(props);
    this.state = {
      modalIsOpen: "none",
      atUserItems: false,
    };

    // this.contentBtn=this.contentBtn.bind(this),
    // this.programBtn=this.programBtn.bind(this),
    this.handleMouseOver = this.handleMouseOver.bind(this);
    this.handleMouseOut = this.handleMouseOut.bind(this);
    // this.userCenter = this.userCenter.bind(this);
    this.handleMouseUserOver = this.handleMouseUserOver.bind(this);
  }

  explanation = this.props.explanation;

  handleMouseOver(e: React.MouseEvent<HTMLImageElement>) {
    this.setState({
      modalIsOpen: "block",
    });
  }

  handleMouseOut() {
    this.setState({
      modalIsOpen: "none",
    });
  }

  handleMouseUserOver(e: React.MouseEvent<HTMLElement>) {
    this.setState({
      modalIsOpen: "block",
    });
  }

  render() {
    return (
      <div className="body">
        <ExplanationSignal
          src="/static/images/small-icons/info_outline_black_24dp.svg"
          width="20px"
          onMouseOver={this.handleMouseOver}
          onMouseLeave={this.handleMouseOut}
        />

        <div
          className="menus"
          style={{ display: this.state.modalIsOpen }}
          onMouseOver={this.handleMouseUserOver}
          onMouseLeave={this.handleMouseOut}
        >
          <ul className="ul">
            <li className="li">
              {this.explanation !== "" ? (
                <Explanation>{this.explanation}</Explanation>
              ) : (
                <Explanation>Loading</Explanation>
              )}
            </li>
          </ul>
        </div>
      </div>
    );
  }
}
