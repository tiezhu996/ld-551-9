<template>
  <section class="page" v-if="course">
    <div class="detail-head">
      <div class="cover-wrapper">
        <img :src="course.cover_image" :alt="course.title" />
        <el-button
          v-if="isLoggedIn"
          class="favorite-btn"
          :type="isFavorited ? 'danger' : 'default'"
          :icon="isFavorited ? StarFilled : Star"
          circle
          size="large"
          @click="handleToggleFavorite"
        />
      </div>
      <div>
        <el-tag>{{ course.category }}</el-tag>
        <h1>{{ course.title }}</h1>
        <p>{{ course.description }}</p>
        <div class="detail-meta">
          <span>{{ course.instructor?.name }}</span>
          <span>{{ formatMinutes(course.total_duration) }}</span>
          <span>评分 {{ course.rating }}</span>
        </div>
        <strong class="price">{{ formatMoney(course.price) }}</strong>
        <div class="actions">
          <el-button type="primary" @click="buy">立即购买</el-button>
          <el-button @click="$router.push(`/learn/${course.id}`)">继续学习</el-button>
        </div>
      </div>
    </div>
    <el-tabs>
      <el-tab-pane label="大纲">
        <ChapterTree :chapters="chapters" />
      </el-tab-pane>
      <el-tab-pane label="介绍">
        <article class="rich-text">{{ course.description }}</article>
      </el-tab-pane>
      <el-tab-pane label="评价">
        <el-empty description="评价模块预留，评分已在课程卡片展示" />
      </el-tab-pane>
    </el-tabs>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Star, StarFilled } from '@element-plus/icons-vue'
import ChapterTree from '@/components/ChapterTree.vue'
import { useCourseStore } from '@/stores/courseStore'
import { useOrderStore } from '@/stores/orderStore'
import { useFavoriteStore } from '@/stores/favoriteStore'
import { useAuthStore } from '@/stores/authStore'
import { FavoriteType } from '@/constants/enums'
import { formatMinutes, formatMoney } from '@/utils/format'

const route = useRoute()
const router = useRouter()
const courseStore = useCourseStore()
const orderStore = useOrderStore()
const favoriteStore = useFavoriteStore()
const authStore = useAuthStore()
const course = computed(() => courseStore.currentCourse)
const chapters = computed(() => courseStore.chapters)
const isLoggedIn = computed(() => authStore.isAuthenticated)
const isFavorited = ref(false)

async function buy() {
  if (!course.value) return
  if (Number(course.value.price) === 0) {
    ElMessage.success('免费课程可直接进入学习')
    router.push(`/learn/${course.value.id}`)
    return
  }
  const order = await orderStore.createOrder(course.value.id)
  await orderStore.payOrder(order.id)
  ElMessage.success('支付成功，已注册课程')
  router.push(`/learn/${course.value.id}`)
}

async function handleToggleFavorite() {
  if (!course.value || !isLoggedIn.value) {
    ElMessage.warning('请先登录')
    return
  }
  const result = await favoriteStore.toggleFavorite(FavoriteType.COURSE, course.value.id)
  isFavorited.value = result.is_favorited
  ElMessage.success(result.is_favorited ? '已收藏' : '已取消收藏')
}

async function loadFavoriteStatus() {
  if (!course.value || !isLoggedIn.value) return
  const cached = favoriteStore.getCachedStatus(FavoriteType.COURSE, course.value.id)
  if (cached) {
    isFavorited.value = cached.is_favorited
  } else {
    const status = await favoriteStore.fetchStatus(FavoriteType.COURSE, course.value.id)
    isFavorited.value = status.is_favorited
  }
}

watch(course, () => loadFavoriteStatus())

onMounted(() => {
  courseStore.fetchCourse(Number(route.params.id))
  loadFavoriteStatus()
})
</script>

<style scoped>
.detail-head {
  display: grid;
  grid-template-columns: 420px 1fr;
  gap: 28px;
  padding: 20px;
  background: #fff;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  margin-bottom: 20px;
}

.cover-wrapper {
  position: relative;
}

.cover-wrapper img {
  width: 100%;
  aspect-ratio: 16 / 10;
  object-fit: cover;
  border-radius: 8px;
}

.favorite-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 1;
}

.detail-meta,
.actions {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.price {
  display: block;
  margin: 16px 0;
  font-size: 28px;
  color: #b45309;
}

.rich-text {
  line-height: 1.8;
  background: #fff;
  padding: 18px;
  border-radius: 8px;
}
</style>
