import { useEffect, useState } from 'react'
import Link from 'next/link'
import Layout from '../components/Layout'
import { apiClient } from "../libs/appClinent";

const IndexPage = () => {
  const [filePath, setFilePath] = useState('')
  const [detectedColor, setDetectedColor] = useState('')
  const [pathList, setPathList] = useState([])  

  useEffect(() => {
    global.ipcRenderer.addListener('message', (_event, args) => {
      alert(args)
    })
    apiClient
    .get("/process/complete")
    .then((response) => {
      setPathList(response.data.pathList)
    })
  }, [])

  const htmlPathList = () => {
    return pathList.map((path: string) => {
      return (<button onClick={() => onClickGetFile(path)}>{path}</button>)
    })
  }

  const onSayHiClick = () => {
    global.ipcRenderer.send('message', 'hi from next')
  }

  const onClickSetFile = async () => {
    setFilePath(await global.ipcRenderer.invoke('getFilePath'))
  }

  const onClickGetFile = async (path: string) => {
    global.ipcRenderer.send('download', path)
  }

  const onClickDoImgProcess = async () => {
    let formData = new FormData();
    formData.append("file", filePath);
    apiClient
      .post("/process/img", formData)
      .then((response) => {
        setDetectedColor(response.data)
      })
  }

  return (
    <Layout title="Home | Next.js + TypeScript + Electron Example">
      <h1>Hello Next.js 👋</h1>
      <button onClick={onSayHiClick}>Say hi to electron</button>
      <button onClick={onClickSetFile}>set file</button>
      <button onClick={onClickDoImgProcess}>do img processing</button>
      <p>
        <Link href="/about">
          <a>About</a>
        </Link>
      </p>
      {htmlPathList()}
      <p>
        {filePath}
      </p>
      <p>
        {detectedColor}
      </p>
    </Layout>
  )
}

export default IndexPage
