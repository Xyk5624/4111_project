import axios from 'axios';
import config from '../config/config';
var url = config.url

export function sendGET(path,params = {}) {
  return new Promise(function(resolve,reject){
    axios.get(url + path, {params: params}).then(response => {
      resolve(response)
    }).catch(error => {
      reject(error)
    })
  })
}

export function sendPOST(path,data = {}) {
  return new Promise(function(resolve,reject){
    axios.post(url + path, data).then(response => {
      resolve(response)
      }).catch(error => {
        reject(error)
    })
  })
}

export function sendDELETE(path,data = {}) {
  return new Promise(function(resolve,reject){
    axios.delete(url + path, data).then(response => {
      resolve(response)
      }).catch(error => {
      if (error.response.status == '403') {
          reject(error)
      } else {
          alert(error)
      }
    })
  })
}
