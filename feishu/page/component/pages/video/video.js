import i18n from '../../../i18n/index'
const iVideo = i18n.video

function getRandomColor () {
  const rgb = []
  for (let i = 0 ; i < 3; ++i){
    let color = Math.floor(Math.random() * 256).toString(16)
    color = color.length == 1 ? '0' + color : color
    rgb.push(color)
  }
  return '#' + rgb.join('')
}

Page({
  data: {
    ...iVideo
  },
  onReady: function (res) {
    this.videoContext = tt.createVideoContext('myVideo')
  },
  inputValue: '',
    data: {
    src: '',
    danmuList:
      [{
        text: 'the text show in 1s',
        color: '#ff0000',
        time: 1
      },
      {
        text: 'the text show in 3s',
        color: '#ff00ff',
        time: 3
      }]
    },
  bindInputBlur: function(e) {
    this.inputValue = e.detail.value
  },
  bindButtonTap: function() {
    tt.chooseVideo({
        sourceType: ['album', 'camera'],
        maxDuration: 60,
        camera: ['front','back'],
        success:res => {
            this.setData({
                src: res.tempFilePath
            })
        }
    })
  },
  bindSendDanmu: function () {
    this.videoContext.sendDanmu({
      text: this.inputValue,
      color: getRandomColor()
    })
  },
  bindPlay: function() {
    this.videoContext.play()
  },
  bindPause: function() {
    this.videoContext.pause()
  },
  videoErrorCallback: function(e) {
    console.log('video error message:')
    console.log(e.detail.errMsg)
  }
})