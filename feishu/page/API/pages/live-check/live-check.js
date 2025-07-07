import i18n from '../../../i18n/index'
const iLiveCheck = i18n.live_check

Page({
  data: {
    ...iLiveCheck
  },
  startFaceVerify: function () {
    tt.startFaceVerify({
      userId: 'ou_3a85bc15f186865bf03d9fa522878a53',
      success: (res) => {
        console.log(res)

      },
      fail: (res) => {
        console.log(res)

      }
    })
  }
})
