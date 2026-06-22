<template>
  <el-card class="course-card" shadow="hover">
    <div class="cover-wrapper">
      <img class="cover" :src="course.cover_image" :alt="course.title" />
      <el-button
        v-if="showFavorite && isLoggedIn"
        class="favorite-btn"
        :type="isFavorited ? 'danger' : 'default'"
        :icon="isFavorited ? StarFilled : Star"
        circle
        size="small"
        @click.stop="handleToggle"
      />
    </div>
    <div class="body">
      <div class="tags">
        <el-tag size="small">{{ course.category }}</el-tag>
        <el-tag size="small" type="success">{{ courseLevelLabel[course.level] }}</el-tag>
        <el-tag v-if="showStatus" size="small" type="info">{{ courseStatusLabel[course.status] }}</el-tag>
      </div>
      <h3>{{ course.title }}</h3>
      <p>{{ course.description }}</p>
      <div class="meta">
        <span>{{ course.instructor?.name || '讲师' }}</span>
        <span>{{ course.total_lessons }} 课时</span>
        <span>评分 {{ course.rating.toFixed(1) }}</span>
      </div>
      <ProgressIndicator v-if="progress !== undefined" :percentage="progress" compact />
      <div class="footer">
        <strong>{{ formatMoney(course.price) }}</strong>
        <el-button type="primary" size="small" @click="$router.push(`/courses/${course.id}`)">查看</el-button>
      </div>
    </div>
  </el-card>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { Star, StarFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { courseLevelLabel, courseStatusLabel, FavoriteType } from '@/constants/enums'
import type { Course } from '@/types/course'
import { formatMoney } from '@/utils/format'
import ProgressIndicator from '@/components/ProgressIndicator.vue'
import { useFavoriteStore } from '@/stores/favoriteStore'
import { useAuthStore } from '@/stores/authStore'

const props = defineProps<{
  course: Course
  progress?: number
  showStatus?: boolean
  showFavorite?: boolean
}>()

const favoriteStore = useFavoriteStore()
const authStore = useAuthStore()
const isLoggedIn = computed(() => authStore.isAuthenticated)
const isFavorited = ref(false)

async function handleToggle() {
  if (!isLoggedIn.value) {
    ElMessage.warning('请先登录')
    return
  }
  const result = await favoriteStore.toggleFavorite(FavoriteType.COURSE, props.course.id)
  isFavorited.value = result.is_favorited
  ElMessage.success(result.is_favorited ? '已收藏' : '已取消收藏')
}

onMounted(async () => {
  if (props.showFavorite && isLoggedIn.value) {
    const cached = favoriteStore.getCachedStatus(FavoriteType.COURSE, props.course.id)
    if (cached) {
      isFavorited.value = cached.is_favorited
    } else {
      const status = await favoriteStore.fetchStatus(FavoriteType.COURSE, props.course.id)
      isFavorited.value = status.is_favorited
    }
  }
})
</script>

<style scoped>
.course-card {
  overflow: hidden;
}

.cover-wrapper {
  position: relative;
}

.cover {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  display: block;
}

.favorite-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1;
}

.body {
  display: grid;
  gap: 12px;
}

.tags,
.meta,
.footer {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

h3 {
  margin: 0;
  font-size: 18px;
}

p {
  margin: 0;
  color: #5f6673;
  min-height: 42px;
}

.meta {
  color: #6b7280;
  font-size: 13px;
}

.footer {
  justify-content: space-between;
}
</style>
