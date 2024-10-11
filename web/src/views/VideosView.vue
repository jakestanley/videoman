<template>
  <div class="videos">
    <h1>This the videos page</h1>
    <div class="video-grid">
      <VideoCard
        v-for="(video, index) in videos"
        :key="index"
        :video-src="video.src"
        :title="video.title"
        :description="video.description"
      />
    </div>
  </div>
</template>

<script>
import VideoCard from '../components/VideoCard.vue'

export default {
  name: 'Videos',
  components: {
    VideoCard
  },
  data() {
    // return {
    //   videos: [
    //     {
    //       src: 'videos/video1.mp4',
    //       title: 'Introduction to Vue.js',
    //       description: 'Learn the basics of Vue.js in this introductory video.'
    //     },
    //     {
    //       src: 'videos/video2.mp4',
    //       title: 'Advanced Vue Techniques',
    //       description: 'Delve deeper into Vue.js with advanced concepts.'
    //     }
    //     // Add more video objects as needed
    //   ]
    // }
    return {
      videos: [],
    }
  },
  created() {
    this.fetchVideos();
  },
  methods: {
    async fetchVideos() {
      
    }
  }
}
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}

.video-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-gap: 20px;
}
</style>
