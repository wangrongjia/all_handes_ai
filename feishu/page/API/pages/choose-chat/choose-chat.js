Page({
    data: {
        chats: [],
        allowCreateGroup: false,
        multiSelect: false,
        ignoreSelf: false,
        selectType: "0",
        confirmTitle: "",
        confirmDesc: ""
    },

    selectModeChange: function (e) {
        this.setData({
            multiSelect: e.detail.value === "true"
        })
    },
    selectTypeChange: function (e) {
        this.setData({
            selectType: e.detail.value
        })
    },
    otherValueChange: function (e) {
        this.setData({
            ignoreSelf: e.detail.value.includes("0"),
            allowCreateGroup: e.detail.value.includes("1")
        })
    },

    titleInput: function (e) {
        this.setData({
            confirmTitle: e.detail.value
        })
    },

    descInput: function (e) {
        this.setData({
            confirmDesc: e.detail.value
        })
    },

    chooseChat: function (e) {
        let that = this;
        tt.login({
            success: res => {
                console.log(JSON.stringify(res))
                if (res.code) {
                    tt.chooseChat({
                        allowCreateGroup: that.data.allowCreateGroup,
                        multiSelect: that.data.multiSelect,
                        ignoreSelf: that.data.ignoreSelf,
                        selectType: that.data.selectType,
                        confirmTitle: that.data.confirmTitle,
                        confirmDesc: that.data.confirmDesc,
                        success: res => {
                            console.log(JSON.stringify(res))
                            that.setData({
                                chats: res.data
                            });
                        },
                        fail(res) {
                            console.log(`choose chat failed` + res);
                        }
                    })
                } else {
                    tt.showModal({
                        title: 'local api call success, but login failed'
                    });
                }
            },
            fail: function () {
                tt.showModal({
                    title: 'login  failed'
                });
            }
        })
    }
});
