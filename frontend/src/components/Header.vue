<template>
  <header class="bg-white shadow-sm sticky top-0 z-50">
    <div class="flex items-center justify-between px-6 py-3">
      <div class="flex items-center gap-6">
        <router-link to="/" class="flex items-center gap-2">
          <div class="w-8 h-8 bg-gradient-to-r from-primary to-secondary rounded-lg flex items-center justify-center">
            <el-icon class="text-white"><VideoPlay /></el-icon>
          </div>
          <span class="text-xl font-bold text-gray-800">哔哩哔哩</span>
        </router-link>

        <nav class="hidden md:flex items-center gap-4">
          <router-link 
            to="/" 
            class="font-medium text-gray-600 hover:text-primary transition-colors"
          >
            首页
          </router-link>
          <a
            href="/?tab=ranking"
            class="font-medium text-gray-600 hover:text-primary transition-colors"
            @click.prevent="$router.push('/?tab=ranking')"
          >
            热门
          </a>
          <router-link 
            to="/upload" 
            class="font-medium text-gray-600 hover:text-primary transition-colors"
          >
            投稿
          </router-link>
        </nav>
      </div>

      <div class="flex-1 max-w-md mx-8">
        <div class="relative">
          <input
            v-model="searchText"
            type="text"
            placeholder="搜索视频"
            class="w-full px-4 py-2 pl-10 bg-gray-100 rounded-full outline-none focus:ring-2 focus:ring-primary focus:bg-white transition-all"
            @keyup.enter="handleSearch"
          />
          <el-icon class="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400"><Search /></el-icon>
        </div>
      </div>

      <div class="flex items-center gap-4">
        <button class="p-2 hover:bg-gray-100 rounded-full transition-colors">
          <el-icon class="text-gray-600"><Bell /></el-icon>
        </button>
        <button class="p-2 hover:bg-gray-100 rounded-full transition-colors">
          <el-icon class="text-gray-600"><Message /></el-icon>
        </button>
        
        <div v-if="userStore.isLoggedIn" class="relative">
          <router-link :to="`/user/${userStore.user?.id}`" class="flex items-center gap-2 hover:bg-gray-100 rounded-full px-2 py-1 transition-colors">
            <img
              :src="userStore.user?.avatar_url || 'https://api.dicebear.com/7.x/avataaars/svg?seed=user'"
              class="w-8 h-8 rounded-full"
              alt="avatar"
            />
            <span class="hidden sm:inline text-sm font-medium">{{ userStore.user?.nickname }}</span>
            <el-icon class="text-gray-400"><ChevronDown /></el-icon>
          </router-link>
        </div>
        
        <div v-else class="flex items-center gap-2">
          <router-link to="/login" class="text-gray-600 hover:text-primary transition-colors">
            登录
          </router-link>
          <router-link to="/register" class="px-3 py-1 bg-primary text-white rounded-full text-sm font-medium">
            注册
          </router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const userStore = useUserStore()

const props = defineProps<{
  searchQuery?: string
}>()

const searchText = ref(props.searchQuery || '')

function handleSearch() {
  const q = searchText.value.trim()
  if (q) {
    router.push({ name: 'Search', query: { q } })
  } else {
    router.push({ name: 'Search' })
  }
}
</script>
