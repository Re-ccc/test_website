<template>
  <div class="min-h-screen bg-gray-50">
    <Header />

    <div class="flex">
      <Sidebar active-tag="" @update-tag="() => {}" />

      <main class="flex-1 p-4">
        <div class="bg-white rounded-lg shadow-sm p-6 max-w-2xl mx-auto">
          <h1 class="text-xl font-bold mb-6">上传视频</h1>

          <div
            class="border-2 border-dashed border-gray-300 rounded-lg p-12 text-center mb-6 hover:border-primary transition-colors cursor-pointer"
            @click="triggerVideoInput"
          >
            <input
              type="file"
              accept="video/*"
              class="hidden"
              ref="videoInputRef"
              @change="handleFileSelect"
            />
            <el-icon class="text-gray-400 text-6xl mx-auto mb-4"><Upload /></el-icon>
            <p class="text-gray-600 mb-2">点击选择视频文件</p>
            <p class="text-gray-400 text-sm">支持 MP4, WebM, MOV 等格式</p>
          </div>

          <div v-if="selectedFile" class="mb-6 p-4 bg-gray-50 rounded-lg">
            <div class="flex items-center gap-4">
              <el-icon class="text-primary text-4xl"><Video /></el-icon>
              <div class="flex-1">
                <p class="font-medium">{{ selectedFile.name }}</p>
                <p class="text-sm text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
              </div>
              <button @click="selectedFile = null" class="text-gray-400 hover:text-red-500">
                <el-icon><Delete /></el-icon>
              </button>
            </div>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              视频封面 <span class="text-red-500">*</span>
            </label>
            <div
              class="border-2 border-dashed rounded-lg p-8 text-center hover:border-primary transition-colors cursor-pointer"
              :class="coverPreview ? 'border-primary' : 'border-gray-300'"
              @click="triggerCoverInput"
            >
              <input
                type="file"
                accept="image/*"
                class="hidden"
                ref="coverInputRef"
                @change="handleCoverSelect"
              />
              <img v-if="coverPreview" :src="coverPreview" class="max-h-40 mx-auto rounded" />
              <div v-else>
                <el-icon class="text-gray-400 text-4xl mx-auto mb-2"><Picture /></el-icon>
                <p class="text-gray-500 text-sm">点击上传封面图</p>
              </div>
            </div>
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">
              标题 <span class="text-red-500">*</span>
            </label>
            <input
              v-model="title"
              type="text"
              placeholder="输入视频标题"
              maxlength="100"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary"
            />
          </div>

          <div class="mb-4">
            <label class="block text-sm font-medium text-gray-700 mb-1">简介</label>
            <textarea
              v-model="description"
              placeholder="输入视频简介"
              rows="4"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary resize-none"
            ></textarea>
          </div>

          <div class="mb-6">
            <label class="block text-sm font-medium text-gray-700 mb-2">
              标签 <span class="text-red-500">*</span>
            </label>
            <div class="flex flex-wrap gap-2 mb-2">
              <span
                v-for="tag in selectedTags"
                :key="tag"
                class="px-3 py-1 bg-primary/10 text-primary rounded-full text-sm flex items-center gap-1"
              >
                {{ tag }}
                <button @click="removeTag(tag)" class="hover:text-red-500">&times;</button>
              </span>
            </div>
            <div class="flex gap-2">
              <input
                v-model="tagInput"
                type="text"
                placeholder="输入标签后按回车"
                maxlength="20"
                class="flex-1 px-4 py-2 border border-gray-300 rounded-lg outline-none focus:ring-2 focus:ring-primary"
                @keyup.enter="addTag"
              />
              <button
                @click="addTag"
                class="px-4 py-2 bg-gray-100 text-gray-600 rounded-lg hover:bg-gray-200 transition-colors"
              >
                添加
              </button>
            </div>
            <p class="text-xs text-gray-400 mt-1">建议添加: 游戏, 舞蹈, 生活, 学习, 科技, 音乐, 美食, 影视, 娱乐</p>
          </div>

          <div class="flex gap-4">
            <button
              @click="handleUpload"
              :disabled="!canUpload || uploading"
              class="flex-1 py-3 bg-gradient-to-r from-primary to-secondary text-white rounded-lg font-medium hover:opacity-90 transition-opacity disabled:opacity-50"
            >
              {{ uploading ? '上传中...' : '发布视频' }}
            </button>
            <button
              @click="$router.push('/')"
              class="px-6 py-3 border border-gray-300 text-gray-600 rounded-lg font-medium hover:bg-gray-50 transition-colors"
            >
              取消
            </button>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import Header from '@/components/Header.vue'
import Sidebar from '@/components/Sidebar.vue'
import { useUserStore } from '@/stores/user'
import { videoApi } from '@/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()

const videoInputRef = ref<HTMLInputElement | null>(null)
const coverInputRef = ref<HTMLInputElement | null>(null)
const selectedFile = ref<File | null>(null)
const coverFile = ref<File | null>(null)
const coverPreview = ref('')
const title = ref('')
const description = ref('')
const tagInput = ref('')
const ALLOWED_TAGS = ['游戏', '舞蹈', '生活', '学习', '科技', '音乐', '美食', '影视', '娱乐', '动画', '知识', '汽车', '运动', '时尚', '动物']

const selectedTags = ref<string[]>([])
const uploading = ref(false)

const canUpload = computed(() =>
  selectedFile.value && coverFile.value && title.value.trim() && selectedTags.value.length > 0 && !uploading.value
)

onMounted(() => {
  if (!userStore.isLoggedIn) {
    ElMessage.warning('请先登录后再上传视频')
    router.push('/login')
  }
})

function triggerVideoInput() {
  videoInputRef.value?.click()
}

function triggerCoverInput() {
  coverInputRef.value?.click()
}

function handleFileSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    selectedFile.value = target.files[0]
  }
}

function handleCoverSelect(event: Event) {
  const target = event.target as HTMLInputElement
  if (target.files && target.files.length > 0) {
    coverFile.value = target.files[0]
    const reader = new FileReader()
    reader.onload = (e) => {
      coverPreview.value = e.target?.result as string
    }
    reader.readAsDataURL(target.files[0])
  }
}

function addTag() {
  const tag = tagInput.value.trim()
  if (!tag) return
  if (!ALLOWED_TAGS.includes(tag)) {
    ElMessage.warning(`"${tag}" 不在允许的标签范围内，请从建议标签中选择`)
    return
  }
  if (selectedTags.value.includes(tag)) {
    ElMessage.warning('标签已存在')
    return
  }
  if (selectedTags.value.length >= 5) {
    ElMessage.warning('最多添加5个标签')
    return
  }
  selectedTags.value.push(tag)
  tagInput.value = ''
}

function removeTag(tag: string) {
  selectedTags.value = selectedTags.value.filter((t) => t !== tag)
}

function formatFileSize(bytes: number): string {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB'
}

async function handleUpload() {
  if (!canUpload.value) return
  uploading.value = true
  try {
    const formData = new FormData()
    formData.append('video_file', selectedFile.value!)
    formData.append('cover_file', coverFile.value!)
    formData.append('title', title.value.trim())
    formData.append('description', description.value.trim())
    formData.append('tags', selectedTags.value.join(','))

    const result = await videoApi.uploadVideo(formData)
    ElMessage.success('视频上传成功！')
    router.push(`/video/${result.bvid}`)
  } catch {
    ElMessage.error('上传失败，请检查文件大小和格式')
  } finally {
    uploading.value = false
  }
}
</script>
