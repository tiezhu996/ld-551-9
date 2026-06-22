<template>
  <section class="page">
    <div class="page-title">
      <h1>我的收藏</h1>
    </div>
    <div v-if="favorites.length === 0 && !loading" class="empty">
      <el-empty description="暂无收藏课程" />
    </div>
    <div v-else class="grid">
      <CourseCard
        v-for="item in favorites"
        :key="item.id"
        :course="item.course!"
        :show-favorite="true"
      />
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import CourseCard from '@/components/CourseCard.vue'
import { useFavoriteStore } from '@/stores/favoriteStore'
import { FavoriteType } from '@/constants/enums'

const store = useFavoriteStore()
const favorites = computed(() => store.favorites)
const loading = computed(() => store.loading)

onMounted(() => store.fetchFavorites(FavoriteType.COURSE))
</script>

<style scoped>
.empty {
  background: #fff;
  padding: 60px 20px;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}
</style>
