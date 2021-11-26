import React, { MouseEventHandler } from 'react'
import styled from '@emotion/styled'

const GeneralButton = styled.button`
  background: #d9d6ff;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  &:hover{
    opacity: .7;
    cursor: pointer;
  }
`

type Props = {
  text: string,
  onClick: MouseEventHandler<HTMLButtonElement>
}

const Button = ({ text, onClick }: Props) => (
  <GeneralButton onClick={onClick}>{text}</GeneralButton>
)

export default Button
