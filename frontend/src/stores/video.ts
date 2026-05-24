import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Video, Danmaku, Comment } from '@/types'
import { videoApi, danmakuApi, commentApi } from '@/api'

export const useVideoStore = defineStore('video', () => {
  const videos = ref<Video[]>([])
  const rankingVideos = ref<Video[]>([])
  const currentVideo = ref<Video | null>(null)
  const danmakus = ref<Danmaku[]>([])
  const comments = ref<Comment[]>([])
  const relatedVideos = ref<Video[]>([])
  const isLoading = ref(false)
  const searchResults = ref<Video[]>([])
  const isSearching = ref(false)

  const likedVideos = ref<Video[]>([])
  const collectedVideos = ref<Video[]>([])
  const myVideos = ref<Video[]>([])

  async function loadHomeFeed(tag?: string) {
    isLoading.value = true
    try {
      const data = await videoApi.getHomeFeed(tag)
      videos.value = data
    } catch {
      videos.value = []
    } finally {
      isLoading.value = false
    }
  }

  async function loadRanking(sort?: string) {
    isLoading.value = true
    try {
      const data = await videoApi.getRanking(sort)
      rankingVideos.value = data
    } catch {
      rankingVideos.value = []
    } finally {
      isLoading.value = false
    }
  }

  async function search(q: string) {
    if (!q.trim()) return
    isSearching.value = true
    try {
      searchResults.value = await videoApi.searchVideos(q)
    } catch {
      searchResults.value = []
    } finally {
      isSearching.value = false
    }
  }

  async function loadVideo(bvid: string) {
    isLoading.value = true
    try {
      const data = await videoApi.getVideo(bvid)
      currentVideo.value = data
    } catch {
      currentVideo.value = null
    } finally {
      isLoading.value = false
    }
  }

  async function loadDanmakus(videoId: number) {
    try {
      const data = await danmakuApi.getDanmakus(videoId)
      danmakus.value = data
    } catch {
      danmakus.value = []
    }
  }

  async function loadComments(videoId: number) {
    try {
      const data = await commentApi.getComments(videoId)
      comments.value = data
    } catch {
      comments.value = []
    }
  }

  async function loadRelatedVideos(videoId: number) {
    try {
      const data = await videoApi.getRelated(videoId)
      relatedVideos.value = data
    } catch {
      relatedVideos.value = []
    }
  }

  async function likeVideo(videoId: number) {
    try {
      const data = await videoApi.likeVideo(videoId)
      if (currentVideo.value && currentVideo.value.id === videoId) {
        currentVideo.value.like_count = data.like_count
      }
      return data
    } catch {
      return null
    }
  }

  async function collectVideo(videoId: number) {
    try {
      const data = await videoApi.collectVideo(videoId)
      if (currentVideo.value && currentVideo.value.id === videoId) {
        currentVideo.value.collect_count = data.collect_count
      }
      return data
    } catch {
      return null
    }
  }

  async function sendDanmaku(videoId: number, content: string, time: number) {
    try {
      const data = await danmakuApi.sendDanmaku({ video_id: videoId, content, time })
      if (data) danmakus.value.push(data)
      return data
    } catch {
      return null
    }
  }

  async function postComment(videoId: number, content: string) {
    try {
      const data = await commentApi.createComment({ video_id: videoId, content })
      if (data) comments.value.unshift(data)
      return data
    } catch {
      return null
    }
  }

  async function loadMyLikes() {
    try {
      likedVideos.value = await videoApi.getMyLikes()
    } catch {
      likedVideos.value = []
    }
  }

  async function loadMyCollections() {
    try {
      collectedVideos.value = await videoApi.getMyCollections()
    } catch {
      collectedVideos.value = []
    }
  }

  async function loadMyVideos() {
    try {
      myVideos.value = await videoApi.getMyVideos()
    } catch {
      myVideos.value = []
    }
  }

  return {
    videos,
    rankingVideos,
    currentVideo,
    danmakus,
    comments,
    relatedVideos,
    isLoading,
    searchResults,
    isSearching,
    likedVideos,
    collectedVideos,
    myVideos,
    loadHomeFeed,
    loadRanking,
    search,
    loadVideo,
    loadDanmakus,
    loadComments,
    loadRelatedVideos,
    likeVideo,
    collectVideo,
    sendDanmaku,
    postComment,
    loadMyLikes,
    loadMyCollections,
    loadMyVideos,
  }
})
