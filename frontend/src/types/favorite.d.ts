import type { FavoriteType } from '@/constants/enums'
import type { Course } from '@/types/course'

export interface Favorite {
  id: number
  user_id: number
  target_type: FavoriteType
  target_id: number
  created_at: string
  course?: Course
}

export interface FavoriteStatus {
  is_favorited: boolean
  favorite_id: number | null
}
