import { useEffect, useState } from 'react'
import Link from 'next/link'
import Layout from '../components/Layout'
// import { apiClient } from "../libs/appClinent";

const IndexPage = () => {
  // const [text, setText] = useState('')

  useEffect(() => {
    // add a listener to 'message' channel
    global.ipcRenderer.addListener('message', (_event, args) => {
      alert(args)
    })
  }, [])

  // apiClient
  //   .get("/", {
  //   })
  //   .then((response) => {
  //     setText(response.data)
  //   })


  const onSayHiClick = () => {
    global.ipcRenderer.send('download', 'sample.mid')
    global.ipcRenderer.send('message', 'hi from next')
  }

  return (
    <Layout title="Home | Next.js + TypeScript + Electron Example">
      <h1>Hello Next.js 👋</h1>
      <button onClick={onSayHiClick}>Say hi to electron</button>
      <p>
        <Link href="/about">
          <a>About</a>
        </Link>
      </p>
      {/* <p>
        {text}
      </p> */}
    </Layout>
  )
}

export default IndexPage
