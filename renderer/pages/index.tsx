import { useEffect, useState } from 'react'
import Layout from '../components/Layout'
import PathTable from '../components/PathTable'
import Button from '../components/Button'
import Title from '../components/Title'
import SelectedFileArea from '../components/SelectedFileArea'
import GeneralSection from '../components/GeneralSection'

import { apiClient } from "../libs/appClinent";
import { doImgProcess } from "../api/Process";

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

  const onClickSetFile = async () => {
    setFilePath(await global.ipcRenderer.invoke('getFilePath'))
  }

  const onClickDoImgProcess = async () => {
    setDetectedColor(await doImgProcess(filePath))
  }

  return (
    <Layout title="generate music based on movie">
      <Title text="動画に基づいた音楽を作るしすてむ" />
      <GeneralSection>
        <Button text="ファイルを選択" onClick={onClickSetFile} />
      </GeneralSection>
      <GeneralSection>
        <SelectedFileArea filePath={filePath} onClickDoImgProcess={ onClickDoImgProcess } />
      </GeneralSection>
      <Title text="生成したファイル" />
      <GeneralSection>
        <PathTable pathList={pathList} />
      </GeneralSection>
    </Layout>
  )
}

export default IndexPage
