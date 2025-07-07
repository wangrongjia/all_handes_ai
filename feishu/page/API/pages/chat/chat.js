Page({
  chatAndProfileInput: function (e) {
    this.inputValue = e.detail.value
    this.setData({
      disabled: this.inputValue.length <= 0
    })
  },
  chatFeishu: function (e) {
    tt.login({
      success: res => {
        console.log(JSON.stringify(res));
        tt.enterChat({
          openid: this.inputValue,
          success: res => {
            console.log(JSON.stringify(res));
          },
          fail: res => {
            console.log(JSON.stringify(res));
          }
        });
      },
      fail: res => {
        console.log(JSON.stringify(res));
      }
    })
  },
  profileFeishu: function (e) {
    tt.login({
      success: res => {
        console.log(JSON.stringify(res))
        tt.enterProfile({ openid: this.inputValue })
      },
      fail: res => {
        console.log(JSON.stringify(res))
      }
    })
  },
  botFeishu: function (e) {
    tt.login({
      success(res) {
        console.log(JSON.stringify(res))
        tt.enterBot({
          success(res) {
            console.log(JSON.stringify(res));
          },
        })
      },
      fail: res => {
        console.log(JSON.stringify(res));
      }
    })
  }
})
