<template>
  <div class="min-h-screen bg-gray-900 text-white">
    <Header />

    <div class="flex p-4 gap-4">
      <div class="flex-1">
        <div class="relative bg-black rounded-lg overflow-hidden" style="height: calc(100vh - 140px); min-height: 500px;">
          <video
            v-if="videoStore.currentVideo?.video_url"
            ref="videoRef"
            :src="videoStore.currentVideo.video_url"
            class="w-full h-full object-contain"
            @timeupdate="onTimeUpdate"
            @loadedmetadata="onLoaded"
            @play="isPlaying = true"
            @pause="isPlaying = false"
          ></video>
          <div v-else class="absolute inset-0 flex items-center justify-center">
            <div class="text-center">
              <el-icon class="text-white text-6xl mb-4"><VideoPlay /></el-icon>
              <p class="text-gray-400">视频加载中...</p>
            </div>
          </div>
          <VideoControls
            :videoEl="videoRef"
            :duration="videoStore.currentVideo?.duration || 0"
            :currentTime="currentTime"
            :isPlaying="isPlaying"
          />
        </div>

        <div v-if="videoStore.currentVideo" class="mt-4 bg-gray-800 rounded-lg p-4">
          <h1 class="text-xl font-bold mb-2">{{ videoStore.currentVideo.title }}</h1>
          <div v-if="videoStore.currentVideo.tags" class="flex gap-2 mb-3">
            <span
              v-for="tag in videoStore.currentVideo.tags.split(',')"
              :key="tag"
              class="px-2 py-0.5 bg-gray-700 text-gray-300 rounded text-xs"
            >
              {{ tag }}
            </span>
          </div>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-4">
              <img
                :src="videoStore.currentVideo.uploader_avatar || 'https://api.dicebear.com/7.x/avataaars/svg?seed=up'"
                class="w-10 h-10 rounded-full"
                alt="avatar"
              />
              <span class="font-medium">{{ videoStore.currentVideo.uploader_name }}</span>
              <button
                @click="handleFollow"
                :class="[
                  'ml-4 px-4 py-1 rounded-full text-sm font-medium transition-colors',
                  isFollowing ? 'bg-gray-600 hover:bg-gray-500' : 'bg-primary hover:bg-pink-500'
                ]"
              >
                {{ isFollowing ? '已关注' : '关注' }}
              </button>
            </div>
            <div class="flex items-center gap-6">
              <div class="flex items-center gap-1 cursor-pointer hover:text-primary transition-colors" @click="handleLike">
                <el-icon :class="liked ? 'text-primary' : ''"><component :is="liked ? 'ThumbsUp' : 'ThumbsUp'" /></el-icon>
                <span>{{ formatNumber(videoStore.currentVideo.like_count) }}</span>
              </div>
              <div class="flex items-center gap-1 cursor-pointer hover:text-yellow-400 transition-colors">
                <el-icon><Coins /></el-icon>
                <span>{{ formatNumber(videoStore.currentVideo.coin_count) }}</span>
              </div>
              <div class="flex items-center gap-1 cursor-pointer hover:text-blue-400 transition-colors" @click="handleCollect">
                <el-icon :class="collected ? 'text-blue-400' : ''"><component :is="collected ? 'Star' : 'Star'" /></el-icon>
                <span>{{ formatNumber(videoStore.currentVideo.collect_count) }}</span>
              </div>
              <div class="flex items-center gap-1 cursor-pointer hover:text-green-400 transition-colors" @click="handleShare">
                <el-icon><Share2 /></el-icon>
                <span>分享</span>
              </div>
            </div>
          </div>

          <div class="mt-4 flex items-center gap-4 text-sm text-gray-400">
            <span>{{ formatNumber(videoStore.currentVideo.view_count) }}次观看</span>
          </div>
        </div>

        <div class="mt-4 bg-gray-800 rounded-lg p-4">
          <h3 class="font-medium mb-2">评论 ({{ videoStore.comments.length }})</h3>
          <div class="flex gap-3 mb-4">
            <img
              :src="userStore.user?.avatar_url || 'https://api.dicebear.com/7.x/avataaars/svg?seed=user'"
              class="w-8 h-8 rounded-full"
            />
            <input
              v-model="commentInput"
              type="text"
              placeholder="发表评论..."
              class="flex-1 bg-gray-700 rounded-full px-4 py-2 outline-none focus:ring-2 focus:ring-primary"
              @keyup.enter="handlePostComment"
            />
            <button
              @click="handlePostComment"
              class="px-4 py-2 bg-primary rounded-full text-sm font-medium"
            >
              发送
            </button>
          </div>
          <CommentList :comments="videoStore.comments" @refresh="videoStore.loadComments(videoStore.currentVideo!.id)" />
        </div>
      </div>

      <div class="w-80">
        <h3 class="font-medium mb-3">推荐视频</h3>
        <RelatedVideoList :videos="videoStore.relatedVideos" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import VideoControls from '@/components/VideoControls.vue'
