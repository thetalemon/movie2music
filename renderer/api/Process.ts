import { apiClient } from '../libs/appClinent';

export async function doImgProcess(filePath: string) {
  let formData = new FormData();
  formData.append('file', filePath);
  return apiClient.post('/process/img', formData).then((response) => {
    return response.data;
  });
}

export async function getComplete() {
  return apiClient.get('/process/complete').then((response) => {
    return response.data.pathList;
  });
}
