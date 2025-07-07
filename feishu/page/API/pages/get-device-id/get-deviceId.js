Page({
  data: {
    deviceId: '',
  },
  getDeviceId: function () {
    var that = this
    tt.getDeviceID({
      success: res => {
        that.setData({
            deviceId: res.deviceID 
        })
      },
      fail: res => {
        console.log("·")
        that.setData({
          deviceId: JSON.stringify(res)
        })
      }
    })
  },
  authorize: function() {
    tt.authorize({
      scope: 'scope.deviceID',
      success () {
        // 用户已经同意小程序使用录音功能，后续调用 tt.startRecord 接口不会弹窗询问
        console.log('grand permission')
      }
    })
  },
  openSetting: () => {
    tt.openSetting({
      success (res) {
        console.log(res.authSetting)
      }
    })
  },
  getSetting: () => {
    tt.getSetting({
      success (res) {
        console.log(res.authSetting)
      }
    })
  }
})