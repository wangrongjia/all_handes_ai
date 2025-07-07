import i18n from '../../../i18n/index'
const iScanSubmit = i18n.scan_submit || {
  title: 'QR Code Scanner & Submitter',
  scan_button: 'Scan QR Code',
  submit_button: 'Submit to OA',
  scan_result: 'Scan Result',
  submit_result: 'Submit Result',
  scan_success: 'Scan successful',
  scan_fail: 'Scan failed',
  submit_success: 'Submit successful',
  submit_fail: 'Submit failed',
  no_data: 'No data to submit'
}

Page({
  data: {
    scanResult: '',
    submitResult: '',
    hasScannedData: false,
    isSubmitting: false,
    ...iScanSubmit
  },
  
  // Scan QR code function
  scanCode: function () {
    const that = this
    tt.scanCode({
      scanType: ['qrCode'],
      success: function (res) {
        console.log('Scan success:', res)
        // Store the scan result
        that.setData({
          scanResult: res.result,
          hasScannedData: true
        })
        
        // Save to Feishu Bitable
        that.saveToTable(res.result)
      },
      fail: function (res) {
        console.log('Scan failed:', res)
        tt.showToast({
          title: that.data.scan_fail,
          icon: 'none',
          duration: 2000
        })
      }
    })
  },
  
  // Save scan result to Feishu Bitable
  saveToTable: function (qrData) {
    const that = this
    
    // Use Feishu Open API to save data to a multi-dimensional table
    // This requires proper authentication and permissions
    tt.getAuthCode({
      success(res) {
        // Get user's auth code
        const authCode = res.code
        
        // Call Feishu Open API to save data
        const app = getApp()
        tt.request({
          url: `https://open.feishu.cn/open-apis/bitable/v1/apps/${app.globalData.bitable.appToken}/tables/${app.globalData.bitable.tableId}/records`,
          method: 'POST',
          header: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + authCode // You might need to exchange this for an access token
          },
          data: {
            fields: {
              'QR Code Data': qrData,
              'Scan Time': new Date().toISOString(),
              'Status': 'Unsubmitted'
            }
          },
          success: function(res) {
            console.log('Saved to Bitable:', res)
            tt.showToast({
              title: that.data.scan_success,
              icon: 'success',
              duration: 2000
            })
          },
          fail: function(err) {
            console.error('Failed to save to Bitable:', err)
            tt.showToast({
              title: 'Failed to save data',
              icon: 'none',
              duration: 2000
            })
          }
        })
      },
      fail(err) {
        console.error('Failed to get auth code:', err)
      }
    })
  },
  
  // Submit unsubmitted data to OA system
  submitToOA: function () {
    const that = this
    
    if (!that.data.hasScannedData) {
      tt.showToast({
        title: that.data.no_data,
        icon: 'none',
        duration: 2000
      })
      return
    }
    
    that.setData({
      isSubmitting: true
    })
    
    // First, get unsubmitted records from Bitable
    tt.getAuthCode({
      success(res) {
        const authCode = res.code
        
        // Get unsubmitted records
        const app = getApp()
        tt.request({
          url: `https://open.feishu.cn/open-apis/bitable/v1/apps/${app.globalData.bitable.appToken}/tables/${app.globalData.bitable.tableId}/records`,
          method: 'GET',
          header: {
            'Authorization': 'Bearer ' + authCode
          },
          data: {
            filter: 'CurrentValue.[Status] = "Unsubmitted"'
          },
          success: function(res) {
            const records = res.data.items || []
            
            if (records.length === 0) {
              that.setData({
                isSubmitting: false,
                submitResult: that.data.no_data
              })
              tt.showToast({
                title: that.data.no_data,
                icon: 'none',
                duration: 2000
              })
              return
            }
            
            // Submit records to OA system
            tt.request({
              url: app.globalData.oaApi,
              method: 'POST',
              header: {
                'Content-Type': 'application/json'
              },
              data: {
                records: records
              },
              success: function(oaRes) {
                console.log('Submitted to OA:', oaRes)
                
                // Update records in Bitable to mark as submitted
                const updatePromises = records.map(record => {
                  return new Promise((resolve, reject) => {
                    tt.request({
                      url: `https://open.feishu.cn/open-apis/bitable/v1/apps/${app.globalData.bitable.appToken}/tables/${app.globalData.bitable.tableId}/records/${record.record_id}`,
                      method: 'PUT',
                      header: {
                        'Content-Type': 'application/json',
                        'Authorization': 'Bearer ' + authCode
                      },
                      data: {
                        fields: {
                          'Status': 'Submitted',
                          'Submit Time': new Date().toISOString()
                        }
                      },
                      success: resolve,
                      fail: reject
                    })
                  })
                })
                
                Promise.all(updatePromises)
                  .then(() => {
                    that.setData({
                      isSubmitting: false,
                      submitResult: that.data.submit_success
                    })
                    tt.showToast({
                      title: that.data.submit_success,
                      icon: 'success',
                      duration: 2000
                    })
                  })
                  .catch(err => {
                    console.error('Failed to update records:', err)
                    that.setData({
                      isSubmitting: false,
                      submitResult: 'Submitted to OA but failed to update status'
                    })
                  })
              },
              fail: function(err) {
                console.error('Failed to submit to OA:', err)
                that.setData({
                  isSubmitting: false,
                  submitResult: that.data.submit_fail
                })
                tt.showToast({
                  title: that.data.submit_fail,
                  icon: 'none',
                  duration: 2000
                })
              }
            })
          },
          fail: function(err) {
            console.error('Failed to get records:', err)
            that.setData({
              isSubmitting: false,
              submitResult: 'Failed to get records'
            })
            tt.showToast({
              title: 'Failed to get records',
              icon: 'none',
              duration: 2000
            })
          }
        })
      },
      fail(err) {
        console.error('Failed to get auth code:', err)
        that.setData({
          isSubmitting: false
        })
      }
    })
  }
})