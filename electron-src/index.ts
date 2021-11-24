import { join } from 'path';
import { format } from 'url';
import { BrowserWindow, app, ipcMain, IpcMainEvent, dialog } from 'electron';
import isDev from 'electron-is-dev';
import prepareNext from 'electron-next';
import { download } from 'electron-dl';
import { IpcMainInvokeEvent } from 'electron/main';

let mainWindow: BrowserWindow;
app.on('ready', async () => {
  await prepareNext('./renderer');

  var subpy = require('child_process').spawn('python', ['./backend/index.py']);

  mainWindow = new BrowserWindow({
    width: 800,
    height: 600,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: false,
      preload: join(__dirname, 'preload.js'),
    },
  });

  mainWindow.on('closed', function () {
    subpy.kill('SIGINT');
  });

  const url = isDev
    ? 'http://127.0.0.1:8000/'
    : format({
        pathname: join(__dirname, '../renderer/out/index.html'),
        protocol: 'file:',
        slashes: true,
      });

  mainWindow.loadURL(url);
});

app.on('window-all-closed', app.quit);

ipcMain.on('message', (event: IpcMainEvent, message: string) => {
  setTimeout(() => event.sender.send('message', message), 500);
});

ipcMain.on('download', async (_event: IpcMainEvent, filename: string) => {
  await download(
    mainWindow,
    `http://127.0.0.1:5000/process/download?ID=${filename}`,
    {
      directory: app.getPath('desktop'),
      filename: filename,
      saveAs: true,
    }
  );
});

ipcMain.handle('getFilePath', async (_event: IpcMainInvokeEvent) => {
  const fileName = await dialog.showOpenDialog(mainWindow, {
    properties: ['openFile'],
    title: 'Select a text file',
    defaultPath: '.',
  });

  return fileName.filePaths[0];
});
