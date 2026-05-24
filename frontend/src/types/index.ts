export interface User {
  id: number
  username: string
  nickname: string | null
  avatar_url: string | null
  signature: string | null
  follower_count: number
  following_count: number
  created_at: string
}

export interface Video {
  id: number
  bvid: string | null
  title: string
  description: string | null
  cover_url: string | null
  video_url: string | null
  duration: number | null
  view_count: number
  like_count: number
  coin_count: number
  collect_count: number
  danmaku_count: number
  tags: string
  uploader_id: number | null
  uploader_name: string | null
  uploader_avatar: string | null
  created_at: string
}

export interface Danmaku {
  id: number
  video_id: number
  content: string
  time: number
  color: string
  type: 'scroll' | 'top' | 'bottom'
  user_id: number | null
  username: string | null
  send_time: string
}

export interface Comment {
  id: number
  video_id: number
  parent_id: number | null
  content: string
  user_id: number | null
  username: string | null
  avatar_url: string | null
  like_count: number
  created_at: string
  replies: Comment[]
}

export interface Token {
  access_token: string
  token_type: string
}

export interface VideoLikeResponse {
  success: boolean
  liked: boolean
  like_count: number
}

export interface CollectionResponse {
  success: boolean
  collected: boolean
  collect_count: number
}
