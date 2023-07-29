import axios from "axios";
import FormData from "form-data";
import { Platform } from 'react-native';
import axiosRetry from 'axios-retry';

import {API_URL} from '@env'

export const findObject = async ({ photoURI, objectName=null }) => {
  const url = `${API_URL}find-object?object_name=${objectName}`;

  const formData = new FormData();
  formData.append("image", {
    uri: photoURI,
    name: "image.jpg",
    type: "image/jpeg",
  });

  const headers = {
    Accept: "application/json",
    "Content-Type": "multipart/form-data",
  };

  if (Platform.OS === "ios") {
    headers["Content-Type"] =
      "multipart/form-data; boundary=" + formData._boundary;
  }
  const axiosConfig = {
    url,
    method: 'post',
    data: formData,
    headers,
  };

  return await axios(axiosConfig)
};



export const describeScene = async ({ photoURI}) => {
  const url = `${API_URL}image-caption`;

  const formData = new FormData();
  formData.append("image", {
    uri: photoURI,
    name: "image.jpg",
    type: "image/jpeg",
  });

  const headers = {
    Accept: "application/json",
    "Content-Type": "multipart/form-data",
  };

  if (Platform.OS === "ios") {
    headers["Content-Type"] =
      "multipart/form-data; boundary=" + formData._boundary;
  }
  const axiosConfig = {
    url,
    method: 'post',
    data: formData,
    headers,
  };

  return await axios(axiosConfig)

};

export const extractText = async ({ photoURI}) => {
  const url = `${API_URL}extract-text`;

  const formData = new FormData();
  formData.append("image", {
    uri: photoURI,
    name: "image.jpg",
    type: "image/jpeg",
  });

  const headers = {
    Accept: "application/json",
    "Content-Type": "multipart/form-data",
  };

  if (Platform.OS === "ios") {
    headers["Content-Type"] =
      "multipart/form-data; boundary=" + formData._boundary;
  }
  const axiosConfig = {
    url,
    method: 'post',
    data: formData,
    headers,
  };

  return await axios(axiosConfig)
};


export const registerFace = async ({ name, photoURI}) => {
  const url = `${API_URL}register-face?name=${name}`;

  const formData = new FormData();
  formData.append("image", {
    uri: photoURI,
    name: "image.jpg",
    type: "image/jpeg",
  });

  const headers = {
    Accept: "application/json",
    "Content-Type": "multipart/form-data",
  };

  if (Platform.OS === "ios") {
    headers["Content-Type"] =
      "multipart/form-data; boundary=" + formData._boundary;
  }
  const axiosConfig = {
    url,
    method: 'post',
    data: formData,
    headers,
  };
  return await axios(axiosConfig)

};


export const recogniseFace = async ({photoURI}) => {
  const url = `${API_URL}recognise-face`;

  const formData = new FormData();
  formData.append("image", {
    uri: photoURI,
    name: "image.jpg",
    type: "image/jpeg",
  });

  const headers = {
    Accept: "application/json",
    "Content-Type": "multipart/form-data",
  };

  if (Platform.OS === "ios") {
    headers["Content-Type"] =
      "multipart/form-data; boundary=" + formData._boundary;
  }
  const axiosConfig = {
    url,
    method: 'post',
    data: formData,
    headers,
  };
  return await axios(axiosConfig) 

};

export const detectColor = async ({ photoURI}) => {
  const url = `${API_URL}detect-color`;

  const formData = new FormData();
  formData.append("image", {
    uri: photoURI,
    name: "image.jpg",
    type: "image/jpeg",
  });

  const headers = {
    Accept: "application/json",
    "Content-Type": "multipart/form-data",
  };

  if (Platform.OS === "ios") {
    headers["Content-Type"] =
      "multipart/form-data; boundary=" + formData._boundary;
  }
  const axiosConfig = {
    url,
    method: 'post',
    data: formData,
    headers,
  };

  return await axios(axiosConfig)

};