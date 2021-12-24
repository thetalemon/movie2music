import React, { MouseEventHandler } from 'react'
import styled from '@emotion/styled'

// const GeneralButton = styled.button`
//   background: #d9d6ff;
//   border: none;
//   padding: 8px 16px;
//   border-radius: 4px;
//   &:hover{
//     opacity: .7;
//     cursor: pointer;
//   }
// `

const GeneralButton = styled.button`
  -webkit-box-sizing: border-box;
  box-sizing: border-box;
  font-size: 62.5%;
  border: none;

  font-size: 24px;
  font-weight: 700;
  line-height: 1.5;
  position: relative;
  display: inline-block;
  /* padding: 1rem 4rem; */
  cursor: pointer;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  -webkit-transition: all 0.3s;
  transition: all 0.3s;
  text-align: center;
  vertical-align: middle;
  text-decoration: none;
  letter-spacing: 0.1em;
  /* color: #212529; */
  /* border-radius: 0.5rem; */
  /* font-weight: 700; */
  line-height: 54px;

  /* width: 204px;
  height: 54px; */
  padding: 8px 16px;
  /* margin: 4px; */

  cursor: pointer;
  text-decoration: none;

  background-color: transparent;

  svg {
    position: absolute;
    top: 0;
    left: 0;

    width: 100%;
    height: 100%;
  }

  svg rect {
    -webkit-transition: all 400ms ease;
    transition: all 400ms ease;

    stroke: #000;
    width: 99%;
    height: 92%;
    stroke-width:2;
    y: 1;
    x: 1;
    stroke-dasharray: 200px, 16px;
    stroke-dashoffset: 70px;
  }

  :hover svg rect {
    stroke-dashoffset: 284px;
  }

  span {
    color: #000;
  }
`


type Props = {
  text: string,
  onClick: MouseEventHandler<HTMLButtonElement>
}

const Button = ({ text, onClick }: Props) => (
  <GeneralButton onClick={onClick}>
    <svg>
      <rect rx="6" fill="none"/>
    </svg>
    <span>{ text }</span>
  </GeneralButton>
)

export default Button
