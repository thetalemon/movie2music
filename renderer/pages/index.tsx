import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import { apiClient } from "../libs/appClinent";
import styled from '@emotion/styled'

const PathTable = styled.table`
  border: #4d7eaf 2px solid;
  border-radius: 4px;
	border-collapse: collapse;
  tr {
    width: 100%;
    border-top: #4d7eaf 1px solid;
    border-bottom: #4d7eaf 1px solid;
  }
  td {
    width: 100%;
    padding: 8px 16px;
    &:hover{
      opacity: .5;
      cursor: pointer;
    }
  }
`

const TitleH1 = styled.h1`
  margin-bottom: 4px;
`

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

const GeneralSection = styled.section`
  margin-left: 8px;
`

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
      return (
        <tr key={path}>
          <td onClick={() => onClickGetFile(path)}>{path}</td>
        </tr>
      )
    })
  }

  function FileSelected (props: { filePath: string; }) {
    if (!props.filePath) {
      return null;
    }
    return (
      <p>
        選択中のファイル: {filePath}<br/>
        <GeneralButton onClick={onClickDoImgProcess}>選択したファイルで処理を開始</GeneralButton>
      </p>
    )
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
      <TitleH1>動画に基づいた音楽を作る</TitleH1>
      <GeneralSection>
        <GeneralButton onClick={onClickSetFile}>ファイルを選択</GeneralButton>
      </GeneralSection>
      <GeneralSection>
        <FileSelected filePath={filePath} />
      </GeneralSection>

      <TitleH1>Generated files</TitleH1>
      <GeneralSection>
        <PathTable>
          <tbody>
            {htmlPathList()}
          </tbody>
        </PathTable>
      </GeneralSection>
    </Layout>
  )
}

export default IndexPage
