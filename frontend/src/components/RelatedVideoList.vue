<template>
  <div class="space-y-3">
    <router-link 
      v-for="video in videos" 
      :key="video.id" 
      :to="`/video/${video.bvid || video.id}`"
      class="flex gap-3 p-2 rounded-lg hover:bg-white/10 transition-colors"
    >
      <div class="relative w-32 h-20 flex-shrink-0">
        <img
          :src="video.cover_url || 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22320%22 height=%22180%22><rect fill=%22%23333%22 width=%22320%22 height=%22180%22/><text fill=%22%23666%22 x=%22160%22 y=%2290%22 text-anchor=%22middle%22>无封面</text></svg>'"
          class="w-full h-full object-cover rounded"
          alt="cover"
        />
        <div v-if="video.duration" class="absolute bottom-1 right-1 bg-black/70 text-white text-xs px-1 rounded">
          {{ formatDuration(video.duration) }}
        </div>
      </div>
      <div class="flex-1 min-w-0">
        <h4 class="font-medium text-white line-clamp-2 text-sm mb-1">{{ video.title }}</h4>
        <p class="text-gray-400 text-xs mb-1 truncate">{{ video.uploader_name }}</p>
        <p class="text-gray-500 text-xs">{{ formatNumber(video.view_count) }}播放</p>
      </div>
    </router-link>
  </div>
</template>

<script setup lang="ts">
import type { Video } from '@/types'
import { formatNumber, formatDuration } from '@/utils'

defineProps<{
  videos: Video[]
}>()
</script>
