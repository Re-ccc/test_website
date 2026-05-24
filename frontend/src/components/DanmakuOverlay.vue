<template>
  <div class="absolute inset-0 pointer-events-none overflow-hidden">
    <div 
      v-for="danmaku in visibleDanmakus" 
      :key="danmaku.id"
      class="absolute whitespace-nowrap text-sm font-medium"
      :style="getDanmakuStyle(danmaku)"
    >
      {{ danmaku.content }}
    </div>

    <div class="absolute bottom-20 left-4 right-32 flex items-center gap-2">
      <input 
        v-model="danmakuInput"
        type="text" 
        placeholder="发个友善的弹幕吧"
        maxlength="50"
        class="flex-1 bg-black/50 text-white px-4 py-2 rounded-full outline-none focus:bg-black/70 transition-colors"
        @keyup.enter="handleSend"
        @focus="showInput = true"
        @blur="setTimeout(() => showInput = false, 200)"
      />
      <button 
        v-if="showInput"
        @click="handleSend"
        class="px-4 py-2 bg-primary text-white rounded-full text-sm font-medium pointer-events-auto"
      >
        发送
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { Danmaku } from '@/types'

const props = defineProps<{
  danmakus: Danmaku[]
  currentTime: number
}>()

const emit = defineEmits<{
  send: [content: string]
}>()

const danmakuInput = ref('')
const showInput = ref(false)

const visibleDanmakus = computed(() => {
  const time = props.currentTime
  return props.danmakus.filter(d => 
    Math.abs(d.time - time) < 10
  )
})

function getDanmakuStyle(danmaku: Danmaku) {
  const lineIndex = danmaku.id % 12
  const topPercent = 5 + lineIndex * 8
  const duration = 6 + Math.random() * 6

  return {
    top: `${topPercent}%`,
    color: danmaku.color,
    textShadow: '0 0 4px rgba(0,0,0,0.8)',
    animation: `danmaku-scroll ${duration}s linear`
  }
}

function handleSend() {
  if (!danmakuInput.value.trim()) return
  emit('send', danmakuInput.value)
  danmakuInput.value = ''
}
</script>

<style scoped>
</style>
