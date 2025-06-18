class BilibiliMusicPlayer {
    constructor() {
        this.playlistData = [];
        this.currentIndex = -1;
        this.isPlaying = false;
        this.searchResultsData = [];
        
        this.initializeElements();
        this.bindEvents();
        this.loadPlaylistFromStorage();
    }

    initializeElements() {
        this.searchInput = document.getElementById('searchInput');
        this.searchBtn = document.getElementById('searchBtn');
        this.searchResults = document.getElementById('searchResults');
        this.playlist = document.getElementById('playlist');
        this.playlistCount = document.getElementById('playlistCount');
        this.clearPlaylistBtn = document.getElementById('clearPlaylist');
        this.shufflePlaylistBtn = document.getElementById('shufflePlaylist');
        this.audioPlayer = document.getElementById('audioPlayer');
        this.playPauseBtn = document.getElementById('playPauseBtn');
        this.prevBtn = document.getElementById('prevBtn');
        this.nextBtn = document.getElementById('nextBtn');
        this.progressSlider = document.getElementById('progressSlider');
        this.currentTime = document.getElementById('currentTime');
        this.totalTime = document.getElementById('totalTime');
        this.currentTitle = document.getElementById('currentTitle');
        this.currentAuthor = document.getElementById('currentAuthor');
        this.loading = document.getElementById('loading');
    }

    bindEvents() {
        this.searchBtn.addEventListener('click', () => this.searchVideos());
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.searchVideos();
        });

        this.clearPlaylistBtn.addEventListener('click', () => this.clearPlaylist());
        this.shufflePlaylistBtn.addEventListener('click', () => this.shufflePlaylist());

        this.playPauseBtn.addEventListener('click', () => this.togglePlayPause());
        this.prevBtn.addEventListener('click', () => this.playPrevious());
        this.nextBtn.addEventListener('click', () => this.playNext());

        this.audioPlayer.addEventListener('loadedmetadata', () => this.updateTotalTime());
        this.audioPlayer.addEventListener('timeupdate', () => this.updateProgress());
        this.audioPlayer.addEventListener('ended', () => this.playNext());

        this.progressSlider.addEventListener('input', () => this.seekTo());

        // 使用事件委托处理动态添加的按钮
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('add-btn')) {
                const bvid = e.target.dataset.bvid;
                this.addToPlaylist(bvid);
            } else if (e.target.classList.contains('play-btn')) {
                const bvid = e.target.dataset.bvid;
                this.playFromPlaylist(bvid);
            } else if (e.target.classList.contains('remove-btn')) {
                const bvid = e.target.dataset.bvid;
                this.removeFromPlaylist(bvid);
            }
        });
    }

    async searchVideos() {
        const query = this.searchInput.value.trim();
        if (!query) return;

        this.showLoading(true);
        
        try {
            // 模拟搜索结果，实际应用中需要调用哔哩哔哩API
            const mockResults = this.generateMockSearchResults(query);
            this.displaySearchResults(mockResults);
        } catch (error) {
            console.error('搜索失败:', error);
            this.showError('搜索失败，请稍后重试');
        } finally {
            this.showLoading(false);
        }
    }

    generateMockSearchResults(query) {
        // 模拟搜索结果数据
        const mockData = [
            {
                bvid: 'BV1xx411c7mD',
                title: `${query} - 热门音乐合集`,
                author: '音乐UP主',
                pic: 'https://via.placeholder.com/160x120/ff6b6b/ffffff?text=Music',
                play: 125000,
                video_review: 1200,
                duration: '3:45'
            },
            {
                bvid: 'BV1yy411c7mE',
                title: `${query} 经典老歌回忆`,
                author: '怀旧音乐馆',
                pic: 'https://via.placeholder.com/160x120/4ecdc4/ffffff?text=Classic',
                play: 89000,
                video_review: 890,
                duration: '4:12'
            },
            {
                bvid: 'BV1zz411c7mF',
                title: `${query} 现场版演唱会`,
                author: '演唱会精选',
                pic: 'https://via.placeholder.com/160x120/45b7aa/ffffff?text=Live',
                play: 156000,
                video_review: 2100,
                duration: '5:30'
            },
            {
                bvid: 'BV1aa411c7mG',
                title: `${query} 翻唱合集`,
                author: '翻唱达人',
                pic: 'https://via.placeholder.com/160x120/667eea/ffffff?text=Cover',
                play: 67000,
                video_review: 650,
                duration: '3:20'
            },
            {
                bvid: 'BV1bb411c7mH',
                title: `${query} 纯音乐版本`,
                author: '纯音乐频道',
                pic: 'https://via.placeholder.com/160x120/764ba2/ffffff?text=Pure',
                play: 45000,
                video_review: 420,
                duration: '4:05'
            }
        ];

        return mockData;
    }

    displaySearchResults(results) {
        this.searchResultsData = results; // 保存搜索结果数据
        this.searchResults.innerHTML = '';
        
        if (results.length === 0) {
            this.searchResults.innerHTML = '<div class="no-results">未找到相关视频</div>';
            return;
        }

        results.forEach(video => {
            const videoElement = this.createVideoElement(video, 'search');
            this.searchResults.appendChild(videoElement);
        });
    }

    createVideoElement(video, type) {
        const videoDiv = document.createElement('div');
        videoDiv.className = 'video-item';
        videoDiv.innerHTML = `
            <img src="${video.pic}" alt="${video.title}" class="video-thumbnail" onerror="this.src='https://via.placeholder.com/160x120/cccccc/666666?text=No+Image'">
            <div class="video-info">
                <div class="video-title">${video.title}</div>
                <div class="video-author">UP主: ${video.author}</div>
                <div class="video-stats">播放: ${this.formatNumber(video.play)} • 弹幕: ${this.formatNumber(video.video_review)} • 时长: ${video.duration}</div>
            </div>
            <div class="video-actions">
                ${type === 'search' ? 
                    `<button class="add-btn" data-bvid="${video.bvid}">添加到列表</button>` :
                    `<button class="play-btn" data-bvid="${video.bvid}">播放</button>
                     <button class="remove-btn" data-bvid="${video.bvid}">移除</button>`
                }
            </div>
        `;
        
        // 存储视频数据到元素上，方便后续使用
        videoDiv.dataset.videoData = JSON.stringify(video);
        
        return videoDiv;
    }

    addToPlaylist(bvid) {
        // 从搜索结果中找到对应的视频
        const video = this.findVideoInSearchResults(bvid);
        if (!video) return;

        // 检查是否已经在播放列表中
        if (this.playlistData.find(item => item.bvid === bvid)) {
            this.showMessage('该视频已在播放列表中');
            return;
        }

        // 添加音频URL（模拟）
        video.audioUrl = this.generateMockAudioUrl(bvid);
        
        this.playlistData.push(video);
        this.updatePlaylistDisplay();
        this.savePlaylistToStorage();
        this.showMessage('已添加到播放列表');
    }

    findVideoInSearchResults(bvid) {
        return this.searchResultsData.find(video => video.bvid === bvid);
    }

    generateMockAudioUrl(bvid) {
        // 模拟音频URL，实际应用中需要通过API获取真实的音频流地址
        return `https://mock-audio-server.com/audio/${bvid}.mp3`;
    }

    removeFromPlaylist(bvid) {
        const index = this.playlistData.findIndex(item => item.bvid === bvid);
        if (index === -1) return;

        // 如果删除的是当前播放的歌曲
        if (index === this.currentIndex) {
            this.audioPlayer.pause();
            this.currentIndex = -1;
            this.updateCurrentSongInfo();
        } else if (index < this.currentIndex) {
            this.currentIndex--;
        }

        this.playlistData.splice(index, 1);
        this.updatePlaylistDisplay();
        this.savePlaylistToStorage();
        this.showMessage('已从播放列表移除');
    }

    playFromPlaylist(bvid) {
        const index = this.playlistData.findIndex(item => item.bvid === bvid);
        if (index === -1) return;

        this.currentIndex = index;
        this.playCurrentSong();
    }

    playCurrentSong() {
        if (this.currentIndex < 0 || this.currentIndex >= this.playlistData.length) return;

        const currentSong = this.playlistData[this.currentIndex];
        
        // 由于无法获取真实的音频流，这里使用示例音频
        // 实际应用中需要调用哔哩哔哩API获取音频流地址
        this.audioPlayer.src = this.getMockAudioUrl();
        this.audioPlayer.load();
        
        this.updateCurrentSongInfo();
        
        this.audioPlayer.play().catch(error => {
            console.error('播放失败:', error);
            this.showError('播放失败，可能是网络问题或音频格式不支持');
        });
    }

    getMockAudioUrl() {
        // 使用一个公开的示例音频文件
        return 'https://www.soundjay.com/misc/sounds/bell-ringing-05.wav';
    }

    updateCurrentSongInfo() {
        if (this.currentIndex >= 0 && this.currentIndex < this.playlistData.length) {
            const currentSong = this.playlistData[this.currentIndex];
            this.currentTitle.textContent = currentSong.title;
            this.currentAuthor.textContent = currentSong.author;
        } else {
            this.currentTitle.textContent = '未选择音乐';
            this.currentAuthor.textContent = '-';
        }
    }

    togglePlayPause() {
        if (this.currentIndex < 0) {
            if (this.playlistData.length > 0) {
                this.currentIndex = 0;
                this.playCurrentSong();
            }
            return;
        }

        if (this.audioPlayer.paused) {
            this.audioPlayer.play();
            this.playPauseBtn.textContent = '⏸️';
            this.isPlaying = true;
        } else {
            this.audioPlayer.pause();
            this.playPauseBtn.textContent = '▶️';
            this.isPlaying = false;
        }
    }

    playPrevious() {
        if (this.playlistData.length === 0) return;
        
        this.currentIndex = this.currentIndex <= 0 ? this.playlistData.length - 1 : this.currentIndex - 1;
        this.playCurrentSong();
    }

    playNext() {
        if (this.playlistData.length === 0) return;
        
        this.currentIndex = this.currentIndex >= this.playlistData.length - 1 ? 0 : this.currentIndex + 1;
        this.playCurrentSong();
    }

    updateProgress() {
        if (this.audioPlayer.duration) {
            const progress = (this.audioPlayer.currentTime / this.audioPlayer.duration) * 100;
            this.progressSlider.value = progress;
            this.currentTime.textContent = this.formatTime(this.audioPlayer.currentTime);
        }
    }

    updateTotalTime() {
        this.totalTime.textContent = this.formatTime(this.audioPlayer.duration);
    }

    seekTo() {
        if (this.audioPlayer.duration) {
            const seekTime = (this.progressSlider.value / 100) * this.audioPlayer.duration;
            this.audioPlayer.currentTime = seekTime;
        }
    }

    clearPlaylist() {
        this.playlistData = [];
        this.currentIndex = -1;
        this.audioPlayer.pause();
        this.audioPlayer.src = '';
        this.updatePlaylistDisplay();
        this.updateCurrentSongInfo();
        this.savePlaylistToStorage();
        this.playPauseBtn.textContent = '▶️';
        this.isPlaying = false;
        console.log('播放列表已清空');
    }

    shufflePlaylist() {
        if (this.playlistData.length < 2) return;
        
        const currentSong = this.currentIndex >= 0 ? this.playlistData[this.currentIndex] : null;
        
        // Fisher-Yates shuffle
        for (let i = this.playlistData.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [this.playlistData[i], this.playlistData[j]] = [this.playlistData[j], this.playlistData[i]];
        }
        
        // 更新当前播放索引
        if (currentSong) {
            this.currentIndex = this.playlistData.findIndex(song => song.bvid === currentSong.bvid);
        }
        
        this.updatePlaylistDisplay();
        this.savePlaylistToStorage();
        this.showMessage('播放列表已随机排序');
    }

    updatePlaylistDisplay() {
        this.playlistCount.textContent = this.playlistData.length;
        
        if (this.playlistData.length === 0) {
            this.playlist.innerHTML = '<div class="no-results">播放列表为空</div>';
            return;
        }

        this.playlist.innerHTML = '';
        this.playlistData.forEach((video, index) => {
            const videoElement = this.createVideoElement(video, 'playlist');
            if (index === this.currentIndex) {
                videoElement.style.background = '#e3f2fd';
                videoElement.style.border = '2px solid #2196f3';
            }
            this.playlist.appendChild(videoElement);
        });
    }

    savePlaylistToStorage() {
        localStorage.setItem('bilibiliMusicPlaylist', JSON.stringify(this.playlistData));
        localStorage.setItem('currentIndex', this.currentIndex.toString());
    }

    loadPlaylistFromStorage() {
        const savedPlaylist = localStorage.getItem('bilibiliMusicPlaylist');
        const savedIndex = localStorage.getItem('currentIndex');
        
        if (savedPlaylist) {
            this.playlistData = JSON.parse(savedPlaylist);
            this.updatePlaylistDisplay();
        }
        
        if (savedIndex) {
            this.currentIndex = parseInt(savedIndex);
            this.updateCurrentSongInfo();
        }
    }

    showLoading(show) {
        this.loading.style.display = show ? 'flex' : 'none';
    }

    showMessage(message) {
        // 简单的消息提示
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #4caf50;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 1001;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        `;
        messageDiv.textContent = message;
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 3000);
    }

    showError(message) {
        const messageDiv = document.createElement('div');
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #f44336;
            color: white;
            padding: 12px 20px;
            border-radius: 8px;
            z-index: 1001;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        `;
        messageDiv.textContent = message;
        document.body.appendChild(messageDiv);
        
        setTimeout(() => {
            document.body.removeChild(messageDiv);
        }, 5000);
    }

    formatNumber(num) {
        if (typeof num === 'string') return num;
        if (num >= 10000) {
            return (num / 10000).toFixed(1) + '万';
        }
        return num.toString();
    }

    formatTime(seconds) {
        if (!seconds || isNaN(seconds)) return '0:00';
        
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
}

// 初始化播放器
const player = new BilibiliMusicPlayer();

// 添加一些示例数据到播放列表（用于演示）
document.addEventListener('DOMContentLoaded', () => {
    // 如果播放列表为空，添加一些示例音乐
    if (player.playlistData.length === 0) {
        const exampleSongs = [
            {
                bvid: 'BV1example1',
                title: '示例音乐 1 - 轻音乐',
                author: '示例UP主',
                pic: 'https://via.placeholder.com/160x120/ff6b6b/ffffff?text=Demo1',
                play: '50000',
                video_review: '500',
                duration: '3:30',
                audioUrl: 'https://www.soundjay.com/misc/sounds/bell-ringing-05.wav'
            },
            {
                bvid: 'BV1example2',
                title: '示例音乐 2 - 流行歌曲',
                author: '音乐达人',
                pic: 'https://via.placeholder.com/160x120/4ecdc4/ffffff?text=Demo2',
                play: '75000',
                video_review: '750',
                duration: '4:15',
                audioUrl: 'https://www.soundjay.com/misc/sounds/bell-ringing-05.wav'
            }
        ];
        
        // 注释掉自动添加示例，让用户自己搜索添加
        // player.playlistData = exampleSongs;
        // player.updatePlaylistDisplay();
    }
});