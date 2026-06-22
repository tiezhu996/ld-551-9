import { defineStore } from 'pinia'
import { ref } from 'vue'
import { FavoriteType } from '@/constants/enums'
import type { Favorite, FavoriteStatus } from '@/types/favorite'
import request from '@/utils/request'

export const useFavoriteStore = defineStore('favorite', () => {
  const favorites = ref<Favorite[]>([])
  const statusMap = ref<Map<string, FavoriteStatus>>(new Map())
  const loading = ref(false)

  function getStatusKey(targetType: FavoriteType, targetId: number): string {
    return `${targetType}:${targetId}`
  }

  async function fetchFavorites(targetType?: FavoriteType) {
    loading.value = true
    try {
      const params = targetType ? { target_type: targetType } : {}
      favorites.value = await request.get<unknown, Favorite[]>('/favorites', { params })
      favorites.value.forEach((fav) => {
        statusMap.value.set(getStatusKey(fav.target_type, fav.target_id), {
          is_favorited: true,
          favorite_id: fav.id
        })
      })
    } finally {
      loading.value = false
    }
  }

  async function toggleFavorite(targetType: FavoriteType, targetId: number): Promise<FavoriteStatus> {
    const result = await request.post<unknown, FavoriteStatus>('/favorites/toggle', {
      target_type: targetType,
      target_id: targetId
    })
    statusMap.value.set(getStatusKey(targetType, targetId), result)
    if (result.is_favorited) {
      await fetchFavorites()
    } else {
      favorites.value = favorites.value.filter(
        (f) => !(f.target_type === targetType && f.target_id === targetId)
      )
    }
    return result
  }

  async function fetchStatus(targetType: FavoriteType, targetId: number): Promise<FavoriteStatus> {
    const key = getStatusKey(targetType, targetId)
    const existing = statusMap.value.get(key)
    if (existing) return existing
    const result = await request.get<unknown, FavoriteStatus>(`/favorites/status/${targetType}/${targetId}`)
    statusMap.value.set(key, result)
    return result
  }

  function getCachedStatus(targetType: FavoriteType, targetId: number): FavoriteStatus | undefined {
    return statusMap.value.get(getStatusKey(targetType, targetId))
  }

  return {
    favorites,
    loading,
    fetchFavorites,
    toggleFavorite,
    fetchStatus,
    getCachedStatus
  }
})
