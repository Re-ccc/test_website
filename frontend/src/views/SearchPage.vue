<template>
  <div class="min-h-screen bg-gray-50">
    <Header :searchQuery="searchQuery" />

    <div class="flex">
      <Sidebar active-tag="" @update-tag="() => {}" />

      <main class="flex-1 p-4">
        <div class="bg-white rounded-lg shadow-sm p-4 mb-4">
          <div class="flex gap-4">
            <input
              v-model="searchQuery"
              type="text"
              placeholder="搜索视频、用户..."
              class="flex-1 px-4 py-2 border border-gray-300 rounded-full outline-none focus:ring-2 focus:ring-primary"
              @keyup.enter="handleSearch"
            />
            <button
              @click="handleSearch"
              class="px-6 py-2 bg-primary text-white rounded-full font-medium hover:bg-opacity-90 transition-opacity"
            >
              搜索
            </button>
          </div>
        </div>

        <div v-if="videoStore.isSearching" class="flex justify-center items-center h-64">
          <div class="animate-spin rounded-full h-10 w-10 border-4 border-primary border-t-transparent"></div>
        </div>

        <div v-else-if="videoStore.searchResults.length > 0" class="grid grid-cols-4 gap-4">
          <VideoCard
            v-for="video in videoStore.searchResults"
            :key="video.id"
            :video="video"
          />
        </div>

        <div v-else-if="searched" class="text-center py-16">
          <p class="text-gray-500 text-lg">没有找到相关结果</p>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import Header from '@/components/Header.vue'
import Sidebar from '@/components/Sidebar.vue'
import VideoCard from '@/components/VideoCard.vue'
import { useVideoStore } from '@/stores/video'

const route = useRoute()
const videoStore = useVideoStore()
const searchQuery = ref((route.query.q as string) || '')
const searched = ref(false)

async function handleSearch() {
  if (!searchQuery.value.trim()) return
  searched.value = true
  await videoStore.search(searchQuery.value)
}

onMounted(() => {
  if (searchQuery.value) {
    handleSearch()
  }
})
</script>
