import i18n from '../../../i18n/index'
const iScreenBrightness = i18n.screen_brightness

Page({
  data: {
     cl: false,
     ...iScreenBrightness
  },
  light () {
    var that = this;
    var now = this.data.cl;
    tt.setKeepScreenOn({
      keepScreenOn: !now,
      success () {
        that.setData({
          cl: !now
        })
        tt.showToast({
          title: `${!now ? iScreenBrightness.constantly_bright : iScreenBrightness.light_out}`
        })
      }
    })
  }
})