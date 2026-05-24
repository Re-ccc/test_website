<template>
  <div class="min-h-screen bg-gradient-to-br from-primary/10 to-secondary/10 flex items-center justify-center">
    <div class="bg-white rounded-2xl shadow-xl p-8 w-96">
      <div class="text-center mb-6">
        <div class="w-16 h-16 bg-gradient-to-r from-primary to-secondary rounded-full mx-auto flex items-center justify-center mb-4">
          <el-icon class="text-white text-3xl"><UserPlus /></el-icon>
        </div>
        <h1 class="text-2xl font-bold text-gray-800">创建账号</h1>
        <p class="text-gray-500 mt-1">开启你的创作之旅</p>
      </div>

      <form @submit.prevent="handleRegister">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
          <input 
            v-model="username"
            type="text" 
            placeholder="请输入用户名"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">昵称</label>
          <input 
            v-model="nickname"
            type="text" 
            placeholder="请输入昵称"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        <div class="mb-6">
          <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
          <input 
            v-model="password"
            type="password" 
            placeholder="请输入密码"
            class="w-full px-4 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary"
          />
        </div>
        <button 
          type="submit"
          :disabled="isLoading"
          class="w-full py-3 bg-gradient-to-r from-primary to-secondary text-white rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          <span v-if="isLoading" class="flex items-center justify-center gap-2">
            <el-icon class="animate-spin"><Loading /></el-icon>
            注册中...
          </span>
          <span v-else>注册</span>
        </button>
      </form>

      <div class="mt-4 text-center">
        <span class="text-gray-500">已有账号？</span>
        <router-link to="/login" class="ml-2 text-primary hover:underline">
          立即登录
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const username = ref('')
const nickname = ref('')
const password = ref('')
const isLoading = ref(false)

async function handleRegister() {
  if (!username.value || !password.value) return

  isLoading.value = true
  const success = await userStore.register(username.value, password.value, nickname.value)
  isLoading.value = false

  if (success) {
    ElMessage.success('注册成功，请登录')
    router.push('/login')
  } else {
    ElMessage.error('注册失败，用户名可能已存在')
  }
}
</script>
