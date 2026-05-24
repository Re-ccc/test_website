<template>
  <div class="min-h-screen bg-gray-50">
    <Header />

    <div class="flex">
      <Sidebar :active-tag="selectedTag" @update-tag="onTagChange" />

      <main class="flex-1 p-4">
        <div class="flex gap-4 mb-4">
          <button
            @click="activeTab = 'recommend'"
            :class="[
              'px-4 py-2 rounded-full font-medium transition-all',
              activeTab === 'recommend'
                ? 'bg-primary text-white'
                : 'bg-white text-gray-600 hover:bg-gray-100'
            ]"
          >
            推荐
          </button>
          <button
            @click="activeTab = 'ranking'"
            :class="[
              'px-4 py-2 rounded-full font-medium transition-all',
              activeTab === 'ranking'
                ? 'bg-primary text-white'
                : 'bg-white text-gray-600 hover:bg-gray-100'
            ]"
          >
            排行榜
          </button>
          <template v-if="activeTab === 'ranking'">
            <button
              v-for="s in sorts"
              :key="s.key"
              @click="currentSort = s.key"
              :class="[
                'px-3 py-2 rounded-full text-sm font-medium transition-all',
                currentSort === s.key
                  ? 'bg-secondary text-white'
                  : 'bg-white text-gray-500 hover:bg-gray-100'
              ]"
            >
              {{ s.label }}
            </button>
          </template>
        </div>

        <div v-if="videoStore.isLoading" class="flex justify-center items-center h-64">
          <div class="animate-spin rounded-full h-10 w-10 border-4 border-primary border-t-transparent"></div>
        </div>

        <div v-else-if="displayVideos.length === 0" class="text-center py-16">
          <p class="text-gray-400 text-lg">暂无视频，快去上传吧~</p>
        </div>

        <div v-else class="grid grid-cols-4 gap-4">
          <VideoCard
            v-for="video in displayVideos"
            :key="video.id"
            :video="video"
          />
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Header from '@/components/Header.vue'
import Sidebar from '@/components/Sidebar.vue'
import VideoCard from '@/components/VideoCard.vue'
import { useVideoStore } from '@/stores/video'

const route = useRoute()
const videoStore = useVideoStore()
const activeTab = ref('recommend')
const selectedTag = ref('全部')
const currentSort = ref('hot')

const sorts = [
  { key: 'hot', label: '综合' },
  { key: 'like', label: '点赞' },
  { key: 'collect', label: '收藏' },
]

const displayVideos = computed(() => {
  if (activeTab.value === 'recommend') {
    return videoStore.videos
  }
  return videoStore.rankingVideos
})

function onTagChange(tag: string) {
  selectedTag.value = tag
  activeTab.value = 'recommend'
  loadData()
}

function loadData() {
  const tag = selectedTag.value === '全部' ? undefined : selectedTag.value
  if (activeTab.value === 'recommend') {
    videoStore.loadHomeFeed(tag)
  } else {
    videoStore.loadRanking(currentSort.value)
  }
}

onMounted(() => {
  if (route.query.tab === 'ranking') {
    activeTab.value = 'ranking'
    videoStore.loadRanking(currentSort.value)
  } else if (route.query.tag) {
    selectedTag.value = route.query.tag as string
    videoStore.loadHomeFeed(selectedTag.value)
  } else {
    videoStore.loadHomeFeed()
  }
})

watch([activeTab, currentSort], () => {
  loadData()
})
</script>
