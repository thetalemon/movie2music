import { useEffect, useState } from 'react'
import Link from 'next/link'
import Layout from '../components/Layout'
import { apiClient } from "../libs/appClinent";

const IndexPage = () => {
  // const [text, setText] = useState('')
  const [filePath, setFilePath] = useState('')

  useEffect(() => {
    global.ipcRenderer.addListener('message', (_event, args) => {
      alert(args)
    })
  }, [])

  const onSayHiClick = () => {
    global.ipcRenderer.send('download', 'sample.mid')
    global.ipcRenderer.send('message', 'hi from next')
  }

  const onClickSetFile = async () => {
    setFilePath(await global.ipcRenderer.invoke('getFilePath'))
  }

  const onClickCopyFile = async () => {
    
    let formData = new FormData();
    formData.append("file", filePath);
    apiClient
      .post("/uploadFile", formData
      )
      .then((response) => {
        // memo: ここで渡した絶対パスの画像・動画を参照して自動生成を行うようにする
        // console.log(response)
      })
  }

  return (
    <Layout title="Home | Next.js + TypeScript + Electron Example">
      <h1>Hello Next.js 👋</h1>
      <button onClick={onSayHiClick}>Say hi to electron</button>
      <button onClick={onClickSetFile}>set file</button>
      <button onClick={onClickCopyFile}>copy file</button>
      <p>
        <Link href="/about">
          <a>About</a>
        </Link>
      </p>
      <p>
        {filePath}
      </p>
    </Layout>
  )
}

export default IndexPage
