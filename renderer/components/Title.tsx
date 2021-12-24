import React from 'react'
import styled from '@emotion/styled'

const TitleH1 = styled.h1`
  margin-bottom: 4px;
  text-align: center;
`

type Props = {
  text: string
}

const Title = ({ text }: Props) => (
  <TitleH1>{text}</TitleH1>
)

export default Title
