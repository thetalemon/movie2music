// Native
import { join } from 'path'
import { format } from 'url'

// Packages
import { BrowserWindow, app, ipcMain, IpcMainEvent, dialog } from 'electron'
import isDev from 'electron-is-dev'
import prepareNext from 'electron-next'
import { download } from "electron-dl";
import { IpcMainInvokeEvent } from 'electron/main'

let mainWindow: BrowserWindow
app.on('ready', async () => {
  await prepareNext('./renderer')

  require('child_process').spawn('python', ['./backend/index.py']);

  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: false,
      preload: join(__dirname, 'preload.js'),
    },
  })

  const url = isDev
    ? 'http://localhost:8000/'
    : format({
        pathname: join(__dirname, '../renderer/out/index.html'),
        protocol: 'file:',
        slashes: true,
      })

  mainWindow.loadURL(url)
})

// Quit the app once all windows are closed
app.on('window-all-closed', app.quit)

// listen the channel `message` and resend the received message to the renderer process
ipcMain.on('message', (event: IpcMainEvent, message: string) => {
  setTimeout(() => event.sender.send('message', message), 500)
})

ipcMain.on("download", async (_event: IpcMainEvent, filename: string) => {
  await download(
    mainWindow,
    "http://127.0.0.1:5000/",
    {
      directory: app.getPath('desktop'),
      filename: filename,
      saveAs: true
    }
  );
});


ipcMain.handle("getFilePath", async (_event: IpcMainInvokeEvent) => {
  const fileName =　await dialog.showOpenDialog(mainWindow, {
    properties: ['openDirectory'],
    title: 'Select a text file',
    defaultPath: '.',
  });

  return fileName.filePaths[0]
});