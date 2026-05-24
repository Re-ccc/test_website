<template>
  <div class="space-y-4">
    <div 
      v-for="comment in comments" 
      :key="comment.id"
      class="bg-gray-700/50 rounded-lg p-4"
    >
      <div class="flex gap-3">
        <img
          :src="comment.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${comment.username || 'user'}`"
          class="w-10 h-10 rounded-full"
          alt="avatar"
        />
        <div class="flex-1">
          <div class="flex items-center gap-2 mb-1">
            <span class="font-medium">{{ comment.username }}</span>
          </div>
          <p class="text-gray-200 mb-2">{{ comment.content }}</p>
          <div class="flex items-center gap-4 text-sm text-gray-400">
            <span class="cursor-pointer hover:text-primary transition-colors flex items-center gap-1" @click="handleLike(comment.id)">
              <el-icon><ThumbsUp /></el-icon>
              {{ comment.like_count }}
            </span>
            <span class="cursor-pointer hover:text-primary transition-colors" @click="startReply(comment.id)">
              回复
            </span>
          </div>

          <div v-if="replyTo === comment.id" class="mt-2 flex gap-2">
            <input
              v-model="replyContent"
              type="text"
              placeholder="写下你的回复..."
              class="flex-1 bg-gray-600 rounded-full px-3 py-1 text-sm outline-none"
              @keyup.enter="submitReply(comment.video_id)"
            />
            <button @click="submitReply(comment.video_id)" class="px-3 py-1 bg-primary text-white rounded-full text-xs">回复</button>
          </div>

          <div v-if="comment.replies && comment.replies.length > 0" class="mt-3 pl-4 border-l-2 border-gray-600 space-y-2">
            <div
              v-for="reply in comment.replies"
              :key="reply.id"
              class="flex gap-2"
            >
              <img
                :src="reply.avatar_url || `https://api.dicebear.com/7.x/avataaars/svg?seed=${reply.username || 'user'}`"
                class="w-6 h-6 rounded-full"
                alt="avatar"
              />
              <div class="flex-1">
                <div class="flex items-center gap-2 mb-1">
                  <span class="font-medium text-sm">{{ reply.username }}</span>
                </div>
                <p class="text-gray-300 text-sm">{{ reply.content }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { Comment } from '@/types'
import { commentApi } from '@/api'
import { ElMessage } from 'element-plus'

const props = defineProps<{
  comments: Comment[]
}>()

const emit = defineEmits<{
  refresh: []
}>()

const replyTo = ref<number | null>(null)
const replyContent = ref('')

async function handleLike(commentId: number) {
  try {
    await commentApi.likeComment(commentId)
    emit('refresh')
  } catch {
    ElMessage.warning('请先登录')
  }
}

function startReply(commentId: number) {
  replyTo.value = commentId
  replyContent.value = ''
}

async function submitReply(videoId: number) {
  if (!replyContent.value.trim() || replyTo.value === null) return
  try {
    await commentApi.createComment({ video_id: videoId, content: replyContent.value, parent_id: replyTo.value })
    replyTo.value = null
    replyContent.value = ''
    emit('refresh')
  } catch {
    ElMessage.warning('请先登录')
  }
}
</script>
