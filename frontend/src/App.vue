<template>
  <div class="min-h-screen bg-gray-50">
    <div v-if="showDisclaimer" class="fixed inset-0 z-[100] flex items-center justify-center">
      <div class="absolute inset-0 bg-black/60"></div>
      <div class="relative bg-white rounded-2xl shadow-2xl p-8 max-w-md mx-4 text-center z-10">
        <img
          src="https://api.dicebear.com/9.x/fun-emoji/svg?seed=nailong&backgroundColor=ffd5dc,b6e3f4"
          class="w-24 h-24 mx-auto mb-4 rounded-full"
          alt="nailong"
        />
        <h2 class="text-xl font-bold mb-3">温馨提示</h2>
        <p class="text-gray-600 leading-relaxed mb-6">
          此网站仅仅是个人开发学习和测试上线使用，不会用于商业用途，尊重原作者，尊重B站。
        </p>
        <button
          @click="acceptDisclaimer"
          class="px-8 py-3 bg-gradient-to-r from-primary to-secondary text-white rounded-full font-medium hover:opacity-90 transition-opacity"
        >
          我已知晓
        </button>
      </div>
    </div>

    <transition name="fade" mode="out-in">
      <router-view />
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const showDisclaimer = ref(false)

function acceptDisclaimer() {
  showDisclaimer.value = false
}

onMounted(() => {
  showDisclaimer.value = true
  if (userStore.isLoggedIn) {
    userStore.loadProfile()
  }
})
</script>
