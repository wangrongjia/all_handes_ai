// const downloadExampleUrl = require('../../../../config').downloadExampleUrl
import i18n from '../../../i18n/index'
const iDownloadFile = i18n.download_file

const imageURL = 'https://sf1-cdn-tos.huoshanstatic.com/obj/larkdeveloper/opdev/img/sunset.jpeg'
const videoURL = 'https://sf1-cdn-tos.huoshanstatic.com/obj/ttfe/tma/test.mp4'

var downloadImageTask;
var downloadVideoTask;
Page({
  data: {
    ...iDownloadFile
  },
  downloadImage: function () {
    var self = this

    downloadImageTask = tt.downloadFile({
      url: imageURL,
      success: function (res) {
        console.log(JSON.stringify(res))
        tt.showToast({
          title: 'downloadFile success',
          icon: 'none'
        });
        self.setData({
          imageSrc: res.tempFilePath
        })
      },
      fail: function (res) {
        console.log(JSON.stringify(res))
        tt.showToast({
          title: 'downloadFile Fail',
          icon: 'none'
        });
      }
    });
    downloadImageTask.onProgressUpdate((res) => {
      console.log(JSON.stringify(res))
      self.setData({
        imageProgress: res.progress
      });
    });



  },
  downloadVideo: function () {
    var self = this

    downloadVideoTask = tt.downloadFile({
      url: videoURL,
      success: function (res) {
        console.log(JSON.stringify(res))
        tt.showToast({
          title: 'downloadFile success',
          icon: 'none'
        });
        self.setData({
          videoSrc: res.tempFilePath
        })
      },
      fail: function (res) {
        console.log(JSON.stringify(res))
        tt.showToast({
          title: 'downloadFile Fail',
          icon: 'none'
        });
      }
    });

    downloadVideoTask.onProgressUpdate((res) => {

      console.log("process:" + res.progress);
      console.log("totalBytesWritten:" + res.totalBytesWritten);
      console.log("totalBytesExpectedToWrite:" + res.totalBytesExpectedToWrite);
      self.setData({
        videoProgress: res.progress
      });

      if (res.progress == 50 || res.progress == 51 || res.progress == 52) {

        console.log("----task.abort--------start")
        task.abort()
        console.log("----task.abort--------end")
      }
    });

  },
  saveImageToPhotosAlbum() {
    tt.saveImageToPhotosAlbum({
      filePath: this.data.imageSrc,
      success: res => {
        console.log(JSON.stringify(res))
        tt.showToast({
          title: 'save success',
          icon: 'none',
          success: res => {
            console.log(JSON.stringify(res))
          },
          fail: res => {
            console.log(JSON.stringify(res))
          }
        })
      },
      fail: res => {
        console.log(JSON.stringify(res))
        tt.showToast({
          title: 'save fail',
          icon: 'none',
          success: res => {
            console.log(JSON.stringify(res))
          },
          fail: res => {
            console.log(JSON.stringify(res))
          }
        })
      }
    })
  },
  saveVideoToPhotosAlbum() {
    tt.saveVideoToPhotosAlbum({
      filePath: this.data.videoSrc,
      success(res) {
        tt.showToast({
          title: 'save success',
          icon: 'none'
        });
        console.log(res);
      },
      fail(res) {
        tt.showToast({
          title: 'save fail',
          icon: 'none'
        });
        console.error(res);
      }
    })
  }
})
