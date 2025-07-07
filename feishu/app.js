const openIdUrl = require('./config').openIdUrl

App({
  onLaunch: function (args) {
    console.log('App Launch')
    console.log(args.query)
  },
  onShow: function (args) {
    console.log('App Show');
    console.log(args);
    console.log('-------------')
    // check the update of Gadget
    let updateManager = tt.getUpdateManager();
    updateManager.onCheckForUpdate((result) => {
      console.log('is there any update?：' + result.hasUpdate);
    });
    updateManager.onUpdateReady((result) => {
      tt.showModal({
        title: 'Update infomation',
        content: 'new version is ready, do you want to restart app?',
        success: res => {
          console.log(JSON.stringify(res))
          if (res.confirm) {
            updateManager.applyUpdate();
          }
        }
      })
    });
    updateManager.onUpdateFailed((result) => {
      console.log('Gadget update failed');
    })
  },
  onHide: function () {
    console.log('App Hide')
  },
  globalData: {
    hasLogin: false,
    openid: null
  }
})
