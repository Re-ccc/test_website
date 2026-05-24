<template>
  <aside class="w-56 bg-white shadow-sm min-h-screen p-4">
    <h3 class="text-sm font-medium text-gray-400 px-3 py-2">视频分类</h3>
    <div class="space-y-1">
      <button
        v-for="tag in tags"
        :key="tag"
        @click="$emit('updateTag', tag)"
        :class="[
          'w-full text-left px-3 py-2 rounded-lg text-sm font-medium transition-all',
          activeTag === tag
            ? 'bg-primary text-white'
            : 'text-gray-600 hover:bg-gray-100'
        ]"
      >
        {{ tag }}
      </button>
    </div>

    <div v-if="userStore.isLoggedIn" class="mt-6 pt-6 border-t border-gray-100">
      <h3 class="text-sm font-medium text-gray-400 px-3 py-2">我的</h3>
      <router-link
        :to="`/user/${userStore.user?.id || 0}`"
        class="block px-3 py-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors"
      >
        个人中心
      </router-link>
    </div>
  </aside>
</template>

<script setup lang="ts">
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()

defineProps<{
  activeTag: string
}>()

defineEmits<{
  updateTag: [tag: string]
}>()

const tags = ['全部', '游戏', '舞蹈', '生活', '学习', '科技', '音乐', '美食', '影视', '娱乐', '动画']
</script>
