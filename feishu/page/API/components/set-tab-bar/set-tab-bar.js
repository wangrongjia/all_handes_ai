import i18n from '../../../i18n/index'
const iTabBar = i18n.set_tab_bar

const defaultTabBarStyle = {
  borderStyle: 'black',
  color: '#7A7E83',
  selectedColor: '#3cc51f',
  backgroundColor: '#ffffff',
}

const defaultItemName = 'API'

Component({
  data: {
    hasSetTabBarBadge: false,
    hasShownTabBarRedDot: false,
    hasCustomedStyle: false,
    hasCustomedItem: false,
    hasHiddenTabBar: false,
    ...iTabBar
  },

  attached() {
    tt.pageScrollTo({
      scrollTop: 0,
      duration: 0
    })
  },

  detached() {
    this.removeTabBarBadge()
    this.hideTabBarRedDot()
    this.showTabBar()
    this.removeCustomStyle()
    this.removeCustomItem()
  },

  methods: {
    navigateBack() {
      this.triggerEvent('unmount')
    },

    setTabBarBadge() {
      if (this.data.hasSetTabBarBadge) {
        this.removeTabBarBadge()
        return
      }
      this.setData({
        hasSetTabBarBadge: true
      })
      tt.setTabBarBadge({
        index: 1,
        text: '1',
      })
    },

    removeTabBarBadge() {
      this.setData({
        hasSetTabBarBadge: false
      })
      tt.removeTabBarBadge({
        index: 1,
      })
    },

    showTabBarRedDot() {
      if (this.data.hasShownTabBarRedDot) {
        this.hideTabBarRedDot()
        return
      }
      this.setData({
        hasShownTabBarRedDot: true
      })
      tt.showTabBarRedDot({
        index: 1
      })
    },

    hideTabBarRedDot() {
      this.setData({
        hasShownTabBarRedDot: false
      })
      tt.hideTabBarRedDot({
        index: 1
      })
    },

    showTabBar() {
      this.setData({hasHiddenTabBar: false})
      tt.showTabBar()
    },

    hideTabBar() {
      if (this.data.hasHiddenTabBar) {
        this.showTabBar()
        return
      }
      this.setData({hasHiddenTabBar: true})
      tt.hideTabBar()
    },

    customStyle() {
      if (this.data.hasCustomedStyle) {
        this.removeCustomStyle()
        return
      }
      this.setData({hasCustomedStyle: true})
      tt.setTabBarStyle({
        color: '#FFF',
        selectedColor: '#1AAD19',
        backgroundColor: '#000000',
        borderStyle: 'white'
      })
    },

    removeCustomStyle() {
      this.setData({hasCustomedStyle: false})
      tt.setTabBarStyle(defaultTabBarStyle)
    },

    customStyleShowTitle() {
      tt.setTabBarItem({
        index: 1,
        text: 'API',
        iconPath: ' ',
        selectedIconPath: ' '
      })
    },

    customStyleShowIconAndSelectedIcon() {
      tt.setTabBarItem({
        index: 1,
        text: ' ',
        iconPath: '',
        selectedIconPath: ''
      })
    },

    customStyleShowIcon() {
      tt.setTabBarItem({
        index: 1,
        text: ' ',
        iconPath: 'image/icon_API.png',
        selectedIconPath: ''
      })
    },

    customStyleShowSelectedIcon() {
      tt.setTabBarItem({
        index: 1,
        text: '',
        iconPath: '',
        selectedIconPath: 'image/icon_component_HL.png'
      })
    },

    customItem() {
      if (this.data.hasCustomedItem) {
        this.removeCustomItem()
        return
      }
      this.setData({hasCustomedItem: true})
      tt.setTabBarItem({
        index: 1,
        text: 'API_Custom'
      })
    },

    removeCustomItem() {
      this.setData({hasCustomedItem: false})
      tt.setTabBarItem({
        index: 1,
        text: defaultItemName
      })
    }
  }
})
