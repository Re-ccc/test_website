<template>
  <div class="absolute bottom-0 left-0 right-0 bg-gradient-to-t from-black/80 to-transparent p-4">
    <div class="flex items-center gap-4">
      <button
        @click="togglePlay"
        class="text-white hover:text-primary transition-colors"
      >
        <el-icon class="text-2xl"><component :is="isPlaying ? 'Pause' : 'Play'" /></el-icon>
      </button>

      <div class="flex-1 flex items-center gap-3">
        <span class="text-white text-sm">{{ formatDuration(currentTime) }}</span>
        <div
          class="flex-1 h-1 bg-white/30 rounded-full cursor-pointer relative group"
          @click="handleProgressClick"
          ref="progressRef"
        >
          <div
            class="h-full bg-primary rounded-full transition-all"
            :style="{ width: `${progress}%` }"
          ></div>
          <div
            class="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-white rounded-full opacity-0 group-hover:opacity-100 transition-opacity"
            :style="{ left: `${progress}%`, transform: 'translate(-50%, -50%)' }"
          ></div>
        </div>
        <span class="text-white text-sm">{{ formatDuration(duration) }}</span>
      </div>

      <button
        @click="toggleFullscreen"
        class="text-white hover:text-primary transition-colors"
      >
        <el-icon class="text-xl"><component :is="isFullscreen ? 'Minimize' : 'Maximize'" /></el-icon>
      </button>

      <select
        v-model="playbackSpeed"
        @change="onSpeedChange"
        class="bg-white/20 text-white text-sm px-2 py-1 rounded outline-none cursor-pointer"
      >
        <option value="0.5" class="bg-gray-800">0.5x</option>
        <option value="1" class="bg-gray-800">1x</option>
        <option value="1.5" class="bg-gray-800">1.5x</option>
        <option value="2" class="bg-gray-800">2x</option>
      </select>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { formatDuration } from '@/utils'

const props = defineProps<{
  videoEl: HTMLVideoElement | null
  duration: number
  currentTime: number
  isPlaying: boolean
}>()

const emit = defineEmits<{
  play: []
  pause: []
  seek: [time: number]
}>()

const isFullscreen = ref(false)
const playbackSpeed = ref('1')
const progressRef = ref<HTMLElement | null>(null)

const progress = computed(() => {
  if (props.duration === 0) return 0
  return (props.currentTime / props.duration) * 100
})

function togglePlay() {
  if (!props.videoEl) return
  if (props.videoEl.paused) {
    props.videoEl.play()
  } else {
    props.videoEl.pause()
  }
}

function toggleFullscreen() {
  if (!props.videoEl) return
  if (document.fullscreenElement) {
    document.exitFullscreen()
    isFullscreen.value = false
  } else {
    props.videoEl.requestFullscreen()
    isFullscreen.value = true
  }
}

function handleProgressClick(event: MouseEvent) {
  if (!progressRef.value || !props.videoEl) return
  const rect = progressRef.value.getBoundingClientRect()
  const percent = (event.clientX - rect.left) / rect.width
  const newTime = percent * props.duration
  props.videoEl.currentTime = newTime
}

function onSpeedChange() {
  if (props.videoEl) {
    props.videoEl.playbackRate = parseFloat(playbackSpeed.value)
  }
}
</script>
