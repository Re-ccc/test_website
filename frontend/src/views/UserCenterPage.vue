<template>
  <div class="min-h-screen bg-gray-50">
    <Header />

    <div class="flex">
      <Sidebar active-tag="" @update-tag="onTagChange" />

      <main class="flex-1 p-4">
        <div class="bg-white rounded-lg shadow-sm p-6 mb-4">
          <div class="flex items-center gap-6">
            <div v-if="isSelf" class="relative group">
              <img
                :src="profileUser?.avatar_url || 'https://api.dicebear.com/7.x/avataaars/svg?seed=user'"
                class="w-20 h-20 rounded-full object-cover"
                alt="avatar"
              />
              <label class="absolute inset-0 bg-black/50 rounded-full flex items-center justify-center opacity-0 group-hover:opacity-100 cursor-pointer transition-opacity">
                <input type="file" accept="image/*" class="hidden" @change="handleAvatarChange" />
                <span class="text-white text-xs">更换头像</span>
              </label>
            </div>
            <img
              v-else
              :src="profileUser?.avatar_url || 'https://api.dicebear.com/7.x/avataaars/svg?seed=user'"
              class="w-20 h-20 rounded-full object-cover"
              alt="avatar"
            />
            <div>
              <h1 class="text-xl font-bold">{{ profileUser?.nickname || profileUser?.username || '用户' }}</h1>
              <p class="text-gray-500">@{{ profileUser?.username }}</p>
              <div class="flex gap-6 mt-2">
                <span>粉丝 {{ formatNumber(profileUser?.follower_count || 0) }}</span>
                <span>关注 {{ formatNumber(profileUser?.following_count || 0) }}</span>
              </div>
            </div>
            <button
              v-if="isSelf"
              @click="handleLogout"
              class="ml-auto px-4 py-2 bg-red-500 text-white rounded-full font-medium hover:bg-red-600 transition-colors"
            >
              退出登录
            </button>
          </div>
          <p class="mt-4 text-gray-600">{{ profileUser?.signature || '这个人很懒，什么都没留下' }}</p>
        </div>

        <div v-if="isSelf" class="bg-white rounded-lg shadow-sm p-6">
          <div class="flex border-b mb-4">
            <button
              v-for="tab in tabs"
              :key="tab.key"
              @click="activeTab = tab.key"
              :class="[
                'px-4 py-2 border-b-2 font-medium transition-colors',
                activeTab === tab.key
                  ? 'border-primary text-primary'
                  : 'border-transparent text-gray-500 hover:text-gray-700'
              ]"
            >
              {{ tab.label }}
            </button>
          </div>

          <div v-if="loading" class="flex justify-center items-center h-32">
            <div class="animate-spin rounded-full h-8 w-8 border-4 border-primary border-t-transparent"></div>
          </div>

          <div v-else-if="tabData.length === 0" class="text-center py-12 text-gray-400">
            暂无{{ tabs.find((t: { key: string; label: string }) => t.key === activeTab)?.label }}
          </div>

          <div v-else-if="activeTab === 'follows'" class="grid grid-cols-4 gap-4">
            <div
              v-for="user in userStore.follows"
              :key="user.id"
              class="bg-gray-50 rounded-lg p-4 text-center hover:shadow-md transition-shadow cursor-pointer"
              @click="$router.push(`/user/${user.id}`)"
            >
              <img
                :src="user.avatar_url || 'https://api.dicebear.com/7.x/avataaars/svg?seed=user'"
                class="w-16 h-16 rounded-full mx-auto mb-2 object-cover"
                alt="avatar"
              />
              <p class="font-medium text-sm">{{ user.nickname || user.username }}</p>
              <p class="text-xs text-gray-400 mt-1">粉丝 {{ formatNumber(user.follower_count) }}</p>
            </div>
          </div>

          <div v-else class="grid grid-cols-4 gap-4">
            <VideoCard
              v-for="video in tabData"
              :key="video.id"
              :video="video"
            />
          </div>
        </div>

        <div v-else class="bg-white rounded-lg shadow-sm p-6">
          <h3 class="font-medium mb-4">TA 的视频</h3>
          <div v-if="otherVideos.length === 0" class="text-center py-12 text-gray-400">暂无视频</div>
          <div v-else class="grid grid-cols-4 gap-4">
            <VideoCard v-for="video in otherVideos" :key="video.id" :video="video" />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import type { User } from '@/types'
import Header from '@/components/Header.vue'
import Sidebar from '@/components/Sidebar.vue'
import VideoCard from '@/components/VideoCard.vue'
import { useUserStore } from '@/stores/user'
import { useVideoStore } from '@/stores/video'
import { formatNumber } from '@/utils'
import { userApi } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()
const videoStore = useVideoStore()

const profileUser = ref<User | null>(null)
const activeTab = ref('videos')
const loading = ref(false)
const otherVideos = ref<any[]>([])

const userId = computed(() => Number(route.params.id))
const isSelf = computed(() => !userId.value || userId.value === userStore.user?.id)

const tabs = [
  { key: 'videos', label: '我的投稿' },
  { key: 'likes', label: '我的点赞' },
  { key: 'collections', label: '我的收藏' },
  { key: 'follows', label: '我的关注' },
]

const tabData = computed(() => {
  switch (activeTab.value) {
    case 'videos':
      return videoStore.myVideos
    case 'likes':
      return videoStore.likedVideos
    case 'collections':
      return videoStore.collectedVideos
    case 'follows':
      return userStore.follows
    default:
      return []
  }
})

async function loadTabData() {
  loading.value = true
  try {
    switch (activeTab.value) {
      case 'videos':
        await videoStore.loadMyVideos()
        break
      case 'likes':
        await videoStore.loadMyLikes()
        break
      case 'collections':
        await videoStore.loadMyCollections()
        break
      case 'follows':
        await userStore.loadMyFollows()
        break
    }
  } finally {
    loading.value = false
  }
}

async function handleAvatarChange(event: Event) {
  const target = event.target as HTMLInputElement
  if (!target.files || target.files.length === 0) return
  try {
    await userApi.uploadAvatar(target.files[0])
    await userStore.loadProfile()
    ElMessage.success('头像更新成功')
  } catch {
    ElMessage.error('头像更新失败')
  }
}

function handleLogout() {
  userStore.logout()
  router.push('/')
}

function onTagChange(tag: string) {
  router.push({ name: 'Home', query: { tag } })
}

async function loadProfileData() {
  if (!userStore.isLoggedIn) {
    router.push('/login')
    return
  }
  if (isSelf.value || !userId.value) {
    await userStore.loadProfile()
    profileUser.value = userStore.user
    await loadTabData()
  } else {
    try {
      const [userData, userVideos] = await Promise.all([
        userApi.getUserById(userId.value),
        userApi.getUserVideos(userId.value),
      ])
      profileUser.value = userData
      otherVideos.value = userVideos
    } catch {
      ElMessage.error('用户不存在')
      router.push('/')
    }
  }
}

onMounted(() => {
  loadProfileData()
})

watch(activeTab, () => {
  loadTabData()
})

watch(() => route.params.id, () => {
  loadProfileData()
})
</script>
