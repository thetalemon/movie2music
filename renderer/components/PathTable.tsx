import React from 'react'
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

const onClickGetFile = async (path: string) => {
  global.ipcRenderer.send('download', path)
}

const htmlPathList = (pathList: string[]) => {
  return pathList.map((path: string) => {
    return (
      <tr key={path}>
        <td onClick={() => onClickGetFile(path)}>{path}</td>
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
