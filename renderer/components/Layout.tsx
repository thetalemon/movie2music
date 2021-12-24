import React, { ReactNode } from 'react'
import Link from 'next/link'
import Head from 'next/head'
import styled from '@emotion/styled'

const MainBody = styled.div`
  background: #fff;
  margin: 0;
`

const MainNav = styled.nav`
  text-align: center;
  padding: 4px 0;
`

const MainFooter = styled.footer`
  padding: 4px 0 ;
  margin-top: 8px;
  text-align: center;
`

type Props = {
  children: ReactNode
  title?: string
}

const Layout = ({ children, title = 'This is the default title' }: Props) => (
  <MainBody>
    <Head>
      <title>{title}</title>
      <meta charSet="utf-8" />
      <meta name="viewport" content="initial-scale=1.0, width=device-width" />
    </Head>
    <header>
      <MainNav>
        <Link href="/">
          <a>Home</a>
        </Link>
        <Link href="/about">
          <a>About</a>
        </Link>
        <Link href="/initial-props">
          <a>With Initial Props</a>
        </Link>
      </MainNav>
    </header>
    <div>
      {children}
    </div>
    <MainFooter>
      <a href='https://manasas.dev'>© manasas</a>
    </MainFooter>
  </MainBody>
)

export default Layout
