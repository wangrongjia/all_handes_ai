import i18n from '../../../i18n/index'
const iFile = i18n.file

Page({
  onLoad: function (e) {
    this.setData({
      savedFilePath: tt.getStorageSync('savedFilePath')
    })
  },
  data: {
    tempFilePath: '',
    savedFilePath: '',
    dialog: {
      hidden: true
    },
    fileList: [],
    ...iFile
  },
  chooseImage: function (e) {
    tt.chooseImage({
      count: 1,
      success: res => {
        console.log(JSON.stringify(res))
        this.setData({
          tempFilePath: res.tempFilePaths[0]
        })
      }
    })
  },
  saveFile: function (e) {
    if (this.data.tempFilePath.length > 0) {
      tt.saveFile({
        tempFilePath: this.data.tempFilePath,
        filePath: "ttfile://user/tt/feishu.png",
        success: res => {
          console.log(JSON.stringify(res))
          this.setData({
            savedFilePath: res.savedFilePath
          })
          tt.setStorageSync('savedFilePath', res.savedFilePath)
          this.setData({
            dialog: {
              title: 'Save Success',
              content: 'The file will restore when you enter app next time.',
              hidden: false
            }
          })
        },
        fail: res => {
          console.log(JSON.stringify(res))
          this.setData({
            dialog: {
              title: 'Save Failed',
              content: 'may be have some bug',
              hidden: false
            }
          })
        }
      })
    }
  },
  clear: function (e) {
    tt.setStorageSync('savedFilePath', '')
    this.setData({
      tempFilePath: '',
      savedFilePath: ''
    })
  },
  filePickerLark: function (e) {
    tt.filePicker({
      maxNum: 2,
      success: res => {
        console.log(JSON.stringify(res))
        this.setData({
          fileList: res.list
        });
      },
      fail: res => {
        console.log(JSON.stringify(res))
        tt.showToast({
          title: 'Choose attachment failed.',
          icon: 'none',
          image: '',
          duration: 1500
        });
      }
    });
  },
  filePickerSystem: function (e) {
    tt.filePicker({
      isSystem: true,
      success: res => {
        console.log(JSON.stringify(res))
        this.setData({
          fileList: res.list
        });
      },
      fail: res => {
        console.log(JSON.stringify(res))
        tt.showToast({
          title: 'Choose attachment failed.',
          icon: 'none',
          image: '',
          duration: 1500
        });
      }
    });
  },
  openDocument: function (e) {
    tt.downloadFile({
      // url example
      url: 'http://10.94.92.192/openFile',
      success: res => {
        console.log(JSON.stringify(res))
        const filePath = res.tempFilePath
        tt.openDocument({
          filePath,
          fileType: "docx",
          success: res => {
            console.log(JSON.stringify(res))
          }
        })
      }
    })
  },
  confirm: function (e) {
    this.setData({
      'dialog.hidden': true
    })
  }
})
