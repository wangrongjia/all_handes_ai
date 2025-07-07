import i18n from '../../../i18n/index'
const iGetConnectedWifi = i18n.get_connected_wifi

var util = require('../../../../util/util.js')
var playTimeInterval
var recordTimeInterval

Page({
  data: {
    recording: false,
    playing: false,
    hasRecord: false,
    recordTime: 0,
    playTime: 0,
    formatedRecordTime: '00:00:00',
    formatedPlayTime: '00:00:00'
  },
  onShow: function () {
    var iac = this.innerAudioContext = tt.createInnerAudioContext();
    iac.startTime = 0;

    var rm = this.recorderManager = tt.getRecorderManager()
    var that = this
    rm.onStart(() => {
      console.log('recorder start')
      that.setData({
        formatedRecordTime: util.formatTime(that.data.recordTime)
      })
    });

    rm.onStop((res) => {
      console.log('recorder stop', res)
      that.setData({
        recording: false,
        hasRecord: true,
        tempFilePath: res.tempFilePath,
        formatedRecordTime: util.formatTime(that.data.recordTime)
      })
      iac.src = res.tempFilePath;
      iac.obeyMuteSwitch = false;
      clearInterval(recordTimeInterval)
    });

    rm.onFrameRecorded((res) => {
      console.log('recorder complete framebuffer:', res.frameBuffer)
      console.log('recorder complete isLastFrame:', res.isLastFrame)
    })


    iac.onPlay(() => {
      console.log('onPlay', 'voice start play');

    });

    iac.onStop(() => {
      console.log('onStop', 'voice stop played');

      this.setData({
        playing: false,
        formatedPlayTime: util.formatTime(0),
        playTime: 0
      })
      clearInterval(playTimeInterval)
    });
    iac.offStop(() => {
      console.log('onoffstop', 'cancel the event for voice stop');

    });

    iac.onPause(() => {
      console.log('onPause', 'voice paused');

      this.setData({
        playing: false,
        formatedPlayTime: util.formatTime(0),
        playTime: 0
      })
      //  clearInterval(playTimeInterval)
    });

    iac.onEnded(() => {
      console.log('onEnded', 'voice play ended');
      this.setData({
        playing: false,
        playTime: 0,
        formatedPlayTime: util.formatTime(0)
      })
      clearInterval(playTimeInterval)
    });


    iac.onError(() => {
      log('onError', 'voice play error');

    });


  },
  onHide: function () {
    if (this.data.playing) {
      this.stopVoice()
    } else if (this.data.recording) {
      this.stopRecordUnexpectedly()
    }
  },
  onUnload() {
    if (this.innerAudioContext) {
      this.innerAudioContext.destroy();
    }
  },
  startRecord: function () {
    this.setData({ recording: true })

    var that = this
    recordTimeInterval = setInterval(function () {
      var recordTime = that.data.recordTime += 1
      that.setData({
        formatedRecordTime: util.formatTime(that.data.recordTime),
        recordTime: recordTime
      })
    }, 1000)
    const options = {
      duration: 100000,
      sampleRate: 44100,
      numberOfChannels: 2,
      encodeBitRate: 320000,
      format: 'aac',
      frameSize: 50
    };

    this.recorderManager.start(options);


  },
  stopRecord: function () {
    this.recorderManager.stop();
  },
  stopRecordUnexpectedly: function () {
    this.stopRecord();
    this.setData({
      recording: false,
      hasRecord: false,
      recordTime: 0,
      formatedRecordTime: util.formatTime(0)
    })
  },
  playVoice: function () {
    var that = this
    playTimeInterval = setInterval(function () {
      var playTime = that.data.playTime + 1
      that.setData({
        playing: true,
        formatedPlayTime: util.formatTime(playTime),
        playTime: playTime
      })
    }, 1000)
    this.innerAudioContext.play();
  },
  stopVoice: function () {
    console.log("stop voice")
    var that = this
    that.setData({

    })
    this.innerAudioContext.stop();

  },
  clear: function () {
    clearInterval(playTimeInterval)
    this.innerAudioContext.stop();
    this.setData({
      playing: false,
      hasRecord: false,
      tempFilePath: '',
      formatedRecordTime: util.formatTime(0),
      recordTime: 0,
      playTime: 0
    })
  }
})
