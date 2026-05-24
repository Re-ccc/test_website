<template>
  <router-link 
    :to="`/video/${video.bvid || video.id}`" 
    class="group bg-white rounded-lg shadow-sm overflow-hidden hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
  >
    <div class="relative aspect-video overflow-hidden">
      <img 
        :src="video.cover_url || 'data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 width=%22320%22 height=%22180%22><rect fill=%22%23333%22 width=%22320%22 height=%22180%22/><text fill=%22%23666%22 x=%22160%22 y=%2290%22 text-anchor=%22middle%22>无封面</text></svg>'"
        :alt="video.title"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300"
      />
      <div v-if="video.duration" class="absolute bottom-2 right-2 bg-black/70 text-white text-xs px-1.5 py-0.5 rounded">
        {{ formatDuration(video.duration) }}
      </div>
    </div>
    <div class="p-3">
      <h3 class="font-medium text-gray-800 line-clamp-2 mb-2 group-hover:text-primary transition-colors">
        {{ video.title }}
      </h3>
      <div class="flex items-center gap-2">
        <img 
          :src="video.uploader_avatar || 'https://api.dicebear.com/7.x/avataaars/svg?seed=' + (video.uploader_name || 'user')"
          class="w-6 h-6 rounded-full"
          alt="uploader"
        />
        <span class="text-sm text-gray-500 truncate">{{ video.uploader_name }}</span>
      </div>
      <div class="flex items-center gap-3 mt-1 text-xs text-gray-400">
        <span>{{ formatNumber(video.view_count) }}播放</span>
        <span>{{ formatNumber(video.danmaku_count) }}弹幕</span>
      </div>
    </div>
  </router-link>
</template>

<script setup lang="ts">
import type { Video } from '@/types'
import { formatNumber, formatDuration } from '@/utils'

defineProps<{
  video: Video
}>()
</script>
