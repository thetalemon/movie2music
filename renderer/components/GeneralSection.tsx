import React, { ReactNode } from 'react'
import styled from '@emotion/styled'

const MySection = styled.section`
  margin-left: 8px;
`

type Props = {
  children: ReactNode
}

const GeneralSection = ({ children }: Props) => (
  <MySection>{children}</MySection>
)

export default GeneralSection
