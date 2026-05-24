<template>
  <div class="min-h-screen bg-gradient-to-br from-primary/10 to-secondary/10 flex items-center justify-center">
    <div class="bg-white rounded-2xl shadow-xl p-8 w-96">
      <div class="text-center mb-6">
        <div class="w-16 h-16 bg-gradient-to-r from-primary to-secondary rounded-full mx-auto flex items-center justify-center mb-4">
          <el-icon class="text-white text-3xl"><VideoPlay /></el-icon>
        </div>
        <h1 class="text-2xl font-bold text-gray-800">欢迎回来</h1>
        <p class="text-gray-500 mt-1">登录你的账号</p>
      </div>

      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
          <input 
            v-model="username"
            type="text" 
            placeholder="请输入用户名"
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
            登录中...
          </span>
          <span v-else>登录</span>
        </button>
      </form>

      <div class="mt-4 text-center">
        <span class="text-gray-500">还没有账号？</span>
        <router-link to="/register" class="ml-2 text-primary hover:underline">
          立即注册
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
const password = ref('')
const isLoading = ref(false)

async function handleLogin() {
  if (!username.value || !password.value) return

  isLoading.value = true
  const success = await userStore.login(username.value, password.value)
  isLoading.value = false

  if (success) {
    router.push('/')
  } else {
    ElMessage.error('用户名或密码错误')
  }
}
</script>