import CommentList from '@/components/CommentList.vue'
import RelatedVideoList from '@/components/RelatedVideoList.vue'
import { useVideoStore } from '@/stores/video'
import { useUserStore } from '@/stores/user'
import { videoApi, userApi } from '@/api'
import { formatNumber } from '@/utils'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const videoStore = useVideoStore()
const userStore = useUserStore()
const currentTime = ref(0)
const isPlaying = ref(false)
const liked = ref(false)
const collected = ref(false)
const isFollowing = ref(false)
const commentInput = ref('')
const videoRef = ref<HTMLVideoElement | null>(null)

onMounted(async () => {
  const bvid = route.params.bvid as string
  await videoStore.loadVideo(bvid)
  if (videoStore.currentVideo) {
    await Promise.all([
      videoStore.loadComments(videoStore.currentVideo.id),
      videoStore.loadRelatedVideos(videoStore.currentVideo.id),
    ])
    if (userStore.isLoggedIn) {
      try {
        const [likes, collections, follows] = await Promise.all([
          videoApi.getMyLikes(),
          videoApi.getMyCollections(),
          userApi.getMyFollows(),
        ])
        liked.value = likes.some((v: any) => v.id === videoStore.currentVideo!.id)
        collected.value = collections.some((v: any) => v.id === videoStore.currentVideo!.id)
        isFollowing.value = follows.some((u: any) => u.id === videoStore.currentVideo!.uploader_id)
      } catch { /* silently ignore */ }
    }
  }
})

function onTimeUpdate() {
  if (videoRef.value) {
    currentTime.value = videoRef.value.currentTime
  }
}

function onLoaded() {}

function needLogin(): boolean {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return true
  }
  return false
}

async function handleLike() {
  if (!videoStore.currentVideo) return
  if (needLogin()) return
  const result = await videoStore.likeVideo(videoStore.currentVideo.id)
  if (result) {
    liked.value = result.liked
  }
}

async function handleCollect() {
  if (!videoStore.currentVideo) return
  if (needLogin()) return
  const result = await videoStore.collectVideo(videoStore.currentVideo.id)
  if (result) {
    collected.value = result.collected
  }
}

async function handleFollow() {
  if (!videoStore.currentVideo) return
  if (needLogin()) return
  const result = await userStore.follow(videoStore.currentVideo.uploader_id!)
  if (result) {
    isFollowing.value = result.followed
    ElMessage.success(result.followed ? '已关注' : '已取消关注')
  } else {
    ElMessage.error('操作失败，请重试')
  }
}

async function handlePostComment() {
  if (!commentInput.value.trim() || !videoStore.currentVideo) return
  if (needLogin()) return
  await videoStore.postComment(videoStore.currentVideo.id, commentInput.value)
  commentInput.value = ''
}

function handleShare() {
  const url = window.location.href
  navigator.clipboard.writeText(url).then(() => {
    ElMessage.success('链接已复制到剪贴板')
  }).catch(() => {
    ElMessage.info('链接: ' + url)
  })
}
</script>
