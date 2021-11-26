import React, { MouseEventHandler } from 'react'
import Button from './Button'

type Props = {
  filePath: string
  onClickDoImgProcess: MouseEventHandler<HTMLButtonElement>
}

const Title = ({ filePath, onClickDoImgProcess }: Props) => {
  if (!filePath) {
    return null;
  }
  return (
    <p>
      選択中のファイル: {filePath}<br/>
      <Button text="選択したファイルで処理を開始" onClick={onClickDoImgProcess} />
    </p>
  )
}
export default Title
