import React from 'react'
import styled from '@emotion/styled'

const PathTable = styled.table`
  border: #4d7eaf 2px solid;
  border-radius: 4px;
	border-collapse: collapse;
  margin: 0 auto;
  tr {
    width: 100%;
    border-bottom: #4d7eaf 1px solid;
    &:last-child {
      border-bottom: none;
    }
  }
  td {
    padding: 8px 16px;
    border-right: #4d7eaf 1px solid;
    &:last-child{
      border-right: none;
    }
  }
`
const DownloadTd = styled.td`
  &:hover{
  opacity: .5;
  cursor: pointer;
  }
`


const onClickGetFile = async (path: string) => {
  global.ipcRenderer.send('download', path)
}

const htmlPathList = (pathList: string[]) => {
  const regexp = new RegExp('[(][0-9]+[)]')
  const onlynum = new RegExp('[0-9]+')
  const sortedPathList = pathList.sort((a, b) => {
    if(a.match(regexp) === null) return -1
    if(b.match(regexp) === null) return -1
    const extractA = a.match(regexp)[0]
    const numA = parseInt(extractA.match(onlynum)[0])
    const extractB = b.match(regexp)[0]
    const numB = parseInt(extractB.match(onlynum)[0])
    return numA - numB
  })
  return sortedPathList.map((path: string) => {
    return (
      <tr key={path}>
        <td>{path}</td>
        <DownloadTd onClick={() => onClickGetFile(path)}>ダウンロード</DownloadTd>
      </tr>
    )
  })
}

type Props = {
  pathList: string[]
}

const PathList = ({ pathList }: Props) => (
  <PathTable>
    <tbody>
      {htmlPathList(pathList)}
    </tbody>
  </PathTable>
)

export default PathList
