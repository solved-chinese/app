import React, { CSSProperties } from "react";
import styled from "styled-components";
import { ProgressBarData } from "@interfaces/CoreLearning";

// Body: use padding to adjust Bar's position
const Body = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 20px 30px;
  font-size: 14px;

  @media only screen and (max-width: 480px) {
    padding: 20px 10px;
    font-size: 13px;
  }
`;
// Outer bar container
const BarContainer = styled.div`
  background-color: #d8d8d8;
  position: relative;
  height: 7px;
  width: 100%;
  display: flex;
  flex-direction: row;
`;
// Inner color bar
const Bar = styled.div`
  background: #d8d8d8;
  box-shadow: 2px 2px 5px #d8d8d8;
  display: flex;
  //align-items: flex-start;
  justify-content: left;
  height: 100%;
  width: 0;
  opacity: 1;
  transition: 1s ease 0.3s;
`;
// Text Container Below
const TextContainer = styled.div`
  position: relative;
  height: 10px;
  width: 100%;
  display: flex;
  flex-direction: row;
  margin-top: 7px;
  font-size: 1em;
`;
const Text = styled.div`
  width: 0;
  min-width: 70px;
  text-align: left;
`;

/**
 * Render a progress bar component with the number of items from
 * the 4 experience categories (mastered, familiar, remaining, bonus).
 */
export default class ProgressBar extends React.Component<ProgressBarData> {
  render(): JSX.Element {
    const total =
      this.props.mastered +
      this.props.familiar +
      this.props.remaining +
      this.props.bonus;

    const margin = 5;
    const modifier = 100 - 4 * margin;
    const colors: string[] = [
      "rgb(85, 162, 30)",
      "rgb(141, 207, 84)",
      "rgb(212, 210, 210)",
      "rgb(255, 195, 0)",
    ];
    const barItemLengthArr: number[] = [
      this.props.mastered,
      this.props.familiar,
      this.props.remaining,
      this.props.bonus,
    ];
    const barStyle: CSSProperties[] = colors.map((color, index) => {
      return {
        width: `${(barItemLengthArr[index] / total) * modifier + margin}%`,
        background: color,
      };
    });

    const textStyle: CSSProperties[] = colors.map((color, index) => {
      return {
        width: `${(barItemLengthArr[index] / total) * modifier + margin}%`,
        color: color,
      };
    });

    return (
      <Body>
        <BarContainer>
          {barStyle.map((style, index) => (
            <Bar style={style} key={index} />
          ))}
        </BarContainer>

        <TextContainer>
          <Text style={textStyle[0]}> {this.props.mastered} mastered</Text>
          <Text style={textStyle[1]}> {this.props.familiar} familiar</Text>
          <Text style={textStyle[2]}> {this.props.remaining} remaining</Text>
          {this.props.bonus > 0 && (
            <Text style={textStyle[3]}> {this.props.bonus} bonus!</Text>
          )}
        </TextContainer>
      </Body>
    );
  }
}
