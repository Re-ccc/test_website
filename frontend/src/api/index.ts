import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 30000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const videoApi = {
  getHomeFeed: (tag?: string): Promise<any[]> =>
    api.get('/video/home', { params: tag ? { tag } : {} }),
  getRanking: (sort?: string): Promise<any[]> =>
    api.get('/video/ranking', { params: sort ? { sort } : {} }),
  searchVideos: (q: string): Promise<any[]> => api.get('/video/search', { params: { q } }),
  getVideo: (bvid: string): Promise<any> => api.get(`/video/detail/${bvid}`),
  getRelated: (videoId: number): Promise<any[]> => api.get(`/video/${videoId}/related`),
  likeVideo: (videoId: number): Promise<any> => api.post(`/video/${videoId}/like`),
  collectVideo: (videoId: number): Promise<any> => api.post(`/video/${videoId}/collect`),
  uploadVideo: (formData: FormData): Promise<any> =>
    api.post('/video/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
      timeout: 120000,
    }),
  getMyCollections: (): Promise<any[]> => api.get('/video/collections'),
  getMyLikes: (): Promise<any[]> => api.get('/video/likes'),
  getMyVideos: (): Promise<any[]> => api.get('/user/videos'),
}

export const danmakuApi = {
  getDanmakus: (videoId: number): Promise<any[]> => api.get(`/danmaku/video/${videoId}`),
  sendDanmaku: (data: { video_id: number; content: string; time: number; color?: string; type?: string }): Promise<any> =>
    api.post('/danmaku', data),
}

export const commentApi = {
  getComments: (videoId: number): Promise<any[]> => api.get(`/comment/video/${videoId}`),
  createComment: (data: { video_id: number; content: string; parent_id?: number }): Promise<any> =>
    api.post('/comment', data),
  likeComment: (commentId: number): Promise<any> => api.post(`/comment/${commentId}/like`),
}

export const authApi = {
  login: (data: { username: string; password: string }): Promise<any> => api.post('/auth/login', data),
  register: (data: { username: string; password: string; nickname?: string }): Promise<any> =>
    api.post('/auth/register', data),
}

export const userApi = {
  getProfile: (): Promise<any> => api.get('/user/profile'),
  updateProfile: (data: { nickname?: string; avatar_url?: string; signature?: string }): Promise<any> =>
    api.put('/user/profile', data),
  uploadAvatar: (file: File): Promise<any> => {
    const fd = new FormData()
    fd.append('file', file)
    return api.post('/user/avatar', fd, { headers: { 'Content-Type': 'multipart/form-data' } })
  },
  followUser: (userId: number): Promise<any> => api.post(`/user/follow/${userId}`),
  getMyFollows: (): Promise<any[]> => api.get('/user/follows'),
  getUserById: (userId: number): Promise<any> => api.get(`/user/${userId}`),
  getUserVideos: (userId: number): Promise<any[]> => api.get(`/user/${userId}/videos`),
}
