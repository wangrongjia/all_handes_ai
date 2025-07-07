import i18n from '../../../i18n/index'
const iScanCode = i18n.scan_code

var scanType = [['barCode'], ['qrCode'], ['barCode', 'qrCode']]
Page({
  data: {
    result: '',
    ...iScanCode
  },
  scanCode: function () {
    var that = this
    tt.scanCode({
      scanType:scanType[1],
      success: function (res) {
        console.log(res);
        that.setData({
          result: res.result
        })
      },
      fail: function (res) {
        console.log('fail:'+res);
      }
    })
  }
})
